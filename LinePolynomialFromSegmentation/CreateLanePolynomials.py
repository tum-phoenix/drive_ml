# based on: https://docs.opencv.org/3.4/da/d0c/tutorial_bounding_rects_circles.html

import cv2 as cv
from matplotlib import pyplot as plt
import matplotlib.patches as patches
import numpy as np
from numpy.polynomial import polynomial as P

image_name = "Image0031.png"
IMAGES_RGB = 'images_simulation/rgb'
IMAGES_LANE = 'images_simulation/lane_segmentation'
image_rgb = IMAGES_RGB + '/' + image_name
image_lane = IMAGES_LANE + '/' + image_name
thr_lane = 5001

def get_lanes(img,min_area):
    # default return
    contours_poly_total = []
    #convert to grey image
    imgray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 40, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for i in contours:
        contours_poly_tmp = cv.approxPolyDP(i, 2, True)

        contours_poly = []
        area = cv.contourArea(contours_poly_tmp)
        if (area>min_area):
            #print("new")
            for j in range(len(contours_poly_tmp)):
                contours_poly.append(contours_poly_tmp[j][0])
            contours_poly_total.append(np.array(contours_poly))
    return contours_poly_total

# load the image
imread_image_rgb = cv.imread(image_rgb)
imread_image_rgb_rgb = cv.cvtColor(imread_image_rgb, cv.COLOR_BGR2RGB)

# load the image
imread_image_lane = cv.imread(image_lane)
imread_image_lane_rgb = cv.cvtColor(imread_image_lane, cv.COLOR_BGR2RGB)

# plot the image
i = 0;
plt.subplot(1,3,i+1),plt.imshow(imread_image_rgb_rgb,'gray')
plt.title("original image")

# plot the image
i = 1;
plt.subplot(1,3,i+1),plt.imshow(imread_image_lane,'gray')
plt.title("lane. image")
# find a bounding box (if available)
contours_poly = get_lanes(imread_image_lane,thr_lane)
print("TOTAL LIST")
print(len(contours_poly))

if contours_poly != []:
    i+=1
    ax = plt.subplot(1,3,i+1)
    ax.imshow(imread_image_lane)
    for j in range(len(contours_poly)):
        contour_poly = contours_poly[j]
        print(contour_poly[:,0])
        line = plt.Polygon(contours_poly[j], closed=None, fill=None, edgecolor='r')
        ax.add_patch(line)
        print(contour_poly)
        c, stats = P.polyfit(contour_poly[:,0],contour_poly[:,1],3,full=True)
        print(c)
    plt.title('found lanes')
else:
    print(" -> empty ")

plt.xticks([]),plt.yticks([])
plt.show()
