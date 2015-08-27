# TRACKING ALGORITHMS
#
# file: trackingalgos.py
# date: 19 AUG 2015
# auth: Jorge Pacheco
# team: E4E, Camera Trap
#
# This file contains functional tracking algos that can be used
# to run the CameraTrap system 

import cv2
import numpy as np
import CameraTrapCV as CTCV
ctcv = CTCV.CameraTrapCV()

#minimum size of the 'white blob' to track
MIN_BLOB_SIZE = 20
#kernel image used to apply morphological changes
kernel = np.ones((5,5),np.uint8)

def diffaccWeight(gray_copy,gray, avg):
	#define default values in case there is nothing to track
	x = -1
	y = -1

	#start by smoothing the image using gaussian blur
	gray_copy = cv2.GaussianBlur(gray_copy,(5,5),0)
	#compute the average weight of frames at rate 0.4
	#this value can and should be changed depending on desired
	#responsiveness of system
	cv2.accumulateWeighted(gray_copy,avg,0.4)
	
	#make the accumulated weight redeable by scaling it down
	res = cv2.convertScaleAbs(avg)
	
	#take the difference of the average frame and the original gray frame
	res2 = cv2.absdiff(gray, res.copy())

	#threshold and smooth the image to reduce noises
	ret,img_grey2 = cv2.threshold( res2, 7, 255, cv2.THRESH_BINARY )
	img_grey2 = cv2.GaussianBlur(img_grey2,(5,5),0)
	ret2,img_grey2 = cv2.threshold( img_grey2, 240, 255, cv2.THRESH_BINARY )

	#apply background subtractor to get significan changes of frames
	img_thresh = ctcv.bg_subtractor.apply(img_grey2, None, 0.05)
	
	#Erode and dilute the frame to further filter frame from noise 
	img_thresh = cv2.morphologyEx(img_thresh, cv2.MORPH_OPEN, kernel)
	
	#only when image has a significant contour to track, compute its maximum area, 
	#and draw that contour onto original gray image
	if np.count_nonzero(img_thresh) > 5:
		# Get the largest contour
		contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		areas = [cv2.contourArea(c) for c in contours]
		i_max  = np.argmax(areas)
		max_index = ctcv.getLargestContourIndex(img_thresh)

		# Make sure it's big enough
		if cv2.contourArea(contours[max_index]) >= MIN_BLOB_SIZE:
			img_out = np.zeros(img_thresh.shape).astype(np.uint8)
			cv2.drawContours(gray, contours, max_index, (255, 255, 255), -1)
			#the the x and y values of the object's centroid
			x, y = ctcv.getCentroid(contours[max_index])

	return gray, x, y


def runningAvg(frame, running_average_in_display, avg):
	x_pos = 0
	y_pos = 0
	display_image = frame.copy()

	#smooth image
	blur = cv2.GaussianBlur(display_image,(5,5),0)

	#calculate running avg
	cv2.accumulateWeighted(blur,avg,0.5)
	res = cv2.convertScaleAbs(avg)
	cv2.convertScaleAbs(avg,running_average_in_display, 1.0, 0.0)

	#get the difference between avg and image
	difference = cv2.absdiff(display_image, running_average_in_display)

	#convert image to grayscale
	img_grey = cv2.cvtColor(difference, cv2.COLOR_RGB2GRAY)

	#compute threshold
	ret,img_grey = cv2.threshold( img_grey, 2, 255, cv2.THRESH_BINARY )

	#smooth and threshold again to eliminate sparkles
	img_grey = cv2.GaussianBlur(img_grey,(5,5),0)
	ret,img_grey = cv2.threshold( img_grey, 240, 255, cv2.THRESH_BINARY )

	grey_image_as_array = np.asarray(  img_grey  )
	non_black_coords_array = np.where( grey_image_as_array > 3 )
	non_black_coords_array = zip( non_black_coords_array[1], non_black_coords_array[0] )

	bounding_box_list = []

	contour,hier = cv2.findContours(img_grey,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

	areas = [cv2.contourArea(c) for c in contour]
	max_index = np.argmax(areas)
	cnt=contour[max_index]
	if (cv2.contourArea(contour[max_index]) > 5000):
		polygon_points = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)
		bounding_rect = cv2.boundingRect( cnt )
		point1 = ( bounding_rect[0], bounding_rect[1] )
		point2 = ( bounding_rect[0] + bounding_rect[2], bounding_rect[1] + bounding_rect[3] )
		bounding_box_list.append( ( point1, point2 ) )
		cv2.fillPoly( img_grey, [ polygon_points ], (255,255,255) )
		x,y,w,h = cv2.boundingRect(cnt)
		x_pos, y_pos = ctcv.getCentroid(contour[max_index])
		cv2.circle(display_image, (x_pos, y_pos), 3, (0,0,0), -1)
		cv2.rectangle(display_image,(x,y),(x+w,y+h),(0,255,0),2)
		#cv2.imshow( "2", display_image )
		#return display_image, x_pos, y_pos
		return display_image, x_pos, y_pos
	
	return frame, x_pos, y_pos