# send an alert email if the allsky is down

from meteortools.utils import sendAnEmail
import paho.mqtt.client as mqtt
import time
import datetime
import os
import logging
from logging.handlers import RotatingFileHandler

from mqConfig import readConfig

MAXDELAY = 300

log = logging.getLogger('sendAllskyAlert')


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info('Connected success')
    else:
        log.info(f'Connected fail with code {rc}')


def on_message(client, userdata, message):
    laststate = 1
    try:
        if os.path.isfile('laststate.txt'):
            laststate = int(open('laststate.txt', 'r').readlines()[0].strip())
    except Exception:
        pass
    topic = message.topic
    payload = message.payload.decode('utf-8')
    log.info(f'{topic} {payload}')
    errstate = False
    if 'last_update' in topic:
        log.info(f'last update {payload}')
        upddt = datetime.datetime.strptime(payload, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
        if (datetime.datetime.now(tz=datetime.timezone.utc) - upddt).seconds > MAXDELAY:
            errstate = True
            errmsg = 'Allsky has not updated for five minutes'
    if 'status' in topic:
        log.info(f'laststate {laststate} current {payload}')
        if int(payload) == 0 and laststate == 1:
            errstate = True
            errmsg = 'Allsky has stalled'
    if errstate:
        try:
            sendAnEmail('mark.jm.mcintyre@cesmail.net',errmsg, 'Allsky Alert', 'noreply@thelinux')
        except Exception as e:
            log.warning('problem connecting to gmail')
            log.warning(e)
    else:
        log.info('all ok')
    if 'status' in topic:
        open('laststate.txt', 'w').write(payload)
    return 


if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser('LOGDIR/sendAllskyAlert.log'), maxBytes=512000, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    done = False
    mqbroker, mqport, mquser, mqpass = readConfig()
    client = mqtt.Client('allsky_checker')
    client.on_connect = on_connect
    client.on_message = on_message
    if mquser != '':
        client.username_pw_set(mquser, mqpass)
    try:
        client.connect(mqbroker, mqport, 60)
        client.subscribe('meteorcams/allsky/status')
        client.subscribe('meteorcams/allsky/last_update')
        client.loop_start()
        while not done:
            log.info('waiting...')
            time.sleep(60)
        client.loop_stop()
    except Exception as e:
        log.info('problem connecting to mqtt broker')
        log.debug(e)
