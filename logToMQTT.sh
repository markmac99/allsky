#!/bin/bash
# Copyright (C) Mark McIntyre
#

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
source ~/vAllsky/bin/activate

cd $here/../rms_mqtt
python -c "from sendToMQTT import sendOtherData;sendOtherData('allsky')"
