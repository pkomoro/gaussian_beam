import numpy as np

import matplotlib.pyplot as plt

from methods import GaussianBeam, Lens, GaussianDistribution , airy_diameter

# Physical constants
wavelength = 3.15  # wavelength in mm
source_waist = 5.6 # mm for photomixing
optics_diameter = 187  # diameter of the lenses in mm
detector_aperture = 5  # diameter of the detector in mm

beam1 = GaussianBeam(wavelength, source_waist, 0)

l1pos = 350
lens1 = Lens(l1pos, optics_diameter, l1pos)

beam2 = lens1.transform(beam1)

l2pos = l1pos + 351  # position of the second lens

# Range of focal lengths (simulate different focusing conditions)
focal_lengths = np.linspace(1, 1000, 1000)

lens2 = Lens(focal_lengths, optics_diameter, l2pos)

beam3 = lens2.transform(beam2)


airy_diameters = airy_diameter(wavelength, focal_lengths, optics_diameter)

detector_overlap = []

for d in airy_diameters:
    if (detector_aperture / d)**2 >=1:
        detector_overlap.append(1)
    else:
        detector_overlap.append((detector_aperture / d)**2)


convergence = 2 * np.rad2deg(np.atan(optics_diameter / 2 / focal_lengths)) / 1.699  # FWHM convergence angle in degrees

detector_acceptance = GaussianDistribution(15, 8.5)  # Detector acceptance in degrees

detector_angular_acceptance = []
for f in focal_lengths:
    detector_angular_acceptance.append(detector_acceptance.overlap(15, 2 * np.rad2deg(np.arctan(optics_diameter / 2 / f)) / 1.699))

total_efficiency = [x * y for x, y in zip(detector_angular_acceptance, detector_overlap)]

max_ef = np.max(total_efficiency)  # Check the maximum efficiency
index_max = np.argmax(total_efficiency)  # Index of the maximum efficiency
focal_length_max = focal_lengths[index_max]  # Focal length corresponding to the maximum efficiency
print(f"Focal length for maximum efficiency: {focal_length_max:.2f} mm")
print(f"Maximum efficiency: {max_ef:.2f}")




plt.figure(figsize=(8, 5))
# plt.plot(focal_lengths, airy_diameters, label='Airy Diameter [mm]')
# plt.plot(focal_lengths, convergence/90, label='Full 3dB convergence angle [degrees]', linestyle='--')
plt.plot(focal_lengths, detector_angular_acceptance, label='Angular efficiency of the detection', linestyle=':')
plt.plot(focal_lengths, detector_overlap, label='Overlap of the detector with the Airy disk', linestyle='--')
plt.plot(focal_lengths, total_efficiency, label='Total efficiency')
plt.xlabel('Focal length [mm]')
plt.ylabel('Efficiency')
plt.title('Comparison of focusing and detection efficiency')
plt.annotate(
    f"Max efficiency: {max_ef:.2f}\nFocal length: {focal_length_max:.2f} mm",
    xy=(focal_length_max, max_ef),
    xytext=(focal_length_max + 50, max_ef - 0.1),
    arrowprops=dict(arrowstyle="->", color='black'),
    fontsize=10,
    color='black',
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1)
)
plt.scatter([focal_length_max], [max_ef], color='red', zorder=5)
plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.show()

name = "outs/THz_telecom/focusing_optimization_lens_d" + str(int(optics_diameter)) + "mm_detector_d" + str(int(detector_aperture)) + "mm"
plt.savefig(name + ".svg")
plt.savefig(name + ".jpg")