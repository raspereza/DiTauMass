#! /usr/bin/env python3
import numpy as np
import os 
from  KinFit import kinfit_3pr, kinfit_3pr_3pr
import ROOT
from argparse import ArgumentParser

sample_dict = {
    'ggH'  : ['GluGluHTo2Tau_UncorrelatedDecay_SM_Filtered_ProdAndDecay'],
    'DY'   : ['DYto2Tau_MLL_50_0J_Filtered_amcatnloFXFX','DYto2Tau_MLL_50_1J_Filtered_amcatnloFXFX','DYto2Tau_MLL_50_2J_Filtered_amcatnloFXFX'],
    'FakesMuTau' : ['Muon_Run2022E','Muon_Run2022F','Muon_Run2022G'],
    'FakesTauTau': ['Tau_Run2022E','Tau_Run2022F','Tau_Run2022G'],
}

# dictionaries ->
indx_cols = {
    'pi_a1'  : ('2','1'),
    'a1_pi'  : ('1','2'),
    'rho_a1' : ('2','1'),
    'a1_rho' : ('1','2'),
    'a1_a1'  : ('1','2'),
}

def fill_hist(hist, array):
    [hist.Fill(x) for x in array]

################
# Main routine #
################

parser = ArgumentParser()
parser.add_argument('-sample','--sample',dest='sample',default='ggH',choices=['ggH','DY','Fakes'])
parser.add_argument('-channel','--channel',dest='channel',default='tt',choices=['mt','tt'])
parser.add_argument('-full_sv_cov','--full_sv_cov',dest='full_sv_cov',action='store_true')
args = parser.parse_args()

sample = args.sample
channel = args.channel
full_sv_cov = args.full_sv_cov
root_files = []
if sample=='Fakes':
    if channel=='tt':
        root_files = sample_dict['FakesTauTau']
    else:
        root_files = sample_dict['FakesMuTau']
else:
    root_files = sample_dict[sample]

print('')
print('List of samples : ',root_files)
print('')

cuts_sign = ''

if sample=='Fakes':
    cuts_sign += '&&os<0.5'
else:
    cuts_sign += '&&os>0.5'

cuts_mu_a1  = 'fabs(ip_LengthSig_1)>1.0&&iso_1<0.15&&pt_1>26&&fabs(eta_1)<2.4&&idDeepTau2018v2p5VSe_2>=2&&idDeepTau2018v2p5VSmu_2>=4&&idDeepTau2018v2p5VSjet_2>=7&&pt_2>20.&&fabs(eta_2)<2.5&&decayModePNet_2==10&&hasRefitSV_2'+cuts_sign

cuts = {}

cuts['pi_a1']  = 'fabs(ip_LengthSig_1)>1.25&&idDeepTau2018v2p5VSe_1>=2&&idDeepTau2018v2p5VSmu_1>=4&&idDeepTau2018v2p5VSjet_1>=7&&pt_1>40.&&fabs(eta_1)<2.5&&decayModePNet_1==0&&idDeepTau2018v2p5VSe_2>=2&&idDeepTau2018v2p5VSmu_2>=4&&idDeepTau2018v2p5VSjet_2>=7&&pt_2>40.&&fabs(eta_2)<2.5&&decayModePNet_2==10&&hasRefitSV_2'+cuts_sign
cuts['a1_pi']  = 'fabs(ip_LengthSig_2)>1.25&&idDeepTau2018v2p5VSe_2>=2&&idDeepTau2018v2p5VSmu_2>=4&&idDeepTau2018v2p5VSjet_2>=7&&pt_2>40.&&fabs(eta_2)<2.5&&decayModePNet_2==0&&idDeepTau2018v2p5VSe_1>=2&&idDeepTau2018v2p5VSmu_1>=4&&idDeepTau2018v2p5VSjet_1>=7&&pt_1>40.&&fabs(eta_1)<2.5&&decayModePNet_1==10&&hasRefitSV_1'+cuts_sign

