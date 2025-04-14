# send an alert email if the allsky is down

from meteortools.utils import sendAnEmail
import sys
import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

MAXDELAY = 400


def checkAndSend(sts, lastupdatedt):
    log = logging.getLogger('sendAllskyAlert')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('LOGDIR/sendAllskyAlert.log'), maxBytes=512000, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    upddt = datetime.datetime.strptime(lastupdatedt, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
    delay = (datetime.datetime.now(tz=datetime.timezone.utc) - upddt).seconds
    try:
        if os.path.isfile('laststate.txt'):
            laststate = float(open('LOGDIR/laststate.txt', 'r').readlines()[0].strip())
    except Exception:
        pass
    if (sts < 0.5 and laststate > 0.5) or delay > MAXDELAY:
        try:
            sendAnEmail('mark.jm.mcintyre@cesmail.net', 'Allsky Stalled', 'Allsky Alert', 'noreply@thelinux')
        except Exception as e:
            log.warning('problem connecting to gmail')
            log.warning(e)
    else:
        log.info(f'all ok, status {sts} at {lastupdatedt}')
    open('LOGDIR/laststate.txt', 'w').write(f'{sts}')
    return 


if __name__ == '__main__':
    checkAndSend(sys.argv[1], sys.argv[2])
