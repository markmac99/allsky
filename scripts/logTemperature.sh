#!/bin/bash
dt=`/bin/date '+%d/%m/%Y %H:%M:%S'`
tm=`/usr/bin/vcgencmd measure_temp | cut -d= -f2`
echo $dt $tm  >> /home/pi/allsky/logs/temperature.log

