#! /usr/bin/env python3
import numpy as np
import os 
from  KinFit import kinfit_3pr, kinfit_3pr_3pr
import ROOT
from argparse import ArgumentParser

def fill_hist(hist, array):
    [hist.Fill(x) for x in array]

################
# Main routine #
################
parser = ArgumentParser()
parser.add_argument('-input','--input',dest='input',help='input file (ROOT or CSV)')
parser.add_argument('-channel','--channel',dest='channel',default='tt',choices=['mt','tt'])
parser.add_argument('-full_sv_cov','--full_sv_cov',dest='full_sv_cov',action='store_true')

args = parser.parse_args()

filename = args.input
full_sv_cov = args.full_sv_cov

print('')
if os.path.isfile:
    print('opening file %s'%(filename))
else:
    print('file %s is not found'%(filename))
    print('Choose files from the following folders:')
    print('1. /eos/cms/store/group/phys_tau/lrussell/forAliaksei/CPSignalStudies/Run3_2022EE/[mt,tt]')
    print('2. /eos/home-w/wmatyszk/HiggsDNA/CleanDNA/higgs-dna-waw/combine_test_run')
    
df = ROOT.RDataFrame("ntuple",filename)
cuts = 'os>0.5&&idDeepTau2018v2p5VSe_2>=6&&idDeepTau2018v2p5VSmu_2>=4&&idDeepTau2018v2p5VSjet_2>=7&&pt_2>20.&&fabs(eta_2)<2.5&&decayModePNet_2==10&&hasRefitSV_2'

cuts_a1a1 = cuts + '&&decayModePNet_1==10&&hasRefitSV_1'

if args.channel=='mt':
    cuts += '&&iso_1<0.10&&pt_1>26&&fabs(eta_1)<2.4'
if args.channel=='tt':
    cuts += '&&idDeepTau2018v2p5VSe_1>=6&&idDeepTau2018v2p5VSmu_1>=4&&idDeepTau2018v2p5VSjet_1>=7&&pt_1>40.&&pt_2>40.&&fabs(eta_1)<2.5'
    cuts_a1a1 += '&&idDeepTau2018v2p5VSe_1>=6&&idDeepTau2018v2p5VSmu_1>=4&&idDeepTau2018v2p5VSjet_1>=7&&pt_1>40.&&pt_2>40.&&fabs(eta_1)<2.5'
    
print('')
# get list of all branches in the tree
all_cols = [str(c) for c in df.GetColumnNames()]

print(f'Found {len(all_cols)} columns')

print('')
print('reading tuple as numpy columns')

cols = df.Filter(cuts).AsNumpy(all_cols)
cols_a1a1 = df.Filter(cuts_a1a1).AsNumpy(all_cols)

print('')
print('Length of column : %1i\n'%(len(cols["pt_1"])))
print('Running KinFit (be patient, it takes awhile)')

# steering parameters
full_sv_cov = args.full_sv_cov # use full covariance or only diagonal elements of covariance
mX = 125.10 # Higgs mass

svx_2_a1 = cols['sv_x_2']-cols['PVBS_x']
svy_2_a1 = cols['sv_y_2']-cols['PVBS_y']
svz_2_a1 = cols['sv_z_2']-cols['PVBS_z']

svx_1 = cols['sv_x_1']-cols['PVBS_x']
svy_1 = cols['sv_y_1']-cols['PVBS_y']
svz_1 = cols['sv_z_1']-cols['PVBS_z']

##########################
# Calling kinfit_3pr_3pr #
##########################
# Both taus to decay to a1 (see definition of cuts above!)
# order of taus doesn't matter
results_a1a1 = kinfit_3pr_3pr(cols_a1a1["pt_2"],cols_a1a1["eta_2"],cols_a1a1["phi_2"],cols_a1a1["mass_2"],
                              cols_a1a1["pt_1"],cols_a1a1["eta_1"],cols_a1a1["phi_1"],cols_a1a1["mass_1"],
                              cols_a1a1["met_pt"],cols_a1a1["met_phi"],
                              cols_a1a1["met_covXX"],cols_a1a1["met_covXY"],cols_a1a1["met_covYY"],
                              svx_2_a1a1,svy_2_a1a1,svz_2_a1a1,
                              cols_a1a1["sv_cov00_2"],cols_a1a1["sv_cov10_2"],cols_a1a1["sv_cov20_2"],
                              cols_a1a1["sv_cov11_2"],cols_a1a1["sv_cov21_2"],cols_a1a1["sv_cov22_2"],
                              svx_1_a1a1,svy_1_a1a1,svz_1_a1a1,
                              cols_a1a1["sv_cov00_1"],cols_a1a1["sv_cov10_1"],cols_a1a1["sv_cov20_1"],
                              cols_a1a1["sv_cov11_1"],cols_a1a1["sv_cov21_1"],cols_a1a1["sv_cov22_1"],
                              full_sv_cov,mX)