cuts['rho_a1'] = 'fabs(pion_E_split_1)>0.2&&idDeepTau2018v2p5VSe_1>=2&&idDeepTau2018v2p5VSmu_1>=4&&idDeepTau2018v2p5VSjet_1>=7&&pt_1>40.&&fabs(eta_1)<2.5&&decayModePNet_1==1&&decayMode_1==1&&idDeepTau2018v2p5VSe_2>=2&&idDeepTau2018v2p5VSmu_2>=4&&idDeepTau2018v2p5VSjet_2>=7&&pt_2>40.&&fabs(eta_2)<2.5&&decayModePNet_2==10&&hasRefitSV_2'+cuts_sign
cuts['a1_rho'] = 'fabs(pion_E_split_2)>0.2&&idDeepTau2018v2p5VSe_2>=2&&idDeepTau2018v2p5VSmu_2>=4&&idDeepTau2018v2p5VSjet_2>=7&&pt_2>40.&&fabs(eta_2)<2.5&&decayModePNet_2==1&&decayMode_2==1&&idDeepTau2018v2p5VSe_1>=2&&idDeepTau2018v2p5VSmu_1>=4&&idDeepTau2018v2p5VSjet_1>=7&&pt_1>40.&&fabs(eta_1)<2.5&&decayModePNet_1==10&&hasRefitSV_1'+cuts_sign

cuts['a1_a1']  = 'idDeepTau2018v2p5VSe_1>=2&&idDeepTau2018v2p5VSmu_1>=4&&idDeepTau2018v2p5VSjet_1>=7&&pt_1>40.&&fabs(eta_1)<2.5&&decayModePNet_1==10&&hasRefitSV_1&&idDeepTau2018v2p5VSe_2>=2&&idDeepTau2018v2p5VSmu_2>=4&&idDeepTau2018v2p5VSjet_2>=7&&pt_2>40.&&fabs(eta_2)<2.5&&decayModePNet_2==10&&hasRefitSV_2'+cuts_sign

chi2max = 25.
chi2svmax = 5.

# clipping chi-squared of the fit
chi2_min = 0.01
chi2_max = chi2max - 0.01
chi2sv_max = chi2svmax - 0.01

# declaring histograms ->
# (pT(reco)-pT(gen))/pT(gen)
hist_dpt_mu  = ROOT.TH1D("dpt_mu","",60,0.,3.)
hist_dpt_pi  = ROOT.TH1D("dpt_pi","",60,0.,3.)
hist_dpt_rho = ROOT.TH1D("dpt_rho","",60,0.,3.)
hist_dpt_a1  = ROOT.TH1D("dpt_a1","",60,0.,3.)
# chi2 of the kinematic fit
hist_chi2_mu_a1  = ROOT.TH1D("chi2_mu_a1","",25,0.,chi2max)
hist_chi2_pi_a1  = ROOT.TH1D("chi2_pi_a1","",25,0.,chi2max)
hist_chi2_rho_a1 = ROOT.TH1D("chi2_rho_a1","",25,0.,chi2max)
hist_chi2_a1_a1  = ROOT.TH1D("chi2_a1_a1","",25,0.,chi2max)
# chi2(met) of the kinematic fit
hist_chi2met_mu_a1  = ROOT.TH1D("chi2met_mu_a1","",25,0.,chi2max)
hist_chi2met_pi_a1  = ROOT.TH1D("chi2met_pi_a1","",25,0.,chi2max)
hist_chi2met_rho_a1 = ROOT.TH1D("chi2met_rho_a1","",25,0.,chi2max)
hist_chi2met_a1_a1  = ROOT.TH1D("chi2met_a1_a1","",25,0.,chi2max)
# chi2(SV) of 
hist_chi2sv_mu_a1  = ROOT.TH1D("chi2sv_mu_a1","",25,0.,chi2svmax)
hist_chi2sv_pi_a1  = ROOT.TH1D("chi2sv_pi_a1","",25,0.,chi2svmax)
hist_chi2sv_rho_a1 = ROOT.TH1D("chi2sv_rho_a1","",25,0.,chi2svmax)
hist_chi2sv_a1_a1  = ROOT.TH1D("chi2sv_a1_a1","",25,0.,chi2svmax)

