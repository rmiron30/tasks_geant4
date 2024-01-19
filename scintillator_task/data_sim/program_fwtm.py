# a program which calculates FWHM and FWTM of the X projection of a 2D histogram 
# from all ROOT files generated by the simulation
# the folders are named with the date and time when they were created
# output file: material, energy, thickness, FWHM, FWTM

from ROOT import TFile
import os
import numpy as np
import json
from operator import itemgetter
import matplotlib.pyplot as plt

output_file = open("output.txt", "w")

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

    fwhm = hist.GetXaxis().GetBinCenter(rightBin) - hist.GetXaxis().GetBinCenter(leftBin)
    return fwhm

def CalculateFwtm(hist):
    tenthmax = hist.GetMaximum() / 10.0
    nbins = hist.GetNbinsX()
    
    leftBin = hist.GetXaxis().FindBin(hist.GetBinCenter(1))
    rightBin = hist.GetXaxis().FindBin(hist.GetBinCenter(nbins))

    for i in range(1, nbins + 1):
        if hist.GetBinContent(i) >= tenthmax:
            leftBin = i
            break

    for i in range(nbins, 0, -1):
        if hist.GetBinContent(i) >= tenthmax:
            rightBin = i
            break

    fwtm = hist.GetXaxis().GetBinCenter(rightBin) - hist.GetXaxis().GetBinCenter(leftBin)
    return fwtm 

def getDataFromFiles(config):

    data = {}

    data["material"] = config["material"]
    data["energy"] = config["energy"]
    data["thickness"] = config["thickness"]
    data["fwhm"] = fwhm_x
    data["fwtm"] = fwtm_x

    return data


data = []

cwd = os.getcwd()
count = 0 # daca a trecut prin toate folderele
for root, dirs, files in os.walk(cwd):
     for dir in dirs:
            # print("folderul curent este "+ dir)
            count += 1
            os.chdir(dir)
            file = TFile("testem4.root", "READ")
            configFile = open("config.json", "r")
            config = json.load(configFile)
            histo = file.Get("eDep2D")
            if histo:
                if config["material"] == "CsI" and config["thickness"] == 1 and config["energy"] == 5:
                    print("folderul CsI 1 mm 5 MeV este "+ dir)
                Xproj = histo.ProjectionX("XProjection")
                # Yproj = histo.ProjectionY("YProjection")
                fwhm_x = CalculateFwhm(Xproj)
                fwtm_x = CalculateFwtm(Xproj)
                # fwhm_y = calculate_fwhm(Yproj)
                # fwtm_y = calculate_fwtm(Yproj)
                # print("FWHM_X :", fwhm_x)
                # print("FWTM_X :", fwtm_x)
                # print("FWHM_Y :", fwhm_y)
                # print("FWTM_Y :", fwtm_y)
                file.Close()
            else:
                print("histogram not found.")
            data.append(getDataFromFiles(config))
            os.chdir(cwd)
data = sorted(data, key=itemgetter("material", "energy", "thickness"))

output_file.write(
    "Mat\tE (MeV)\tWidth\tFWHM\t FWTM \n"
)

for dataPoint in data:
    output_file.write(dataPoint["material"])
    output_file.write("\t")
    output_file.write(str(dataPoint["energy"]))
    output_file.write("\t\t")
    output_file.write(str(dataPoint["thickness"]))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["fwhm"], 3)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["fwtm"], 3)))
    output_file.write("\n")
# json.dump(data, output_file, indent=4)

output_file.close()
print("S-au parcurs "+ str(count) + " foldere.")


########## grafice

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
        if dataPoint["thickness"] == 0.5:
            xc05.append(dataPoint["energy"])
            yc05.append(dataPoint["fwtm"])
        elif dataPoint["thickness"] == 1:
            xc1.append(dataPoint["energy"])
            yc1.append(dataPoint["fwtm"])
        elif dataPoint["thickness"] == 2:
            xc2.append(dataPoint["energy"])
            yc2.append(dataPoint["fwtm"])
    elif dataPoint["material"]=="LYSO":
        if dataPoint["thickness"] == 0.5:
            xl05.append(dataPoint["energy"])
            yl05.append(dataPoint["fwtm"])
        elif dataPoint["thickness"] == 1:
            xl1.append(dataPoint["energy"])
            yl1.append(dataPoint["fwtm"])
        elif dataPoint["thickness"] == 2:
            xl2.append(dataPoint["energy"])
            yl2.append(dataPoint["fwtm"])
    elif dataPoint["material"]=="BGO":
        if dataPoint["thickness"] == 0.5:
            xb05.append(dataPoint["energy"])
            yb05.append(dataPoint["fwtm"])
        elif dataPoint["thickness"] == 1:
            xb1.append(dataPoint["energy"])
            yb1.append(dataPoint["fwtm"])
        elif dataPoint["thickness"] == 2:
            xb2.append(dataPoint["energy"])
            yb2.append(dataPoint["fwtm"])
            
