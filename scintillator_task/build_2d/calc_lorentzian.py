import numpy as np
import matplotlib.pyplot as plt
import ROOT

from lmfit.models import LorentzianModel, VoigtModel

#########

file = ROOT.TFile("testem4.root", "READ")


histo = file.Get("Hist2D")

def getXY(hist):

    x_values = []
    y_values = []
    for i in range(1, hist.GetNbinsX() + 1):
        x_values.append(hist.GetBinCenter(i))
        y_values.append(hist.GetBinContent(i))
    return np.array(x_values), np.array(y_values)

x_data, y_data = getXY(histo.ProjectionX("XProjection"))


#########

mod = LorentzianModel()

pars =  mod.guess(y_data, x=x_data)
out = mod.fit(y_data, pars, x=x_data)

print(out.fit_report(min_correl=0.25))


#########

plt.plot(x_data, y_data, 'bo', label = "real data")
plt.plot(x_data, out.best_fit, color = 'red', label = "best fit")
plt.xlim([-1,1])
plt.legend()
plt.show()