# PART OF TRACKING ALGORITHMS SERIES
#
# file: trackingAlgorithm1.py
# date: 27 AUG 2015
# auth: Jorge Pacheco
# team: E4E, Camera Trap
#
# This file contains part of our tracking algorithm 

import cv2
import numpy as np
import CameraTrapCV as CTCV

#define dependencies
MIN_BLOB_SIZE = 200
ctcv = CTCV.CameraTrapCV()
cam = cv2.VideoCapture(0)

#create two gray images for tracking
gray = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
gray_copy = gray.copy()
avg = np.float32(gray_copy)

while(1):
  
  #apply smoothing and thresholding to an average frame
  #and feed it to a background subtractor
  gray_copy = cv2.GaussianBlur(gray_copy,(5,5),0)
  cv2.accumulateWeighted(gray_copy,avg,0.4)
  res = cv2.convertScaleAbs(avg)
  res2 = cv2.absdiff(gray, res.copy())
  ret,img_threshold = cv2.threshold( res2, 7, 255, cv2.THRESH_BINARY )
  img_threshold = cv2.GaussianBlur(img_threshold,(5,5),0)
  ret2,img_threshold = cv2.threshold( img_threshold, 240, 255, cv2.THRESH_BINARY )


  bs = ctcv.bg_subtractor.apply(img_threshold, None, 0.05)

  # only track if image contains white contours
  if np.count_nonzero(bs) > 5:
    # Get the largest contour
    contours, hierarchy = cv2.findContours(bs, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    i_max  = np.argmax(areas)
    max_index = ctcv.getLargestContourIndex(bs)

    #draw a contour and compute its centroid only if object its big enough
    if cv2.contourArea(contours[max_index]) >= MIN_BLOB_SIZE:
      cv2.drawContours(gray, contours, max_index, (255, 255, 255), -1)
      x_pos, y_pos = ctcv.getCentroid(contours[max_index])
      cv2.circle(gray, (x_pos, y_pos), 5, (0,0,0), -1)
  
  #display image 
  cv2.imshow('original',gray)
  gray = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
  gray_copy = gray.copy()
  k = cv2.waitKey(1)
 
  if k == 27:
    break
 
cv2.destroyAllWindows()
cam.release()
