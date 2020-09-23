# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.insert
# NOTES:
# 1. This sample code uploads a file and can't be executed via this interface.
#    To test this code, you must run it locally using your own API credentials.
#    See: https://developers.google.com/explorer-help/guides/code_samples#python
# 2. This example makes a simple upload request. We recommend that you consider
#    using resumable uploads instead, particularly if you are transferring large
#    files or there's a high likelihood of a network interruption or other
#    transmission failure. To learn more about resumable uploads, see:
#    https://developers.google.com/api-client-library/python/guide/media_upload

import os, sys
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    # set to 1 to disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    title=sys.argv[1]
    fname=sys.argv[2]

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "/home/pi/allsky/scripts/client_secret.json"

    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/home/pi/allsky/scripts/token.pickle'):
        with open('/home/pi/allsky/scripts/token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:# Get credentials and create an API client
          flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
          credentials = flow.run_console()
        # Save the credentials for the next run
        with open('/home/pi/allsky/scripts/token.pickle', 'wb') as token:
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
        
        media_body=MediaFileUpload(fname,  chunksize=-1, resumable=True)
    )
    try: 
      status, response = request.next_chunk() # request.execute()
      print(status, response)
      if response is not None:
        if 'id' in response:
          print "Video id '%s' was successfully uploaded." % response['id']
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
       error='HTTP error %d arose with status: \'%s\' ' % (e.resp.status, e.content)
       print(error)

if __name__ == "__main__":
    main()

