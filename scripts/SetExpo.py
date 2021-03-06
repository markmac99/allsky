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
    minexp='0x00000064'
    maxexp='0x00013880'
else:
    expo=100
    gain=70
    cmode='0x00000002'
    minexp='0x00013880'
    maxexp='0x00013880'

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
cam.set_info("Camera.Param.[0].ExposureParam",{"LeastTime":minexp})
cam.set_info("Camera.Param.[0].ExposureParam",{"MostTime":maxexp})
params = cam.get_info("Camera")
print(params['Param'][0]['ElecLevel'])

cam.close()

#[{'AeSensitivity': 1, 'ApertureMode': '0x00000000', 'BLCMode': '0x00000001', 
# 'DayNightColor': '0x00000002', 'Day_nfLevel': 0, 'DncThr': 50, 'ElecLevel': 30, 
# 'EsShutter': '0x00000006', 
# 'ExposureParam': {'LeastTime': '0x00000064', 'Level': 0, 'MostTime': '0x00013880'}, 
# 'GainParam': {'AutoGain': 1, 'Gain': 65}, 
# 'IRCUTMode': 0, 'IrcutSwap': 0, 'Night_nfLevel': 0, 
# 'PictureFlip': '0x00000001', 'PictureMirror': '0x00000001', 
# 'RejectFlicker': '0x00000000', 'WhiteBalance': '0x00000002'}]

# 'DayNightColor': '0x00000002' BW
# 'DayNightColor': '0x00000001' Colour

# 0.1ms 40ms 80ms
# '0x00000064'
# '0x00009C40'
# '0x00013880'
