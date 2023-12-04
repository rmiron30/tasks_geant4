import numpy as np
import matplotlib.pyplot as plt

from lmfit.models import LorentzianModel

def lorentzian(x, amplitude, center, width):
    return amplitude/np.pi * (width/2) / ((x-center)**2 + (width/2)**2)

np.random.seed(42)
x_data = np.linspace(0,10,500)
true_params = [1.0, 5.0, 0.01] #amp, center, width
y_true = lorentzian(x_data, *true_params)

noise = np.random.normal(scale = 0.05, size = len(x_data))
y_data = y_true + noise

mod = LorentzianModel()

pars =  mod.guess(y_data, x=x_data)
out = mod.fit(y_data, pars, x=x_data)

print(out.fit_report(min_correl=0.25))

plt.plot(x_data, y_data, 'bo', label = "real data")
plt.plot(x_data, out.best_fit, color = 'red', label = "fitted curve")
plt.legend()
plt.show()


    