basedir = '/eos/cms/store/group/phys_tau/lrussell/forAliaksei/AprilCPStudies/Run3_2022EE'
# steering parameters
full_sv_cov = args.full_sv_cov # full SV covariance (True) or only diagonal elements (False)
mX = 125.10 # Higgs mass

print('')
print('running selection... be patient, it takes a while')
print('')
for root_file in root_files:
    filename = '%s/%s/%s/nominal/merged.root'%(basedir,args.channel,root_file)
    if not os.path.isfile:
        print('file %s is not found'%(filename))
        print('Choose ROOT files (w/o extension .root from the following folders:')
        print('/eos/cms/store/group/phys_tau/lrussell/forAliaksei/AprilCPStudies/Run3_2022EE/[mt,tt]')
        exit()
    
    print('processing file %s'%(filename))
    df = ROOT.RDataFrame("ntuple",filename)
    
    # get list of all branches in the tree
    all_cols = [str(c) for c in df.GetColumnNames()]

    print(f'Found {len(all_cols)} columns')
    print('')

    results = None
    if channel=='tt':
        cols = {}
        for fs in cuts:
            print('Cuts %s : %s'%(fs,cuts[fs]))
            cols = df.Filter(cuts[fs]).AsNumpy(all_cols)
            print('Length of column %s : %1i\n'%(fs,len(cols["pt_1"])))
            # initializing colums
            pt1 = cols['pt_%s'%(indx_cols[fs][0])]
            eta1 = cols['eta_%s'%(indx_cols[fs][0])]
            phi1 = cols['phi_%s'%(indx_cols[fs][0])]
            mass1 = cols['mass_%s'%(indx_cols[fs][0])]
            pt2 = cols['pt_%s'%(indx_cols[fs][1])]
            eta2 = cols['eta_%s'%(indx_cols[fs][1])]
            phi2 = cols['phi_%s'%(indx_cols[fs][1])]
            mass2 = cols['mass_%s'%(indx_cols[fs][1])]
            svx1 = cols['sv_x_%s'%(indx_cols[fs][0])]-cols['PVBS_x']
            svy1 = cols['sv_y_%s'%(indx_cols[fs][0])]-cols['PVBS_y']
            svz1 = cols['sv_z_%s'%(indx_cols[fs][0])]-cols['PVBS_z']
            svx2 = cols['sv_x_%s'%(indx_cols[fs][1])]-cols['PVBS_x']
            svy2 = cols['sv_y_%s'%(indx_cols[fs][1])]-cols['PVBS_y']
            svz2 = cols['sv_z_%s'%(indx_cols[fs][1])]-cols['PVBS_z']
            svcovxx1 = cols['sv_cov00_%s'%(indx_cols[fs][0])]
            svcovxy1 = cols['sv_cov10_%s'%(indx_cols[fs][0])]
            svcovxz1 = cols['sv_cov20_%s'%(indx_cols[fs][0])]
            svcovyy1 = cols['sv_cov11_%s'%(indx_cols[fs][0])]
            svcovyz1 = cols['sv_cov21_%s'%(indx_cols[fs][0])]
            svcovzz1 = cols['sv_cov22_%s'%(indx_cols[fs][0])]
            svcovxx2 = cols['sv_cov00_%s'%(indx_cols[fs][1])]
            svcovxy2 = cols['sv_cov10_%s'%(indx_cols[fs][1])]
            svcovxz2 = cols['sv_cov20_%s'%(indx_cols[fs][1])]
            svcovyy2 = cols['sv_cov11_%s'%(indx_cols[fs][1])]
            svcovyz2 = cols['sv_cov21_%s'%(indx_cols[fs][1])]
            svcovzz2 = cols['sv_cov22_%s'%(indx_cols[fs][1])]
            met_pt = cols['met_pt']
            met_phi = cols['met_phi']
            metcovxx = cols['met_covXX']
            metcovxy = cols['met_covXY']
            metcovyy = cols['met_covYY']
            if fs=='a1_a1':            
                ##########################
                # Calling kinfit_3pr_3pr #
                ##########################
                # Both taus to decay to a1(3-prong)
                results = kinfit_3pr_3pr(pt1,eta1,phi1,mass1, # 4P of the 1st tau
                                         pt2,eta2,phi2,mass2, # 4P of the 2nd tau
                                         met_pt,met_phi, # MET
                                         metcovxx,metcovxy,metcovyy, # MET covariance
                                         svx1,svy1,svz1, # SV-PV vector of the 1st tau
                                         svcovxx1,svcovxy1,svcovxz1, # SV covariance of the 1st tau
                                         svcovyy1,svcovyz1,svcovzz1, # SV covariance of the 1st tau
                                         svx2,svy2,svz2, # SV-PV vector of the 2nd tau
                                         svcovxx1,svcovxy1,svcovxz1, # SV covariance of the 2nd tau
                                         svcovyy1,svcovyz1,svcovzz1, # SV covariance of the 2nd tau
                                         full_sv_cov,mX # use full SV covariance (bool), m(Higgs)
                                         )
            else:
                #######################
                # Calling  kinfit_3pr #
                #######################
                # The tau decaying to a1(3-prong) should be passed
                # to the routine first (pt1,eta1,phi1,mass1)
                results = kinfit_3pr(pt1,eta1,phi1,mass1, # 4P of the 1st tau(->3-prong)
                                     pt2,eta2,phi2,mass2, # 4P of the 2nd tau(->pi,rho,a1)
                                     met_pt,met_phi, # MET
                                     metcovxx,metcovxy,metcovyy, # MET covariance
                                     svx1,svy1,svz1, # SV-PV vector of the 1st tau
                                     svcovxx1,svcovxy1,svcovxz1, # SV covariance of the 1st tau
                                     svcovyy1,svcovyz1,svcovzz1, # SV covariance of the 1st tau
                                     full_sv_cov,mX)
            # first tau
            px1 = results['px_1']
            py1 = results['py_1']
            pt1 = np.sqrt(px1*px1+py1*py1)
            dpt1 = pt1
            if sample in ['ggH','DY']:
                dpt1 = pt1/cols['genPart_pt_1']
            # second tau
            px2 = results['px_2']
            py2 = results['py_2']
            pt2 = np.sqrt(px2*px2+py2*py2)
            dpt2 = pt2
            if sample in ['ggH','DY']:
                dpt2 = pt2/cols['genPart_pt_2'] 
            # chi2 of the kinematic fit
            chi2 = np.clip(results['chi2'],chi2_min,chi2_max)
            chi2met = np.clip(results['chi2_met'],chi2_min,chi2_max)
            chi2sv = np.clip(results['chi2_sv'],chi2_min,chi2sv_max)

            fill_hist(hist_dpt_a1,dpt1)
            if fs=='a1_a1':
                fill_hist(hist_dpt_a1,dpt2)
                fill_hist(hist_chi2_a1_a1,chi2)
                fill_hist(hist_chi2sv_a1_a1,chi2sv)
                fill_hist(hist_chi2met_a1_a1,chi2met)
            elif fs=='pi_a1' or fs=='a1_pi':
                fill_hist(hist_dpt_pi,dpt2)
                fill_hist(hist_chi2_pi_a1,chi2)
                fill_hist(hist_chi2sv_pi_a1,chi2sv)
                fill_hist(hist_chi2met_pi_a1,chi2met)
            elif fs=='rho_a1' or fs=='a1_rho':
                fill_hist(hist_dpt_rho,dpt2)
                fill_hist(hist_chi2_rho_a1,chi2)
                fill_hist(hist_chi2sv_rho_a1,chi2sv)
                fill_hist(hist_chi2met_rho_a1,chi2met)
    elif channel=='mt':    
        print('Cuts mu_a1 : %s'%(cuts_mu_a1))
        cols = df.Filter(cuts_mu_a1).AsNumpy(all_cols)
        print('Length of column mu_a1 : %1i\n'%(len(cols["pt_1"])))
        pt1 = cols['pt_2']
        eta1 = cols['eta_2']
        phi1 = cols['phi_2']
        mass1 = cols['mass_2']
        pt2 = cols['pt_1']
        eta2 = cols['eta_1']
        phi2 = cols['phi_1']
        mass2 = cols['mass_1']
        svx1 = cols['sv_x_2']
        svy1 = cols['sv_y_2']
        svz1 = cols['sv_z_2']
        svcovxx1 = cols['sv_cov00_2']
        svcovxy1 = cols['sv_cov10_2']
        svcovxz1 = cols['sv_cov20_2']
        svcovyy1 = cols['sv_cov11_2']
        svcovyz1 = cols['sv_cov21_2']
        svcovzz1 = cols['sv_cov22_2']
        met_pt = cols['met_pt']
        met_phi = cols['met_phi']
        metcovxx = cols['met_covXX']
        metcovxy = cols['met_covXY']
        metcovyy = cols['met_covYY']
        #######################
        # Calling  kinfit_3pr #
        #######################
        # The tau decaying to a1(3-prong) should be passed
        # to the routine first (pt1,eta1,phi1,mass1)
        results = kinfit_3pr(pt1,eta1,phi1,mass1, # 4P of the 1st tau(->a1(3-prong))
                             pt2,eta2,phi2,mass2, # 4P of the 2nd tau(->mu)
                             met_pt,met_phi, # MET
                             metcovxx,metcovxy,metcovyy, # MET covariance
                             svx1,svy1,svz1, # SV-PV vector of the 1st tau
                             svcovxx1,svcovxy1,svcovxz1, # SV covariance of the 1st tau
                             svcovyy1,svcovyz1,svcovzz1, # SV covariance of the 1st tau
                             full_sv_cov,mX)
        # first tau
        px1 = results['px_1']
        py1 = results['py_1']
        pt1 = np.sqrt(px1*px1+py1*py1)
        dpt1 = pt1
        if sample in ['ggH','DY']:
            dpt1 = pt1/cols['genPart_pt_1']
        # second tau
        px2 = results['px_2']
        py2 = results['py_2']
        pt2 = np.sqrt(px2*px2+py2*py2)
        dpt2 = pt2
        if sample in ['ggH','DY']:
            dpt2 = pt2/cols['genPart_pt_2'] 
        # chi2 of the kinematic fit
        chi2 = np.clip(results['chi2'],chi2_min,chi2_max)
        chi2met = np.clip(results['chi2_met'],chi2_min,chi2_max)
        chi2sv = np.clip(results['chi2_sv'],chi2_min,chi2sv_max)
        # filling histograms
        fill_hist(hist_dpt_a1,dpt1)
        fill_hist(hist_dpt_mu,dpt2)
        fill_hist(hist_chi2_mu_a1,chi2)
        fill_hist(hist_chi2sv_mu_a1,chi2sv)
        fill_hist(hist_chi2met_mu_a1,chi2met)
     
