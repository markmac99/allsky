#!/bin/bash
source /home/pi/allsky/config.sh
source /home/pi/allsky/scripts/filename.sh

cd  /home/pi

/usr/bin/python allsky/scripts/SetExpo.py 192.168.1.11 $1
