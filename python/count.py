#!/usr/bin/env python

import sys
import time
import opc

run = True

client = opc.Client('localhost:7890')

if client.can_connect():
    print('    connected to %s' % "localhost:7890")
else:
    print('    WARNING: could not connect to %s' % "localhost:7890")

lastX = 1199
x = 0
nextX = 1

pixels = [(0,0,100)]*1200
while True:
    pixels[x] = (0,250,0)
    pixels[lastX] = (0,0,100)
    pixels[nextX] = (0,250,0)

    client.put_pixels(pixels,channel=0)
    lastX = x
    x = (x+1)%1200
    nextX = (x+1)%1200
