#!/bin/bash
source /home/pi/allsky/scripts/ftp-settings.sh

# Set to true to upload current image to your website
UPLOAD_IMG=true

# Set to true to upload timelapse video to your website at the end of each night
UPLOAD_VIDEO=true

# Set to true to send data to your server at the end of each night
POST_END_OF_NIGHT_DATA=true

# Set to true to generate a timelapse at the end of the night
TIMELAPSE=true

# Set to true to generate a keogram at the end of the night (image summary of the night)
KEOGRAM=true

# Set to true to upload the keogram after it has been generated
UPLOAD_KEOGRAM=true

# Set to true to generate a startrails image of the night. Will skip brighter images to avoid over-exposure
STARTRAILS=true

# Images with a brightness higher than the threshold will be skipped for startrails image generation
BRIGHTNESS_THRESHOLD=0.40

# Set to true to upload the startrails after it has been generated
UPLOAD_STARTRAILS=true

# Set to true to enable automatic deletion of archived data (images + videos)
AUTO_DELETE=true

# Set this value to the number of archived nights you want to keep. Needs AUTO_DELETE=true to work
NIGHTS_TO_KEEP=14

# Path to the dark frame for hot pixels subtraction. Can be jpg or png.
DARK_FRAME="dark.png"

# Set to 0 to disable Daytime Capture
DAYTIME="1"

# set to 0 to disable image stretching
STRETCH="1"

# stretch parameters - see documentation for 'convert -sigmoidal-contrast'
CONTRAST=8
MIDPOINT=25

# IP Camera address, if needed
IPCAMADDR=192.168.1.11
DEVICESTRING="rtsp://192.168.1.11:554/user=admin&password=&channel=1&stream=0.sdp"
export DEVICESTRING

# Path to the camera settings (exposure, gain, delay, overlay, etc)
CAMERA_SETTINGS="/etc/raspap/settings.json"
