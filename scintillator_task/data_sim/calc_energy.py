# calculate fwhm, fwtm, eDep, eHalf, eTen, eTen/eDep*100, scintillations=eDep*yield

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from lmfit import Model   
import os
import json
from ROOT import TFile
from operator import itemgetter

yields = {"CsI": 54, "BGO": 8, "LYSO": 40} #photons/kev

def CalculateFwhm(hist):
    halfmax = hist.GetMaximum() / 2.0
    nbins = hist.GetNbinsX()
    
    leftBin = hist.GetXaxis().FindBin(hist.GetBinCenter(1))
    rightBin = hist.GetXaxis().FindBin(hist.GetBinCenter(nbins))

    for i in range(1, nbins + 1):
        if hist.GetBinContent(i) >= halfmax:
            leftBin = i
            break

    for i in range(nbins, 0, -1):
        if hist.GetBinContent(i) >= halfmax:
            rightBin = i
            break
        
    sum = 0

    for i in range(leftBin, rightBin, +1):
        sum+=hist.GetBinContent(i)

    fwhm = hist.GetXaxis().GetBinCenter(rightBin) - hist.GetXaxis().GetBinCenter(leftBin)
    return hist.GetXaxis().GetBinCenter(leftBin), hist.GetXaxis().GetBinCenter(rightBin), halfmax, fwhm, sum


def CalculateFwtm(hist):
    tenthmax = hist.GetMaximum() / 10.0
    nbins = hist.GetNbinsX()
    
    leftBin = hist.GetXaxis().FindBin(hist.GetBinCenter(1))
    rightBin = hist.GetXaxis().FindBin(hist.GetBinCenter(nbins))

    for i in range(10, nbins + 1):
        if hist.GetBinContent(i) >= tenthmax:
            leftBin = i
            break

    for i in range(nbins, 10, -1):
        if hist.GetBinContent(i) >= tenthmax:
            rightBin = i
            break

    fwtm = hist.GetXaxis().GetBinCenter(rightBin) - hist.GetXaxis().GetBinCenter(leftBin)

    sum = 0

    for i in range(leftBin, rightBin, +1):
        sum+=hist.GetBinContent(i)

    return hist.GetXaxis().GetBinCenter(leftBin), hist.GetXaxis().GetBinCenter(rightBin), tenthmax, fwtm, sum


def getDataFromFiles(config):

    data = {}

    data["material"] = config["material"]
    data["energy"] = config["energy"]
    data["width"] = config["thickness"]
    data["fwhm"] = fwhm
    data["fwtm"] = fwtm
    data["eDep"] = eDep
    data["eHalf"] = eHalf
    data["eTen"] = eTen
    data["raport"] = eTen/eDep*100
    data["total_opt_yield"] = yields[data["material"]] * data["eDep"] * 1000

    return data


colors_energy = {'0.1': "purple", '0.5':"green", '1':"red", '3':"blue", '5':"orange", '10':"lawngreen"}
energies = ["0.1", "0.5", "1", "3", "5", "10"]
order = [energies.index(i) for i in energies]

data = []

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
            hist1D = file.Get("Hist1D")
            
            if histo:
                Xproj = histo.ProjectionX("XProjection")
                x_values = [Xproj.GetBinCenter(i) for i in range(1, Xproj.GetNbinsX()+1)]
                y_values = [Xproj.GetBinContent(i) for i in range(1, Xproj.GetNbinsX()+1)]

                left, right, halfmax, fwhm, eHalf = CalculateFwhm(Xproj)
                left2, right2, tenthmax, fwtm, eTen = CalculateFwtm(Xproj)
                eDep = 0
                for i in range(1, hist1D.GetNbinsX() + 1):
                    eDep += hist1D.GetBinCenter(i) * hist1D.GetBinContent(i)
                file.Close()
            data.append(getDataFromFiles(config))
            os.chdir(cwd)
