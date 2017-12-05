# HowTo Guide
1. find start and end position in the video you want to label
2. convert video to `*.png` files with ffmpeg (this can be done on the workstation):

`ffmpeg -i <input-file>.mp4 -r <framerate> -ss <start_time> -to <end_time> <dest_folder>/%05d.png`

example:

`ffmpeg -i signs003.mp4 -r 60 -ss 00:23 -to 02:12 signs003_manually_labeled/%05d.png`

3. you may want to copy files on your computer (grab a coffee, a couple of free GBs needed) or mount workstation folder to a local folder (good connection recommended)
4. fire up Matlab with installed  [Automated Driving System Toolbox](https://de.mathworks.com/videos/introduction-to-automated-driving-system-toolbox-1497301373787.html)
5. launch "Ground Truth Labeler" from App menu
6. load "label definitions" file `traffic_sign_labels.mat`
7. load "Image Sequence" and point to the directory where all `*.png` files are stored
8. do the labeling
- more infos [here](https://de.mathworks.com/videos/introduction-to-automated-driving-system-toolbox-1497301373787.html)
- tip: "Temporal Interpolator" works pretty good (only one label at a time possible)
- **important**: always make sure to use the correct label (hard to correct afterwards)
9. export labels to file as `groundTruth.mat`
10. convert `groundTruth.mat` file to `*.csv` file running the script `convertToCSV.m`
11. store `*.csv` and `*.mat` files in the same folder on workstation
