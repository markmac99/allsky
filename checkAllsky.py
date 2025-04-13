# python script to check and restart the allsky camera if needed
# copyright Mark McIntyre 2025-

import os
import datetime
import time
import logging
from logging.handlers import RotatingFileHandler

from sendToMQTT import sendStatusUpdate

log = logging.getLogger('checkAllsky')

MAXDELAY = 120      # time to wait to rebood
SUPERMAXDELAY=1800  # wait 30 mins to create timelapse in case its still working


if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('LOGDIR/checkAllsky.log'), maxBytes=512000, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    stopfile = os.path.expanduser('LOGDIR/stopcheckallsky')

    if os.path.isfile(stopfile):
        os.remove(stopfile)
    runme = True
    log.info('starting')
    logfile = '/var/log/allsky.log'
    while runme is True:
        log.info('checking')
        status = 1
        loglines = open(logfile, 'r').readlines()
        try:
            lastline = loglines[-1]
            prevline = loglines[-2]
            
            lastdt = datetime.datetime.strptime(lastline[:15], '%b %d %H:%M:%S')
            delay = (datetime.datetime.now()-lastdt).seconds 
            if 'Unable to' in lastline or 'Unable to' in prevline or delay > MAXDELAY:
                stalled = True
                log.info('stuck, alerting operator')
                status = 0
        except Exception:  
            pass
        sendStatusUpdate(status, datetime.datetime.now())
            
        if os.path.isfile(stopfile):
            os.remove(stopfile)
            log.info('quitting')
            runme = False
        else:
            log.info('sleeping')
            time.sleep(MAXDELAY)
