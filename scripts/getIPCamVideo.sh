#!/bin/bash
source /home/pi/allsky/config.sh
source /home/pi/allsky/scripts/filename.sh

cd /home/pi/allsky

echo $# $0 $1 
timeout 6 vlc "rtsp://192.168.1.11:554/user=admin&password=&channel=1&stream=0.sdp" --sout file/ts:/home/pi/allsky/test.avi -I dummy

# my ipcamera generates 1280x720 images but the jpeg is onlt 704x576 for some reason.
#convert $FULL_FILENAME -resize 1280x720\! $FULL_FILENAME.tmp
#mv -f $FULL_FILENAME.tmp $FULL_FILENAME

#if [ "$1" == "NIGHT" ]
#then 
#    scripts/saveImageNight.sh
#else
#    scripts/saveImageDay.sh
#fi

