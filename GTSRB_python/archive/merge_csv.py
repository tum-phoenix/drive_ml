import os
import fnmatch

absolute_path = "C:\\Users\\q423132\\Desktop\\GTRSB\\GTSRB\\Final_Training\\Images"

csv_paths = []
for root, dirs, files in os.walk(absolute_path):
    for file in files:
        if fnmatch.fnmatch(file, '*.csv'):
            csv_paths.append(os.path.join(root, file))

with open('generated_concat_csv.csv', mode='w') as writefile:
    with open(csv_paths[0], mode='r') as readfile:
        for line in readfile:
            writefile.write(line)
    for csv_path in csv_paths:
        with open(csv_path, mode='r') as readfile:
            next(readfile)
            for line in readfile:
                writefile.write(line)