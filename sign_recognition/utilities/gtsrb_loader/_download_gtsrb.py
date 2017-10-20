# to import GTSRB data
import os
import math
import zipfile
import urllib.request
import sys


def _download_and_unzip(target_path, download_url):
    target_root, target_dirname = os.path.split(target_path)
    zip_path = os.path.join(target_root, target_dirname + '.zip')
    req = urllib.request.urlopen(download_url)
    total_size = int(req.getheader('Content-Length').strip())
    downloaded = 0
    CHUNK = 256 * 10240
    with open(zip_path, 'wb') as fp:
        while True:
            chunk = req.read(CHUNK)
            downloaded += len(chunk)
            sys.stdout.write('\r' + 'Downloaded ' + str(math.floor((downloaded / total_size) * 100)) + '%')
            if not chunk: break
            fp.write(chunk)
    zip_ref = zipfile.ZipFile(zip_path, 'r')
    zip_ref.extractall(target_path)
    zip_ref.close()
    os.remove(zip_path)
    sys.stdout.write('\n')



def download_gtsrb_testdata(path) -> str: 
    # get absolute path
    absolute_path = os.path.abspath(os.path.join(path, 'GTSRB', 'Final_Training', 'Images'))

    if not os.path.isdir(absolute_path):
        print("You do not have the GTSRB test dataset in the desired location, downloading if for you")
        filepath = os.path.join(path, 'GTSRB_Final_Test_Images.zip')
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
        zip_ref.extractall(path)
        zip_ref.close()
        os.remove(filepath)
        sys.stdout.write('\n')
        print("Extracted GTSRB test dataset for you.")
        print(absolute_path)
    else:
        print("GTSRB test dataset is in place, you're fine.")
        print(absolute_path)

    if not os.path.isfile(os.path.join(absolute_path, 'GT-final_test.csv')):
        print("download test classes")
        _download_and_unzip(target_path=absolute_path,
                            download_url='http://benchmark.ini.rub.de/Dataset/GTSRB_Final_Test_GT.zip')

    return absolute_path


def download_gtsrb(path) -> str:
    # get absolute path
    absolute_path = os.path.abspath(os.path.join(path, 'GTSRB', 'Final_Training', 'Images'))
    if not os.path.isdir(absolute_path):
        print("You do not have the GTSRB dataset in the desired location, downloading if for you")
        filepath = os.path.join(path, 'GTSRB_Final_Training_Images.zip')
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
        zip_ref.extractall(path)
        zip_ref.close()
        os.remove(filepath)
        sys.stdout.write('\n')
        print("Extracted GTSRB dataset for you.")
        print(absolute_path)
    else:
        print("GTSRB test dataset is in place, you're fine.")
        print(absolute_path)
    return absolute_path
