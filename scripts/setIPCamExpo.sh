#!/bin/bash
source /home/pi/allsky/config.sh
source /home/pi/allsky/scripts/filename.sh

/usr/bin/python3 /home/pi/allsky/scripts/SetExpo.py $IPCAMADDR $1
