#!/bin/bash
source /home/pi/allsky/config.sh
source /home/pi/allsky/scripts/filename.sh

cd /home/pi/allsky

wget -t 1 -T 5 -O "$FULL_FILENAME" "http://192.168.1.11/webcapture.jpg?command=snap&channel=1&user=admin&password=tlJwpbo6"

# my ipcamera generates 1280x720 images but the jpeg is onlt 704x576 for some reason.
# might have fixed this - testing
convert $FULL_FILENAME -resize 1280x720\! $FULL_FILENAME.tmp
mv -f $FULL_FILENAME.tmp $FULL_FILENAME
if [ "$1" == "NIGHT" ]
then 
    scripts/saveImageNight.sh
else
    scripts/saveImageDay.sh
fi

