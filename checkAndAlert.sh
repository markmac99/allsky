#!/bin/bash
#
# script to check and restart allsky if frozen
# Copyright (C) Mark McIntyre
#

srcdir="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $srcdir
source $HOME/miniconda3/bin/activate ukmon-shared

python $srcdir/sendAllskyAlert.py
