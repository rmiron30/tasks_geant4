from numpy import loadtxt

from lmfit.models import LinearModel, LorentzianModel

# peak = LorentzianModel()
# background = LinearModel()
# model = peak+background

# print(model)

data = loadtxt('test_peak.dat')
x=data[:,0]
y=data[:,1]

mod = LorentzianModel()

pars =  mod.guess(y, x=x)
out = mod.fit(y, pars, x=x)

print(out.fit_report(min_correl=0.25))