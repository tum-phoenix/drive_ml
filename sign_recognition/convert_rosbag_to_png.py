#!/usr/bin/python

# Start up ROS pieces.
import rosbag
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import os
import sys
from tqdm import tqdm

class ImageCreator():
    def __init__(self):
        # Get command line arguments 'bag_to_images.py <save_dir> <filename>', where save_dir and filename exist relative to this executable file.
        if len(sys.argv) == 3:
            save_dir = os.path.join(sys.path[0], sys.argv[1])
            filename = os.path.join(sys.path[0], sys.argv[2])
            print('Bag filename = {}'.format(filename))
        else:
            raise ValueError('Invalid number of launch arguments provided, must provide 2 (save_dir and filename) in that order')

        # Use a CvBridge to convert ROS images to OpenCV images so they can be saved.
        self.bridge = CvBridge()

        # Open bag file.
        with rosbag.Bag(filename, 'r') as bag:
            for idx, (topic, msg, t) in tqdm(enumerate(bag.read_messages())):
                if topic == '/camera/image_raw':
                    try:
                        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
                    except CvBridgeError, e:
                        print e
                    image_name = os.path.join(save_dir, '{}.png'.format(idx))
                    cv2.imwrite(image_name, cv_image)

if __name__ == '__main__':
     image_creator = ImageCreator()
