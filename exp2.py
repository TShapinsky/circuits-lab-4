#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
import matplotlib.pyplot as plt


ix1 = [[],[],[]]
iy1 = [0.0001, 0.001, 0.01]
iy_names = [".1", "1", "10"]
iz1 = [[],[],[]]

for i in range(3):
  with open("data/exp2_sink_(%sma).csv" % iy_names[i]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      ix1[i] += [float(row[0])]
      iz1[i] += [-float(row[1])] # Iz goes the other way, so invert it

ix2 = [0.0001, 0.001, 0.01]
ix_names = [".1", "1", "10"]
iy2 = [[],[],[]]
iz2 = [[],[],[]]

for i in range(3):
  with open("data/exp2_source_(%sma).csv" % ix_names[i]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      iy2[i] += [-float(row[0])] # Iy goes the other way, so invert it
      iz2[i] += [-float(row[1])] # Iz goes the other way, so invert it


# Now let's do some theoretical fits
def iz_t(ix, iy): return np.sqrt(ix * iy) 
ix_t = [[iz_t(ix, iy) for ix in ixs] for (ixs, iy) in zip(ix1, iy1)]
iy_t = [[iz_t(ix, iy) for iy in iys] for (ix, iys) in zip(ix2, iy2)]

fig = plt.figure(figsize=(8,6))
ax = plt.subplot(111)

# Sink log-log plot
for i in range(3):
  ax.loglog(ix1[i], iz1[i], ['r.', 'g.', 'b.'][i], label="Iz (Iy = %s ma)" % iy_names[i])

plt.title("Geometric mean finder with fixed Iy")
plt.xlabel("Input current Ix (A)")
plt.ylabel("Output current Iz (A)")
plt.grid(True)
ax.legend()
plt.savefig("exp2_sink.pdf")
ax.cla()

# Source log-log plot
for i in range(3):
  ax.loglog(iy2[i], iz2[i], ['r.', 'g.', 'b.'][i], label="Iz (Ix = %s ma)" % ix_names[i])

plt.title("Geometric mean finder with fixed Ix")
plt.xlabel("Input current Iy (A)")
plt.ylabel("Output current Iz (A)")
plt.grid(True)
ax.legend()
plt.savefig("exp2_source.pdf")
ax.cla()

