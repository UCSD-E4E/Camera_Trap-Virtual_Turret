# CONTROLLER THREAD
#
# file: controllerThread.py
# date: 7 AUG 2015
# auth: Anne Christy
# team: E4E, Camera Trap
#

# To postprocess the video in the command line:
# cat cam* | avconv -f rawvideo -pix_fmt bgr24 -s 640x480 -r 30 -i - -an -f avi -q:v 2 -r 30 test.avi


import threading
import Queue
import writerThread
import trackerThread
import devmap
import cv2
from datetime import datetime
import time
from threading import Thread, current_thread


class Controller(object):
	def __init__(self, ports, isCircle, firstCamera, delay):
		#self.name = "controller"
		# Boolean to clean up program at quit.
		self.isRunning = True

		# Make queues for communicating with other threads.
		self.writerQ = Queue.Queue(maxsize=0)
		self.trackerQ = Queue.Queue(maxsize=0)

		self.trackerDelay = delay

		# Create a lock for safely using the callback function.
		self.lock = threading.RLock()
		self.threadLock = threading.RLock()

		# Indicates whether the cameras should wrap around at list end.
		self.is360 = isCircle
		# Save the list of usb ports the cameras are attached to. This must
		# be hard-coded and input to the Controller constuctor.
		self.portList = ports
		self.numCameras = len(self.portList)

		self.currentDev = 0 # For initialization.
		self.currentPort = None  # For initialization.
		# Set the correct values for the currentPort.
		if len(self.portList) > 0:
			self.currentPort = self.portList[firstCamera]
			#print "current port: " + str(self.currentPort)
			self.currentDev = devmap.getdevnum(self.currentPort)

		# Create the VideoCapture object.
		self.cap = cv2.VideoCapture(self.currentDev)
		self.cap.set(3,640)
		self.cap.set(4,480)

		#print str(self.name) + ": initializing the controller"

	# Returns a Writer Thread object.
	def createWriter(self):
		#print str(self.name) + ": creating the writer"
		writer = writerThread.Writer(self.writerQ, parent=self)
		return writer

	# Returns a Tracker Thread object that can run callbacks on the Controller.
	def createTracker(self):
		#print str(self.name) + ": creating the tracker"
		tracker = trackerThread.Tracker(self.trackerQ, self.threadLock, self.trackerDelay, parent=self)
		#print "Port List = " + str(self.portList)
		return tracker

	def finish(self):
		self.isRunning = False

	# A callback function for the tracker to tell the view to move left.
	def moveLeft(self):
		leftCam = self.getCameraLeft()
		if not self.currentDev == leftCam:
			self.currentDev = leftCam
			self.lock.acquire()
			self.cap.release()
			self.cap.open(self.currentDev)
			self.lock.release()


	# A callback function for the tracker to tell the view to move right.
	def moveRight(self):
		rightCam = self.getCameraRight()
		if not self.currentDev == rightCam:
			self.currentDev = rightCam
			self.lock.acquire()
			self.cap.release()
			self.cap.open(self.currentDev)
			self.lock.release()	


	# Returns the device number of the camera left of the current camera.
	def getCameraRight(self):
		nextPort = self.currentPort
		currentIndex = self.portList.index(self.currentPort)
		#print "currentIndex = " + str(currentIndex)
		if currentIndex > 0:  # Check if the camera is on the far right.
			nextPort = self.portList[currentIndex - 1]
		elif self.is360 == True and currentIndex == 0:
			nextPort = self.portList[-1]  # Wrap around.
		#print "nextport = " + str(nextPort)
		self.currentPort = nextPort
		return devmap.getdevnum(nextPort) 
		
	# Returns the device number of the camera right of the current camera.
	def getCameraLeft(self):
		nextPort = self.currentPort 
		currentIndex = self.portList.index(self.currentPort)
		#print "currentIndex = " + str(currentIndex)
		if currentIndex < self.numCameras - 1: # Check if camera is on end.
			nextPort = self.portList[currentIndex + 1]
		elif self.is360 == True and currentIndex == self.numCameras - 1:
			nextPort = self.portList[0] # Wrap around.
		#print "nextport = " + str(nextPort)
		self.currentPort = nextPort
		return devmap.getdevnum(nextPort)

	# Run the contoller.
	def control(self):
		# Create the threads.
		writer = self.createWriter()
		tracker = self.createTracker()
		# Start the threads.
		writer.start()
		tracker.start()

 		while self.isRunning:
 			self.lock.acquire()
			ret, frame = self.cap.read()  # Read the frame from the camera.
			self.lock.release()
			resize_image = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_NEAREST)
			if ret:
				timestamp = datetime.utcnow().strftime('%y%m%d%H%M%S%f')
				devNum = self.currentDev
				#filename = 'cam' + str(devNum) + '_' + timestamp
				tup = (frame, timestamp, devNum, self.isRunning)
				#tup2 = (resize_image, devNum)
				self.writerQ.put(tup)  # Send the frame to the writer.
				self.threadLock.acquire()
				self.trackerQ.queue.clear() # empty so tracker pulls newest frame.
				#print "put frame in trackerQ"
				self.trackerQ.put(resize_image) # Send the frame to the tracker.
				self.threadLock.release()
				# cv2.imshow('frame', frame)
		  #       if cv2.waitKey(1) & 0xFF == ord('q'):
		  #       	break
		writer.join()
		tracker.join()

if __name__=='__main__':
	orderedPorts = ['1-1.1', '1-1.2', '1-1.3']
	# Cameras at the front of the list are on the "right" and cameras at the
	# end of the list are on the "left."
	firstCamera = 0  # Index in orderPorts list for which camera turns on first.

	# Create and start the controller object.
	controller = Controller(ports=orderedPorts, isCircle=False, firstCamera=firstCamera, delay=10)
	controller.control()
	
