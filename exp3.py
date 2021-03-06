#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
import matplotlib.pyplot as plt


ix1 = [[],[],[]]
iy1 = np.array([107.5, 10.8, 1.0]) * 1e-6 # microamps to amps
iy_names = [".1ma", ".01ma", ".001ma"]
iz1 = [[],[],[]]

for i in range(3):
  with open("data/exp3_sink_(%s).csv" % iy_names[i]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      ix1[i] += [float(row[0])]
      iz1[i] += [-float(row[1])] # Iz goes the other way, so invert it

ix2 = np.array([100.2, 10.0, 1.0]) * 1e-6 # microamps to amps
ix_names = [".1ma", ".01ma", ".001ma"]
iy2 = [[],[],[]]
iz2 = [[],[],[]]

for i in range(3):
  with open("data/exp3_source_(%s).csv" % ix_names[i]) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      iy2[i] += [-float(row[0])] # Iy goes the other way, so invert it
      iz2[i] += [-float(row[1])] # Iz goes the other way, so invert it


# Now let's do some theoretical fits
def iz_f(ix, iy): return np.power(ix, 2)/iy
iz1t = [[iz_f(ix, iy) for ix in ixs] for (ixs, iy) in zip(ix1, iy1)]
iz2t = [[iz_f(ix, iy) for iy in iys] for (ix, iys) in zip(ix2, iy2)]

def clip_range(xs, ys, bounds):
  pairs = [(x, y) for (x, y) in zip(xs, ys) if (bounds[0] <= y) and (y <= bounds[1])]
  return list(zip(*pairs))

clipped1 = [clip_range(ix, iz, (1e-8, 1e-1)) for (ix, iz) in zip(ix1, iz1t)]
clipped2 = [clip_range(iy, iz, (1e-8, 1e-2)) for (iy, iz) in zip(iy2, iz2t)]


fig = plt.figure(figsize=(8,6))
ax = plt.subplot(111)

# Sink log-log plot
for i in range(3):
  ax.loglog(ix1[i], iz1[i], ['r.', 'g.', 'b.'][i], label="Iz (Iy = %g μA)" % (iy1[i] * 1e6))
  ax.loglog(clipped1[i][0], clipped1[i][1], ['c-', 'm-', 'y-'][i], label="Theoretical fit (Iy = %g μA)" % (iy1[i] * 1e6))

plt.title("Quadratic inverter (fixed Iy)")
plt.xlabel("Input current Ix (A)")
plt.ylabel("Output current Iz (A)")
plt.grid(True)
ax.legend()
plt.savefig("exp3_sink.pdf")
ax.cla()

# Source log-log plot
for i in range(3):
  ax.loglog(iy2[i], iz2[i], ['r.', 'g.', 'b.'][i], label="Iz (Ix = %g μA)" % (ix2[i] * 1e6))
  ax.loglog(clipped2[i][0], clipped2[i][1], ['c-', 'm-', 'y-'][i], label="Theoretical fit (Ix = %g μA)" % (ix2[i] * 1e6))

plt.title("Quadratic inverter (fixed Ix)")
plt.xlabel("Input current Iy (A)")
plt.ylabel("Output current Iz (A)")
plt.grid(True)
ax.legend()
plt.savefig("exp3_source.pdf")
ax.cla()

