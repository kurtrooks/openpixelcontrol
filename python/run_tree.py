#!/usr/bin/env python

from glob import glob
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



def playAnimation(filename,maxDuration=10.0,loop=True,sim=False,zig=True,rotate=False):

    play = True
    cap = cv2.VideoCapture(filename)

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


    if cap.isOpened() == False:
        print("Error opening",filename)
        return 

    fn = 0
    first = True
    frame = None
    frames = []

    fps = None
    numFrames =0 

    if major_ver < 3:
        # TODO: might still be a typo here, refer to openCV documentation!!
        fps  = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        numFrames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)
        numFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for i in range(0,numFrames):
        ret,frame = cap.read()
        if ret == True:
            frames.append(frame)

    cap.release()

    startTime = time.time()
    global run

    rotate_offset = 0

    while play and run:

        t = time.time()

        frame = frames[fn]
        fn += 1
        if fn >= len(frames):
            if loop:
                fn = 0
            else:
                play = False


        pframe = processFrame(frame,sim,zig)
        if rotate:
            roff = int(rotate_offset)
            rframe = pframe[50*roff:] + pframe[:roff*50]
            pframe = rframe
            rotate_offset = (rotate_offset + 1/6.0) % 25

        client.put_pixels(pframe,channel=0)

        while time.time() - t < (1.0/fps):
            time.sleep(0.001)
    
        if time.time() - startTime > maxDuration:
            play = False


if __name__ == "__main__":

    signal.signal(signal.SIGINT,signal_handler)

    parser = OptionParser()
    parser.add_option("-d","--dir",dest="dir",default="/home/pi/Desktop/Animations")
    parser.add_option("-f","--file",dest="filename")
    parser.add_option("-i","--ip",dest="ip_port",default="localhost:7890")
    parser.add_option("-l",action="store_true",dest="loop",default=False)
    parser.add_option("-s",action="store_true",dest="sim",default=False)
    parser.add_option("-z",action="store_true",dest="zig",default=True)
    parser.add_option("-r",action="store_true",dest="rotate",default=False)

    (options,args) = parser.parse_args()

    client = opc.Client(options.ip_port)

    if client.can_connect():
        print('    connected to %s' % options.ip_port)
    else:
        print('    WARNING: could not connect to %s' % options.ip_port)

    
    while run:
        files = glob(options.dir + "/*")
        for animation in sorted(files):
            try:
                rotate = False
                if "_rotate" in animation and options.rotate is True:
                    rotate = True

                playAnimation(animation,sim=options.sim,zig=options.zig,rotate=rotate)
            except Exception as ex:
                print("Exception with animation",animation,ex)

    cv2.destroyAllWindows()
