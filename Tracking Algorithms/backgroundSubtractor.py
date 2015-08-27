import cv2
import numpy as np

cam = cv2.VideoCapture(0)

winName = "Background Subtractor"
cv2.namedWindow(winName[0], cv2.CV_WINDOW_AUTOSIZE)
bg = cv2.BackgroundSubtractorMOG(history=200, nmixtures=3, backgroundRatio=0.7, noiseSigma=0)
got_frame, frame = cam.read()
while ((got_frame) or (frame != None)):

	#apply background subtractor
	fg = bg.apply(frame)

	#create kernel image to apply morphological operations
	kernel = np.zeros((11,11),np.uint8)

	# 'open' the image
	erosion = cv2.erode(fg,kernel,iterations = 1)
	dilation = cv2.dilate(erosion,kernel,iterations = 1)

	cv2.imshow( winName[0], fg )
	# Read next image
	got_frame, frame = cam.read()
	key = cv2.waitKey(10)
	if key == 27:
		cv2.destroyWindow(winName[1])
		break

print "Goodbye"
