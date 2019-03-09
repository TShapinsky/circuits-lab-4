#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

vrangeAll = (0, 1) # Throw away data points outside this voltage range
vrangeFit = (0.4, 0.625) # Use data points inside this range for curve-fitting

vb_exp = [[],[],[],[]]
ib_exp = [[],[],[],[]]
ie_exp = [[],[],[],[]]
valid = [(0,0), (0,0), (0,0), (0,0)]

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

  # Find the bounds of the data points we should use to fit 
  for j in range(len(vb_exp[i])):
    if vb_exp[i][j] >= vrangeFit[0]:
      validLower = j
      break
  for j in range(len(vb_exp[i])-1, -1, -1):
    if vb_exp[i][j] <= vrangeFit[1]:
      validUpper = j
      break
  valid[i] = (validLower, validUpper)


ic_exp = np.array(ie_exp) - np.array(ib_exp)

# Do the fit
def ic_f(Vbe, Ut, Is):
  return Is * (np.exp(Vbe/Ut) - 1)

Ut = [0,0,0]
Is = [0,0,0]
β = [0,0,0]
for i in range(4):

  # First, filter the data so we only fit to the right parts
  pts = zip(vb_exp[i], ib_exp[i], ic_exp[i])
  validPts = [pt for pt in pts if (vrangeFit[0] <= pt[0]) and (pt[0] <= vrangeFit[1]) and 0 < pt[1] and 0 < pt[2]]
  thisVb, thisIb, thisIc = list(zip(*validPts))

  # params = curve_fit(lambda Vbe, Ut, Is: np.log(ic_f(Vbe, Ut, Is)), vb_exp[i][valid[i][0]:valid[i][1]], np.log(ic_exp[i][valid[i][0]:valid[i][1]]))
  params = curve_fit(lambda Vbe, Ut, Is: np.log(ic_f(Vbe, Ut, Is)), thisVb, np.log(thisIc))
  Ut[i], Is[i] = params[0][0], params[0][1]

  def ib_f(Vbe, β):
    return (Is/β) * (np.exp(Vbe/Ut) - 1)


  # params = curve_fit(lambda Vbe, β: np.log(ib_f(Vbe, β)), vb_exp[i][valid[i][0]:valid[i][1]], np.log(ib_exp[i][valid[i][0]:valid[i][1]]))
  params = curve_fit(lambda Vbe, β: np.log(ib_f(Vbe, β)), thisVb, np.log(thisIb))
  β[i] = params[0][0]
  print("Transistor %i: Ut = %g, Is = %g, β = %g" % (i, Ut, Is, β))


fig = plt.figure()
ax = plt.subplot(111)

# Joined semilog plot
for i in range(4):
  ax.semilogy(vb_exp[i], ib_exp[i], ['r.', 'y.', 'g.', 'b.'][i], label="Base current (%i)" % (i+1))
  ax.semilogy(vb_exp[i], ic_exp[i], ['ro', 'yo', 'go', 'bo'][i], label="Collector current (%i)" % (i+1), markersize=1)
  ax.semilogy(vb_exp, ic_f(vb_exp, Ut, Is), 'k-', label="Theoretical Ic (Ut = %.4g, Is = %.4g)" % (Ut, Is))
  ax.semilogy(vb_exp, ib_f(vb_exp, β), 'k--', label="Theoretical Ib (Ut = %.4g, Is = %.4g, β = %.4g)" % (Ut, Is, β))

# ax.axvline(vb_exp[valid[0]], label='Sampled Data')
# ax.axvline(vb_exp[valid[1]])

plt.title("Transistor Currents vs Base Voltage")
plt.xlabel("Base Voltage (V)")
plt.ylabel("Current (A)")
plt.grid(True)
ax.legend()
plt.show()
# plt.savefig("exp1.pdf")
ax.cla()
