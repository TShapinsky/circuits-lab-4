#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
import matplotlib.pyplot as plt

V = []
Ix = []
Iz = []

with open('data/exp2_sink_(.001ma).csv') as f:
    c = csv.reader(f, delimiter=",")
    next(c)
    
    for row in c:
        Ix+= [float(row[0])]
        Iz += [-float(row[1])]
        
fig = plt.figure()
ax = plt.subplot(111)



ax.loglog(Ix, Iz, 'b.', label="Base-Emitter Gain")
plt.title("Current")
ax.legend()
plt.show()
