import numpy as np
from math import pi
import matplotlib.pyplot as plt

class impedance:
    def __init__(self, value):
        self.value = value

class r(impedance):
    def z(self, f):
        return self.value

class l(impedance):
    def z(self, f):
        return 2j*pi*f*self.value

class c(impedance):
    def z(self, f):
        return 1/(2j*pi*f*self.value)

class series:
    def __init__(self, z1, z2):
        self.z1 = z1
        self.z2 = z2

    def z(self, f):
        return self.z1.z(f)+self.z2.z(f)

class parallel:
    def __init__(self, z1, z2):
        self.z1 = z1
        self.z2 = z2

    def z(self, f):
        return 1/(1/self.z1.z(f)+1/self.z2.z(f))



f = np.linspace(15.85e6, 16e6, 1001)
z0 = np.zeros(f.shape)

c0 = c(10e-12)
c1 = c(10e-15)
l1 = l(10e-3)
r1 = r(10)

s = series(series(c1, l1), r1)
p = parallel(s, c0)

z = [p.z(i).imag for i in f]

plt.plot(f, z, f, z0)
plt.show()
