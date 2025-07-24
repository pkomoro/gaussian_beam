import numpy as np

import matplotlib.pyplot as plt

from methods import GaussianBeam, Lens, GaussianDistribution , airy_diameter

# Physical constants
wavelength = 3.15  # wavelength in mm
source_waist = 5.6 # mm for photomixing
optics_diameter = 187  # diameter of the lenses in mm
detector_aperture = 7.38  # diameter of the detector in mm
detector_acceptance_angle = 8.5  # acceptance angle of the detector in degrees

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


convergence = 2 * np.rad2deg(np.atan(optics_diameter / 2 / focal_lengths)) # Apex angle of a convergence cone in degrees
# add factor 1 / 1.699  for translation from 1/e2 to FWHM 

detector_acceptance = GaussianDistribution(15, detector_acceptance_angle)  # Detector acceptance in degrees

detector_angular_acceptance = []
for f in focal_lengths:
    detector_angular_acceptance.append(detector_acceptance.overlap(15, 2 * np.rad2deg(np.arctan(optics_diameter / 2 / f))))

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

name = "outs/THz_telecom/focusing_optimization_lens_d" + str(int(optics_diameter)) + "mm_detector1_d" + str(detector_aperture) + "mm" 


# Alternative detector aperture analysis
# Uncomment the following lines to analyze an alternative detector aperture

# detector_aperture_alt = 20  # alternative detector aperture in mm

# detector_overlap_alt = []
# for d in airy_diameters:
#     if (detector_aperture_alt / d)**2 >= 1:
#         detector_overlap_alt.append(1)
#     else:
#         detector_overlap_alt.append((detector_aperture_alt / d)**2)

# detector_angular_acceptance_alt = []
# for f in focal_lengths:
#     detector_angular_acceptance_alt.append(detector_acceptance.overlap(15, 2 * np.rad2deg(np.arctan(optics_diameter / 2 / f))))

# total_efficiency_alt = [x * y for x, y in zip(detector_angular_acceptance_alt, detector_overlap_alt)]

# plt.plot(focal_lengths, detector_angular_acceptance_alt, label=f'Angular efficiency (detector {detector_aperture_alt} mm)', linestyle=':')
# plt.plot(focal_lengths, detector_overlap_alt, label=f'Overlap (detector {detector_aperture_alt} mm)', linestyle='--')
# plt.plot(focal_lengths, total_efficiency_alt, label=f'Total efficiency (detector {detector_aperture_alt} mm)')

# max_ef_alt = np.max(total_efficiency_alt)
# index_max_alt = np.argmax(total_efficiency_alt)
# focal_length_max_alt = focal_lengths[index_max_alt]
# plt.annotate(
#     f"Alt max efficiency: {max_ef_alt:.2f}\nFocal length: {focal_length_max_alt:.2f} mm",
#     xy=(focal_length_max_alt, max_ef_alt),
#     xytext=(focal_length_max_alt + 50, max_ef_alt - 0.1),
#     arrowprops=dict(arrowstyle="->", color='blue'),
#     fontsize=10,
#     color='blue',
#     bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1)
# )
# plt.scatter([focal_length_max_alt], [max_ef_alt], color='blue', zorder=5)

# name = "outs/THz_telecom/focusing_optimization_lens_d" + str(int(optics_diameter)) + "mm_detector1_d" + str(detector_aperture) + "mm_detector2_d" + str(detector_aperture_alt) + "mm"


# Alternative detector acceptance angle analysis
# Uncomment and modify the following lines to analyze an alternative detector acceptance angle

# detector_acceptance_angle_alt = 20  # alternative detector acceptance angle in degrees

# detector_acceptance_alt = GaussianDistribution(15, detector_acceptance_angle_alt)  # Alternative detector acceptance

# detector_angular_acceptance_alt = []
# for f in focal_lengths:
#     detector_angular_acceptance_alt.append(detector_acceptance_alt.overlap(15, 2 * np.rad2deg(np.arctan(optics_diameter / 2 / f))))

# total_efficiency_acceptance_alt = [x * y for x, y in zip(detector_angular_acceptance_alt, detector_overlap)]

# plt.plot(focal_lengths, detector_angular_acceptance_alt, label=f'Angular efficiency (acceptance {detector_acceptance_angle_alt}°)', linestyle=':')
# plt.plot(focal_lengths, total_efficiency_acceptance_alt, label=f'Total efficiency (acceptance {detector_acceptance_angle_alt}°)')

# max_ef_acceptance_alt = np.max(total_efficiency_acceptance_alt)
# index_max_acceptance_alt = np.argmax(total_efficiency_acceptance_alt)
# focal_length_max_acceptance_alt = focal_lengths[index_max_acceptance_alt]
# plt.annotate(
#     f"Alt max efficiency: {max_ef_acceptance_alt:.2f}\nFocal length: {focal_length_max_acceptance_alt:.2f} mm",
#     xy=(focal_length_max_acceptance_alt, max_ef_acceptance_alt),
#     xytext=(focal_length_max_acceptance_alt + 50, max_ef_acceptance_alt - 0.1),
#     arrowprops=dict(arrowstyle="->", color='green'),
#     fontsize=10,
#     color='green',
#     bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", lw=1)
# )
# plt.scatter([focal_length_max_acceptance_alt], [max_ef_acceptance_alt], color='green', zorder=5)

# name = "outs/THz_telecom/focusing_optimization_lens_d" + str(int(optics_diameter)) + "mm_detector1_d" + str(detector_aperture) + "mm_acceptance1_" + str(detector_acceptance_angle) + "deg_acceptance2_" + str(detector_acceptance_angle_alt) + "deg"


plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.show()

plt.savefig(name + ".svg")
plt.savefig(name + ".jpg")