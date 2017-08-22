# The German Traffic Sign Recognition Benchmark
#
# sample code for reading the traffic sign images and the
# corresponding labels
#
# example:
#            
# trainImages, trainLabels = readTrafficSigns('GTSRB/Training')
# print len(trainLabels), len(trainImages)
# plt.imshow(trainImages[42])
# plt.show()
#
# have fun, Christian

import matplotlib.pyplot as plt
import csv
import os
import fnmatch

# function for reading the images
# arguments: path to the traffic sign data, for example './GTSRB/Training'
# returns: list of images, list of corresponding labels
# TOMAS: tried to deprecate this function.
"""
def get_train_data(rootpath):
    '''Reads traffic sign data for German Traffic Sign Recognition Benchmark.

    Arguments: path to the traffic sign data, for example './GTSRB/Training'
    Returns:   list of images, list of corresponding labels'''
    images = []  # images
    labels = []  # corresponding labels
    # loop over all 42 classes
    for c in range(0, 43):
        prefix = os.path.join(rootpath, format(c, '05d'))
        gtFile = open(os.path.join(prefix, 'GT-' + format(c, '05d')) + '.csv')
        gtReader = csv.reader(gtFile, delimiter=';')  # csv parser for annotations file
        next(gtReader)  # skip header
        # loop over all images in current annotations file
        for row in gtReader:
            images.append(plt.imread(os.path.join(prefix, row[0])))  # the 1th column is the filename
            labels.append(row[7])  # the 8th column is the label
        gtFile.close()
        # if c >= 1: break
    return images, labels
"""


def load_data(path):
    images = []
    labels = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file, '*.csv'):
                with open(os.path.join(root, file), mode='r') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=';')
                    try:
                        next(csv_file)[7] # will throw an index error when there is no 7. column
                        for row in csv_reader:
                            ppm_filepath = os.path.join(root, row[0])
                            images.append(plt.imread(ppm_filepath))
                            labels.append(row[7])
                    except IndexError:
                        pass
    return images, labels


def load_bounding_boxes_generator(path, batch_size: int):
    while True:
        for root, _, files in os.walk(path):
            images, bounding_boxes = [], []
            for file in files:
                if fnmatch.fnmatch(file, '*.csv'):
                    with open(os.path.join(root, file), mode='r') as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=';')
                        next(csv_reader)
                        for row in csv_reader:
                            ppm_filepath = os.path.join(root, row[0])
                            images.append(plt.imread(ppm_filepath))
                            bounding_boxes.append(row[3:7])
                            if len(images) >= batch_size:
                                yield images, bounding_boxes
                                images, bounding_boxes = [], []

