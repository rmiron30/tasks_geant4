import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Assuming your data is in a file named 'your_data_file.txt'
# Adjust the file name accordingly
file_path = 'output2.txt'

# Read the data into a Pandas DataFrame
data = pd.read_csv(file_path, delimiter='\t')

materials = np.array(data.iloc[:,0])
energy = np.array(data.iloc[:,1])
eDepTot = np.array(data.iloc[:,4])
width = np.array(data.iloc[:,2])
total_scintills = np.array(data.iloc[:,8])
entries =  np.array(data.iloc[:,3])

incident_energy =[]
scintillations = []
# Loop through unique materials and plot DepEner vs Energy
for i in range(len(materials)):
    if materials[i] == 'BGO':
        plt.scatter(energy[i], total_scintills[i]/entries[i], label=materials[i], linestyle = '-')

def legend_without_duplicate_labels(figure):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    figure.legend(by_label.values(), by_label.keys(), loc='upper left')
legend_without_duplicate_labels(plt)

# Add labels and legend
plt.xlabel('Energy (MeV)')
plt.ylabel('Total scintillations')

# Show the plot
plt.show()