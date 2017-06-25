import matplotlib.pyplot as plt
from ._download_gtsrb import download_gtsrb, download_gtsrb_testdata

from skimage.transform import resize
from PIL import Image

import numpy as np
import pandas as pd

import sys
import os
import fnmatch


def _transform_csv(df: pd.DataFrame) -> pd.DataFrame:
    pixels = 64
    columns = ['Width', 'Height', 'Roi.X1', 'Roi.Y1', 'Roi.X2', 'Roi.Y2', 'ClassId']
    matrix = df.as_matrix(columns=columns)
    matrix2 = np.zeros(matrix.shape)
    for i, row in enumerate(matrix):
        xfac = pixels / row[0]
        yfac = pixels / row[1]
        matrix2[i] = [pixels, pixels, round(row[2] * xfac), round(row[3] * yfac), round(row[4] * xfac), round(row[5] * yfac),
                      row[6]]
    matrix2 = matrix2.astype(int)
    df2 = pd.DataFrame(matrix2, columns=columns)
    df2['Filename'] = df['Filename']
    df2 = df2[['Filename'] + columns]
    return df2


def generate_64x64(test=False) -> str:
    pixels = 64
    absolute_path = download_gtsrb_testdata() if test else download_gtsrb()
    new_abs_path = absolute_path.replace('GTSRB', 'GTSRB_64x64')
    if os.path.isdir(new_abs_path):
        print("Folder already exists.")
        print(new_abs_path)
        return new_abs_path

    ppm_filelist = []
    csv_filelist = []
    for root, dirs, files in os.walk(absolute_path):
        ppm_filelist += [os.path.join(root, file) for file in files if fnmatch.fnmatch(file, '*.ppm')]
        csv_filelist += [os.path.join(root, file) for file in files if fnmatch.fnmatch(file, '*.csv')]

    for idx, filepath in enumerate(ppm_filelist):
        pic = plt.imread(filepath)
        resized = resize(pic, (pixels, pixels), mode='edge')
        im = Image.fromarray(np.uint8(resized * 255))
        new_path = filepath.replace('GTSRB', 'GTSRB_64x64')
        directory = os.path.split(new_path)[0]
        if not os.path.exists(directory):
            os.makedirs(directory)
        im.save(new_path)
        if idx % 100 == 0: sys.stdout.write('\r' + str(idx) + " pictures processed")

    for filepath in csv_filelist:
        df = pd.read_csv(filepath, sep=';')
        df2 = _transform_csv(df)
        new_path = filepath.replace('GTSRB', 'GTSRB_64x64')
        df2.to_csv(new_path, sep=';', index=False)

    return new_abs_path
