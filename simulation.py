import numpy as np

from methods import GaussianBeam, Lens, Plotter

wavelength = 1
source_waist = 2

beam1 = GaussianBeam(wavelength, source_waist, 0)

l1pos = 1000
lens1 = Lens(1000, 600, l1pos)

beam2 = lens1.transform(beam1)

l2pos = 100000
lens2 = Lens(1000, 600, l2pos)

beam3 = lens2.transform(beam2)

plot = Plotter()

plot.add_beam(beam1, 0, l1pos)
plot.add_lens(lens1)
plot.add_transmission(beam1, lens1)
plot.add_beam(beam2, l1pos, l2pos)
plot.add_lens(lens2)
plot.add_transmission(beam2, lens2)
plot.add_beam(beam3, l2pos, beam3.waist_position)
plot.save("outs/v300GHz_z100m.svg")
