#
#template_fit_py/template_fit/template_fit.py
#
"""
Main program to run the analysis: uses processed Monte Carlo distributions as templates (PDFs)
to be fit to the data distribution. Each template corresponds to a jet flavor (bottom, charm,
light). x-axis values are output weights from the MV1c algorithm.

Program iterates through values of the Z boson pT to perform momentum-binned fits

"""
import numpy as np
import matplotlib.pyplot as plt
import scipy
from ROOT import TFile, TH1D, TH2D
from root_numpy import hist2array
import os

import sys
sys.path.append("/Users/kristinalooper/WorkArea/template_fit_py/template_fit")

from run_fit import run_fit

dirname = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dirname)

#Paths to data directories
data_dir = os.path.join(dirname, '../data/data_histograms/')
mc_dir   = os.path.join(dirname, '../data/MC_histograms/')

#Names of MC files
light_n  =  'Z_ptmv1c_light_jets_hmatch_leadjet'
charm_n  = 'Z_ptmv1c_charm_jets_hmatch_leadjet'
bottom_n = 'Z_ptmv1c_bottom_jets_hmatch_leadjet'

light_fn  = mc_dir+light_n+'.root'
charm_fn  = mc_dir+charm_n+'.root'
bottom_fn = mc_dir+bottom_n+'.root'

#Names of data files
data_fn = data_dir+'alldata.root'
data_hname = 'mv1cweight_ptbinned_leadjet'

#Open ROOT files
flight  = TFile.Open(light_fn,"READ")
fcharm  = TFile.Open(charm_fn,"READ")
fbottom = TFile.Open(bottom_fn,"READ")
fdata   = TFile.Open(data_fn,"READ")

#Fetch ROOT histograms
#2D histograms, MV1c template value on X axis, Z momentum on Y axis
hlight_2D  = flight.Get(light_n+'_mc')
hcharm_2D  = fcharm.Get(charm_n+'_mc')
hbottom_2D = fbottom.Get(bottom_n+'_mc')
hdata_2D   = fdata.Get(data_hname)

#Convert ROOT histogram to numpy arrays
#hist2array returns tuple, first element has arrays of hist. values, 2nd has list of arrays of bin edges
hlight_numpy2D  = hist2array(hlight_2D,return_edges=True)
hcharm_numpy2D  = hist2array(hcharm_2D,return_edges=True)
hbottom_numpy2D = hist2array(hbottom_2D,return_edges=True)
hdata_numpy2D   = hist2array(hdata_2D,return_edges=True)

#loop over Z momenta (pT)
#for pt_bin in range(1,len(hlight_numpy2D[1][1])-1):
#use 1-5 as a subsample for interview
for pt_bin in range(1,6):
    light_h = (hlight_numpy2D[0][:,pt_bin],hlight_numpy2D[1][0]) #Tuple with (bin_content,bin_edges)
    charm_h = (hcharm_numpy2D[0][:,pt_bin],hcharm_numpy2D[1][0])
    bottom_h =(hbottom_numpy2D[0][:,pt_bin],hbottom_numpy2D[1][0])
    data_h = (hdata_numpy2D[0][:,pt_bin],hdata_numpy2D[1][0])
    run_fit(bottom_h,charm_h,light_h,data_h) #performs least squares fit of data to sum of templates, returns [b_frac,c_frac]
