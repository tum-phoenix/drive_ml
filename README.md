# Machine Learning
This is the repository for the TUM Phoenix Autonomous Drive Machine Learning applications. 
* [Literature (TUM Phoenix Wiki)](https://wiki.tum.de/display/phoenix/Machine+Learning)
* [Todo List (Issues page)](https://github.com/tum-phoenix/drive_ml/issues)

## Use on TUM Phoenix Hardware
There is a workstation available with all software preinstalled and decent training hardware (Nvidia GTX1070 8GB). Just ask the project leader for an account. Access only from TUM University network (or use LRZ-VPN).

## Use on own Hardware
If you want to install it on your own device follow these instructions:
1. Install [requirements](https://github.com/tum-phoenix/drive_ml/blob/master/requirements.txt) using pip3 (`sudo pip3 install -r requirements.txt`)
2. Todo: Setup Git or Jupyter Hooks
3. Start Jupyter notebook and start editing files

## Dataset location
GTSRB Dataset will be loaded automatically when running the Jupyter notebooks. Additional files are on the TUM Phoenix server (please contact project leader). You may need to change the paths to your environment.

## Structure of sign recognition folder
- `models` (trained and untrained netmodels)
- `dicts` (translation: signs <-> category number)
- `utilities` (utility functions and scripts for data processing, training helpers, ...)
