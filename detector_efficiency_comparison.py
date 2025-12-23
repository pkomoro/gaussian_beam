import numpy as np

import matplotlib.pyplot as plt

from methods import GaussianBeam, Lens, GaussianDistribution , airy_diameter
from scipy.optimize import minimize

# Physical constants
wavelength = 3.15  # wavelength in mm
source_waist = 5.6 # mm for photomixing
optics_diameter = 187  # diameter of the lenses in mm

# Alvidas detector parameters
detector_acceptance_angle1 = 8.5  # acceptance angle of the detector in degrees (half-angle FWHM)
detname1 = "Alvidas"
experiment1 = [[118, 3.18 ], [158, 5.46], [180, 5.89], [300, 5.79]]

# Small cone detector parameters
detector_acceptance_angle2 = 7  # acceptance angle of the detector in degrees (half-angle FWHM)
detname2 = "smallCone"
experiment2 = [[158, 6.75], [180, 8.49], [300, 13.51], [466, 4.16]]

# Big cone detector parameters
detector_acceptance_angle3 = 11.5/2  # acceptance angle of the detector in degrees (half-angle FWHM)
detname3 = "bigCone"
experiment3 = [[158, 5.47], [180, 7.18], [300, 13.41], [466, 4.55]]

# Bare waveguide detector parameters
detector_acceptance_angle4 = 60/2  # acceptance angle of the detector in degrees (half-angle FWHM)
detname4 = "bareWG"
experiment4 = [[68, 2.13], [118, 4.0], [158, 4.09], [180, 4]]



# Plot experimental data points
plt.figure(figsize=(10, 6))

# Plot each experiment data
experiments = [(experiment1, detname1), (experiment2, detname2), (experiment3, detname3), (experiment4, detname4)]
for experiment, detname in experiments:
    distances, efficiencies = zip(*experiment)
    plt.plot(distances, efficiencies, 'o--', label=detname)

# Add labels, legend, and grid
plt.xlabel('Distance (mm)')
plt.ylabel('Measured power [mW]')
plt.title('Detector Efficiency Comparison')
plt.legend()
plt.grid(True)


name = "outs/THz_telecom/detector_efficiency_comparison"


plt.savefig(name + ".svg")
plt.savefig(name + ".jpg", dpi=1000)
