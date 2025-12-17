import numpy as np

from methods import GaussianBeam, Lens, Plotter

wavelength = 3.15 # mm
source_waist = 5.6 # mm for photomixing

def waist_from_angle(a):
    # Convert acceptance angle in degrees to waist in mm
    a_rad = np.radians(a)
    return wavelength / (np.pi * a_rad)

# detector_acceptance_angle = 7  # acceptance angle of the detector in degrees (half-angle FWHM)
# detname = "smallCone"

beam1 = GaussianBeam(wavelength, source_waist, 0)

l1pos = 50
l1f = -33.33  # focal length of the first lens in mm
lens1 = Lens(l1f, 27, l1pos)

beam2 = lens1.transform(beam1)

l2f = 120
l2pos = l1pos + l2f - 22
lens2 = Lens(l2f, 187, l2pos)

beam3 = lens2.transform(beam2)

plot = Plotter()

plot.add_beam(beam1, 0, l1pos)
plot.add_lens(lens1)
plot.add_transmission(beam1, lens1)
plot.add_beam(beam2, l1pos, l2pos)
plot.add_lens(lens2)
plot.add_transmission(beam2, lens2)
z = 20000
plot.add_beam(beam3, l2pos, z)
name = "v96GHz_2lens_diffusing_z" + str(z / 1000) + "m_f1_" + str(l1f) + "mm_f2_" + str(l2f) + "mm"
plot.save("outs/THz_telecom/Emmiter/" + name + ".svg")
plot.save("outs/THz_telecom/Emmiter/" + name + ".jpg")
