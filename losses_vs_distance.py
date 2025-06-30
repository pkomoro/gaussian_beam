import numpy as np

from methods import GaussianBeam, Lens

import matplotlib.pyplot as plt

wavelength = 3.15
source_waist = 8

beam1 = GaussianBeam(wavelength, source_waist, 0)

l1pos = 4000
lens1 = Lens(l1pos, 4000, l1pos)

beam2 = lens1.transform(beam1)

x = np.arange(l1pos, 10 ** 8, 100)
y = [0] * len(x)
for i in range(len(x)):
    #y[i] = beam2.power_through_aperture(lens1.diameter / 2, x[i])
    y[i] = beam2.power_through_aperture(1000 / 2, x[i])


plt.xlabel('Distance [mm]')
plt.ylabel('Relative transmitted power')
plt.semilogy(x,y)
plt.savefig("outs/v96GHz_d4m_l100km_loss_log.svg")