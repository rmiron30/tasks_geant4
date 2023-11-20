from ROOT import TFile, gPad


file = TFile("testem4.root")

hist2 = file.Get("Hist2D")

hist1d = file.Get("Hist")



# print(hist.GetNbinsX())

hist = hist2.ProjectionX()


def getEdep(hist):

    x_values = []
    y_values = []
    E = 0
    total_energy=0.0
    for i in range(1, hist.GetNbinsX() + 1):

        #energy_bin = hist.GetBinCenter(i)
        #counts = hist.GetBinContent(i)
        #total_energy += energy_bin * counts
        x_values.append(hist.GetBinCenter(i))
        y_values.append(hist.GetBinContent(i))
        
    for i in range(len(x_values)):
        E+=x_values[i]*y_values[i]

    #total_energy=hist.Integral()

    '''
    print("X values:")
    print(x_values)

    print("Y values:")
    print(y_values)
    '''
    print(E, "MeV", hist.GetEntries())

    #hist.Draw("hist")

    #gPad.WaitPrimitive("ggg")


getEdep(hist)
getEdep(hist1d)
