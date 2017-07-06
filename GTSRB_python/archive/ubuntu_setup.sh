#!/bin/bash -e
sudo apt-get install python-virtualenv

virtualenv -p python3 env
. ./env/bin/activate
pip install -r requirements.txt