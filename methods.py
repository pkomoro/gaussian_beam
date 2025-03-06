import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

class GaussianBeam:
    def __init__(self, wavelength: float, waist: float, waist_position: float):        
        # Wavelength of radiation in [mm]
        self.wavelength = wavelength
        # Beam waist (1/e2 radius) in [mm]
        self.waist = waist
        # Beam waist position in space (one dimensional) in [mm]
        self.waist_position = waist_position
        # Rayleigh length in [mm]
        self.zR = np.pi * self.waist**2 / self.wavelength


    def radius(self, distance: float):
        return self.waist * np.sqrt(1 + ((distance - self.waist_position) / self.zR)**2)
    
    def divergence(self):
        return self.wavelength / np.pi / self.waist


class Lens:
    def __init__(self, focal_length: float, diameter: float, position: float):        
        # Focal lenght in [mm]
        self.focal_length = focal_length
        # Diameter in [mm]
        self.diameter = diameter
        # Lens position in space (one dimensional) in [mm]
        self.position = position
    

    def transform(self, input: GaussianBeam):
        d1 = self.position - input.waist_position
        if d1 <= 0:
            raise Exception("Lens positioned before waist of the input beam.")
        w2 = self.focal_length * input.waist / np.sqrt((d1 -self.focal_length)**2 + input.zR ** 2)
        d2 = self.focal_length + self.focal_length ** 2 * (d1 - self.focal_length) / ((d1 - self.focal_length) ** 2 + input.zR ** 2)

        return GaussianBeam(input.wavelength, w2, self.position + d2)
    

class Plotter:
    def __init__(self, point_density: float = 1.0):        
        # Density of points in the plot
        self.point_density = point_density
        plt.xlabel('Distance [mm]')
        plt.ylabel('1/e2 beam radius [mm]')


    def add_beam(self, beam: GaussianBeam, start: float, end: float):
        x = np.arange(start, end, self.point_density)
        y = [0] * len(x)
        for i in range(len(x)):
            y[i] = beam.radius(x[i])

        plt.plot(x,y)

    def add_lens(self, lens: Lens):
        x = [lens.position, lens.position]
        y = [0, lens.diameter / 2]

        plt.plot(x, y)

    def add_transmission(self, beam: GaussianBeam, lens: Lens):
        T = 1 - np.exp(-2 * (lens.diameter / 2) ** 2 / beam.radius(lens.position) ** 2)
        plt.text(lens.position, lens.diameter / 2, "T = " + str(int(100*T)) + "%")

    def save(self, path):
        self._prepare_path_to_save(path)
        plt.savefig(path)

    def _prepare_path_to_save(self, path):
        dirs = os.path.dirname(path)
        Path(dirs).mkdir(parents=True, exist_ok=True)