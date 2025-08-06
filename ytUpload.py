# -*- coding: utf-8 -*-

import os
import sys
import pickle
import datetime
from time import sleep
from crontab import CronTab
import ephem
import socket
import requests
import glob
import logging
from logging.handlers import RotatingFileHandler
import configparser

import google_auth_oauthlib.flow
import googleapiclient.discovery

from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

log = logging.getLogger('ytUpload')


def updateSentList(here, fname):
    """
    update the list of sent files
    parameters:
        here [string]:      current working directory
        fname [string]:     full path to the mp4 video    
    """

    # reads the list and strip newlines, appends the new entry, 
    # then makes sure the list is unique and writes it back with newlines
    if os.path.isfile(os.path.join(here, 'ytdone.txt')):
        sentlist = open(os.path.join(here, 'ytdone.txt'), 'r').readlines()
    else:
        sentlist = []
    sentlist = [x.strip() for x in sentlist]
    sentlist.append(fname)
    sentlist = list(set(sentlist))  
    sentlist.sort()
    open(os.path.join(here, 'ytdone.txt'), 'w').writelines([x + '\n' for x in sentlist])
    return


def checkIfSent(here, fname):
    """
    check to avoid sending the same video twice
    parameters:
        here [string]:      current working directory
        fname [string]:     full path to the mp4 video    
    """
    sentlist = open(os.path.join(here, 'ytdone.txt'), 'r').readlines()
    sentlist = [x.strip() for x in sentlist]
    if fname in sentlist:
        return True
    return False
    

def uploadToYoutube(here, title, fname, forceUpload=False):
    """
    Upload video to youtube
    parameters:
        here [string]:      current working directory
        title [string]:     title for youtube
        fname [string]:     full path to the mp4 video
        forceupload [bool]: force upload even if already done. Default False
    """
    # set to 1 to disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # workaround for slow or failing to resolve ipv6 addresses
    socket.setdefaulttimeout(60)
    requests.packages.urllib3.util.connection.HAS_IPV6 = False

    api_service_name = 'youtube'
    api_version = 'v3'
    client_secrets_file = os.path.join(here, 'client_secret.json')

    if checkIfSent(here, fname) and forceUpload is False:
        log.info(f'{fname} already uploaded')
        return False
    log.info(f'   uploading {fname}')
    
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    tokfile = os.path.join(here, 'token.pickle')
    if os.path.exists(tokfile):
        with open(tokfile, 'rb') as token:
            credentials = pickle.load(token, encoding='latin1')
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:# Get credentials and create an API client
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            credentials = flow.run_console()
        # Save the credentials for the next run
        with open(tokfile, 'wb') as token:
            pickle.dump(credentials, token)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": "Allsky camera timelapse",
                "title": title
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        
        media_body=MediaFileUpload(fname, chunksize=-1, resumable=True)
    )
    try: 
        status,response = request.next_chunk() # request.execute()
        log.debug(status)
        if response is not None:
            if 'id' in response:
                log.info(f'Video id  {response["id"]} was successfully uploaded.')
                ret = True
                updateSentList(here, fname)
            else:
                log.debug(f'The upload failed with an unexpected response: {response}')
                ret = False
    except HttpError as e:
        log.debug(f'HTTP error {e.resp.status} arose with message: {e.content}')
        ret = False
    socket.setdefaulttimeout(None)
    if ret is False:
        log.info('waiting a minute before trying again')
        sleep(60)
    return ret 


def updateCrontab(here, logdir, offset=30, lati=51.88, longi=-1.31, elev=80):
    """
    Add a cron job to run this script every 15 minutes for a three hour period around dawn
    parameters:
        here [string]:      current working directory
        logdir [strin]:     where to write logfiles
        offset [int]:       how long after dawn to start running
        lati [float]:       ovservers latitude
        longi [float]:      ovservers longitude
        elev [float]:       ovservers elevation above sea level

    """
    obs = ephem.Observer()
    obs.lat = float(lati) / 57.3 # convert to radians, close enough for this
    obs.lon = float(longi) / 57.3
    obs.elev = float(elev)
    obs.horizon = -6.0 / 57.3 # degrees below horizon for darkness
    sun = ephem.Sun()
    rise = obs.next_rising(sun).datetime()
    starttime = rise + datetime.timedelta(minutes=-offset)
    log.info(f'Setting batch start time to {starttime.strftime("%H")}')
    hourstr = f'{starttime.hour},{starttime.hour+1},{starttime.hour+2}'
    cron = CronTab(user=True)
    for job in cron:
        if 'youtubeUploader.sh' in job.command:
            cron.remove(job)
            cron.write()
    job = cron.new(f'{here}/youtubeUploader.sh > {logdir}/checkYtConn.log 2>&1')
    job.setall('*/15', hourstr, '*', '*', '*')
    cron.write()
    return


def mp4Ready(logfile, mp4name):
    """ 
    Search the last couple of allsky.log files to make sure the mp4 is ready to upload
    parameters:
        logfile [string]:   the full path to the allsky.log file
        mp4name [string]:   bare name of the video to check for eg allsky-20240101.mp4
    """
    srchtext = f'{mp4name} success'
    llines = open(logfile, 'r').readlines()
    for li in llines:
        if srchtext in li:
            return True
    llines = open(f'{logfile}.1', 'r').readlines()
    for li in llines:
        if srchtext in li:
            return True
    llines = open(f'{logfile}.2', 'r').readlines()
    for li in llines:
        if srchtext in li:
            return True
    return False


if __name__ == "__main__":
    """
    Upload allsky videos to youtube
    Arguments:
        logfile:    full path to allsky.log
        allskyhome: full path to the folder containing the allsky software eg $HOME/allsky
        forceupload: if present, uploads will be forced through
    """
    today = datetime.datetime.now()
    inprogressfn = '/tmp/ytinprogress'
    if os.path.isfile(inprogressfn):
        print('already running')
        exit(0)
    open(inprogressfn,'w').write('1\n')
    here = os.path.split(os.path.abspath(__file__))[0]

    localcfg = configparser.ConfigParser()
    localcfg.read(os.path.join(here, 'config.ini'))
    logdir = localcfg['checking']['logdir']
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    fh = RotatingFileHandler(os.path.expanduser(f'{logdir}/ytUploader.log'), maxBytes=10240, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    logfile = sys.argv[1]
    allskyhome = sys.argv[2]
    forceUpload = False
    if len(sys.argv) > 3:
        forceUpload = True

    log.info('======================')
    log.info(f'checking for new mp4s at {datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}')
    allmp4s = glob.glob(os.path.join(os.path.expanduser(allskyhome),'images/**/*.mp4'), recursive=True)
    allmp4s = list(set(allmp4s))
    allmp4s.sort()
    for fname in allmp4s:
        mp4name = os.path.split(fname)[1]
        if not mp4Ready(logfile, mp4name) and forceUpload is False:
            log.info(f'{mp4name} not ready for upload')
            continue
        filedate = mp4name.split('-')[1][:8]
        yy = filedate[:4]
        mm = filedate[4:6]
        dd = filedate[6:]
        title = f'Allsky timelapse for {yy}-{mm}-{dd}'
        ret = uploadToYoutube(here, title, fname, forceUpload)
        if ret:
            sleep(60)
    updateCrontab(here, logdir)
    try:
        os.remove(inprogressfn)
    except:
        log.warning('!!! Unable to remove flag file')