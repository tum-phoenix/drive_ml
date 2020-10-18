# imports
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import matplotlib.patches as patches

# parameters for optimization
min_rel_area_bbox = (1/10)**2   # exampe: if (rel. area of sign) >= (10% of width/height) --> (1/10)^2
min_rel_area_lane = (1/50)**2   # exampe: if (rel. area of mark) >= (10% of width/height) --> (1/10)^2
noise_reduction_bbox = 31;       # [px] pixel size for noise reduction (odd nr.)
noise_reduction_lane = 1;       # [px] pixel size for noise reduction (odd nr.)
focallength = 1000/0.649;       # [mm] focallength of camera

# define the marking dictionary
dict_traffic_marking = {
 '30_zone_beginn':          {'type':'sign',           'rgb':(212,158,212),  'size':150},
 '60_zone_beginn':          {'type':'sign',           'rgb':(93, 242, 93),  'size':150},
 'ende_30_zone':            {'type':'sign',           'rgb':(216, 152, 216),'size':150},
 'ende_60_zone':            {'type':'sign',           'rgb':(155, 214, 155),'size':150},
 'pedestrian':              {'type':'sign',           'rgb':(223,139,223),  'size':150},
 'lane colour 1':           {'type':'lane',           'rgb':(188,0,0),      'size':None},
 'lane colour 2':           {'type':'lane',           'rgb':(128,0,0),      'size':None},
 'no_passing_zone':         {'type':'sign',           'rgb':(196,179,196),  'size':100},
 '30_zone_beginn_street':   {'type':'street_marking', 'rgb':(248,71,71),    'size':60},
 '60_zone_beginn_street':   {'type':'street_marking', 'rgb':(237,110,110),  'size':60},
 'sharp_turn_left_long':    {'type':'sign',           'rgb':(231,125,231),  'size':100},
 'sharp_turn_left':         {'type':'sign',           'rgb':(227,132,227),  'size':100},
 }

# function: split the image into its RGB components
def rgb_filter(img,rgb,type,noise_reduction):
    # split image in R,G,B
    (B, G, R) = cv.split(img)

    # find the maximum pixel intensity values for each
    R[R != rgb[0]] = 0
    G[G != rgb[1]] = 0
    B[B != rgb[2]] = 0

    # merge the channels back together and return the image
    img = cv.merge([B, G, R])

    if type != 'lane':
        # apply blur filter
        blur = cv.GaussianBlur(img,(noise_reduction,noise_reduction),0)
        thresh = cv.threshold(blur, 100, 255, cv.THRESH_BINARY)[1]
    else:
        kernel = np.ones((10,10), np.uint8)  # this is a hor+vert kernel
        #kernel = np.identity(100, np.uint8)
        d_im = cv.dilate(img, kernel, iterations=1)
        e_im = cv.erode(d_im, kernel, iterations=1)
        blur = cv.GaussianBlur(e_im,(noise_reduction,noise_reduction),0)
        thresh = cv.threshold(blur, 100, 255, cv.THRESH_BINARY)[1]
        return thresh
    return thresh

# function: calculate distance, based on size
def distance_to_camera(size_real,focallength,size_pixel):
    return(size_real * focallength / size_pixel)

# function: get the bounding box, based on the image
def get_bounding_box(img,min_area):
    boundRect = []
    #convert to grey image
    imgray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 40, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    largest_area=min_area;
    for i in contours:
        contours_poly = cv.approxPolyDP(i, 3, True)
        area = cv.contourArea(contours_poly)
        if (area>largest_area):
            #print(area)
            largest_area=area
            boundRect = cv.boundingRect(contours_poly)
    return boundRect

# function: get the lanes from the image
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

# function: find unique rgb values
def find_unique_rgb_values(img,min_area):
    rgb_filtered_1 = np.unique(img.reshape((-1, 3)), axis=0, return_counts = True)
    idx = np.argwhere(rgb_filtered_1[1]>=min_area)
    unique_rgb_values = np.squeeze(rgb_filtered_1[0][idx,:])
    #print(rgb_filtered_1[0][idx,:]); print(rgb_filtered_1[1][idx])
    return unique_rgb_values

