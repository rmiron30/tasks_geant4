import numpy as np
import matplotlib.pyplot as plt

from astropy.modeling.models import Lorentz1D


plt.figure()
s1 = Lorentz1D(1,0,1)
print(s1.fwhm)
r = np.arange(-5, 5, .01)

for factor in range(1, 10):
    s1.amplitude = factor
    #s1.fwhm-=0.05
    plt.plot(r, s1(r), color=str(0.1 * factor), lw=2)

plt.axis([-5, 5, -1, 10])
plt.show()
