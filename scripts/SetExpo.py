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
    cmode='0x00000001'
else:
    expo=100
    gain=70
    cmode='0x00000002'

cam = DVRIPCam(host_ip, "admin", "")
if cam.login():
        print("Success! Connected to " + host_ip)
else:
        print("Failure. Could not connect.")

params = cam.get_info("Camera")
print(params['Param'])
print(params['Param'][0]['ElecLevel'])

cam.set_info("Camera.Param.[0]",{"ElecLevel":expo})
cam.set_info("Camera.Param.[0]",{"DayNightColor":cmode})
cam.set_info("Camera.Param.[0].GainParam",{"Gain":gain})
params = cam.get_info("Camera")
print(params['Param'][0]['ElecLevel'])

cam.close()

#params['Params']
# 'DayNightColor': '0x00000002' BW
# 'DayNightColor': '0x00000001' Colour

# 0.1ms to 80ms
#'ExposureParam': {'LeastTime': '0x00000064', 'Level': 0, 'MostTime': '0x00013880'}
#and 40ms = 0x00009C40

#'GainParam': {'AutoGain': 1, 'Gain': 65}
