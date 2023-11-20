import ROOT


def calculate_fwhm(histogram):

    halfmax = histogram.GetMaximum() / 2.0
    nbins = histogram.GetNbinsX()
    
    leftBin = histogram.GetXaxis().FindBin(histogram.GetBinCenter(1))
    rightBin = histogram.GetXaxis().FindBin(histogram.GetBinCenter(nbins))

    for i in range(1, nbins + 1):
        if histogram.GetBinContent(i) >= halfmax:
            leftBin = i
            break

    for i in range(nbins, 0, -1):
        if histogram.GetBinContent(i) >= halfmax:
            rightBin = i
            break

    fwhm = histogram.GetXaxis().GetBinCenter(rightBin) - histogram.GetXaxis().GetBinCenter(leftBin)
    return fwhm

file = ROOT.TFile("testem4.root", "READ")


histo = file.Get("Hist2D")


if histo:

    Xproj = histo.ProjectionX("XProjection")
    Yproj = histo.ProjectionY("YProjection")


    print("Max X projection:", Xproj.GetMaximum())
    print("Max Y projection:", Yproj.GetMaximum())

   # print("Contents of X projection:")
   #for i in range(1, Xproj.GetNbinsX() + 1):
   # 	print(f"Bin {i}: {Xproj.GetBinContent(i)}")

    c1 = ROOT.TCanvas("c1", "X Projection", 800, 600)
    Xproj.Draw()
    c1.SaveAs("XProjection.png")

    c2 = ROOT.TCanvas("c2", "Y Projection", 800, 600)
    Yproj.Draw()
    c2.SaveAs("YProjection.png")

    fwhm_x = calculate_fwhm(Xproj)
    print("FWHM_X :", fwhm_x)

    fwhm_y = calculate_fwhm(Yproj)
    print("FWHM_Y :", fwhm_y)

    file.Close()
else:
    print("Histogram not found.")
    
    
    '''
    half_maximum = histogram.GetMaximum() / 2.0
    bin1 = histogram.FindFirstBinAbove(half_maximum)
    bin2 = histogram.FindLastBinAbove(half_maximum)
    fwhm = histogram.GetBinCenter(bin2) - histogram.GetBinCenter(bin1)
     '''

