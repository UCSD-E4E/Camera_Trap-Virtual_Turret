The information here is to help users get our system up and running. If you are interested in reading more about the project, you should read the paper detailing the system architecture, tracking algorithm structure, and the results of initial research and development.

Dependencies
------------
The system was developed on a MinnowBoardMAX running Ubuntu 14.04. Note that future work involving GPIO signals will require Linux 3.19.

You will need to install the following software to use the Camera Trap program:

python 2.4.9
OpenCV 2.4
numpy
avconv
v4l-utils


Camera Setup 
------------
The program is designed to run on a complete unit, so some camera setup is required if it is being run independently of a complete camera trap.

You can determine your camera setup by writing a quick python script that imports the devmap file. It should look something like the following:

import devmap
print "/dev/video0 --> " + str(devmap.getportid(0))
print "/dev/video1 --> " + str(devmap.getportid(1))
print "/dev/video2 --> " + str(devmap.getportid(2))


Alter the script so that it prints results for all the cameras that you see when you run ls /dev/video*. The output of this script shows the mapping between the device number and the port id of the USB port it is plugged into. The main point of all this is for you to get a sense of what the port ids are for the different USB ports in case you are running them on different computers or hubs.

After you have some understanding of the USB port tree on your system, you will need to alter the array of port ids at the bottom of ControllerThread.py to let the software know the layout of the camera array. The array is formatted from right to left from the point of view of the cameras. Add the array elements in the same order that the physical cameras are configured. This may take some testing since it is a bit counterintuitive at first how the camera setup relates to the array. At this stage, you can also change the first camera parameter to determine which camera will turn on first, and the isCircle parameter which determines whether movement off the end of the array will wrap around to the other side. Another option here is to set the delay value which will set how long the tracker should wait before shutting off the program after it has stopped detecting movement.

Run the Program
---------------

Now that the cameras are configured, you can run the program. Navigate to the sourceCode folder and run python controllerThread.py. This will turn the first camera on, and will begin writing individual frames out to disk. If the cameras do not seem to transition in the correct order, you may need to return to the Camera Setup step and change the order of the port ids that were entered into the array.

To exit the program, make sure you have the visible tracking window in focus and press esc.

Post Processing
---------------

The program saves all the video it writes in the form of individual binary files. Each file represents a frame. The writerThread program names the file according to camera sequences. Each time a new camera begins recording, the sequence number is increased. You need to compile each sequence into a video. For example compile sequence 0 into video, pipe all of its frames into the following avconv command in the correct order.

cat seq0_vid* | avconv -f rawvideo -pix_fmt bgr24 -s 640x480 -r 24 -i - -an -f avi -q:v 2 -r 24 testvideo0.avi
A video file called testvideo0.avi should be created in your working directory.
