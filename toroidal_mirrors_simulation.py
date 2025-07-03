import numpy as np

from methods import GaussianBeam, Lens, Plotter, ToroidalMirror

wavelength = 0.6 # mm (500 GHz)
# zR = 204 mm
source_waist = 6.2 # mm

beam1 = GaussianBeam(wavelength, source_waist, 0)

m1pos = 1280
mirror1 = ToroidalMirror(1099.8, 549.9, np.pi / 4 , 100, m1pos)
beam2 = mirror1.transform(beam1)

m2pos = 2380
mirror2 = ToroidalMirror(1309.42, 654.71, np.pi / 4 , 100, m2pos)
beam3 = mirror2.transform(beam2)

m3pos = 7480
mirror3 = ToroidalMirror(5030.62, 2515.31, np.pi / 4 , 100, m3pos)
beam4 = mirror3.transform(beam3)

m4pos = 14580
mirror4 = ToroidalMirror(4795.34, 2397.67, np.pi / 4 , 100, m4pos)
beam5 = mirror4.transform(beam4)

m5pos = 19070
#mirror5 = ToroidalMirror.from_focal_lengths(2090, 10**8, np.pi / 4 , 100, m5pos)
R = 6200
mirror5 = ToroidalMirror(R, R/2, np.pi / 4 , 100, m5pos)
print(mirror5.R, mirror5.r)
beam6 = mirror5.transform(beam5)




plot = Plotter()

plot.add_beam(beam1, 0, m1pos)
plot.add_mirror(mirror1)
plot.add_beam(beam2, m1pos, m2pos)
plot.add_mirror(mirror2)
plot.add_beam(beam3, m2pos, m3pos)
plot.add_mirror(mirror3)
plot.add_beam(beam4, m3pos, m4pos)
plot.add_mirror(mirror4)
plot.add_beam(beam5, m4pos, m5pos)
plot.add_mirror(mirror5)
plot.add_beam(beam6, m5pos, m5pos + 2000)



plot.save("outs/polfel/v500GHz_TM1.svg")



#Polfel setup

# m1pos = 1280
# mirror1 = ToroidalMirror(1099.8, 549.9, np.pi / 4 , 100, m1pos)
# beam2 = mirror1.transform(beam1)

# m2pos = 2380
# mirror2 = ToroidalMirror(1309.42, 654.71, np.pi / 4 , 100, m2pos)
# beam3 = mirror2.transform(beam2)

# m3pos = 7480
# mirror3 = ToroidalMirror(5030.62, 2515.31, np.pi / 4 , 100, m3pos)
# beam4 = mirror3.transform(beam3)

# m4pos = 14580
# mirror4 = ToroidalMirror(4795.34, 2397.67, np.pi / 4 , 100, m4pos)
# beam5 = mirror4.transform(beam4)

# m5pos = 19380
# mirror5 = ToroidalMirror(2879.80, 1439.90, np.pi / 4 , 100, m5pos)
# beam6 = mirror5.transform(beam5)

# m6pos = 22560
# mirror6 = ToroidalMirror(4678.64, 2339.32, np.pi / 4 , 100, m6pos)
# beam7 = mirror6.transform(beam6)


# plot = Plotter()

# plot.add_beam(beam1, 0, m1pos)
# plot.add_mirror(mirror1)
# plot.add_beam(beam2, m1pos, m2pos)
# plot.add_mirror(mirror2)
# plot.add_beam(beam3, m2pos, m3pos)
# plot.add_mirror(mirror3)
# plot.add_beam(beam4, m3pos, m4pos)
# plot.add_mirror(mirror4)
# plot.add_beam(beam5, m4pos, m5pos)
# plot.add_mirror(mirror5)
# plot.add_beam(beam6, m5pos, m6pos)
# plot.add_mirror(mirror6)
# plot.add_beam(beam7, m6pos, m6pos + 1000)


# plot.save("outs/polfel/v500GHz_test.svg")
