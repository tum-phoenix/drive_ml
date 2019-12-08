###
# Goal: filter a dataset based on:
#  - image similarity (structural_similarity)
#  - minimum relative area of the label in the image (too small image doesn't make sense)
#
# install Python dependencies
#  - python -m pip install numpy scikit-image ssim
#  - python -m pip install scikit-image opencv-python imutils

# 1. Import the necessary packages
from skimage import metrics
import cv2
import pandas as pd
import glob
import os
from shutil import copyfile

# 2. Specify constants
folder_input = r'<PATH_INPUT_FOLDER>'
folder_output = os.path.join(folder_input, 'output')
threshold_relAreaLabels = 0.005; # what should the minimum relative area of a label in an image be?
threshold_imageSimilarity = 0.5;

# 3. Create output directory if not exist
if not os.path.exists(folder_output):
    os.makedirs(folder_output)

# 4. Load the data in a dataframe
df = pd.DataFrame(columns=['basename','label_exist','label_area_min','label_area_ok'])
for fn in glob.glob(folder_input + '\*'): 
    #add restriction: extension
    if '.jpg' in os.path.basename(fn) or '.png' in os.path.basename(fn):  
        #print(os.path.basename(fn))
        txtfile = os.path.join(os.path.dirname(fn), os.path.splitext(os.path.basename(fn))[0] + ".txt") 
        if os.path.exists(txtfile) and os.path.getsize(txtfile) > 0: 
            
            #print(txtfile)
            relArea_min = None
            with open(txtfile) as fp:
                line = fp.readline()
                cnt = 1
                while line:
                    #print("Line {}: {}".format(cnt, line.strip()))
                    index, center_x, center_y, width, height = line.strip().split()
                    relArea = float(width) * float(height)
                    if relArea_min == None:
                        relArea_min = relArea
                    else:
                        if relArea<relArea_min:
                            Area_min = relArea
                    line = fp.readline()
                    cnt += 1
            
            if relArea>threshold_relAreaLabels:
                df = df.append({'basename': os.path.basename(fn), 'label_exist':1, 'label_area_min':relArea, 'label_area_ok':1}, ignore_index=True)
            else:
                df = df.append({'basename': os.path.basename(fn), 'label_exist':1, 'label_area_min':relArea, 'label_area_ok':0}, ignore_index=True)
        else:
            df = df.append({'basename': os.path.basename(fn), 'label_exist':0, 'label_area_min':None, 'label_area_ok':None}, ignore_index=True)

print(df.head(10))        

# 5. Check if images also have labels
boolLabelsExist = (df['label_exist'].sum() > 0)
print(boolLabelsExist)

# 6. Check some images and store them in a new folder
file_image_prev = None
for index, row in df.iterrows():
    if (boolLabelsExist == False) or (row['label_area_ok']==1):
        file_image_curr = os.path.join(folder_input, row['basename']) 
        if boolLabelsExist == True:
            file_text_curr = os.path.join(folder_input, os.path.splitext(row['basename'])[0] + ".txt")
        
        if file_image_prev == None:
            file_image_prev = file_image_curr
            
            copyfile(file_image_curr, os.path.join(folder_output,row['basename']))
            if boolLabelsExist == True:
                copyfile(file_text_curr, os.path.join(folder_output,os.path.splitext(row['basename'])[0] + ".txt"))
            print("Copy file to: ")
            print(" - " + str(os.path.join(folder_output,row['basename'])))
        else:
            image_prev = cv2.imread(file_image_prev)
            image_curr = cv2.imread(file_image_curr)

            # Convert the images to gray-scale
            image_grey_prev = cv2.cvtColor(image_prev, cv2.COLOR_BGR2GRAY)
            image_grey_curr = cv2.cvtColor(image_curr, cv2.COLOR_BGR2GRAY)

            # Compute the Structural Similarity Index (SSIM) between the two
            (score, diff) = metrics.structural_similarity(image_grey_prev, image_grey_curr, full=True)
            #print(file_image_prev)
            #print(file_image_curr)
            #print(score)
            if score < threshold_imageSimilarity:
                file_image_prev = file_image_curr
                copyfile(file_image_curr, os.path.join(folder_output,row['basename']))
                if boolLabelsExist == True:
                    copyfile(file_text_curr, os.path.join(folder_output,os.path.splitext(row['basename'])[0] + ".txt"))
                print(" - " + str(os.path.join(folder_output,row['basename'])))

# 7. Final steps
print("Done -> ouptut at: " + str(folder_output))