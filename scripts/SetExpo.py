# SetExpo.py
# sets the exposure on the IPCamera using Python_DVRIP
#
import os, sys
sys.path.append('/home/pi/python-dvr')
from dvrip import DVRIPCam
from time import sleep

host_ip = sys.argv[1]
daynight=sys.argv[2]
if daynight == 'DAY':
    expo=30
    gain=30
else:
    expo=100
    gain=70

cam = DVRIPCam(host_ip, "admin", "")
if cam.login():
        print("Success! Connected to " + host_ip)
else:
        print("Failure. Could not connect.")

params = cam.get_info("Camera")
print(params['Param'])
print(params['Param'][0]['ElecLevel'])

cam.set_info("Camera.Param.[0]",{"ElecLevel":expo})
params = cam.get_info("Camera")
print(params['Param'][0]['ElecLevel'])

cam.close()

