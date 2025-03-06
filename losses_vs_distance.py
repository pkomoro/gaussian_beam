import numpy as np

from methods import GaussianBeam, Lens

import matplotlib.pyplot as plt

wavelength = 3.15
source_waist = 8

beam1 = GaussianBeam(wavelength, source_waist, 0)

l1pos = 1000
lens1 = Lens(1000, 600, l1pos)

beam2 = lens1.transform(beam1)

x = np.arange(l1pos, 2 * 10 ** 6, 10)
y = [0] * len(x)
for i in range(len(x)):
    y[i] = 100 * beam2.power_through_aperture(lens1.diameter / 2, x[i])


plt.xlabel('Distance [mm]')
plt.ylabel('Transmitted power [%]')
plt.semilogy(x,y)
plt.savefig("outs/v96GHz_loss_log.svg")