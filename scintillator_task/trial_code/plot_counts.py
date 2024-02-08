# plot counts versus energy for 1D histogram

import numpy as np
import matplotlib.pyplot as plt
import os
from ROOT import TFile

# get the current working directory
cwd = os.getcwd()
print("Current working directory: {0}".format(cwd))

# get the path to the data file in all he folders from the cwd
data_file_paths = []
for root, dirs, files in os.walk(cwd):
    for file in files:
        if file.endswith("root"):
            data_file_paths.append(os.path.join(root, file))

# print the paths to the data files
print("Data file paths:")
for path in data_file_paths:
    print(path)

# get the energies from the config.json in each folder
energies = []



