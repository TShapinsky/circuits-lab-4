#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

vrangeAll = (0, 1) # Throw away data points outside this voltage range

vb_exp = [[],[],[],[]]
ib_exp = [[],[],[],[]]
ie_exp = [[],[],[],[]]

for i in range(4):
  with open("data/exp1_trans%s.csv" % str(i+1)) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for row in c:
      vb = float(row[0])
      if (vb >= vrangeAll[0]) and (vb <= vrangeAll[1]):
        vb_exp[i] += [vb]
        ib_exp[i] += [float(row[1])]
        ie_exp[i] += [-float(row[2])] # Ie goes the other way, so invert it

ic_exp = np.array(ie_exp) - np.array(ib_exp)

# Do the fit
def ic_f(Vbe, Ut, Is):
  return Is * (np.exp(Vbe/Ut) - 1)

Uts = [0,0,0,0]
Iss = [0,0,0,0]
βs = [0,0,0,0]
for i in range(4):

  # First, filter the data so we only fit to the right parts
  vrangeFit = (0.2, 0.65) # Use data points inside this range for curve-fitting
  pts = zip(vb_exp[i], ib_exp[i], ic_exp[i])
  validPts = [pt for pt in pts if (vrangeFit[0] <= pt[0]) and (pt[0] <= vrangeFit[1]) and 0 < pt[1] and 0 < pt[2]]
  thisVb, thisIb, thisIc = list(zip(*validPts))

  params = curve_fit(lambda Vbe, Ut, Is: np.log(ic_f(Vbe, Ut, Is)), thisVb, np.log(thisIc))
  Ut, Is = params[0][0], params[0][1]

  def ib_f(Vbe, β):
    return (Is/β) * (np.exp(Vbe/Ut) - 1)

  # Re-filter the data
  vrangeFit = (0.575, 0.625) # Use data points inside this range for curve-fitting
  pts = zip(vb_exp[i], ib_exp[i], ic_exp[i])
  validPts = [pt for pt in pts if (vrangeFit[0] <= pt[0]) and (pt[0] <= vrangeFit[1]) and 0 < pt[1] and 0 < pt[2]]
  thisVb, thisIb, thisIc = list(zip(*validPts))

  params = curve_fit(lambda Vbe, β: np.log(ib_f(Vbe, β)), thisVb, np.log(thisIb))
  β = params[0][0]
  print("Transistor %i: Ut = %g, Is = %g, β = %g" % (i+1, Ut, Is, β))
  Uts[i], Iss[i], βs[i] = Ut, Is, β


fig = plt.figure(figsize=(8,6))
ax = plt.subplot(111)

# Joined semilog plot
for i in range(4):
  ax.semilogy(vb_exp[i], ib_exp[i], ['r.', 'y.', 'g.', 'b.'][i], label="Base current (%i)" % (i+1))
  ax.semilogy(vb_exp[i], ic_exp[i], ['ro', 'yo', 'go', 'bo'][i], label="Collector current (%i)" % (i+1), markersize=1)
  ax.semilogy(vb_exp[i], ic_f(vb_exp[i], Uts[i], Iss[i]), ['r-', 'y-', 'g-', 'b-'][i], label="Theoretical Ic (%i)" % (i+1))
  ax.semilogy(vb_exp[i], ib_f(vb_exp[i], βs[i]), ['r--', 'y--', 'g--', 'b--'][i], label="Theoretical Ib (%i)" % (i+1))

plt.title("Transistor Currents vs Base Voltages")
plt.xlabel("Base Voltage (V)")
plt.ylabel("Current (A)")
plt.grid(True)
ax.legend()
plt.savefig("exp1_semilog.pdf")
ax.cla()


# Plot of differences
ic_avg = np.average(ic_exp, 0)
ic_errs = [(ic - ic_avg)/ic_avg for ic in ic_exp]
for i in range(4):
  ax.plot(vb_exp[i], 100 * ic_errs[i], ['ro', 'yo', 'go', 'bo'][i], label="Collector current error (%i)" % (i+1), markersize=1)

plt.title("Transistor Currents vs Base Voltages")
plt.xlabel("Base Voltage (V)")
plt.ylabel("Error (%)")
plt.grid(True)
ax.legend()
plt.savefig("exp1_err.pdf")
ax.cla()

