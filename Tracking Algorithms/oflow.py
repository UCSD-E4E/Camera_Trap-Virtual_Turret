import cv2
import numpy as np

cam = cv2.VideoCapture(0)

winName = "1", "2"
cv2.namedWindow(winName[0], cv2.CV_WINDOW_AUTOSIZE)

got_frame, frame = cam.read()
prev_gray = None

while got_frame:

	frame2 = frame.copy()
	gray = cv2.cvtColor(frame2, cv2.cv.CV_BGR2GRAY)

	if prev_gray != None:

		xsum, ysum = 0,0

		xvel, yvel = 0,0

		flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, pyr_scale=0.5, levels=5, winsize=13, iterations=10, poly_n=5, poly_sigma=1.1, flags=0) 

		for y in range(0, flow.shape[0], 16):

			for x in range(0, flow.shape[1], 16):

				fx, fy = flow[y, x]
				xsum += fx
				ysum += fy

				cv2.line(frame2, (x,y), (int(x+fx),int(y+fy)), (0,255,0))
				cv2.circle(frame2, (x,y), 1, (0,255,0), -1)

		cv2.imshow( winName[1], frame2 )

	prev_gray = gray

	got_frame, frame = cam.read()
	key = cv2.waitKey(10)
	if key == 27:
		cv2.destroyWindow(winName[1])
		break

print "Goodbye"
