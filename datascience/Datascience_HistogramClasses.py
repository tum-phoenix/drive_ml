###
# Goal: create a bar plot how many images per class exist
#  - Requirement: Folder with annation files (.txt) that have information about the class
#  - How does it work: go through all the text files, and check which classes exist

# 1. Import the necessary packages
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

# 2. Specify constants
folder_input = r'<PATH_INPUT_FOLDER>'

# 3. Load the data in a dataframe
df = pd.DataFrame(columns=['basename','class'])
df_row = 0
for fn in glob.glob(folder_input + '\*'): 
    if '.txt' in os.path.basename(fn):  
        #print(os.path.basename(fn))
        if os.path.exists(fn) and os.path.getsize(fn) > 0: 
            #print(os.path.basename(fn))
            index_arr=[]
            with open(fn) as fp:
                line = fp.readline()
                cnt = 1
                while line:
                    #print("Line {}: {}".format(cnt, line.strip()))
                    class_index, center_x, center_y, width, height = line.strip().split()
                    index_arr.append(class_index)
                    line = fp.readline()
                    cnt += 1
                    if class_index not in df: 
                        print("Column added  to df:" + str(class_index))
                        df[class_index] = None
            df = df.append({'basename': os.path.basename(fn), 'class':index_arr}, ignore_index=True)
            for ind in index_arr:
                #print(ind)
                df.loc[df_row, ind] = 1
            #df.loc[df_row, 'New Column Title'] = "some value"
        else:
            df = df.append({'basename': os.path.basename(fn), 'class':None}, ignore_index=True)
        df_row +=1

# 4. get the unique list of classes sorted order
print(df.head(20))
classes_unique = []
for i in range(len(df["class"])):
    for j in pd.Series(df["class"].iloc[i]).unique():
        classes_unique.append(j)
classes_unique = list(set(classes_unique))
classes_unique_sorted = sorted(classes_unique, key=lambda x: float(x))
print("found classes:" + str(classes_unique_sorted))

# 5. get the amount of images per class
classes_unique_sorted_amount = []
for class_i in classes_unique_sorted:
    classes_unique_sorted_amount.append(df[class_i].count())
print("# images/class:" + str(classes_unique_sorted_amount))

# 6. plot histogram
fig, ax = plt.subplots()
plt.bar(classes_unique_sorted, classes_unique_sorted_amount)
plt.xticks(classes_unique_sorted)
plt.xlabel("class id"); plt.ylabel("amount of labels");
plt.title("amount of labels per class"); plt.grid(True)
plt.tight_layout(); plt.savefig(folder_input + '\plot_histogram_classes.png');
plt.show()

# 7. Final steps
print("Done -> ouptut at: " + str(folder_input) + '\plot_histogram_classes.png')