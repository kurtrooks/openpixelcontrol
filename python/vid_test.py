#!/usr/bin/env python

import sys
import time
import cv2
import opc
from optparse import OptionParser
import signal

run = True

def signal_handler(sig,frame):
    print("k thx bye")
    global run
    run = False

def processFrame(frame,sim=False,zig=False):
    pixels = []
    for i in range(0,48):
        # Bottom to top
        col_pixels = []
        for j in range(0,25):
            f = frame[49-(j*2)][95-(i*2)]
            r = f[1]
            g = f[2]
            b = f[0]
            if sim:
                col_pixels.append( (g,r,b) )
            else:
                col_pixels.append( (r,g,b))
        if zig and (i % 2 == 1):
            pixels += reversed(col_pixels)
        else:
            pixels += col_pixels


    return pixels 


signal.signal(signal.SIGINT,signal_handler)


parser = OptionParser()
parser.add_option("-f","--file",dest="filename")
parser.add_option("-i","--ip",dest="ip_port",default="192.168.1.189:7890")
parser.add_option("-l",action="store_true",dest="loop",default=False)
parser.add_option("-s",action="store_true",dest="sim",default=False)
parser.add_option("-z",action="store_true",dest="zig",default=False)

(options,args) = parser.parse_args()

client = opc.Client(options.ip_port)

if client.can_connect():
    print('    connected to %s' % options.ip_port)
else:
    print('    WARNING: could not connect to %s' % options.ip_port)


cap = cv2.VideoCapture(options.filename)

if cap.isOpened() == False:
    print("Error opening")
    exit()

frames = []
fps  = cap.get(cv2.cv.CV_CAP_PROP_FPS)

numFrames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)) 
for i in range(0,numFrames):
    ret,frame = cap.read()
    if ret == True:
        frames.append(frame)

cap.release()

fn = 0
first = True
frame = None
frmaes = []

while run:
    t = time.time()

    frame = frames[fn]
    fn += 1
    if fn >= len(frames):
        if options.loop:
            fn = 0
        else:
            break

    client.put_pixels(processFrame(frame,options.sim,options.zig),channel=0)

    while time.time() - t < (1.0/fps):
        time.sleep(0.001)

cap.release()
cv2.destroyAllWindows()
