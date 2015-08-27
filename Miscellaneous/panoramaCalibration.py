# PANORAMA CALIBRATION
#
# file: panoramaCalibration.py
# date: 26 AUG 2015
# auth: Jorge Pacheco
# team: E4E, Camera Trap
#
# Program shows a simple way to stich images together in order to create a viewing panorama.
# This example only shows a panorama of 3 cameras. User can easily modify the code to make it work
# with any number of cameras. 
# User needs to make sure that cameras are connected different buses for bandwidth issues.

import cv2
import numpy as np
import camera as Camera

#Create Camera objects
myCamera0 = Camera.Camera(0, "cam0.avi")
myCamera1 = Camera.Camera(1, "cam0.avi")
myCamera2 = Camera.Camera(2, "cam0.avi")

#grab camera frames
got_frame0, frame0 = myCamera0.getFrameLowRes()
got_frame1, frame1 = myCamera1.getFrameLowRes()
got_frame2, frame2 = myCamera2.getFrameLowRes()

#define height and width of each individual images
width = frame0.shape[1]
height = frame0.shape[0]

#create blank image to stitch the individual frames
blank_image = np.zeros((height,(width*3),3), np.uint8)

while True:

    #define regoin of interest for each new frame
    roi0 = frame0[0:height, 0:width]
    roi1 = frame1[0:height, 0:width]
    roi2 = frame2[0:height, 0:width]
    
    #copy individual ROIs to blank image
    blank_image[0:height, width:width*2] = roi0
    blank_image[0:height, width*2:width*3] = roi1
    blank_image[0:height, 0:width] = roi2
    
    #show image
    cv2.imshow('pan images', blank_image)
    
    #grab new frames
    got_frame0, frame0 = myCamera0.getFrameLowRes()
    got_frame1, frame1 = myCamera1.getFrameLowRes()
    got_frame2, frame2 = myCamera2.getFrameLowRes()

    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyWindow("1")
        myCamera0.off()
        myCamera1.off()
        myCamera2.off()
        break