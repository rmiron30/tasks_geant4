# calculeaza dimensiunea zonei in care se depune X % din depunerea totala de energie
# din centrul histogramei. bin cu bin (la stanga si la dreapta) cauta pana cand
# suma BinContent(i) este egala cu X % din eDep

import numpy as np
import matplotlib.pyplot as plt
import os
import json
from ROOT import TFile

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
    return dim, sum

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
            print(findDim(Xproj), calcEdep(Xproj,1, Xproj.GetNbinsX()+1), dir)
            if count == 10:
                break
            os.chdir(cwd)