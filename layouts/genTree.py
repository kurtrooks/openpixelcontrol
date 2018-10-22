#!/usr/bin/env python

import numpy as np
import math

ledsPerStrand = 50
numStrands = 24
vertSpacing = .2 # inches
treeTopRadius = .4 # inch
treeBaseRadius = .8 # inch
treeCoverageAngle = 180. # deg
treeHeight = 2  # inches


lines = []

step = (treeBaseRadius-treeTopRadius)/ledsPerStrand
angle = float(treeCoverageAngle) / numStrands

hNum = ledsPerStrand
tmpH = treeHeight - treeTopRadius*2 
r = treeTopRadius
for x in range(0,ledsPerStrand):
    i = 0
    while i < treeCoverageAngle:
        lines.append('  {"point": [%.2f, %.2f, %.2f]}' %
                (r*np.sin(i*np.pi/180.),r*np.cos(i*np.pi/180.),hNum))
        i += angle

    hNum -= (treeHeight/ledsPerStrand)
    r += step

print '[\n' + ',\n'.join(lines) + '\n]'
