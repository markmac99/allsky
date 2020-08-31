#!/bin/bash

export PATH=$PATH:/usr/bin:/usr/sbin:/sbin
/usr/bin/logger `date +%Y%m%d-%H%M%S` checking network 

ping -c 1 -w 5 192.168.1.254  >/dev/null 2>1
ret=$?
if [ $ret -ne 0 ] ; then 
  sleep 10
  ping -c 1 -w 5 192.168.1.254 > /dev/null 2>&1
  ret=$?
  if [ $ret -ne 0 ] ; then 
    /usr/bin/logger `date +%Y%m%d-%H%M%S` rebooting 
    /sbin/shutdown -r now 
  else
    /usr/bin/logger check 2 network up - retcode was $ret
  fi
else 
  /usr/bin/logger network up - retcode was $ret
fi