#######################
# Calling  kinfit_3pr #
#######################
# The second tau is assumed to decay to a1 (see definition of cuts above!)
# should be passed first to the routine
results = kinfit_3pr(cols["pt_2"],cols["eta_2"],cols["phi_2"],cols["mass_2"],
                     cols["pt_1"],cols["eta_1"],cols["phi_1"],cols["mass_1"],
                     cols["met_pt"],cols["met_phi"],
                     cols["met_covXX"],cols["met_covXY"],cols["met_covYY"],
                     svx,svy,svz,
                     cols["sv_cov00_2"],cols["sv_cov10_2"],cols["sv_cov20_2"],
                     cols["sv_cov11_2"],cols["sv_cov21_2"],cols["sv_cov22_2"],
                     full_sv_cov,mX)    


##############################################################
# accessing results of kinfit_3pr (library: keyword->column) #
##############################################################
# this is tau not decaying to a1 (second tau passed to kinfit)
px1 = results['px_2']
py1 = results['py_2']
pz1 = results['pz_2']

# this is tau decaying to a1 (first tau passed to kinfit)
px2 = results['px_1']
py2 = results['py_1']
pz2 = results['pz_1']

# chi-squared of the fit
chi2 = np.min(results['chi2'],19.5)
chi2_met = np.min(results['chi2_met'],19.5)
chi2_sv = np.min(results['chi2_sv'],19.5)

pt1 = np.sqrt(px1**2+py1**2)
pt2 = np.sqrt(px2**2+py2**2)

# --- store KinFit outputs ---
cols["KinFit_pt_1"] = pt1
cols["KinFit_pt_2"] = pt2

dpt1_kinfit = pt1/cols['genPart_pt_1']
dpt1_FastMTT = cols['FastMTT_pt_1']/cols['genPart_pt_1'] 
dpt1_FastMTT_const = cols['FastMTT_pt_1_constraint']/cols['genPart_pt_1']

dpt2_kinfit = pt2/cols['genPart_pt_2'] 
dpt2_FastMTT = cols['FastMTT_pt_2']/cols['genPart_pt_2'] 
dpt2_FastMTT_const = cols['FastMTT_pt_2_constraint']/cols['genPart_pt_2']

##############################################################
# accessing results of kinfit_3pr (library: keyword->column) #
##############################################################
# this is tau not decaying to a1 (second tau passed to kinfit)
px1 = results['px_2']
py1 = results['py_2']
pz1 = results['pz_2']

# this is tau decaying to a1 (first tau passed to kinfit)
px2 = results['px_1']
py2 = results['py_1']
pz2 = results['pz_1']

# chi-squared of the fit
chi2 = np.min(results['chi2'],19.5)
chi2_met = np.min(results['chi2_met'],19.5)
chi2_sv = np.min(results['chi2_sv'],19.5)

pt1 = np.sqrt(px1**2+py1**2)
pt2 = np.sqrt(px2**2+py2**2)

# --- store KinFit outputs ---
cols["KinFit_pt_1"] = pt1
cols["KinFit_pt_2"] = pt2

dpt1_kinfit = pt1/cols['genPart_pt_1']
dpt1_FastMTT = cols['FastMTT_pt_1']/cols['genPart_pt_1'] 
dpt1_FastMTT_const = cols['FastMTT_pt_1_constraint']/cols['genPart_pt_1']

dpt2_kinfit = pt2/cols['genPart_pt_2'] 
dpt2_FastMTT = cols['FastMTT_pt_2']/cols['genPart_pt_2'] 
dpt2_FastMTT_const = cols['FastMTT_pt_2_constraint']/cols['genPart_pt_2']

