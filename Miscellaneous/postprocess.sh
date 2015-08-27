#!/bin/bash
#name = $2 # The first argument is the filename.

# Get the highest sequence number
numVideos=`ls | grep seq | sort -nr | head -1 | cut -c 4`
# maybe build in an option that allows you to pick which sequence to run (so you don't always have to do all of them)

# turn these into optional arguments later?
#width=640
#height=480
#fps=30

for i in `seq 0 $numVideos`;
do
	echo $i
	cat seq$i_* | avconv -f rawvideo -pix_fmt bgr24 -s 640x480 -r 30 -i - -an -f avi -q:v 2 -r 30 test$i.avi
done


