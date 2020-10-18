#https://www.researchgate.net/figure/Top-A-square-with-top-down-ground-truth-world-measurements-right-projects-onto-the_fig4_265097667

import cv2
import numpy as np
from matplotlib import pyplot as plt

### toy example
#a = np.array([[1, 2], [4, 5], [7, 8]], dtype='float32')
#h = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype='float32')
#print(cv2.perspectiveTransform(np.array([a]), h))

# calculate matrix H
pnt_A_s = np.array([0.19, 0.75]);   pnt_A_t = np.array([0, 0.9]);
pnt_B_s = np.array([0.45, 0.54]);   pnt_B_t = np.array([1, 0.9]);
pnt_C_s = np.array([0.55, 0.54]);   pnt_C_t = np.array([1, -0.9]);
pnt_D_s = np.array([0.95, 0.84]);   pnt_D_t = np.array([0, -0.9]);

pts_src = np.array([pnt_A_s, pnt_B_s, pnt_C_s, pnt_D_s])
pts_dst = np.array([pnt_A_t, pnt_B_t, pnt_C_t, pnt_D_t])
h, status = cv2.findHomography(pts_src, pts_dst)
np.save('homography', h)
h = np.load('homography.npy')
print(h)

# calculate transformed image
n_points = 10
x = np.expand_dims(np.linspace(0,1,n_points), axis=1);
t = np.linspace(0,1,10);

xy_1 = np.expand_dims(np.linspace(0,1,n_points), axis=1) * (pnt_B_s-pnt_A_s)+ np.ones((n_points,1))*pnt_A_s
xy_2 = np.expand_dims(np.linspace(0,1,n_points), axis=1) * (pnt_C_s-pnt_B_s)+ np.ones((n_points,1))*pnt_B_s
xy_3 = np.expand_dims(np.linspace(0,1,n_points), axis=1) * (pnt_D_s-pnt_C_s)+ np.ones((n_points,1))*pnt_C_s
xy_4 = np.expand_dims(np.linspace(0,1,n_points), axis=1) * (pnt_A_s-pnt_D_s)+ np.ones((n_points,1))*pnt_D_s
xy_1_trans = cv2.perspectiveTransform(np.array([xy_1]), h)
xy_2_trans = cv2.perspectiveTransform(np.array([xy_2]), h)
xy_3_trans = cv2.perspectiveTransform(np.array([xy_3]), h)
xy_4_trans = cv2.perspectiveTransform(np.array([xy_4]), h)

# plotting
ax = plt.subplot(1,2,1)
plt.plot(pts_src[:,0],pts_src[:,1],'ro');
plt.plot(xy_1[:,0],xy_1[:,1]); 
plt.plot(xy_2[:,0],xy_2[:,1]); 
plt.plot(xy_3[:,0],xy_3[:,1]); 
plt.plot(xy_4[:,0],xy_4[:,1]); 
plt.text(pts_src[0,0],pts_src[0,1],'a')
plt.text(pts_src[1,0],pts_src[1,1],'b')
plt.text(pts_src[2,0],pts_src[2,1],'c')
plt.text(pts_src[3,0],pts_src[3,1],'d')
plt.xlim(0,1); plt.ylim(0,1); plt.grid(True)
plt.xlabel('x'); plt.ylabel('y'); plt.title('original');
plt.gca().invert_yaxis(); 

ax = plt.subplot(1,2,2)
plt.plot(xy_1_trans[0][:,0],xy_1_trans[0][:,1]); 
plt.plot(xy_2_trans[0][:,0],xy_2_trans[0][:,1]); 
plt.plot(xy_3_trans[0][:,0],xy_3_trans[0][:,1]); 
plt.plot(xy_4_trans[0][:,0],xy_4_trans[0][:,1]); 
plt.plot(pts_dst[:,0],pts_dst[:,1],'go'); 
plt.text(pts_dst[0,0],pts_dst[0,1],'a')
plt.text(pts_dst[1,0],pts_dst[1,1],'b')
plt.text(pts_dst[2,0],pts_dst[2,1],'c')
plt.text(pts_dst[3,0],pts_dst[3,1],'d')
plt.xlim(-0.1,1.1); plt.ylim(-1.1,1.1); plt.grid(True)
plt.xlabel('y'); plt.xlabel('x'); 
plt.title('transformed'); 

plt.show()