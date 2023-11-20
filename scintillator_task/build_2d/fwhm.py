import ROOT

# Open the ROOT file
root_file = ROOT.TFile("testem4.root", "READ")

# Access the 2D histogram
energy_deposition_map = root_file.Get("Hist2D")

# Check if the histogram exists
if energy_deposition_map:
    # Create X projection
    x_projection = energy_deposition_map.ProjectionX("XProjection")

    # Create Y projection
    y_projection = energy_deposition_map.ProjectionY("YProjection")

    # Plot the histograms
    c1 = ROOT.TCanvas("c1", "X Projection", 800, 600)
    x_projection.Draw()
    c1.SaveAs("XProjection.png")

    c2 = ROOT.TCanvas("c2", "Y Projection", 800, 600)
    y_projection.Draw()
    c2.SaveAs("YProjection.png")

    # Close the ROOT file
    root_file.Close()
else:
    print("Histogram not found in the ROOT file.")
