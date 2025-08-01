#!/bin/bash

# Copyright (C) Mark McIntyre
#
# install the cronjobs

srcdir="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $srcdir
source ~/vAllsky/bin/activate

apiserver=www.googleapis.com
oauthserver=oauth2.googleapis.com
failed=1
loop=0
while [ $failed != 0 ] ; do 
    ping -4 -c 2 -W 10 -w 30 $oauthserver # ensure the v4 address is in the DNS cache
    ping -6 -c 2 -W 10 -w 30 $oauthserver 
    ping -4 -c 2 -W 10 -w 30 $apiserver 
    ping -6 -c 2 -W 10 -w 30 $apiserver 
    failed=$?
    loop=$((loop+1))
    if [ $loop -gt 30 ] ; then 
        echo "failed to find the api server"
        failed=0
    else
        if [ $failed == 0 ]; then 
            python $srcdir/ytUpload.py /var/log/allsky.log $HOME/allsky
        fi
    fi
done