# --------------------------------------------------------------------------------
# --- MAIN FUNCTION ------------------------------------------------------------------------
def main(imread_seg, imread_rgb=None):

    # initialize the output
    dict_output = {'markings':{},'polynomials':{}}
    # note: polynomials are in increasing order (y=a0+a1*x+a2*x^2+...)

    # get shape of image
    H = imread_seg.shape[0]
    W = imread_seg.shape[1]

    # calculate min pixel area (thresholds)
    min_area_bbox = H * W * min_rel_area_bbox
    min_area_lane = H * W * min_rel_area_lane

    # find all unique rgb values in the image
    unique_rgb_values = find_unique_rgb_values(imread_seg,min(min_area_bbox,min_area_lane))

    # plot the image
    if imread_rgb is not None:
        imread_rgb_rgb = cv.cvtColor(imread_rgb, cv.COLOR_BGR2RGB)
        imread_seg_rgb = cv.cvtColor(imread_seg, cv.COLOR_BGR2RGB)
        plt.subplot(3,3,1),plt.imshow(imread_rgb_rgb,'gray'); plt.title("original image")
        plt.subplot(3,3,2),plt.imshow(imread_seg_rgb,'gray'); plt.title("segm. image")
        plt.xticks([]),plt.yticks([]);

    # define index values
    index_dict_marking = 0
    index_dict_polynomials = 0
    index_subplot = 2;

    # loop over all possible colors
    bool_lane = False
    for key in dict_traffic_marking:
        # find the RGB-key
        dict_val = dict_traffic_marking[key]
        #print(dict_val)

        # check if rgb is inside image
        if dict_val['rgb'] in unique_rgb_values:
            #print("found rgb value: " + str(rgb))

            # apply the RGB-filter
            noise_reduction = 0
            if dict_val['type']!='lane':
                noise_reduction = noise_reduction_bbox
            if dict_val['type']=='lane':
                noise_reduction = noise_reduction_lane
            image_filter = rgb_filter(imread_seg,dict_val['rgb'],dict_val['type'],noise_reduction)

            # object detection: bounding box + distance
            box = None; dist = None
            if dict_val['type'] != "lane":
                #print("\nrgb: " + str(dict_val['rgb']))
                box = get_bounding_box(image_filter,min_area_bbox)
                if box != []:
                    size_pixel = 0
                    if dict_val['type']=='sign':
                        # use heigth as basis for distance
                        size_pixel = box[3]
                    if dict_val['type']=='street_marking':
                        # use width as basis for distance
                        size_pixel = box[2]
                    dist = distance_to_camera(dict_val['size'],focallength,size_pixel)
                    dict_output['markings'][index_dict_marking] = {'class':key,'color':dict_val['rgb'],'type':dict_val['type'],'distance_mm':int(dist)}
                    index_dict_marking =+ 1

            # lane detection: lanes
            contours_poly = None;
            if dict_val['type']=='lane' and bool_lane == False:
                contours_poly = get_lanes(image_filter,min_area_lane)

                for contour_poly in contours_poly:
                    bool_lane = True
                    contour_poly = contour_poly.astype('float64')
                    contour_poly[:,0] = np.divide(contour_poly[:,0], W)
                    contour_poly[:,1] = np.divide(contour_poly[:,1], H)

                    h = np.load('homography/homography.npy')
                    contour_poly = np.array([contour_poly])
                    #print("\ncontour_poly")
                    #print(contour_poly)
                    contour_poly_hom = cv.perspectiveTransform(contour_poly, h)
                    print("\ncontour_poly_hom")
                    print(contour_poly_hom)
                    contour_poly_hom = contour_poly_hom[0]

                    # Calculate the coefficients of the polynomial
                    coef1, res1, _, _, _ = np.polyfit(contour_poly_hom[:,0],contour_poly_hom[:,1],1, full=True)
                    coef2, res2, _, _, _ = np.polyfit(contour_poly_hom[:,0],contour_poly_hom[:,1],2, full=True)
                    res_diff = np.abs(np.sum(res1)-np.sum(res2)); print("residual: " + str(res_diff));
                    if res_diff<=0.2:
                        coef = coef1
                    else:
                        coef = coef2

                    #filter: remove lines if same weighting
                    bool_add_coef = True
                    for key_coef in dict_output['polynomials'].keys():
                        if len(coef)==len(dict_output['polynomials'][key_coef]):
                            coef_diff = np.linalg.norm(coef - dict_output['polynomials'][key_coef])
                            if coef_diff<0.5:
                                bool_add_coef = False
                                break

                    if bool_add_coef:
                        dict_output['polynomials'][index_dict_polynomials] = coef
                        index_dict_polynomials += 1

            if imread_rgb is not None:
                # plot results
                if (box != None and dist!=None) or (len(contours_poly)>0):
                    index_subplot +=1
                    if index_subplot<=9:
                        #print(str(dict_val['rgb']) + " - " + str(key) + " -> FOUND! -> box = " + str(box), "distance = " + str(dist))
                        ax = plt.subplot(3,3,index_subplot)
                        ax.imshow(image_filter)
                        if dict_val['type'] != "lane" and box != []:
                            rect = patches.Rectangle((box[0],box[1]),box[2],box[3],linewidth=1,edgecolor='r',facecolor='none')
                            ax.add_patch(rect)
                        if dict_val['type'] == "lane" :
                            #print("amount of lanes found: " + str(len(contours_poly)))
                            #x = np.linspace(0,1,100);
                            for j in range(len(contours_poly)):
                                contour_poly = contours_poly[j]
                                line = plt.Polygon(contours_poly[j], closed=None, fill=None, edgecolor='r')
                                ax.add_patch(line)
                        plt.title(str(key)); #plt.xticks([]),plt.yticks([]);

                        if dict_val['type'] == "lane" :
                            index_subplot +=1
                            #ax = plt.subplot(3,3,index_subplot)
                            ax = plt.subplot(3,3,index_subplot)
                            ax.set_xlim(0, 1);ax.set_ylim(-1, 1);
                            plt.xlabel('x_car'); plt.ylabel('y_car');plt.title('lane poly: 90deg cw')
                            for j in range(len(dict_output['polynomials'].keys())):
                                coef = dict_output['polynomials'][j]
                                #print(coef)
                                x = np.linspace(0,1,100);
                                contour_poly_appr = np.array(np.polyval(coef,x));
                                contour_poly_appr = np.transpose(np.concatenate((np.expand_dims(x, axis=0), np.expand_dims(contour_poly_appr, axis=0))));
                                line = plt.Polygon(contour_poly_appr, closed=None, fill=None, edgecolor='r')
                                ax.add_patch(line)

    if imread_rgb is not None:
        plt.show()

    return dict_output

# --------------------------------------------------------------------------------
# --- OFFINE ---------------------------------------------------------------------
bEvaluateOffline = True
if bEvaluateOffline==True:
    print("OFFLINE evaluation is activated. If online version is needed, set bEvaluateOffline->False")
    image_name = "TEST_3lines.png"
    #image_name = "Image0100.png"
    image_name = "Image0094.png"
    folder = 'images_simulation/machine-hall-1/'
    #folder = 'images_simulation/machine-hall-2/'
    #folder = 'images_simulation/colorful-studio-2/'
    path_image_rgb = folder + 'rgb/' + image_name
    path_image_segm = folder + 'semseg_color/' + image_name
    imread_rgb = cv.imread(path_image_rgb)
    imread_seg = cv.imread(path_image_segm)

    #print(imread_rgb)
    # option 1:
    #print("\nTest 1")
    #outp = main(imread_seg)
    #print("outp_markings: " + str(outp['markings']))
    #print("outp_polynomials: " + str(outp['polynomials']))

    # option 2:
    print("\nTest 2")
    outp = main(imread_seg, imread_rgb)
    print("outp_markings: " + str(outp['markings']))
    print("outp_polynomials: " + str(outp['polynomials']))
