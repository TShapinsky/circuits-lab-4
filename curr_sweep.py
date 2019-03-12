import smu
import numpy as np

s = smu.smu()

a = np.logspace(-8, -2, 1000)

f = open("data/exp3_sink_(.1ma).csv",'w')
f.write('"Iy","Iz"\n')

s.set_current(1,0)
s.autorange(1)
s.set_voltage(2,0)
s.autorange(2)

for val in a:
    s.set_current(1, val)
    s.autorange(1)
    s.set_voltage(2,0)
    s.autorange(2)
    f.write('{!s},{!s}\n'.format(s.get_current(1),s.get_current(2)))

s.set_current(1,0)
f.close()
