import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x = np.linspace(0, 5, 10)
y = [0.0, 0.05, 0.16, 0.3, 0.6, 0.8, 0.6, 0.3, 0.16, 0.0]


def fit_Lorenz(x, y, f0, init):

    def Lorentzian(f, amp, cen, wid, Offset):
        return amp*wid/((f-cen)**2 + wid**2) + Offset

    init_vals = init
    popt, cov = curve_fit(Lorentzian, x, y, p0=init_vals, maxfev=10000)

    Amp = popt[0]
    cen = np.abs(popt[1])
    wid = np.abs(popt[2])
    Offset = popt[3]

    x_fit = np.linspace(min(x), max(x), 1000)
    y_fit = np.zeros(len(x_fit))

    for i in range(len(x_fit)):
        y_fit[i] = Lorentzian(x_fit[i], Amp, cen, wid, Offset)

    return x_fit, y_fit, wid, cen, Amp, Offset


init_vals = [1, 2, 1, 1]
x_fit, y_fit, sigma, x0, Amp, Offset = fit_Lorenz(x, y, max(y), init_vals)

# peak is Amp/sigma high, so half the height is half that
half_height = 0.5*Amp/sigma + Offset
FWHM = 2*sigma
f1 = x0-FWHM/2
f2 = x0+FWHM/2

print(half_height)
print(f2-f1)

plt.plot(x, y, '.', label='data', color='blue')
plt.plot(x_fit, y_fit, '-', label='Lorentzian fit', color='red')
plt.xlim(0, 5)
plt.hlines(half_height, f1, f2, linestyle='solid', color='green')
plt.legend(loc='upper left', fontsize=13)

plt.show()