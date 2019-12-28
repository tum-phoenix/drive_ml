import pandas as pd
import os
import argparse
import tensorflow as tf
from sign_recognition.dict.sign_names_dict import sign_name_carolo_dict
import sys
from random import shuffle

import numpy as np
import PIL.Image as pil

# append https://github.com/tensorflow/models to your PYTHONPATH
sys.path.append('/home/mykyta/models')
sys.path.append('/home/mykyta/models/research')
from research.object_detection.utils import dataset_util
from research.object_detection.utils import label_map_util

import logging


_LOGGER = logging.getLogger(__name__)


def write_phoenix_label_map(target_path):
    classnames = sign_name_carolo_dict.keys()

    output_file_path = os.path.join(target_path, 'phoenix_label_map.pbtxt')
    file = open(output_file_path, "w+")
    for id in classnames:
        file.write("item {\n")
        file.write("  id: " + str(id + 1) + "\n")
        file.write("  name: '" + str(id + 1) + "'\n")
        file.write("  display_name: '" + sign_name_carolo_dict[id] + "'\n}\n\n")
    file.close()
    return output_file_path


def convert_to_tfrecord(image_path, annotation_path, target_path):
    training_path = os.path.join(target_path, 'train')
    validation_path = os.path.join(target_path, 'val')
    test_path = os.path.join(target_path, 'test')
    if not os.path.exists(training_path):
        os.makedirs(training_path)
    if not os.path.exists(validation_path):
        os.makedirs(validation_path)
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

    width = int(image.shape[0])
    height = int(image.shape[1])

    xmin_norm = annotations['xmin'] / float(width)
    ymin_norm = annotations['ymin'] / float(height)
    xmax_norm = annotations['xmax'] / float(width)
    ymax_norm = annotations['ymax'] / float(height)

    if np.any(xmin_norm > 1.0) or np.any(xmin_norm < 0.0):
        logging.warn('Image {}, x_min out of bounds: {}'.format(image_path, xmin_norm))

    if np.any(xmax_norm > 1.0) or np.any(xmax_norm < 0.0):
        logging.warn('Image {}, x_max out of bounds: {}'.format(image_path, xmax_norm))

    if np.any(ymin_norm > 1.0) or np.any(ymin_norm < 0.0):
        logging.warn('Image {}, y_min out of bounds: {}'.format(image_path, ymin_norm))

    if np.any(ymax_norm > 1.0) or np.any(ymax_norm < 0.0):
        logging.warn('Image {}, y_max out of bounds: {}'.format(image_path, ymax_norm))

    # we ignore the "difficult object" labels for now
    difficult_obj = [0] * len(xmin_norm)

    example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(image_path.encode('utf8')),
        'image/source_id': dataset_util.bytes_feature(image_path.encode('utf8')),
        # 'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
        # 'image/encoded': dataset_util.bytes_feature(encoded_png),
        'image/format': dataset_util.bytes_feature('jpg'.encode('utf8')),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmin_norm),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmax_norm),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymin_norm),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymax_norm),
        'image/object/class/text': dataset_util.bytes_list_feature(
            [sign_name_carolo_dict[x - 1].encode('utf8') for x in annotations['class']]),
        'image/object/class/label': dataset_util.int64_list_feature(
            [x for x in annotations['class']]),
        'image/object/difficult': dataset_util.int64_list_feature(difficult_obj),
    }))
    return example


def convert_phoenix_to_tfrecords(image_dir, annotation_path, output_path, label_map_path):
    train_writer = tf.python_io.TFRecordWriter(os.path.join(output_path, 'train.tfrecord'))
    val_writer = tf.python_io.TFRecordWriter(os.path.join(output_path, 'val.tfrecord'))
    test_writer = tf.python_io.TFRecordWriter(os.path.join(output_path, 'eval.tfrecord'))

    df = pd.read_csv(annotation_path)

    img_to_obj = {}
    for i in range(len(df)):
        frame_filename = df['Filename'][i]
        bbox_dict = {
            'xmin': df['Roi.X1'][i],
            'xmax': df['Roi.X2'][i],
            'ymin': df['Roi.Y1'][i],
            'ymax': df['Roi.Y2'][i],
            'class': df['ClassId'][i] + 1
        }
        if frame_filename not in img_to_obj:
            img_to_obj[frame_filename] = []
        img_to_obj[frame_filename].append(bbox_dict)

    label_map_dict = label_map_util.get_label_map_dict(label_map_path, use_display_name=True)

    images = tf.io.gfile.listdir(image_dir)
    shuffle(images)

    counter = 0
    split_train = 0.7
    split_val = 0.2
    num_train = int(len(images) * split_train)
    num_val = int(len(images) * split_val)
    for img_name in images:
        if img_name not in img_to_obj.keys():
            img_to_obj[img_name] = []

        img_annos = read_annotation_objects(img_to_obj[img_name])
        image_path = os.path.join(image_dir, img_name)
        example = prepare_tfexample(image_path, img_annos, label_map_dict)

        if counter < num_train:
            train_writer.write(example.SerializeToString())
            _LOGGER.debug('Image {} added to train record'.format(img_name))
        elif counter < num_train + num_val:
            val_writer.write(example.SerializeToString())
            _LOGGER.debug('Image {} added to val record'.format(img_name))
        elif counter < num_train + num_val:
            test_writer.write(example.SerializeToString())
            _LOGGER.debug('Image {} added to test record'.format(img_name))

        counter += 1

    train_writer.close()
    val_writer.close()
    test_writer.close()
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
