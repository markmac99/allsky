#!/bin/bash
source /home/pi/allsky/config.sh
source /home/pi/allsky/scripts/filename.sh

cd  /home/pi/allsky/scripts

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

if [ $# -lt 1 ]
  then
    echo -en "${RED}You need to pass a day argument\n"
        echo -en "    ex: uploadForDay.sh 20180119${NC}\n"
        exit 3
fi

# Upload keogram
echo -e "Uploading Keogram\n"
KEOGRAM="/home/pi/allsky/images/$1/keogram/keogram-$1.jpg"
scp -i $IDFILE $KEOGRAM $USER@$HOST:$KEOGRAM_DIR
echo -e "\n"

# Upload Startrails
echo -e "Uploading Startrails\n"
STARTRAILS="/home/pi/allsky/images/$1/startrails/startrails-$1.jpg"
scp -i $IDFILE $STARTRAILS $USER@$HOST:$STARTRAILS_DIR
echo -e "\n"

# Upload timelapse
echo -e "Uploading Timelapse\n"
TIMELAPSE="/home/pi/allsky/images/$1/allsky-$1.mp4"
scp -i $IDFILE $TIMELAPSE $USER@$HOST:$MP4DIR
echo -e "\n"
