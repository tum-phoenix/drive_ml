import pandas as pd
import os
import argparse
import tensorflow as tf
from sign_recognition.dict.sign_names_dict import sign_name_carolo_dict
import sys
from random import shuffle

import numpy as np
import PIL.Image as pil
import hashlib
import contextlib2

# append https://github.com/tensorflow/models to your PYTHONPATH
sys.path.append('/home/mykyta/models')
sys.path.append('/home/mykyta/models/research')
from research.object_detection.utils import dataset_util
from research.object_detection.utils import label_map_util
from research.object_detection.dataset_tools import tf_record_creation_util
from tqdm import tqdm

import logging


_LOGGER = logging.getLogger(__name__)


def write_phoenix_label_map(target_path):
    classnames = sign_name_carolo_dict.keys()

    output_file_path = os.path.join(target_path, 'phoenix_label_map.pbtxt')
    file = open(output_file_path, "w+")
    for idx, id in enumerate(classnames):
        file.write("item {\n")
        file.write("  id: " + str(idx + 1) + "\n")
        file.write("  display_name: '" + sign_name_carolo_dict[id] + "'\n}\n\n")
    file.close()
    return output_file_path


def convert_to_tfrecord(image_path, annotation_path, target_path):
    training_path = os.path.join(target_path, 'train')
    test_path = os.path.join(target_path, 'test')
    if not os.path.exists(training_path):
        os.makedirs(training_path)
    if not os.path.exists(test_path):
        os.makedirs(test_path)

    label_map_path = write_phoenix_label_map(target_path)
    convert_phoenix_to_tfrecords(image_path, annotation_path, target_path, label_map_path)


def read_annotation_objects(object_list):
    anno = {}
    anno['xmin'] = np.array([object['xmin'] for object in object_list])
    anno['xmax'] = np.array([object['xmax'] for object in object_list])
    anno['ymin'] = np.array([object['ymin'] for object in object_list])
    anno['ymax'] = np.array([object['ymax'] for object in object_list])
    anno['class'] = [object['class'] for object in object_list]
    return anno


def prepare_tfexample(image_path, annotations, label_map_dict):
    image = pil.open(image_path)
    image = np.asarray(image)

    width = int(image.shape[1])
    height = int(image.shape[0])

    xmin_norm = annotations['xmin'] / float(width)
    ymin_norm = annotations['ymin'] / float(height)
    xmax_norm = annotations['xmax'] / float(width)
    ymax_norm = annotations['ymax'] / float(height)

    if np.any(xmin_norm > xmax_norm):
        logging.warn('Image {}, xmin and xmax are replaced: {} - {} / {} - {}'.format(image_path, xmin_norm, xmax_norm,
                                                                                      annotations['xmin'],
                                                                                      annotations['xmax']))
        xmin_norm[xmin_norm > xmax_norm], xmax_norm[xmin_norm > xmax_norm] = xmax_norm[xmin_norm > xmax_norm], \
                                                                             xmin_norm[xmin_norm > xmax_norm]

    if np.any(ymin_norm > ymax_norm):
        logging.warn('Image {}, ymin and ymax are replaced: {} - {} / {} - {}'.format(image_path, ymin_norm, ymax_norm,
                                                                                      annotations['ymin'],
                                                                                      annotations['ymax']))
        ymin_norm[ymin_norm > ymax_norm], ymax_norm[ymin_norm > ymax_norm] = ymax_norm[ymin_norm > ymax_norm], \
                                                                             ymin_norm[ymin_norm > ymax_norm]

    if np.any(xmin_norm > 1.0) or np.any(xmin_norm < 0.0):
        logging.warn('Image {}, x_min out of bounds: {} / {} - bound: {}'.format(image_path, xmin_norm,
                                                                                 annotations['xmin'], width))
        # remove completely if the min is out of bounds, broken annotation
        indices = xmin_norm < 1.0
        xmin_norm = xmin_norm[indices]
        xmax_norm = xmax_norm[indices]
        ymin_norm = ymin_norm[indices]
        ymax_norm = ymax_norm[indices]

    if np.any(xmax_norm > 1.0) or np.any(xmax_norm < 0.0):
        logging.warn('Image {}, x_max out of bounds: {} / {} - bound: {}'.format(image_path, xmax_norm,
                                                                                 annotations['xmax'], width))

        # cut down max out of bounds to 1.0
        xmax_norm[xmax_norm > 1.0] = np.ones_like(xmax_norm[xmax_norm > 1.0])

    if np.any(ymin_norm > 1.0) or np.any(ymin_norm < 0.0):
        logging.warn('Image {}, y_min out of bounds: {} / {} - bound: {}'.format(image_path, ymin_norm,
                                                                                 annotations['ymin'], height))

        # remove completely if the min is out of bounds, broken annotation
        indices = ymin_norm < 1.0
        ymin_norm = ymin_norm[indices]
        xmin_norm = xmin_norm[indices]
        ymax_norm = ymax_norm[indices]
        xmax_norm = xmax_norm[indices]

    if np.any(ymax_norm > 1.0) or np.any(ymax_norm < 0.0):
        logging.warn('Image {}, y_max out of bounds: {} / {} - bound: {}'.format(image_path, ymax_norm,
                                                                                 annotations['ymax'], height))

        # cut down max out of bounds to 1.0
        ymax_norm[ymax_norm > 1.0] = np.ones_like(ymax_norm[ymax_norm > 1.0])

    # we ignore the "difficult object" labels for now
    difficult_obj = [0] * len(xmin_norm)

    with tf.gfile.GFile(image_path, 'rb') as fid:
        encoded_png = fid.read()
    key = hashlib.sha256(encoded_png).hexdigest()

    class_to_key_map = {key: idx+1 for idx, key in enumerate(sign_name_carolo_dict.keys())}

    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(image_path.encode('utf8')),
        'image/source_id': dataset_util.bytes_feature(image_path.encode('utf8')),
        'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
        'image/encoded': dataset_util.bytes_feature(encoded_png),
        'image/format': dataset_util.bytes_feature('jpg'.encode('utf8')),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmin_norm),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmax_norm),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymin_norm),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymax_norm),
        'image/object/class/text': dataset_util.bytes_list_feature(
            [sign_name_carolo_dict[x].encode('utf8') for x in annotations['class']]),
        'image/object/class/label': dataset_util.int64_list_feature(
            [class_to_key_map[x] for x in annotations['class']]),
        'image/object/difficult': dataset_util.int64_list_feature(difficult_obj),
    }))

    return example


