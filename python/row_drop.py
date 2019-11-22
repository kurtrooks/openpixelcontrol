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

numPix = 480
numRow = 60
numCol = numPix / numRow
rowCount = 0

while True:
    pixels = [(0,0,0)]*numPix
    for i in range(0,numPix):
        if i % numRow == rowCount:
            pixel = (250,250,250)
            pixels[i] = pixel

    client.put_pixels(pixels,channel=0)
    rowCount += 1
    rowCount %= numRow

    time.sleep(0.06)
