import os
import pandas as pd


def gen_zero_csv(folder_path, image_size, csv_output_path):
    """
    This function generated the csv containing the information for the Zero Class images,
    it walks the passed path_to_images collecting all images and outputs a csv file with
    the size passed in image_size and bounding boxes on 0.
    :param image_size: tuple (width, height)
    :param folder_path: an absolute path were the images are
    :param csv_output_path: an file handle created with open() as output_file
    :return: none
    """
    assert len(image_size) == 2, "image size need two dimensions, heighth and width. " + len(image_size) + " were passed."

    filenames = []
    for _, _, files in os.walk(folder_path):
        filenames += [file for file in files if file.endswith('.ppm')]

    df = pd.DataFrame({
        "Filename": filenames,
        "Width": image_size[0],
        "Height": image_size[1],
        "Roi.X1": 0,
        "Roi.Y1": 0,
        "Roi.X2": 0,
        "Roi.Y2": 0,
        "ClassId": 43,
    })[["Filename", "Width", "Height", "Roi.X1", "Roi.Y1", "Roi.X2", "Roi.Y2", "ClassId"]]

    df.to_csv(csv_output_path, index=False, sep=";")
