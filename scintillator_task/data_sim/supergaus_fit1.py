# super Gaussian fit for the data, X projection

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from lmfit import Model   
import os
import json
from ROOT import TFile

def super_gaussian(x, amplitude=1.0, center=0.0, sigma=1.0, expon=2.0):
    """super-Gaussian distribution
    super_gaussian(x, amplitude, center, sigma, expon) =
        (amplitude/(sqrt(2*pi)*sigma)) * exp(-abs(x-center)**expon / (2*sigma**expon))
    """
    sigma = max(1.e-15, sigma)
    return ((amplitude/(np.sqrt(2*np.pi)*sigma))
            * np.exp(-abs(x-center)**expon / 2*sigma**expon))

colors_energy = {'0.1': "blue", '0.5':"green", '1':"red", '3':"purple", '5':"orange", '10':"lawngreen"}
energies = ["0.1", "0.5", "1", "3", "5", "10"]
order = [energies.index(i) for i in energies]
# get data from root file
cwd = os.getcwd()
for root, dirs, files in os.walk(cwd):
     for dir in dirs:
            # print("folderul curent este "+ dir)
            os.chdir(dir)
            file = TFile("testem4.root", "READ")
            configFile = open("config.json", "r")
            config = json.load(configFile)
            histo = file.Get("eDep2D")
            if histo and config["material"] == "LYSO" and config["thickness"] == 2:
                Xproj = histo.ProjectionX("XProjection")
                x_values = [Xproj.GetBinCenter(i) for i in range(1, Xproj.GetNbinsX()+1)]
                y_values = [Xproj.GetBinContent(i) for i in range(1, Xproj.GetNbinsX()+1)]
                plt.figure(1)
                plt.plot(x_values, y_values, label = "{} MeV".format(config["energy"]), color = colors_energy[str(config["energy"])])
                plt.title("LYSO 2 mm")
                plt.yscale("log")
                plt.xlim(-1,1)
                plt.xlabel("X [mm]")
                plt.ylabel("counts")    
                plt.legend()
                # plt.legend([plt.gca().get_legend().legendHandles[idx] for idx in order], [f'{energies[idx]} MeV' for idx in order])
            elif histo and config["material"] == "BGO" and config["thickness"] == 2:
                Xproj = histo.ProjectionX("XProjection")
                x_values = [Xproj.GetBinCenter(i) for i in range(1, Xproj.GetNbinsX()+1)]
                y_values = [Xproj.GetBinContent(i) for i in range(1, Xproj.GetNbinsX()+1)]
                plt.figure(2)
                plt.plot(x_values, y_values, label = "{} MeV".format(config["energy"]), color = colors_energy[str(config["energy"])])
                plt.title("BGO 2 mm")
                plt.yscale("log")
                plt.xlim(-1,1)
                plt.xlabel("X [mm]")
                plt.ylabel("counts") 
                plt.legend()
            elif histo and config["material"] == "CsI" and config["thickness"] == 2:
                Xproj = histo.ProjectionX("XProjection")
                x_values = [Xproj.GetBinCenter(i) for i in range(1, Xproj.GetNbinsX()+1)]
                y_values = [Xproj.GetBinContent(i) for i in range(1, Xproj.GetNbinsX()+1)]
                plt.figure(3)
                plt.plot(x_values, y_values, label = "{} MeV".format(config["energy"]), color = colors_energy[str(config["energy"])])
                plt.title("CsI 2 mm")
                plt.yscale("log")
                plt.xlim(-1,1)
                plt.xlabel("X [mm]")
                plt.ylabel("counts") 
                plt.legend()
            os.chdir(cwd)
# k = [0.1, 0.5, 1, 3, 5, 10]
# def legend_sorted(figure):
#     handles, labels = plt.gca().get_legend_handles_labels()
#     # by_label = dict(zip(labels, handles))
#     sorted_labels = [x for _,x in sorted(zip(k, labels),reverse=True)]
#     sorted_handles = [x for _,x in sorted(zip(k, handles),reverse=True)]
#     figure.legend(sorted_handles,sorted_labels, loc='upper left')
# legend_sorted(plt)

plt.figure(1)
plt.savefig("LYSO_2mm.pdf")
plt.figure(2)
plt.savefig("BGO_2mm.pdf")
plt.figure(3)
plt.savefig("CsI_2mm.pdf")

plt.show()
# x = np.linspace(0, 10, 101)
# y = super_gaussian(x, amplitude=7.1, center=4.5, sigma=2.5, expon=1.5)
# y += np.random.normal(size=len(x), scale=0.015)

# # make Model from the super_gaussian function
# model = Model(super_gaussian)

# # build a set of Parameters to be adjusted in fit, named from the arguments 
# # of the model function (super_gaussian), and providing initial values
# params = model.make_params(amplitude=1, center=5, sigma=2., expon=2)

# # you can place min/max bounds on parameters
# params['amplitude'].min = 0
# params['sigma'].min = 0
# params['expon'].min = 0
# params['expon'].max = 100

# # note: if you wanted to make this strictly Gaussian, you could set 
# # expon=2  and prevent it from varying in the fit:
# ### params['expon'].value = 2.0
# ### params['expon'].vary = False

# # now do the fit
# result = model.fit(y, params, x=x)

# # print out the fit statistics, best-fit parameter values and uncertainties
# print(result.fit_report())

# # plot results
# import matplotlib.pyplot as plt
# plt.plot(x, y, label='data')
# plt.plot(x, result.best_fit, label='fit')
# plt.legend()
# plt.show()