colors_materials = {'CSI': "blue", 'BGO': "green", 'LYSO': "red"}
markers_thickness = {'0.5': "o", '1.0': "v", '2.0': "s"}

plt.figure(1)
plt.plot(xc05, yc05, color = colors_materials["CSI"], label = "CsI 0.5 mm", marker = markers_thickness["0.5"])
plt.plot(xc1, yc1, color = colors_materials["CSI"], label = "CsI 1 mm", marker = markers_thickness["1.0"])
plt.plot(xc2, yc2, color = colors_materials["CSI"], label = "CsI 2 mm", marker = markers_thickness["2.0"])
plt.plot(xl05, yl05, color = colors_materials["LYSO"], label = "LYSO 0.5 mm", marker = markers_thickness["0.5"])
plt.plot(xl1, yl1, color = colors_materials["LYSO"], label = "LYSO 1 mm", marker = markers_thickness["1.0"])
plt.plot(xl2, yl2, color = colors_materials["LYSO"], label = "LYSO 2 mm", marker = markers_thickness["2.0"])
plt.plot(xb05, yb05, color = colors_materials["BGO"], label = "BGO 0.5 mm", marker = markers_thickness["0.5"])
plt.plot(xb1, yb1, color = colors_materials["BGO"], label = "BGO 1 mm", marker = markers_thickness["1.0"])
plt.plot(xb2, yb2, color = colors_materials["BGO"], label = "BGO 2 mm", marker = markers_thickness["2.0"])
plt.xlabel('Energy (MeV)')
plt.ylabel("FWTM")
plt.title("FWTM as function of energy")
plt.xlim([-0.5,10.5])
plt.legend()
plt.savefig("FWTM_all.pdf")
# plt.show()

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
        if dataPoint["thickness"] == 0.5:
            xc05.append(dataPoint["energy"])
            yc05.append(dataPoint["fwhm"])
        elif dataPoint["thickness"] == 1:
            xc1.append(dataPoint["energy"])
            yc1.append(dataPoint["fwhm"])
        elif dataPoint["thickness"] == 2:
            xc2.append(dataPoint["energy"])
            yc2.append(dataPoint["fwhm"])
    elif dataPoint["material"]=="LYSO":
        if dataPoint["thickness"] == 0.5:
            xl05.append(dataPoint["energy"])
            yl05.append(dataPoint["fwhm"])
        elif dataPoint["thickness"] == 1:
            xl1.append(dataPoint["energy"])
            yl1.append(dataPoint["fwhm"])
        elif dataPoint["thickness"] == 2:
            xl2.append(dataPoint["energy"])
            yl2.append(dataPoint["fwhm"])
    elif dataPoint["material"]=="BGO":
        if dataPoint["thickness"] == 0.5:
            xb05.append(dataPoint["energy"])
            yb05.append(dataPoint["fwhm"])
        elif dataPoint["thickness"] == 1:
            xb1.append(dataPoint["energy"])
            yb1.append(dataPoint["fwhm"])
        elif dataPoint["thickness"] == 2:
            xb2.append(dataPoint["energy"])
            yb2.append(dataPoint["fwhm"])

plt.figure(2)
plt.plot(xc05, yc05, color = colors_materials["CSI"], label = "CsI 0.5 mm", marker = markers_thickness["0.5"])
plt.plot(xc1, yc1, color = colors_materials["CSI"], label = "CsI 1 mm", marker = markers_thickness["1.0"])
plt.plot(xc2, yc2, color = colors_materials["CSI"], label = "CsI 2 mm", marker = markers_thickness["2.0"])
plt.plot(xl05, yl05, color = colors_materials["LYSO"], label = "LYSO 0.5 mm", marker = markers_thickness["0.5"])
plt.plot(xl1, yl1, color = colors_materials["LYSO"], label = "LYSO 1 mm", marker = markers_thickness["1.0"])
plt.plot(xl2, yl2, color = colors_materials["LYSO"], label = "LYSO 2 mm", marker = markers_thickness["2.0"])
plt.plot(xb05, yb05, color = colors_materials["BGO"], label = "BGO 0.5 mm", marker = markers_thickness["0.5"])
plt.plot(xb1, yb1, color = colors_materials["BGO"], label = "BGO 1 mm", marker = markers_thickness["1.0"])
plt.plot(xb2, yb2, color = colors_materials["BGO"], label = "BGO 2 mm", marker = markers_thickness["2.0"])
plt.xlabel('Energy (MeV)')
plt.ylabel("FWHM")
plt.title("FWHM as function of energy")
plt.xlim([-0.5,10.5])
plt.legend(loc='upper left')
plt.savefig("FWHM_all.pdf")
# plt.show()



plt.show()

         
            