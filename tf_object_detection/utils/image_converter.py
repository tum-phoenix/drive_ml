import cv2
import os


def convert_to_jpg(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file[-4]==".jp2"
                img = Image(os.join(path,file)) # Input Image
            img.write('CB_TM432.jpeg')