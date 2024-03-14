# calculeaza dimensiunea zonei in care se depune X % din depunerea totala de energie
# din centrul histogramei. bin cu bin (la stanga si la dreapta) cauta pana cand
# suma BinContent(i) este egala cu X % din eDep

import numpy as np
import matplotlib.pyplot as plt
import os
import json
from ROOT import TFile
from operator import itemgetter

X = 90 # percentage

def calcEdep(hist, left, right):
    sum = 0
    for i in range(left, right + 1):
        sum +=hist.GetBinContent(i)
    return sum

def findDim(hist):
    nbins = hist.GetNbinsX()
    binmax = hist.GetMaximumBin()
    # max = hist.GetXaxis().GetBinCenter(binmax)
    leftBin = binmax
    rightBin = binmax + 1
    eDep = calcEdep(hist, 1, nbins +1)
    check = True
    while check:
        sum = calcEdep(hist, leftBin, rightBin)
        if  sum >= X/100 * eDep:
            dim = hist.GetXaxis().GetBinCenter(rightBin) - hist.GetXaxis().GetBinCenter(leftBin)
            check = False
        else:
            leftBin -= 1
            rightBin +=1
    return dim, sum, eDep

def getDataFromFiles(config):

    data = {}

    data["material"] = config["material"]
    data["energy"] = config["energy"]
    data["width"] = 2*config["thickness"]
    data["dimX"] = dim
    data["enerX"] = sum
    data["eDep"] = eDep
    data["raport"] = sum/eDep*100

    return data

data = []

cwd = os.getcwd()
count = 0
for root, dirs, files in os.walk(cwd):
     for dir in dirs:
            # print("folderul curent este "+ dir)
            os.chdir(dir)
            count+=1
            file = TFile("testem4.root", "READ")
            configFile = open("config.json", "r")
            config = json.load(configFile)
            histo = file.Get("eDep2D")
            Xproj = histo.ProjectionX("XProjection")
            dim, sum, eDep = findDim(Xproj)
            file.Close()
            data.append(getDataFromFiles(config))
            os.chdir(cwd)

data = sorted(data, key=itemgetter("material", "energy", "width"))

output_file = open("results_{}ener.txt".format(X), "w")

output_file.write(
    "Mat\tE (MeV)\tWidth\tDimX\tEnerX\teDep\traport\n"
)

for dataPoint in data:
    output_file.write(dataPoint["material"])
    output_file.write("\t")
    output_file.write(str(dataPoint["energy"]))
    output_file.write("\t")
    output_file.write(str(dataPoint["width"]))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["dimX"], 4)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["enerX"], 4)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["eDep"], 4)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["raport"], 4)))
    output_file.write("\n")

output_file.close()

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
            yc05.append(dataPoint["dimX"])
        elif dataPoint["width"] == 1:
            xc1.append(dataPoint["energy"])
            yc1.append(dataPoint["dimX"])
        elif dataPoint["width"] == 2:
            xc2.append(dataPoint["energy"])
            yc2.append(dataPoint["dimX"])
    elif dataPoint["material"]=="LYSO":
        if dataPoint["width"] == 0.5:
            xl05.append(dataPoint["energy"])
            yl05.append(dataPoint["dimX"])
        elif dataPoint["width"] == 1:
            xl1.append(dataPoint["energy"])
            yl1.append(dataPoint["dimX"])
        elif dataPoint["width"] == 2:
            xl2.append(dataPoint["energy"])
            yl2.append(dataPoint["dimX"])
    elif dataPoint["material"]=="BGO":
        if dataPoint["width"] == 0.5:
            xb05.append(dataPoint["energy"])
            yb05.append(dataPoint["dimX"])
        elif dataPoint["width"] == 1:
            xb1.append(dataPoint["energy"])
            yb1.append(dataPoint["dimX"])
        elif dataPoint["width"] == 2:
            xb2.append(dataPoint["energy"])
            yb2.append(dataPoint["dimX"])

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
plt.ylabel("Dimension of the region (mm)")
plt.title("Size of the region where {} % of the energy is deposited".format(X))
plt.ylim(bottom = 0)
plt.xlim([-0.5,10.5])
plt.legend()
plt.savefig("plot_{}ener.pdf".format(X))
plt.show()