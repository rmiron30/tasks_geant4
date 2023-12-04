import numpy as np
import matplotlib.pyplot as plt
import ROOT

from lmfit.models import LorentzianModel, VoigtModel

#########

file = ROOT.TFile("testem4.root", "READ")


histo = file.Get("Hist2D")

# def calculate_fwhm(histogram):

#     halfmax = histogram.GetMaximum() / 2.0
#     nbins = histogram.GetNbinsX()
    
#     leftBin = histogram.GetXaxis().FindBin(histogram.GetBinCenter(1))
#     rightBin = histogram.GetXaxis().FindBin(histogram.GetBinCenter(nbins))

#     for i in range(1, nbins + 1):
#         if histogram.GetBinContent(i) >= halfmax:
#             leftBin = i
#             break

#     for i in range(nbins, 0, -1):
#         if histogram.GetBinContent(i) >= halfmax:
#             rightBin = i
#             break

#     fwhm = histogram.GetXaxis().GetBinCenter(rightBin) - histogram.GetXaxis().GetBinCenter(leftBin)
#     return fwhm

# if histo:

#     Xproj = histo.ProjectionX("XProjection")
#     Yproj = histo.ProjectionY("YProjection")


#     print("Max X projection:", Xproj.GetMaximum())
#     print("Max Y projection:", Yproj.GetMaximum())

#     c1 = ROOT.TCanvas("c1", "X Projection", 800, 600)
#     Xproj.Draw()
#     c1.SaveAs("XProjection.png")

#     c2 = ROOT.TCanvas("c2", "Y Projection", 800, 600)
#     Yproj.Draw()
#     c2.SaveAs("YProjection.png")

#     fwhm_x = calculate_fwhm(Xproj)
#     print("FWHM_X :", fwhm_x)

#     fwhm_y = calculate_fwhm(Yproj)
#     print("FWHM_Y :", fwhm_y)

#     file.Close()
# else:
#     print("Histogram not found.")


def getX(hist):

    x_values = []
    y_values = []
    for i in range(1, hist.GetNbinsX() + 1):
        x_values.append(hist.GetBinCenter(i))
        y_values.append(hist.GetBinContent(i))
    return x_values

def getY(hist):

    x_values = []
    y_values = []
    for i in range(1, hist.GetNbinsX() + 1):
        x_values.append(hist.GetBinCenter(i))
        y_values.append(hist.GetBinContent(i))
    return y_values
x_data = np.array(getX(histo.ProjectionX("XProjection")))
y_data = np.array(getY(histo.ProjectionX("XProjection")))



#########

mod = LorentzianModel()

pars =  mod.guess(y_data, x=x_data)
out = mod.fit(y_data, pars, x=x_data)

print(out.fit_report(min_correl=0.25))


#########

plt.plot(x_data, y_data, 'bo', label = "real data")
plt.plot(x_data, out.init_fit, color = 'red', label = "initial fit")
plt.plot(x_data, out.best_fit, color = 'red', label = "best fit")
plt.xlim([-1,1])
plt.legend()
plt.show()