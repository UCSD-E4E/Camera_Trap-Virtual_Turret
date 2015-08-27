#!/bin/python
#
# PROG: devmap.py
# AUTH: Anne Christy
# DATE: 13 AUG 2015
# TEAM: Camera Trap, E4E
#
# These functions create a mapping between the devid (ex: /dev/video0) and the
# usb port number (ex: 1-1.4) on the MinnowBoard MAX running Ubuntu 14.04 with
# Linux 3.19. The mapping can be used to intelligently address the cameras in
# the virtual turret through opencv without regard to the actual identity of 
# the capture device (i.e. serial number). 
#

import os, subprocess

# Takes in a portid as a string (example: "1-1.4").
# Returns the path to the video device (example: "/dev/video1"). If the device
# or portid are nonexistent, returns None. 
def getdevid(portid):
	DIR = '/dev'
	for device in os.listdir(DIR):		# Gets the /dev directory list.
		if device.startswith("video"):  # Parses for video* (like grep).
			pathinfo = getInfoAsList("/dev/" + str(device))
			port = pathinfo[6]		# Item 6 identifies the usb port hierarchy.
			if port == portid:
				return "/dev/" + pathinfo[-1].rstrip()
	return None

# Same as getdevid, but it returns an int.
def getdevnum(portid):
	DIR = '/dev'
	for device in os.listdir(DIR):		# Gets the /dev directory list.
		if device.startswith("video"):  # Parses for video* (like grep).
			pathinfo = getInfoAsList("/dev/" + str(device))
			port = pathinfo[6]		# Item 6 identifies the usb port hierarchy.
			if port == portid:
				return int(pathinfo[-1].rstrip()[5:])
	return None	



# Takes in a video device path as a string (example: "/dev/video1").
# Returns a string representing the usb port the device is attached to
# (example: "1-1.4"). If devid does not exist, returns None.
def getportid(devid):
	if int(devid[-1]) in listDevNums(): 		# Confirm that devid exists.
		return getInfoAsList(devid)[6]
	else:
		return None

# This is the same as getportid(devid) except it takes in an integer.
def getportid(devnum):
	if devnum in listDevNums():
		return getInfoAsList("/dev/video" + str(devnum))[6]
	else:
		return None


# Takes in a video device path as a string (exanple: "/dev/video1").
# Returns the grep result in the form of a list for parsing. If the devid
# does not exist on the system, returns None.
def getInfoAsList(devid):
	if int(devid[-1]) in listDevNums(): 		# Confirm that devid exists.
		# Define the subprocess as udevadm info /dev/video* | grep DEVPATH
		subproc = "udevadm info " + devid + " | grep DEVPATH" 
		# This just runs a simple grep call to filter the results of udevadm.
		grepresult = subprocess.Popen(subproc, 
				 stdout=subprocess.PIPE,
				 shell=True,
				 preexec_fn=os.setsid)
		# Return a list using the / symbol as the delimiter.
		return grepresult.stdout.read().split("/")  
	else:
		return None


# Returns the number of /dev/video* devices present on the system.
def countVideoDevices():
	DIR = '/dev'
	return len([item for item in os.listdir(DIR) if item.startswith("video")])


# Returns a list containing the device numbers. For example, if the system
# currently has /dev/video0 and /dev/video2, it will return [0, 2]. This is
# useful for making certain that user cannot request devices that are not
# currently running on the system.
def listDevNums():
	DIR = '/dev'
	result = []  # The list is empty if no video devices are connected.
	for device in os.listdir(DIR):
		if device.startswith("video"):
			result += [int(device[5:])] # Add the int device number to the list.
	return result
print getportid(0)
print getportid(1)
print getportid(2)
print getportid(3)







