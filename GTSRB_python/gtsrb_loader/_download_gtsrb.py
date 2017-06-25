# to import GTSRB data
import os
import math
import zipfile
import urllib.request
import sys

def download_gtsrb_testdata() -> str:
    # convention: we store our GTSRB folder at the same height as the ML repo
    absolute_path = os.path.abspath(
        os.path.join(os.path.realpath('.'), '..', '..', 'GTSRB', 'Final_Test', 'Images'))

    if not os.path.isdir(absolute_path):
        print("You do not have the GTSRB test dataset in the desired location, downloading if for you")
        folder_path = os.path.join(os.path.realpath('.'), '../../')
        filepath = os.path.join(folder_path, 'GTSRB_Final_Test_Images.zip')
        urlfile = 'http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Test_Images.zip'
        req = urllib.request.urlopen(urlfile)
        total_size = int(req.getheader('Content-Length').strip())
        downloaded = 0
        CHUNK = 256 * 10240
        with open(filepath, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                sys.stdout.write('\r' + 'Downloaded ' + str(math.floor((downloaded / total_size) * 100)) + '%')
                if not chunk: break
                fp.write(chunk)
        zip_ref = zipfile.ZipFile(filepath, 'r')
        zip_ref.extractall(folder_path)
        zip_ref.close()
        os.remove(filepath)
        sys.stdout.write('\n')
        print("Extracted GTSRB test dataset for you.")
        print(absolute_path)
    else:
        print("GTSRB test dataset is in place, you're fine.")
        print(absolute_path)

    return absolute_path


def download_gtsrb() -> str:
    # convention: we store our GTSRB folder at the same height as the ML repo
    absolute_path = os.path.abspath(
        os.path.join(os.path.realpath('.'), '..', '..', 'GTSRB', 'Final_Training', 'Images'))
    if not os.path.isdir(absolute_path):
        print("You do not have the GTSRB dataset in the desired location, downloading if for you")
        folder_path = os.path.join(os.path.realpath('.'), '../../')
        filepath = os.path.join(folder_path, 'GTSRB_Final_Training_Images.zip')
        urlfile = 'http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Training_Images.zip'
        req = urllib.request.urlopen(urlfile)
        total_size = int(req.getheader('Content-Length').strip())
        downloaded = 0
        CHUNK = 256 * 10240
        with open(filepath, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                sys.stdout.write('\r' + 'Downloaded ' + str(math.floor((downloaded / total_size) * 100)) + '%')
                if not chunk: break
                fp.write(chunk)
        zip_ref = zipfile.ZipFile(filepath, 'r')
        zip_ref.extractall(folder_path)
        zip_ref.close()
        os.remove(filepath)
        sys.stdout.write('\n')
        print("Extracted GTSRB dataset for you.")
        print(absolute_path)
    else:
        print("GTSRB test dataset is in place, you're fine.")
        print(absolute_path)
    return absolute_path
