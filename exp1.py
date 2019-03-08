#!/usr/bin/env python3
# coding=utf-8
import csv
import numpy as np
from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

vb_exp = [[],[],[]]
ib_exp = [[],[],[]]
ie_exp = [[],[],[]]

for i in range(4):
  with open("exp1_trans%s.csv" % str(i+1)) as f:
    c = csv.reader(f, delimiter=",")
    next(c) # Throw away the header
    for _ in range(0):
      next(c) # Throw away bad data points
    for row in c:
      vb_exp[i] += [float(row[0])]
      ib_exp[i] += [float(row[1])]
      ie_exp[i] += [-float(row[2])] # Ie goes the other way, so invert it

  ic_exp = np.array(ie_exp) - np.array(ib_exp)


valid = (100, 350)

def ic_f(Vbe, Ut, Is):
  return Is * (np.exp(Vbe/Ut) - 1)

params = curve_fit(lambda Vbe, Ut, Is: np.log(ic_f(Vbe, Ut, Is)), vb_exp[:valid[1]], np.log(ic_exp[:valid[1]]))
Ut, Is = params[0][0], params[0][1]

def ib_f(Vbe, β):
  return (Is/β) * (np.exp(Vbe/Ut) - 1)

params = curve_fit(lambda Vbe, β: np.log(ib_f(Vbe, β)), vb_exp[valid[0]:valid[1]], np.log(ib_exp[valid[0]:valid[1]]))
β = params[0][0]
print("Ut = %g, Is = %g, β = %g" % (Ut, Is, β))

fig = plt.figure()
ax = plt.subplot(111)
ax.semilogy(vb_exp, ib_exp, '.', label="Measured base current", markersize=1)
#ax.semilogy(vb_exp, ie_exp, 'g.', label="Measured emitter current")
ax.semilogy(vb_exp, ic_exp, '.', label="Calculated collector current", markersize=1)
ax.semilogy(vb_exp, ic_f(vb_exp, Ut, Is), 'k-', label="Theoretical Ic (Ut = %.4g, Is = %.4g)" % (Ut, Is))
ax.semilogy(vb_exp, ib_f(vb_exp, β), 'k--', label="Theoretical Ib (Ut = %.4g, Is = %.4g, β = %.4g)" % (Ut, Is, β))

ax.axvline(vb_exp[valid[0]], label='Sampled Data')
ax.axvline(vb_exp[valid[1]])

plt.title("Transistor Currents vs Base Voltage")
plt.xlabel("Base Voltage (V)")
plt.ylabel("Current (A)")
plt.grid(True)
ax.legend()
#plt.show()
plt.savefig("consts.pdf")
