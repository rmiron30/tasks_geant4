from ROOT import TFile
import os
import numpy as np
import json
from operator import itemgetter
import matplotlib.pyplot as plt

def CalculateTwenty(hist):
    tenthmax = hist.GetMaximum() / 20.0
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

    for i in range(leftBin, rightBin +1):
        sum+=hist.GetBinContent(i)

    return hist.GetXaxis().GetBinCenter(leftBin), hist.GetXaxis().GetBinCenter(rightBin), tenthmax, fwtm, sum

def getDataFromFiles(config):

    data = {}

    data["material"] = config["material"]
    data["energy"] = config["energy"]
    data["width"] = 2*config["thickness"]
    data["fwtm"] = fwtm
    data["eDep"] = eDep
    data["eTwenty"] = eTwenty
    data["raport"] = eTwenty/eDep*100

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
            entries = hist1D.GetEntries()
            
            if histo:
                Xproj = histo.ProjectionX("XProjection")
                x_values = [Xproj.GetBinCenter(i) for i in range(1, Xproj.GetNbinsX()+1)]
                y_values = [Xproj.GetBinContent(i) for i in range(1, Xproj.GetNbinsX()+1)]
                left, right, tenthmax, fwtm, eTwenty = CalculateTwenty(Xproj)
                eDep = 0
                for i in range(1, Xproj.GetNbinsX() + 1):
                    eDep += Xproj.GetBinContent(i)
                file.Close()
            data.append(getDataFromFiles(config))
            # if config["energy"] == 10 and config["material"] == "LYSO" and config["thickness"]*2 == 2:
            #     # left2, right2, tenthmax, fwtm, eTwenty = CalculateTwenty(Xproj)
            #     plt.figure(3)
            #     plt.plot(x_values, y_values, label = "{} MeV".format(config["energy"]), color = colors_energy[str(config["energy"])])
            #     plt.hlines(tenthmax, left, right, color = 'green', linestyle= 'solid' )
            #     plt.title("LYSO 2 mm")
            #     # plt.yscale("log")
            #     plt.xlim(-1,1)
            #     plt.xlabel("X [mm]")
            #     plt.ylabel("deposited energy")    
            #     plt.legend()
            #     print(dir)
            os.chdir(cwd)
data = sorted(data, key=itemgetter("material", "energy", "width"))

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
plt.title("Deposited energy in FW twenty max zone")
plt.ylim(bottom = 0)
plt.xlim([-0.5,10.5])
plt.savefig("dep_twenty.pdf")
plt.legend()

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
            yc05.append(dataPoint["fwtm"])
        elif dataPoint["width"] == 1:
            xc1.append(dataPoint["energy"])
            yc1.append(dataPoint["fwtm"])
        elif dataPoint["width"] == 2:
            xc2.append(dataPoint["energy"])
            yc2.append(dataPoint["fwtm"])
    elif dataPoint["material"]=="LYSO":
        if dataPoint["width"] == 0.5:
            xl05.append(dataPoint["energy"])
            yl05.append(dataPoint["fwtm"])
        elif dataPoint["width"] == 1:
            xl1.append(dataPoint["energy"])
            yl1.append(dataPoint["fwtm"])
        elif dataPoint["width"] == 2:
            xl2.append(dataPoint["energy"])
            yl2.append(dataPoint["fwtm"])
    elif dataPoint["material"]=="BGO":
        if dataPoint["width"] == 0.5:
            xb05.append(dataPoint["energy"])
            yb05.append(dataPoint["fwtm"])
        elif dataPoint["width"] == 1:
            xb1.append(dataPoint["energy"])
            yb1.append(dataPoint["fwtm"])
        elif dataPoint["width"] == 2:
            xb2.append(dataPoint["energy"])
            yb2.append(dataPoint["fwtm"])
            
colors_materials = {'CSI': "blue", 'BGO': "green", 'LYSO': "red"}
markers_thickness = {'0.5': "o", '1.0': "v", '2.0': "s"}

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
plt.ylabel("FW20M")
plt.title("FW20M as function of energy")
plt.xlim([-0.5,10.5])
plt.legend()
plt.savefig("FW20M_all.pdf")


plt.show()