#!/bin/bash
# Script: my-pi-temp.sh
# Purpose: Display the ARM CPU and GPU  temperature of Raspberry Pi 2/3
# Author: Vivek Gite <www.cyberciti.biz> under GPL v2.x+
# -------------------------------------------------------
cpuk=`cat /sys/class/thermal/thermal_zone0/temp`
cpu=$((cpuk/1000))\'C
gpu=`/opt/vc/bin/vcgencmd measure_temp | awk -F"=" '{print $2}'`
echo "`date '+%Y%m%d-%H%M%S'`, $(hostname), $cpu , $gpu "

