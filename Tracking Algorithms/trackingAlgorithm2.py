# PART OF TRACKING ALGORITHMS SERIES
#
# file: trackingAlgorithm2.py
# date: 27 AUG 2015
# auth: Jorge Pacheco
# team: E4E, Camera Trap
#
# This file contains another example of a tracking 

import cv2
import numpy as np
import CameraTrapCV as CTCV

MIN_BLOB_SIZE = 30

def diffImg(t0, t1, t2):
  d1 = cv2.absdiff(t2, t1)
  d2 = cv2.absdiff(t1, t0)
  return cv2.bitwise_and(d1, d2)

ctcv = CTCV.CameraTrapCV()

cam = cv2.VideoCapture(0)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

winName = "1", "2"
cv2.namedWindow(winName[0], cv2.CV_WINDOW_AUTOSIZE)
cv2.namedWindow(winName[1], cv2.CV_WINDOW_AUTOSIZE)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

while True:

  img = diffImg(t_minus, t, t_plus)
  imgcopy = img.copy()

  ret,img = cv2.threshold( img, 10, 255, cv2.THRESH_BINARY )
  img_grey = cv2.GaussianBlur(img,(5,5),0)
  ret,img_grey = cv2.threshold( img_grey, 10, 255, cv2.THRESH_BINARY )
  
  contour,hier = cv2.findContours(img_grey,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
  if contour:
    areas = [cv2.contourArea(c) for c in contour]
    if (areas > 1):
      max_index = np.argmax(areas)
      cnt=contour[max_index]
      
      if cv2.contourArea(contour[max_index]) >= MIN_BLOB_SIZE:
        img_out = np.zeros(img_grey.shape).astype(np.uint8)
        cv2.drawContours(img_grey, contour, max_index, (255, 255, 255), -1)
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(t,(x,y),(x+w,y+h),(0,255,0),2)

  cv2.imshow( winName[0], t )
  cv2.imshow( winName[1], img_grey )
  
  # Read next image
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

  key = cv2.waitKey(10)
  if key == 27:
    cv2.destroyWindow(winName)
    break

print "Goodbye"
