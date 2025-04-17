# python script to check and restart the allsky camera if needed
# copyright Mark McIntyre 2025-

import os
import datetime
import time
import logging
from logging.handlers import RotatingFileHandler
from random import randint
import RPi.GPIO as GPIO
import configparser

from sendToMQTT import sendStatusUpdate

log = logging.getLogger('checkAllsky')

MAXDELAY = 120      # time to wait to rebood
SUPERMAXDELAY=1800  # wait 30 mins to create timelapse in case its still working


if __name__ == '__main__':
    srcdir = os.path.split(os.path.abspath(__file__))[0]
    localcfg = configparser.ConfigParser()
    localcfg.read(os.path.join(srcdir, 'config.ini'))

    logdir = localcfg['checking']['logdir']
    triggerpin = int(localcfg['checking']['triggerpin'])
    logfile = localcfg['checking']['allskylog']
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser(f'{logdir}/checkAllsky.log'), maxBytes=512000, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    stopfile = os.path.expanduser(f'{logdir}/stopcheckallsky')

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(triggerpin, GPIO.OUT)
    GPIO.output(triggerpin, GPIO.LOW)

    if os.path.isfile(stopfile):
        os.remove(stopfile)
    runme = True
    log.info('starting')
    while runme is True:
        log.info('checking')
        status = 1
        loglines = open(logfile, 'r').readlines()
        try:
            lastline = loglines[-1]
            prevline = loglines[-2]
            
            lastdt = datetime.datetime.strptime(lastline[:15], '%b %d %H:%M:%S').replace(tzinfo=datetime.timezone.utc)
            delay = (datetime.datetime.now(tz=datetime.timezone.utc)-lastdt).seconds 
            # if 'Unable to' in lastline or 'Unable to' in prevline or delay > MAXDELAY:
            if delay > MAXDELAY:
                stalled = True
                log.info('stuck, alerting operator')
                status = 0
        except Exception:  
            pass
        # add some randomness to ensure that OpenHab logs the values.
        status = status + (randint(0,9)/1000.0)
        sendStatusUpdate(status, datetime.datetime.now())
        if status == 0:
            GPIO.output(triggerpin, GPIO.HIGH)
            log.info('rebooting')
            os.system('sudo shutdown -h now')

        if os.path.isfile(stopfile):
            os.remove(stopfile)
            log.info('quitting')
            GPIO.cleanup()
            runme = False
        else:
            log.info('sleeping')
            time.sleep(MAXDELAY)
