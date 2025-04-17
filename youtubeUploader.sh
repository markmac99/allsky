#!/bin/bash

# Copyright (C) Mark McIntyre
#
# install the cronjobs

srcdir="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $srcdir
source ~/vAllsky/bin/activate

ping -c 1 www.googleapis.com # ensure the URL is in the DNS cache

python $srcdir/ytUpload.py /var/log/allsky.log $HOME/allsky