def write_to_tfrecord(images, img_to_obj, path, phase, label_map_dict, image_dir, images_per_record=30):
    num_total_records = len(images) // images_per_record + (len(images) % images_per_record > 0)
    output_path = os.path.join(path, '{}_dataset.record'.format(phase))

    with contextlib2.ExitStack() as tf_record_close_stack:
        output_tfrecords = tf_record_creation_util.open_sharded_output_tfrecords(
            tf_record_close_stack, output_path, num_total_records)
        for index, img_name in tqdm(enumerate(images)):
            if img_name not in img_to_obj:
                img_to_obj[img_name] = []
            img_annos = read_annotation_objects(img_to_obj[img_name])
            image_path = os.path.join(image_dir, img_name)
            example = prepare_tfexample(image_path, img_annos, label_map_dict)
            output_shard_index = index // images_per_record
            output_tfrecords[output_shard_index].write(example.SerializeToString())


def convert_phoenix_to_tfrecords(image_dir, annotation_path, output_path, label_map_path):
    df = pd.read_csv(annotation_path)

    img_to_obj = {}
    for i in range(len(df)):
        frame_filename = df['Filename'][i]
        bbox_dict = {
            'xmin': df['Roi.X1'][i],
            'xmax': df['Roi.X2'][i],
            'ymin': df['Roi.Y1'][i],
            'ymax': df['Roi.Y2'][i],
            'class': df['ClassId'][i] 
        }
        if frame_filename not in img_to_obj:
            img_to_obj[frame_filename] = []
        img_to_obj[frame_filename].append(bbox_dict)

    label_map_dict = label_map_util.get_label_map_dict(label_map_path, use_display_name=True)

    images = []
    for root, dirs, found_images in tf.io.gfile.walk(image_dir, topdown=False):
        prefix = ''
        if os.path.relpath(image_dir, root) != '.':
            prefix = os.path.relpath(image_dir, root)
        images += [os.path.join(prefix, image) for image in found_images if image.endswith('.png')
                   or image.endswith('.jpg') or image.endswith('.ppm')]
    print(images)
    shuffle(images)

    split_train = 0.8
    num_train = int(len(images) * split_train)

    training_path = os.path.join(output_path, 'train')
    test_path = os.path.join(output_path, 'test')

    write_to_tfrecord(images[:num_train], img_to_obj, training_path, 'train', label_map_dict, image_dir)
    write_to_tfrecord(images[num_train:], img_to_obj, test_path, 'test', label_map_dict, image_dir)
    _LOGGER.debug('Done!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate phoenix-style annotations from synthetic segmantation & '
                                                 'sign id')
    parser.add_argument('source_path', type=str, nargs=1,
                        help='Source image path')
    parser.add_argument('annotation_path', type=str, nargs=1,
                        help='Phoenix .csv annotation file path')
    parser.add_argument('target_path', type=str, nargs=1,
                        help='Destination target path')
    args = parser.parse_args()

    # tf.app.run()

    convert_to_tfrecord(args.source_path[0], args.annotation_path[0], args.target_path[0])
