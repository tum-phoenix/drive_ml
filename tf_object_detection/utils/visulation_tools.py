import numpy as np
import pandas as pd
import matplotlib as mlp
import pickle
import os
from matplotlib import pyplot as plt
import random
from utils.dicts_transformer import *
from utils.visulation_tools import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

def draw_image_with_box(file,labels):
    im = Image.open(file)
    boxes=get_boxes(labels,file)
    draw_boxes(boxes)
    plt.imshow(im)
    plt.legend(bbox_to_anchor=(2.1, 0.5), loc='center right', ncol=1)
    
def random_visualisation(files,labels):
    list_for_key=[file for file in files]
    file=random.choice(list_for_key)
    random_file=random.choice(files[file])
    draw_image_with_box(random_file,labels)
    print(random_file)

def get_boxes(label_dict,filename):
    [file,name]=filename.split('/')[-2:]
    labels=label_dict[file][label_dict[file]['Filename'].str.match(name)]
    return labels

def draw_boxes(labels):
    colors=['red','green','yellow','blue','magenta','orange']
    for j, (index, row) in enumerate(labels.iterrows()): 
        plt.gca().add_patch(Rectangle((row['Roi.X1'],row['Roi.Y1']),row['Roi.X2']-row['Roi.X1'],row['Roi.Y2']-row['Roi.Y1'],linewidth=1,edgecolor=colors[j],facecolor='none',label=row['ClassId']))