from ROOT import TFile, gPad
import glob
import numpy as np
import pandas as pd
from operator import itemgetter
import matplotlib.pyplot as plt

yields = {"CSI": 54, "BGO": 8, "LYSO": 40} #photons/kev

output_file = open("output2.txt", "w")


def extractFromHistogram(filename):
    tFile = TFile(filename)

    hist = tFile.Get("1")

    eDep = 0

    for i in range(1, hist.GetNbinsX() + 1):
        eDep += hist.GetBinCenter(i) * hist.GetBinContent(i)

    entries = hist.GetEntries()

    tFile.Close()

    return eDep, entries


def extractFromRoot(file):
    rootFile = file
    file = file.split("/")[-1][:-5]

    file = file.split("_")

    dataPoint = {"material": file[0], "energy": float(file[1]), "width": float(file[2])}

    eDep, entries = extractFromHistogram(rootFile)

    dataPoint["eDep"] = eDep
    dataPoint["entries"] = entries
    dataPoint["eDepPart"] = eDep/entries

    return dataPoint


def extractAttenuationCoefficients(filename):
    excel_file = "linear_coeffs.xlsx"

    data_frame = pd.read_excel(excel_file)

    excel_dict = {}
    for row in data_frame.itertuples(index=False):
        material, energy, mu = row
        if material not in excel_dict:
            excel_dict[material] = {}
        excel_dict[material][energy] = mu

    return excel_dict


output_file.write(
    "Mat\tEnergy (MeV)\tWidth\tEntries\t \t DepEner (MeV)\t DepEnerPart (MeV/part) \t N comp \t scintills \t total scintills\n"
)


def getDataFromFiles(filePath, att):
    files = glob.glob(filePath)

    i_zero = 10**6

    data = []

    for file in files:
        dataPoint = extractFromRoot(file)

        mu = att[dataPoint["material"]][dataPoint["energy"]]

        dataPoint["i_final"] = i_zero * (1 - np.exp(-mu * dataPoint["width"] / 10))

        dataPoint["opt_yield"] = yields[dataPoint["material"]] * dataPoint["eDepPart"] * 1000

        dataPoint["total_opt_yield"] = yields[dataPoint["material"]] * dataPoint["eDep"] * 1000

        data.append(dataPoint)

    return data


att = extractAttenuationCoefficients("linear_coeffs.xlsx")

data = getDataFromFiles("data/*", att)


data = sorted(data, key=itemgetter("material", "energy", "width"))


for dataPoint in data:
    output_file.write(dataPoint["material"])
    output_file.write("\t")
    output_file.write(str(dataPoint["energy"]))
    output_file.write("\t")
    output_file.write(str(dataPoint["width"]))
    output_file.write("\t")
    output_file.write(str(dataPoint["entries"]))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["eDep"], 3)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["eDepPart"], 3)))
    output_file.write("\t")
    output_file.write(str(np.round(dataPoint["i_final"], 3)))
    output_file.write("\t")
    output_file.write(str(dataPoint["opt_yield"]))
    output_file.write("\t")
    output_file.write(str(dataPoint["total_opt_yield"]))
    output_file.write("\n")

output_file.close()

colors_width = {'0.5': "blue", '1.0': "green", '2.0': "red"}
colors_materials = {'CSI': "blue", 'BGO': "green", 'LYSO': "red"}
markers_width = {'0.5': "o", '1.0': "v", '2.0': "s"}
markers_materials = {'CSI': "o", 'BGO': "v", 'LYSO': "s"}
colors_energy = {'0.1': "blue", '0.5':"green", '1.0':"red", '3.0':"purple", '5.0':"orange", '10.0':"lawngreen"}

#x_values = []
#y_values = []

# def functionPlot(data, material, width):
#     x_val = []
#     y_val = []
#     for dataPoint in data:
#         if dataPoint["material"] == f"{material}":
#             if dataPoint["width"] == f"{width}":
#                 x_val.append(dataPoint["energy"])
#                 y_val.append(dataPoint["opt_yield"])
#     return np.array(x_val), np.array(y_val)
# material = "CSI"
# width = 0.5
# x_values, y_values = functionPlot(data, material, width)
# plt.scatter(x_values, y_values)
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
    if dataPoint["material"]=="CSI":
        if dataPoint["width"] == 0.5:
            xc05.append(dataPoint["energy"])
            yc05.append(dataPoint["eDepPart"])
        elif dataPoint["width"] == 1:
            xc1.append(dataPoint["energy"])
            yc1.append(dataPoint["eDepPart"])
        elif dataPoint["width"] == 2:
            xc2.append(dataPoint["energy"])
            yc2.append(dataPoint["eDepPart"])
    elif dataPoint["material"]=="LYSO":
        if dataPoint["width"] == 0.5:
            xl05.append(dataPoint["energy"])
            yl05.append(dataPoint["eDepPart"])
        elif dataPoint["width"] == 1:
            xl1.append(dataPoint["energy"])
            yl1.append(dataPoint["eDepPart"])
        elif dataPoint["width"] == 2:
            xl2.append(dataPoint["energy"])
            yl2.append(dataPoint["eDepPart"])
    elif dataPoint["material"]=="BGO":
        if dataPoint["width"] == 0.5:
            xb05.append(dataPoint["energy"])
            yb05.append(dataPoint["eDepPart"])
        elif dataPoint["width"] == 1:
            xb1.append(dataPoint["energy"])
            yb1.append(dataPoint["eDepPart"])
        elif dataPoint["width"] == 2:
            xb2.append(dataPoint["energy"])
            yb2.append(dataPoint["eDepPart"])

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
plt.ylabel("Deposited energy per interacting photon (MeV/part)")
plt.title("Deposited energy per interacting photons as function of energy for " + r"$10^6$" + "incident photons")
plt.xlim([-0.5,10.5])
plt.legend()
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
    if dataPoint["material"]=="CSI":
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
plt.title("Optical yield as function of energy for " + r"$10^6$" + "incident photons")
plt.xlim([-0.5,10.5])
plt.legend(loc='upper left')
# plt.show()

plt.figure(3)
for dataPoint in data:
    if dataPoint["material"]=="CSI":
        plt.plot(dataPoint["energy"], dataPoint["opt_yield"], label = f'{dataPoint["width"]} mm', linestyle ='-', linewidth = 2, marker = 'o', color = colors_width[str(dataPoint["width"])])

#plt.legend()
def legend_without_duplicate_labels(figure):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    figure.legend(by_label.values(), by_label.keys(), loc='upper left')
legend_without_duplicate_labels(plt)
plt.xlabel("Energy (MeV)")
plt.ylabel("Number of scintillations")
plt.title("Optical yield as function of energy for CsI(Tl) (y=54 ph/keV)")
'''
for dataPoint in data:
    if dataPoint["material"]=="CSI":
        plt.scatter(dataPoint["width"], dataPoint["opt_yield"], label = f'{dataPoint["energy"]} MeV', color = colors_energy[str(dataPoint["energy"])])

#plt.legend()
def legend_without_duplicate_labels(figure):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    figure.legend(by_label.values(), by_label.keys(), loc='upper left')
legend_without_duplicate_labels(plt)
plt.xlabel("Width (mm)")
plt.ylabel("Number of scintillations")
plt.title("Optical yield as function of scintillator width for CsI(Tl)")
'''
plt.show()
