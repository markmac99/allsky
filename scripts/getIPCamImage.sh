#!/bin/bash
source /home/pi/allsky/config.sh
source /home/pi/allsky/scripts/filename.sh

cd /home/pi/allsky

mkdir tmp >/dev/null 2>&1
# get a bunch images and stack them - aim for about 10 secs worth in total
date > tmp/start.txt
for i in {1..25}
do 
    FN=tmp/$i-$FULL_FILENAME
    wget -t 1 -T 5 -O "$FN" "http://192.168.1.11/webcapture.jpg?command=snap&channel=1&user=admin&password=tlJwpbo6"

done
date >> tmp/start.txt
./startrails tmp $EXTENSION $BRIGHTNESS_THRESHOLD $FULL_FILENAME

# my ipcamera generates 1280x720 images but the jpeg is squashed for some reason.
#convert test-$FULL_FILENAME -resize 1280x720\! test-$FULL_FILENAME.tmp
#mv -f test-$FULL_FILENAME.tmp test-$FULL_FILENAME
# decided not to do that after all 

rm -f tmp/*.$EXTENSION

if [ "$1" == "NIGHT" ]
then 
    scripts/saveImageNight.sh
else
    scripts/saveImageDay.sh
fi