data = sorted(data, key=itemgetter("material", "energy", "width"))



output_file = open("energy_fwtm.txt", "w")

output_file.write(
    "Mat\tE (MeV)\tWidth\tFWHM\tFWTM\teHalf\teTen\teDep\traport\tscintillations\n"
)

for dataPoint in data:
    output_file.write(dataPoint["material"])
    output_file.write("\t")
    output_file.write(str(dataPoint["energy"]))
    output_file.write("\t")
    output_file.write(str(dataPoint["width"]))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["fwhm"], 4)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["fwtm"], 4)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["eHalf"], 4)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["eTen"], 4)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["eDep"], 4)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["raport"], 4)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["total_opt_yield"], 4)))
    output_file.write("\n")

output_file.close()

######## grafice
colors_width = {'0.5': "blue", '1.0': "green", '2.0': "red"}
colors_materials = {'CSI': "blue", 'BGO': "green", 'LYSO': "red"}
markers_width = {'0.5': "o", '1.0': "v", '2.0': "s"}
markers_materials = {'CSI': "o", 'BGO': "v", 'LYSO': "s"}
colors_energy = {'0.1': "blue", '0.5':"green", '1.0':"red", '3.0':"purple", '5.0':"orange", '10.0':"lawngreen"}

xc05 = []
xc1 = []
xc2 = []
yc05 = []
yc1 = []
yc2 = []

xb05 = []
xb1 = []
xb2 = []
yb05 = []
yb1 = []
yb2 = []

xl05 = []
xl1 = []
xl2 = []
yl05 = []
yl1 = []
yl2 = []

for dataPoint in data:
    if dataPoint["material"]=="CsI":
        if dataPoint["width"] == 0.5:
            xc05.append(dataPoint["energy"])
            yc05.append(dataPoint["raport"])
        elif dataPoint["width"] == 1:
            xc1.append(dataPoint["energy"])
            yc1.append(dataPoint["raport"])
        elif dataPoint["width"] == 2:
            xc2.append(dataPoint["energy"])
            yc2.append(dataPoint["raport"])
    elif dataPoint["material"]=="LYSO":
        if dataPoint["width"] == 0.5:
            xl05.append(dataPoint["energy"])
            yl05.append(dataPoint["raport"])
        elif dataPoint["width"] == 1:
            xl1.append(dataPoint["energy"])
            yl1.append(dataPoint["raport"])
        elif dataPoint["width"] == 2:
            xl2.append(dataPoint["energy"])
            yl2.append(dataPoint["raport"])
    elif dataPoint["material"]=="BGO":
        if dataPoint["width"] == 0.5:
            xb05.append(dataPoint["energy"])
            yb05.append(dataPoint["raport"])
        elif dataPoint["width"] == 1:
            xb1.append(dataPoint["energy"])
            yb1.append(dataPoint["raport"])
        elif dataPoint["width"] == 2:
            xb2.append(dataPoint["energy"])
            yb2.append(dataPoint["raport"])

plt.figure(1)
plt.plot(xc05, yc05, color = colors_materials["CSI"], label = "CsI 0.5 mm", marker = markers_width["0.5"])
plt.plot(xc1, yc1, color = colors_materials["CSI"], label = "CsI 1 mm", marker = markers_width["1.0"])
plt.plot(xc2, yc2, color = colors_materials["CSI"], label = "CsI 2 mm", marker = markers_width["2.0"])
plt.plot(xl05, yl05, color = colors_materials["LYSO"], label = "LYSO 0.5 mm", marker = markers_width["0.5"])
plt.plot(xl1, yl1, color = colors_materials["LYSO"], label = "LYSO 1 mm", marker = markers_width["1.0"])
plt.plot(xl2, yl2, color = colors_materials["LYSO"], label = "LYSO 2 mm", marker = markers_width["2.0"])
plt.plot(xb05, yb05, color = colors_materials["BGO"], label = "BGO 0.5 mm", marker = markers_width["0.5"])
plt.plot(xb1, yb1, color = colors_materials["BGO"], label = "BGO 1 mm", marker = markers_width["1.0"])
plt.plot(xb2, yb2, color = colors_materials["BGO"], label = "BGO 2 mm", marker = markers_width["2.0"])
plt.xlabel('Energy (MeV)')
plt.ylabel("Ratio (%)")
plt.title("Deposited energy in FWTM zone")
plt.xlim([-0.5,10.5])
plt.legend()

