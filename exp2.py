#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
import matplotlib.pyplot as plt


ix1 = [[],[],[]]
iy1 = np.array([99.2, 9.8, 0.9]) * 1e-6 # microamps to amps
iy_names = [".1ma", ".01ma", ".001ma"]
iz1 = [[],[],[]]

for i in range(3):
  with open("data/exp2_sink_(%s).csv" % iy_names[i]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      ix1[i] += [float(row[0])]
      iz1[i] += [-float(row[1])] # Iz goes the other way, so invert it

ix2 = np.array([102.8, 10.3, 1.0]) * 1e-6 # microamps to amps
ix_names = [".1ma", ".01ma", ".001ma"]
iy2 = [[],[],[]]
iz2 = [[],[],[]]

for i in range(3):
  with open("data/exp2_source_(%s).csv" % ix_names[i]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      this_iz2 = -float(row[1])
      if this_iz2 >= 10e-8: # Remove bad data
        iy2[i] += [-float(row[0])] # Iy goes the other way, so invert it
        iz2[i] += [this_iz2] # Iz goes the other way, so invert it


# Now let's do some theoretical fits
def iz_f(ix, iy): return np.sqrt(ix * iy) 
iz1t = [[iz_f(ix, iy) for ix in ixs] for (ixs, iy) in zip(ix1, iy1)]
iz2t = [[iz_f(ix, iy) for iy in iys] for (ix, iys) in zip(ix2, iy2)]

fig = plt.figure(figsize=(8,6))
ax = plt.subplot(111)

# Sink log-log plot
for i in range(3):
  ax.loglog(ix1[i], iz1[i], ['r.', 'g.', 'b.'][i], label="Iz (Iy = %s)" % iy_names[i])
  ax.loglog(ix1[i], iz1t[i], ['r-', 'g-', 'b-'][i], label="Theoretical fit (Iy = %s)" % iy_names[i])

plt.title("Translinear geometric mean finder (fixed Iy)")
plt.xlabel("Input current Ix (A)")
plt.ylabel("Output current Iz (A)")
plt.grid(True)
ax.legend()
plt.savefig("exp2_sink.pdf")
ax.cla()

# Source log-log plot
for i in range(3):
  ax.loglog(iy2[i], iz2[i], ['r.', 'g.', 'b.'][i], label="Iz (Ix = %s)" % ix_names[i])
  ax.loglog(iy2[i], iz2t[i], ['r-', 'g-', 'b-'][i], label="Theoretical fit (Ix = %s)" % ix_names[i])

plt.title("Translinear geometric mean finder (fixed Ix)")
plt.xlabel("Input current Iy (A)")
plt.ylabel("Output current Iz (A)")
plt.grid(True)
ax.legend()
plt.savefig("exp2_source.pdf")
ax.cla()

