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

def processFrame(frame):
    pixels = []
    for i in range(0,24):
        for j in range(0,50):
            f = frame[99-(j*2)][47-(i*2)]
            pixels.append( (f[2],f[1],f[0] ))
    return pixels 


signal.signal(signal.SIGINT,signal_handler)


parser = OptionParser()
parser.add_option("-f","--file",dest="filename")
parser.add_option("-i","--ip",dest="ip_port",default="192.168.1.189:7890")
parser.add_option("-l",action="store_true",dest="loop",default=False)

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

    client.put_pixels(processFrame(frame),channel=0)

    while time.time() - t < (1.0/fps):
        time.sleep(0.001)

cap.release()
cv2.destroyAllWindows()
