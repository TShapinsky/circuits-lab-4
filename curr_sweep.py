import smu
import numpy as np

s = smu.smu()

a = np.logspace(-9, -2, 1000)

f = open("data/exp2_sink_(.001ma).csv",'w')
f.write('"Ix","Iz"\n')

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
