#!/usr/bin/env python2
import smu
import numpy as np
s = smu.smu()
#v = np.logspace(-3, np.log10(5), 1000)
v = np.linspace(0,5,1000)

f = open("data/exp1_trans4.csv", 'w')
f.write('"Vbe","Ib","Ie"\n')

s.set_voltage(1,0)
s.autorange(1)
#s.set_vrange(2,0)
s.set_voltage(2,0)
s.autorange(2)
for val in v:
    s.set_voltage(1, val)
    s.autorange(1)
    s.set_voltage(2, 0)
    s.autorange(2)
    f.write('{!s},{!s},{!s}\n'.format(val, s.get_current(1), s.get_current(2)))

s.set_current(1, 0.)
f.close()
