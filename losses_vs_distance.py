import numpy as np

from methods import GaussianBeam, Lens

import matplotlib.pyplot as plt

wavelength = 3.15
source_waist = 5.6
diameter = 187  # mm

beam1 = GaussianBeam(wavelength, source_waist, 0)

l1pos = 350  # mm
lens1 = Lens(l1pos, diameter, l1pos)

beam2 = lens1.transform(beam1)

scan_range = 10 ** 5  # mm

x = np.arange(l1pos, scan_range, 100)
y = [0] * len(x)
for i in range(len(x)):
    #y[i] = beam2.power_through_aperture(lens1.diameter / 2, x[i])
    y[i] = beam2.power_through_aperture(diameter / 2, x[i])

x = x / 1000  # convert to meters

plt.xlabel('Distance [m]')
plt.ylabel('Relative transmitted power')
plt.semilogy(x,y)
plt.savefig("outs/łącze_małe_średnice/v96GHz_d" + str(diameter) + "mm_l" + str(scan_range / 10**6) + "km_loss_log.svg")
plt.savefig("outs/łącze_małe_średnice/v96GHz_d" + str(diameter) + "mm_l" + str(scan_range / 10**6) + "km_loss_log.jpg")