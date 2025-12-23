import numpy as np

import matplotlib.pyplot as plt

from methods import GaussianBeam, Lens, GaussianDistribution , airy_diameter
from scipy.optimize import minimize

# Physical constants
wavelength = 3.15  # wavelength in mm
source_waist = 5.6 # mm for photomixing
optics_diameter = 187  # diameter of the lenses in mm

# Alvidas detector parameters
# detector_aperture = 10  # diameter of the detector in mm
# detector_acceptance_angle = 8.5  # acceptance angle of the detector in degrees (half-angle FWHM)
# detname = "Alvidas"
# experiment = [[118, 3.18 ], [158, 5.46], [180, 5.89], [300, 5.79]]
# scaling_factor = 0.04  # Scaling factor for experimental values; adjust as needed

# Small cone detector parameters
# detector_aperture = 12  # diameter of the detector in mm
# detector_acceptance_angle = 7  # acceptance angle of the detector in degrees (half-angle FWHM)
# detname = "smallCone"
# experiment = [[158, 6.75], [180, 8.49], [300, 13.51], [466, 4.16]]
# scaling_factor = 0.022  # Scaling factor for experimental values; adjust as needed

# Big cone detector parameters
# detector_aperture = 12  # diameter of the detector in mm
# detector_acceptance_angle = 11.5/2  # acceptance angle of the detector in degrees (half-angle FWHM)
# detname = "bigCone"
# experiment = [[158, 5.47], [180, 7.18], [300, 13.41], [466, 4.55]]
# scaling_factor = 0.02  # Scaling factor for experimental values; adjust as needed

# Bare waveguide detector parameters
detector_aperture = 2  # diameter of the detector in mm
detector_acceptance_angle = 60/2  # acceptance angle of the detector in degrees (half-angle FWHM)
detname = "bareWG"
experiment = [[68, 2.13], [118, 4.0], [158, 4.09], [180, 4]]
scaling_factor = 0.16  # Scaling factor for experimental values; adjust as needed

# Extract experimental data points
experiment_focal_lengths = [point[0] for point in experiment]
experiment_efficiencies = [point[1] * scaling_factor for point in experiment]



# Range of focal lengths (simulate different focusing conditions)
focal_lengths = np.linspace(1, 1000, 1000)


airy_diameters = airy_diameter(wavelength, focal_lengths, optics_diameter)


convergence = 2 * np.rad2deg(np.atan(optics_diameter / 2 / focal_lengths)) # Apex angle of a convergence cone in degrees
# add factor 1 / 1.699  for translation from 1/e2 to FWHM 

detector_acceptance = GaussianDistribution(15, detector_acceptance_angle / 1.699)  # Detector acceptance in degrees

detector_angular_acceptance = []
for f in focal_lengths:
    detector_angular_acceptance.append(detector_acceptance.overlap(15, 2 * np.rad2deg(np.arctan(optics_diameter / 2 / f))))


airy_diameters = airy_diameter(wavelength, focal_lengths, optics_diameter)


def loss_function(aperture):
    detector_overlap = []
    for d in airy_diameters:
        if (aperture / d)**2 >= 1:
            detector_overlap.append(1)
        else:
            detector_overlap.append((aperture / d)**2)
    total_efficiency = [x * y for x, y in zip(detector_angular_acceptance, detector_overlap)]
    
    # Include only specified range of experimental points
    valid_indices = [i for i, f in enumerate(experiment_focal_lengths) if 100 <= f <= 400]
    filtered_focal_lengths = [experiment_focal_lengths[i] for i in valid_indices]
    filtered_efficiencies = [experiment_efficiencies[i] for i in valid_indices]
    
    loss = np.mean((np.interp(filtered_focal_lengths, focal_lengths, total_efficiency) - filtered_efficiencies)**2)
    return loss

apertures = np.linspace(5, 20, 100)  # Range of apertures to test
losses = [loss_function(aperture) for aperture in apertures]

best_aperture = apertures[np.argmin(losses)]
print(f"Best detector aperture: {best_aperture:.2f} mm")

plt.figure(figsize=(8, 5))
plt.plot(apertures, losses, label='Mean Squared Error')
plt.xlabel('Detector Aperture [mm]')
plt.ylabel('Loss')
plt.title('Optimization of Detector Aperture')
plt.scatter([best_aperture], [min(losses)], color='red', label=f'Best Aperture: {best_aperture:.2f} mm')
plt.legend()
plt.grid(True)
plt.tight_layout()

name = "outs/THz_telecom/aperturefit_" + detname

plt.savefig(name + ".svg")
plt.savefig(name + ".jpg")

detector_aperture = best_aperture

detector_overlap = []

for d in airy_diameters:
    if (detector_aperture / d)**2 >=1:
        detector_overlap.append(1)
    else:
        detector_overlap.append((detector_aperture / d)**2)


convergence = 2 * np.rad2deg(np.atan(optics_diameter / 2 / focal_lengths)) # Apex angle of a convergence cone in degrees
# add factor 1 / 1.699  for translation from 1/e2 to FWHM 

detector_acceptance = GaussianDistribution(15, detector_acceptance_angle / 1.699)  # Detector acceptance in degrees

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

 
# Plot experimental data points

plt.scatter(experiment_focal_lengths, experiment_efficiencies, color='purple', label='Experimental data', zorder=6)



# Include uncertainty crosses around experimental data points
y_errors = []
for f in experiment_focal_lengths:
    if 100 <= f <= 400:
        y_errors.append(1 - 0.96)  # Example uncertainty for focal lengths in the range
    else:
        y_errors.append(1 - 0.96**2)  # Example uncertainty for focal lengths outside the range
for (x, y) in zip(experiment_focal_lengths, experiment_efficiencies):
    plt.errorbar(x, y, xerr=5, yerr=y_errors[experiment_focal_lengths.index(x)], fmt='o', color='purple', elinewidth=1, capsize=3, label='_nolegend_')




plt.xlabel('Focal length [mm]')
plt.ylabel('Efficiency')
plt.title('Comparison of focusing and detection efficiency')
plt.annotate(
    f"Max efficiency: {max_ef:.2f}\nFocal length: {focal_length_max:.2f} mm",
    xy=(focal_length_max, max_ef),
    xytext=(focal_length_max - 250, max_ef + 0.15),
    arrowprops=dict(arrowstyle="->", color='black'),
    fontsize=10,
    color='black',
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1)
)
plt.scatter([focal_length_max], [max_ef], color='red', zorder=5)

name = "outs/THz_telecom/aperturefit_lens_d" + str(int(optics_diameter)) + "mm_" + detname + "_d" + f"{best_aperture:.2f} mm"


plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.show()

plt.savefig(name + ".svg")
plt.savefig(name + ".jpg", dpi=1000)