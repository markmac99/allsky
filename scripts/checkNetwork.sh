#!/bin/bash

echo  `date +%Y%m%d-%H%M%S` checking network | tee -a /home/pi/allsky/logs/reboot-`date +%Y%m%d`.log

ping -c 1 -w 5 192.168.1.11

if [ $? -ne 0 ]
then
  echo `date +%Y%m%d-%H%M%S` rebooting | tee -a /home/pi/allsky/logs/reboot-`date +%Y%m%d`.log
  /sbin/shutdown -r now | tee -a /home/pi/allsky/logs/reboot-`date +%Y%m%d`.log
fi

