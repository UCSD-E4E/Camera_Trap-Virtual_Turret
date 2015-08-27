# file: savevid.py
# date: 26 AUG 2015
# auth: Jorge Pacheco
# team: E4E, Camera Trap
#
# Simple example of how create a video using OpenCV
# Press 'q' to exit program

import cv2

path = ('output.avi')

cap = cv2.VideoCapture(0)
cap.set(1, 20.0) #Match fps
cap.set(3,640)   #Match width
cap.set(4,480)   #Match height

#choose appropriate formate to wirte video
fourcc = cv2.cv.CV_FOURCC(*'DIV3')
video_writer = cv2.VideoWriter(path,fourcc, 20.0, (640,480))

while(cap.isOpened()):
    #read the frame
    ret, frame = cap.read()
    if ret==True:
        #show the frame
        cv2.imshow('frame',frame)
        #Write the frame
        video_writer.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
video_writer.release()
cv2.destroyAllWindows()
