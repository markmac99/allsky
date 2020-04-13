#!/bin/bash
source /home/pi/allsky/config.sh
source /home/pi/allsky/scripts/filename.sh

cd  /home/pi/allsky/scripts
LAST_NIGHT=$(date -d '17 hours ago' +'%Y%m%d')
#LAST_NIGHT=$(date -d '1 days ago' +'%Y%m%d')

# Post end of night data. This includes next twilight time
if [[ $POST_END_OF_NIGHT_DATA == "true" ]]; then
        echo -e "Posting next twilight time to let server know when to resume liveview\n"
        ./postData.sh
	echo -e "\n"
fi

# Uncomment this to scan for, and remove corrupt images before generating
# keograms and startrails. This can take several (tens of) minutes to run
# and isn't necessary unless your system produces corrupt images which then
# generate funny colors in the summary images...
# ./removeBadImages.sh /home/pi/allsky/images/$LAST_NIGHT/  

# Generate keogram from collected images
if [[ $KEOGRAM == "true"  && ! -f /home/pi/allsky/images/$LAST_NIGHT/keogram/keogram-$LAST_NIGHT.jpg ]]; then
        echo -e "Generating Keogram\n"
	mkdir -p /home/pi/allsky/images/$LAST_NIGHT/keogram/
        ../keogram /home/pi/allsky/images/$LAST_NIGHT/ $EXTENSION /home/pi/allsky/images/$LAST_NIGHT/keogram/keogram-$LAST_NIGHT.jpg
	if [[ $UPLOAD_KEOGRAM == "true" ]] ; then
		OUTPUT="/home/pi/allsky/images/$LAST_NIGHT/keogram/keogram-$LAST_NIGHT.jpg"
		timeout 5 scp -i $IDFILE $OUTPUT $USER@$HOST:$KEOGRAM_DIR
	fi
        echo -e "\n"
fi

# Generate startrails from collected images. Treshold set to 0.1 by default in config.sh to avoid stacking over-exposed images
if [[ $STARTRAILS == "true"  && ! -f /home/pi/allsky/images/$LAST_NIGHT/startrails/startrails-$LAST_NIGHT.jpg ]]; then
    echo -e "Generating Startrails\n"
	mkdir -p /home/pi/allsky/images/$LAST_NIGHT/startrails/
    ../startrails /home/pi/allsky/images/$LAST_NIGHT/ $EXTENSION $BRIGHTNESS_THRESHOLD /home/pi/allsky/images/$LAST_NIGHT/startrails/startrails-$LAST_NIGHT.jpg
    convert  /home/pi/allsky/images/$LAST_NIGHT/startrails/startrails-$LAST_NIGHT.jpg -resize 1280x720\!  /home/pi/allsky/images/$LAST_NIGHT/startrails/startrails-$LAST_NIGHT.jpg.tmp
	mv  /home/pi/allsky/images/$LAST_NIGHT/startrails/startrails-$LAST_NIGHT.jpg.tmp  /home/pi/allsky/images/$LAST_NIGHT/startrails/startrails-$LAST_NIGHT.jpg
	if [[ $UPLOAD_STARTRAILS == "true" ]] ; then
		OUTPUT="/home/pi/allsky/images/$LAST_NIGHT/startrails/startrails-$LAST_NIGHT.jpg"
		timeout 5 scp -i $IDFILE $OUTPUT $USER@$HOST:$STARTRAILS_DIR
		timeout 5 scp -i $IDFILE $OUTPUT $USER@$HOST:$IMGDIR/startrails-latest.jpg
        fi

        echo -e "\n"
fi

# Generate timelapse from collected images
if [[ $TIMELAPSE == "true" && ! -f /home/pi/allsky/images/$LAST_NIGHT/allsky-$LAST_NIGHT.mp4 ]]; then
	echo -e "Generating Timelapse\n"
	./timelapse.sh $LAST_NIGHT
	echo -e "\n"
fi

# Automatically delete old images and videos
if [[ $AUTO_DELETE == "true" ]]; then
	del=$(date --date="$NIGHTS_TO_KEEP days ago" +%Y%m%d)
	for i in `find /home/pi/allsky/images/ -type d -name "2*"`; do
	  (($del > $(basename $i))) && rm -rf $i
	done
fi
