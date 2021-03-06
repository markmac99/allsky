#!/bin/bash
source /home/pi/allsky/config.sh

# TODO Needs fixing when civil twilight happens after midnight
cd /home/pi/allsky/scripts

latitude=51.88N
longitude=1.31W
timezone=-000
streamDaytime=false

if [[ $DAYTIME == "1" ]] ; then
	streamDaytime=true;
fi

echo "Posting Next Twilight Time"
today=`date +%Y-%m-%d`
time="$(/home/pi/allsky/sunwait list set civil $latitude $longitude)"
timeNoZone=${time:0:5}
echo { > data.json
echo \"sunset\": \"$today"T"$timeNoZone":00.000$timezone"\", >> data.json
echo \"streamDaytime\": \"$streamDaytime\" >> data.json
echo } >> data.json
echo "Uploading data.json"
timeout 5 scp -i $IDFILE data.json $USER@$HOST:$IMGDIR
