#!/usr/bin/env python

import numpy as np
import math

ledsPerStrand = 50
numStrands = 24
treeCoverageAngle = 180. # deg

# Tree dimensions, units don't really matter, just ratios
treeTopRadius = 0.5
treeHeight = 8.
baseRadius = 4.

stepAngle = treeCoverageAngle / numStrands
treeHyp = math.sqrt( (baseRadius*baseRadius) + (treeHeight*treeHeight) )
baseAngle = math.atan(treeHeight/baseRadius)
stepHeight = (treeHyp/ledsPerStrand)*math.sin(baseAngle)

# Generate evenly spaced pixels
# Index starts at base of first column, proceeds to top of first column
# then continues at base of second column...ending at top of last column
pixels = []
angle = 0.0
for col in range(0,numStrands):
    z = 0.0
    for pixel in range(0,ledsPerStrand):
        r = baseRadius - z*math.cos(baseAngle) + treeTopRadius
        x = r*np.sin(angle*np.pi/180.)
        y = r*np.cos(angle*np.pi/180.)
        pixels.append( (x,y,z) )
        z += stepHeight
    angle += stepAngle

# Write out to screen
lines = []
for p in pixels:
    lines.append('  {"point": [%.2f, %.2f, %.2f]}' % p )

print '[\n' + ',\n'.join(lines) + '\n]'
