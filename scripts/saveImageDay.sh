#!/bin/bash
source /home/pi/allsky/config.sh
source /home/pi/allsky/scripts/filename.sh

cd /home/pi/allsky

# Make a directory to store current images
CURRENT=$(date +'%Y%m%d')
mkdir -p images/$CURRENT/daytime/thumbnails

IMAGE_TO_USE="$FULL_FILENAME"
cp $IMAGE_TO_USE "liveview-$FILENAME.$EXTENSION"

# If upload is true, create a smaller version of the image and upload it
if [ "$UPLOAD_IMG" = true ] ; then
	echo -e "Resizing $FULL_FILENAME\n"

	# Create a thumbnail for live view
	# Here's what I use with my ASI224MC
	convert "$IMAGE_TO_USE" -resize 1280x720\! "$FILENAME-resize.$EXTENSION";

	# Here's what I use with my ASI185MC (larger sensor so I crop the black around the image)
	# convert "$IMAGE_TO_USE" -resize 962x720 -gravity Center -crop 680x720+40+0 +repage "$FILENAME-resize.$EXTENSION";
	
	echo -e "Uploading $FILENAME-resize.$EXTENSION \n" 
	timeout 5 scp -i $IDFILE $FILENAME-resize.$EXTENSION $USER@$HOST:$IMGDIR/allsky-latest.$EXTENSION
fi

# Create a thumbnail of the image for faster load in web GUI
if identify $IMAGE_TO_USE >/dev/null 2>&1; then
        convert "$IMAGE_TO_USE" -resize 100x75 "images/$CURRENT/daytime/thumbnails/$FILENAME-$(date +'%Y%m%d%H%M%S').$EXTENSION";
fi

echo -e "Saving $FILENAME-$(date +'%Y%m%d%H%M%S').$EXTENSION\n"
cp $FULL_FILENAME images/$CURRENT/daytime/$FILENAME-$(date +'%Y%m%d%H%M%S').$EXTENSION

