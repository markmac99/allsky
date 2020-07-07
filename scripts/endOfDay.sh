#!/bin/bash
source /home/pi/allsky/config.sh
source /home/pi/allsky/scripts/filename.sh

cd  /home/pi/allsky/scripts
LAST_NIGHT=$(date +'%Y%m%d')

# Uncomment this to scan for, and remove corrupt images before generating
# keograms and startrails. This can take several (tens of) minutes to run
# and isn't necessary unless your system produces corrupt images which then
# generate funny colors in the summary images...
# ./removeBadImages.sh /home/pi/allsky/images/$LAST_NIGHT/  

# Generate timelapse from collected images
if [[ $TIMELAPSE == "true" && ! -f /home/pi/allsky/images/$LAST_NIGHT/daytime/allsky-$LAST_NIGHT.mp4 ]]; then
	echo -e "Generating Timelapse\n"
	./daytimelapse.sh $LAST_NIGHT
	echo -e "\n"
fi
