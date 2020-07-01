#!/bin/bash
source /home/pi/allsky/config.sh
source /home/pi/allsky/scripts/filename.sh

cd  /home/pi/python-dvr

/usr/bin/python3 /home/pi/allsky/scripts/SetExpo.py 192.168.1.11 $1
