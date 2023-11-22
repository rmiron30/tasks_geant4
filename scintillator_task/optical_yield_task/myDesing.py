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
colors_energy = {'0.1': "blue", '0.5':"green", '1.0':"red", '3.0':"purple", '5.0':"orange", '10.0':"lawngreen"}

#x_values = []
#y_values = []
'''
def functionPlot(data, material, width):
    x_val = []
    y_val = []
    for dataPoint in data:
        if dataPoint["material"] == f"{material}":
            if dataPoint["width"] == f"{width}":
                x_val.append(dataPoint["energy"])
                y_val.append(dataPoint["opt_yield"])
    return x_val, y_val
material = "CSI"
width = 0.5
x_values, y_values = functionPlot(data, material, width)
plt.scatter(x_values, y_values)
plt.show()
'''

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
