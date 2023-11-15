import ROOT
import os
import pandas as pd

# Specify the directory where your ROOT files are located
root_files_directory = '/home/raluca/geant4/tasks_geant4/scintillator_task/analysis'

# Create a text file
output_file = open("output.txt", "w")

# Write the header
output_file.write("Material\tEnergy (MeV)\tWidth\tEntries\tDeposited Energy (MeV)\n")

# Initialize a list to store the data
data = []

# Loop through the files in the directory
for filename in os.listdir(root_files_directory):
    if filename.endswith(".root"):
        # Split the filename to extract MATERIAL, ENERGY, and WIDTH
        parts = filename.split('_')
        if len(parts) == 3:
            material = parts[0]
            energy = float(parts[1])
            width = parts[2].split('.root')[0]  # Remove the '.root' extension

            # Open the ROOT file
            file_path = os.path.join(root_files_directory, filename)
            root_file = ROOT.TFile(file_path, 'READ')

            if root_file.IsOpen():
                # Access the histogram from the ROOT file
                hist = root_file.Get("1")

                x_values = []
                y_values = []
                E = 0

                for i in range(1, hist.GetNbinsX() + 1):
                    x_values.append(hist.GetBinCenter(i))
                    y_values.append(hist.GetBinContent(i))

                for i in range(len(x_values)):
                    E += x_values[i] * y_values[i]

                #print(f"File: {filename}")
                #print(E, "MeV")
                #print(hist.GetEntries())
                
                # Write the data to the text file
               # output_file.write(f"{material}\t{energy}\t{width}\t{hist.GetEntries()}\t{E/1000000} \n")
                # Append the data to the list
                data.append((material, energy, width, hist.GetEntries(), E/1000000))


                # Don't forget to close the file when you're done
                root_file.Close()

            else:
                print(f"Failed to open: {filename}")

print(float(data[0][1]))
                
                # Sort the data by material, energy, and thickness
sorted_data = sorted(data, key=lambda x: (x[0], float(x[1]), float(x[2])))

# Write the sorted data to the text file
for item in sorted_data:
    output_file.write(f"{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}\t{item[4]} \n")
    

excel_file = 'linear_coeffs.xlsx'

# Read the Excel file
data_frame = pd.read_excel(excel_file_path)

# Convert the DataFrame to a dictionary
excel_data_dict = {}
for row in data_frame.itertuples(index=False):
    material, energy, mu = row
    if material not in excel_data_dict:
        excel_data_dict[material] = {}
    excel_data_dict[material][energy] = mu

# Print the dictionary
print(excel_data_dict)

# Close the output file
output_file.close()

# Make sure to close any open ROOT sessions
ROOT.gROOT.Reset()