# saving histograms to RooT file
outputFile="kinfit_%s_%s"%(channel,sample)
if full_sv_cov:
    outputFile += "_svcov"
outputFile += ".root"
f = ROOT.TFile(outputFile,"recreate")
f.cd('')
if channel=='mt':
    hist_dpt_mu.Write('dpt_mu')
    hist_dpt_a1.Write('dpt_a1')
    hist_chi2_mu_a1.Write('chi2_mu_a1')
    hist_chi2sv_mu_a1.Write('chi2sv_mu_a1')
    hist_chi2met_mu_a1.Write('chi2met_mu_a1')
else:
    hist_dpt_pi.Write("dpt_pi")
    hist_dpt_rho.Write("dpt_rho")
    hist_dpt_a1.Write("dpt_a1")
    
    hist_chi2_pi_a1.Write("chi2_pi_a1")
    hist_chi2sv_pi_a1.Write("chi2sv_pi_a1")
    hist_chi2met_pi_a1.Write("chi2met_pi_a1")
    
    hist_chi2_rho_a1.Write("chi2_rho_a1")
    hist_chi2sv_rho_a1.Write("chi2sv_rho_a1")
    hist_chi2met_rho_a1.Write("chi2met_rho_a1")
    
    hist_chi2_a1_a1.Write("chi2_a1_a1")
    hist_chi2sv_a1_a1.Write("chi2sv_a1_a1")
    hist_chi2met_a1_a1.Write("chi2met_a1_a1")
    
f.Close()
print('')
print('Histograms are saved in file %s'%(outputFile))
print('')

