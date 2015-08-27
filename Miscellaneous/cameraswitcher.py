import os
import signal
import subprocess


class Camera:
    #and switch between cameras.

	def __init__(self, device_number):
		self.filecount = 0;  # Number appended on each new video file.
		self.dev = device_number 
		self.proc_id = -1 # Inistialize the pid. 


	def start_recording(self):
		''' Begin recording on the camera at /dev/video<camera_number>.'''

		# Name the device.
		device = "/dev/video" + str(self.dev)
		# Name the output file.
		filename = "dev" + str(self.dev) + "_output_" + str(self.filecount) + ".avi"
		# Identify the linux command to turn on the camera.
		print "Filming with " + str(device)
		print "writing file " + str(filename)
		# Turn on the camera. This executes a shell command.
		p = subprocess.Popen(subproc, 
					 stdout=subprocess.PIPE,
					 shell=True,
					 preexec_fn=os.setsid)

		self.proc_id = p.pid        # Update the pid so we can kill the process later.

	def stop_recording(self):
		''' Send a signal to stop the camera.'''
		# Check if the camera has been started before trying to kill it.
		if self.proc_id > 0:
			# Send an interrupt to the camera process.
			os.killpg(self.proc_id, signal.SIGTERM) 
			# Update the filename.
			self.filecount += 1
			# Make pid reflect camera being off.
			self.proc_id = -1
		else:
			print "Camera " + str(self.dev) + "not running."


	def is_recording(self):
		'''Check if the camera is currently on.'''
		if self.proc_id < 0:
			return False
		else:
			return True
		






