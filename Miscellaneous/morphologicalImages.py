# EXAMPLE THAT DOES MORPHOLOGICAL OPERATIONS
#
# file: morphologicalImages.py
# date: 26 AUG 2015
# auth: Jorge Pacheco
# team: E4E, Camera Trap
#

import numpy as np
import cv2

#open video file or use camera if desired
cap = cv2.VideoCapture('forest.mp4')
#cap = cv2.VideoCapture(0)

ret, frame = cap.read()
t0 = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
avg = np.float32(t0)
kernel = np.ones((5,5),np.uint8)

width = frame.shape[1]
height = frame.shape[0]

blank_image = np.zeros(((height*2),(width*3)), np.uint8)

while True:
	
	#setting up parameters
	ret, frame = cap.read()

	if(ret == None or frame == None):
		break
		
	gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
	gray_copy = gray.copy()
	
	#blur gray scale image
	gray_copy = cv2.GaussianBlur(gray_copy,(5,5),0)
	
	#compute the accumulated weight of images
	cv2.accumulateWeighted(gray_copy,avg,0.4)
	
	#scale down image
	res = cv2.convertScaleAbs(avg)
	
	#compute difference between weighted and original gray scale image
	res2 = cv2.absdiff(gray, res.copy())

	#threshold the image
	ret,img_threshold = cv2.threshold( res2, 7, 255, cv2.THRESH_BINARY )
	
	#apply gaussian blur
	img_blur = cv2.GaussianBlur(img_threshold,(5,5),0)
	
	#threshold the image again
	ret2,img_threshold = cv2.threshold( img_blur, 240, 255, cv2.THRESH_BINARY )

	#set region of interst for each image
	roi0 = img_threshold[0:height, 0:width]
	opening = cv2.morphologyEx(img_threshold, cv2.MORPH_OPEN, kernel)
	roi1 = opening[0:height, 0:width]
	closing = cv2.morphologyEx(img_threshold, cv2.MORPH_CLOSE, kernel)
	roi2 = closing[0:height, 0:width]
	gradient = cv2.morphologyEx(img_threshold, cv2.MORPH_GRADIENT, kernel)
	roi3 = gradient[0:height, 0:width]
	tophat = cv2.morphologyEx(img_threshold, cv2.MORPH_TOPHAT, kernel)
	roi4 = tophat[0:height, 0:width]
	blackhat = cv2.morphologyEx(img_threshold, cv2.MORPH_BLACKHAT, kernel)
	roi5 = blackhat[0:height, 0:width]

	#assign region of interest to blank image
	blank_image[0:height, 0:width] = roi0
	blank_image[0:height, width:width*2] = roi1
	blank_image[0:height, width*2:width*3] = roi2
	blank_image[height:height*2, 0:width] = roi3
	blank_image[height:height*2, width:width*2] = roi4
	blank_image[height:height*2, width*2:width*3] = roi5

	cv2.imshow('Mophological Images', blank_image)
	
	k = cv2.waitKey(1) & 0xff
	if k == 27:
		break


cap.release()
cv2.destroyAllWindows()