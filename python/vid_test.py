#!/usr/bin/env python

import sys
import time
import cv2
import opc

#-------------------------------------------------------------------------------
# handle command line

if len(sys.argv) == 1:
    IP_PORT = '192.168.1.189:7890'
elif len(sys.argv) == 2 and ':' in sys.argv[1] and not sys.argv[1].startswith('-'):
    IP_PORT = sys.argv[1]
else:
    print('''
Usage: raver_plaid.py [ip:port]

If not set, ip:port defauls to 127.0.0.1:7890
''')
    sys.exit(0)


#-------------------------------------------------------------------------------
# connect to server

client = opc.Client(IP_PORT)
if client.can_connect():
    print('    connected to %s' % IP_PORT)
else:
    # can't connect, but keep running in case the server appears later
    print('    WARNING: could not connect to %s' % IP_PORT)
print('')


fps = 30         # frames per second

cap = cv2.VideoCapture('/home/pi/Desktop/bunny_tiny.m4v')

if cap.isOpened() == False:
    print("Error opening")

num = 0
while cap.isOpened():
    t = time.time() 
    ret,frame = cap.read()
    pixels = []
    if ret == True:
        for i in range(0,24):
            for j in range(0,50):
                f = frame[99-(j*2)][47-(i*2)]
                pixels.append( (f[2],f[1],f[0] ))
    client.put_pixels(pixels,channel=0)
    while time.time() - t < (1.0/30.0):
        time.sleep(0.001)

cap.release()
cv2.destroyAllWindows()