# saving to RooT file
outputFile="kinfit_3pr_%s.root"%(args.channel)
if full_sv_cov:
    outputFile="kinfit_3pr_%s_svcov.root"%(args.channel)
f = ROOT.TFile(outputFile,"recreate")
f.cd('')

hist_dpt1_kinfit = ROOT.TH1D("dpt1_kinfit","",60,0.,3.)
hist_dpt2_kinfit = ROOT.TH1D("dpt2_kinfit","",60,0.,3.)
hist_chi2_kinfit = ROOT.TH1D("chi2_kinfit","",40,0.,20.)


#####################
# Filling histograms
#####################

fill_hist(hist_dpt1_kinfit,dpt1_kinfit)
fill_hist(hist_dpt2_kinfit,dpt2_kinfit)
fill_hist(hist_dpt1_FastMTT,dpt1_FastMTT)
fill_hist(hist_dpt2_FastMTT,dpt2_FastMTT)
fill_hist(hist_dpt1_FastMTT_const,dpt1_FastMTT_const)
fill_hist(hist_dpt2_FastMTT_const,dpt2_FastMTT_const)
fill_hist(hist_mvis,cols['m_vis'])
# fill_hist(hist_mass_FastMTT,mass)

#####################
# saving histograms
#####################
f.cd('')
hist_mvis.Write("mvis")
hist_mass_FastMTT.Write("mtt")

hist_dpt1_kinfit.Write("dpt1_kinfit")
hist_dpt1_FastMTT.Write("dpt1_FastMTT")
hist_dpt1_FastMTT_const.Write("dpt1_FastMTT_const")

hist_dpt2_kinfit.Write("dpt2_kinfit")
hist_dpt2_FastMTT.Write("dpt2_FastMTT")
hist_dpt2_FastMTT_const.Write("dpt2_FastMTT_const")

f.Close()
print('')
print('Histograms are saved in file %s'%(outputFile))
print('')

################################
# Save new ROOT file with tree #
################################

print("\nSaving ROOT file with new columns...")

from pathlib import Path

# --- output path ---
outdir = Path.cwd()
outfile = outdir / "merged.root"

# 🔒 nie nadpisuj
if outfile.exists():
    i = 1
    while (outdir / f"merged_{i}.root").exists():
        i += 1
    outfile = outdir / f"merged_{i}.root"

########################################
# Create ROOT file and TTree manually #
########################################

import array

fout = ROOT.TFile(str(outfile), "RECREATE")
tree = ROOT.TTree("ntuple", "ntuple")

# --- prepare branch buffers ---
buffers = {}
branches = {}

skipped_cols = []

for name, arr in cols.items():
    dtype = arr.dtype

    if np.issubdtype(dtype, np.floating):
        buffers[name] = array.array('f', [0.])
        tree.Branch(name, buffers[name], f"{name}/F")
    elif np.issubdtype(dtype, np.integer):
        buffers[name] = array.array('i', [0])
        tree.Branch(name, buffers[name], f"{name}/I")
    else:
        # try to coerce object columns
        try:
            cols[name] = np.asarray(cols[name], dtype=np.int32)
            buffers[name] = array.array('i', [0])
            tree.Branch(name, buffers[name], f"{name}/I")
            print(f"[WARN] coerced {name} to int32")
        except Exception:
            try:
                cols[name] = np.asarray(cols[name], dtype=np.float32)
                buffers[name] = array.array('f', [0.])
                tree.Branch(name, buffers[name], f"{name}/F")
                print(f"[WARN] coerced {name} to float32")
            except Exception:
                skipped_cols.append(name)
                print(f"[SKIP] dropping non-numeric column: {name}")
                continue

n = len(next(iter(cols.values())))

print(f"Writing {n} entries...")

# --- event loop ---
active_cols = list(buffers.keys())

for i in range(n):
    for name in active_cols:
        buffers[name][0] = cols[name][i]
    tree.Fill()

print(f"Skipped {len(skipped_cols)} non-numeric columns: {skipped_cols}")

tree.Write()
fout.Close()

print(f"✅ ROOT saved to: {outfile}")
print("")
