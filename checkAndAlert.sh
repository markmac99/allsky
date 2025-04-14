#!/bin/bash
#
# script to check and restart allsky if frozen
# Copyright (C) Mark McIntyre
#

srcdir="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $srcdir
source $HOME/miniconda3/bin/activate ukmon-shared

BROKER=broker
MQUSER=mquser
MQPASS=mqpass

sts=$(mosquitto_sub -h ${BROKER} -u ${MQUSER} -P ${MQPASS} -t meteorcams/allsky/status -i checkallsky -C 1)
lastupdate=$(mosquitto_sub -h ${BROKER} -u ${MQUSER} -P ${MQPASS} -t meteorcams/allsky/last_update -i checkallsky -C 1)

python -c "from sendAllskyAlert import checkAndSend;checkAndSend($sts, '$lastupdate');"