########

xc05 = []
xc1 = []
xc2 = []
yc05 = []
yc1 = []
yc2 = []

xb05 = []
xb1 = []
xb2 = []
yb05 = []
yb1 = []
yb2 = []

xl05 = []
xl1 = []
xl2 = []
yl05 = []
yl1 = []
yl2 = []

for dataPoint in data:
    if dataPoint["material"]=="CsI":
        if dataPoint["width"] == 0.5:
            xc05.append(dataPoint["energy"])
            yc05.append(dataPoint["total_opt_yield"])
        elif dataPoint["width"] == 1:
            xc1.append(dataPoint["energy"])
            yc1.append(dataPoint["total_opt_yield"])
        elif dataPoint["width"] == 2:
            xc2.append(dataPoint["energy"])
            yc2.append(dataPoint["total_opt_yield"])
    elif dataPoint["material"]=="LYSO":
        if dataPoint["width"] == 0.5:
            xl05.append(dataPoint["energy"])
            yl05.append(dataPoint["total_opt_yield"])
        elif dataPoint["width"] == 1:
            xl1.append(dataPoint["energy"])
            yl1.append(dataPoint["total_opt_yield"])
        elif dataPoint["width"] == 2:
            xl2.append(dataPoint["energy"])
            yl2.append(dataPoint["total_opt_yield"])
    elif dataPoint["material"]=="BGO":
        if dataPoint["width"] == 0.5:
            xb05.append(dataPoint["energy"])
            yb05.append(dataPoint["total_opt_yield"])
        elif dataPoint["width"] == 1:
            xb1.append(dataPoint["energy"])
            yb1.append(dataPoint["total_opt_yield"])
        elif dataPoint["width"] == 2:
            xb2.append(dataPoint["energy"])
            yb2.append(dataPoint["total_opt_yield"])

plt.figure(2)
plt.plot(xc05, yc05, color = colors_materials["CSI"], label = "CsI 0.5 mm", marker = markers_width["0.5"])
plt.plot(xc1, yc1, color = colors_materials["CSI"], label = "CsI 1 mm", marker = markers_width["1.0"])
plt.plot(xc2, yc2, color = colors_materials["CSI"], label = "CsI 2 mm", marker = markers_width["2.0"])
plt.plot(xl05, yl05, color = colors_materials["LYSO"], label = "LYSO 0.5 mm", marker = markers_width["0.5"])
plt.plot(xl1, yl1, color = colors_materials["LYSO"], label = "LYSO 1 mm", marker = markers_width["1.0"])
plt.plot(xl2, yl2, color = colors_materials["LYSO"], label = "LYSO 2 mm", marker = markers_width["2.0"])
plt.plot(xb05, yb05, color = colors_materials["BGO"], label = "BGO 0.5 mm", marker = markers_width["0.5"])
plt.plot(xb1, yb1, color = colors_materials["BGO"], label = "BGO 1 mm", marker = markers_width["1.0"])
plt.plot(xb2, yb2, color = colors_materials["BGO"], label = "BGO 2 mm", marker = markers_width["2.0"])
plt.xlabel('Energy (MeV)')
plt.ylabel("Total number of scintillations")
plt.title("Optical yield as function of energy for " + r"$10^7$" + "incident photons")
plt.xlim([-0.5,10.5])
plt.ylim(bottom=0)
plt.legend(loc='upper left')
plt.show()