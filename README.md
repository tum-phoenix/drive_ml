# Machine Learning
This is the repository for the TUM Phoenix Autonomous Drive Machine Learning applications. 

## Use on TUM Phoenix Hardware
There is a workstation available with all software preinstalled. Just ask the project leader for an account. This is the easiest method.

## Use on own Hardware
If you want to install it to your own device follow the following instructions:
1. Install [requirements](https://github.com/tum-phoenix/drive_ml/blob/master/requirements.txt) using pip3 (`sudo pip3 install -r requirements.txt`)
2. Dataset will be loaded automatically when running the Jupyter notebooks

## Dataset location
To load the GTSRB dataset correctly in the jupyter notebook, please extract the file at the same level as your ml repo, so you should have something like (a cell can also do this for you):

`../drive_ml`

`../GTSRB/Final_Training/..`

Additional files are on our server (please contact project leader).

## Structure
- `models` (the trained and untrained netmodels)
- `dicts` (translation into signs)
- `utilities` (functions and scripts for assitence)


## Further Information
* [TUM Phoenix CNN Wiki page](https://wiki.tum.de/display/phoenix/Machine+Learning)

