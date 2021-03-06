#!/usr/bin/env python

import numpy as np
import math

ledsPerStrand = 25
numStrands = 48
treeCoverageAngle = 360. # deg

# Tree dimensions, units don't really matter, just ratios
treeTopRadius = .75
treeHeight = 5.
baseRadius = 2.

stepAngle = treeCoverageAngle / numStrands
treeHyp = math.sqrt( (baseRadius*baseRadius) + (treeHeight*treeHeight) )
baseAngle = math.atan(treeHeight/baseRadius)
stepHeight = (treeHyp/ledsPerStrand)*math.sin(baseAngle)

# Generate evenly spaced pixels
# Index starts at base of first column, proceeds to top of first column
# then continues at base of second column...ending at top of last column
pixels = []
angle = 0.0
zig = True
for col in range(0,numStrands):
    z = 0.0
    col_pixels = []
    for pixel in range(0,ledsPerStrand):
        r = baseRadius - z*math.cos(baseAngle) + treeTopRadius
        x = r*np.sin(angle*np.pi/180.)
        y = r*np.cos(angle*np.pi/180.)
        col_pixels.append( (x,y,z))
        z += stepHeight
    angle += stepAngle
    if zig and (col % 2 == 1):
        pixels += reversed(col_pixels)
    else:
        pixels += col_pixels
# Write out to screen
lines = []
for p in pixels:
    lines.append('  {"point": [%.2f, %.2f, %.2f]}' % p )

print '[\n' + ',\n'.join(lines) + '\n]'
