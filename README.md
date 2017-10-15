# Machine Learning
This is the repository for the TUM Phoenix Autonomous Drive Machine Learning applications. 

## Use on TUM Phoenix Hardware
There is a workstation available with all software preinstalled. Just ask the project leader for an account. This is the easiest method.

## Use on own Hardware
If you want to install it to your own device follow the following instructions:
1. Install [Jupyter](http://jupyter.org/)
2. Install [requirements](https://github.com/tum-phoenix/drive_ml/blob/master/GTSRB_python/requirements.txt) 
3. Download GTRSB dataset and put it in the correct location (see below)


## Dataset location
To load the GTSRB dataset correctly in the jupyter notebook, please extract the file at the same level as your ml repo, so you should have something like (a cell can also do this for you):

`../drive_ml`

`../GTSRB/Final_Training/..`


## Further ML resources
* [TUM LDV Wiki (Convolutional Neural Networks for Image and Video Processing)](https://wiki.tum.de/display/lfdv/Convolutional+Neural+Networks+for+Image+and+Video+Processing)
* [TUM Phoenix CNN Wiki page](https://wiki.tum.de/display/phoenix/Resources%3A+Convolutional+Neural+Networks)
* [NVIDIA Deep Learning Institute Online Labs](https://developer.nvidia.com/dli/onlinelabs)
