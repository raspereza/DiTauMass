#! /usr/bin/env python3
# Author: Alexei Raspereza (June 2026)
# Plotting macro to test kinematic fit
import ROOT
import math
import os
import DiTauMass.utils.stylesKinFit as styles

dict_DM_header = {
    'mu_a1' : '#mu+a_{1}',
    'pi_a1' : '#pi+a_{1}',
    'rho_a1': '#rho+a_{1}',
    'a1_a1' : 'a_{1}+a_{1}', 
}

dict_Chi2_XTitle = {
    'chi2' : '#chi^{2}_{KinFit}',
    'chi2sv' : '#chi^{2}_{SV}',
    'chi2met' : '#chi^{2}_{MET}',
}

dict_dPt_header = {
    'mu' : '#tau#rightarrow#mu#nu#nu',
    'pi' : '#tau#rightarrow#pi#nu',
    'rho' : '#tau#rightarrow#rho#nu',
    'a1' : '#tau#rightarrowa_{1}(3-prong)#nu',
}

def Plot_chi2(hists,**kwargs):
    
    channel = kwargs.get('channel','a1_a1')
    chi2 = kwargs.get('chi2','chi2')
    hist_ggH = hists['ggH%s_%s'%(chi2,channel)]
    hist_DY = hists['DY%s_%s'%(chi2,channel)]
    hist_Fakes = hists['Fakes%s_%s'%(chi2,channel)]
    
    hist_ggH.Scale(1.0/hist_ggH.GetSumOfWeights())
    hist_DY.Scale(1.0/hist_DY.GetSumOfWeights())
    hist_Fakes.Scale(1.0/hist_Fakes.GetSumOfWeights())
    
    xtitle = dict_Chi2_XTitle[chi2]
    ytitle = 'normalized to unity'
    header = dict_DM_header[channel]
    name = '%s_%s'%(channel,chi2)
    
    styles.InitModel(hist_ggH,xtitle,ytitle,ROOT.kRed)
    styles.InitModel(hist_DY,xtitle,ytitle,ROOT.kBlue)
    styles.InitModel(hist_Fakes,xtitle,ytitle,ROOT.kBlack)

    hist_ggH.GetYaxis().SetRangeUser(0.0,1.0)

    canvas_name = 'canv_%s'%(name)
    canvas = ROOT.TCanvas(canvas_name,'',800,700)

    hist_ggH.Draw('h')
    hist_DY.Draw('hsame')
    hist_Fakes.Draw('hsame')

    leg = ROOT.TLegend(0.25,0.75,0.5,0.9)
    styles.SetLegendStyle(leg)
    leg.SetHeader(header)
    leg.SetTextSize(0.04)
    leg.AddEntry(hist_ggH,'H#rightarrow#tau#tau')
    leg.AddEntry(hist_DY,'Z#rightarrow#tau#tau')
    leg.AddEntry(hist_Fakes,'jet#rightarrow#tau fakes')
    leg.Draw()
    canvas.RedrawAxis()
    canvas.Modified()
    canvas.Update()

    graphics = '%s.png'%(name)
    canvas.Print(graphics)
    
def Plot_dpt(hists,**kwargs):

    mode = kwargs.get('mode','a1')
    header = dict_dPt_header[mode]
    hist = hists['ggHdpt_%s'%(mode)]
    
    xtitle = '(p_{T}^{rec}-p_{T}^{gen})/p_{T}^{gen}'
    ytitle = 'normalized to unity'

    styles.InitModel(hist,xtitle,ytitle,ROOT.kBlack)

    headerMean = 'Mean = %4.2f'%(hist.GetMean())
    headerRMS  = 'RMS  = %4.2f'%(hist.GetRMS())
    
    canv_name = 'canv_dpt_%s'%(mode)
    canvas = styles.MakeCanvas(canv_name,"",800,700)
    
    hist.Draw('h')

    leg = ROOT.TLegend(0.65,0.8,0.85,0.9)
    styles.SetLegendStyle(leg)
    leg.SetHeader(header)
    leg.SetTextSize(0.04)
    leg.Draw()
    
    legMean = ROOT.TLegend(0.65,0.7,0.85,0.8)
    styles.SetLegendStyle(legMean)
    legMean.SetHeader(headerMean)
    legMean.SetTextSize(0.04)
    legMean.Draw()

    legRMS = ROOT.TLegend(0.65,0.6,0.85,0.7)
    styles.SetLegendStyle(legRMS)
    legRMS.SetHeader(headerRMS)
    legRMS.SetTextSize(0.04)
    legRMS.Draw()
    
    canvas.RedrawAxis()
    canvas.Modified()
    canvas.Update()

    outputGraphics = 'dpt_%s.png'%(mode)
    canvas.Print(outputGraphics)

if __name__ == "__main__":

    styles.InitROOT()
    styles.SetStyle()
    
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-channel','--channel', dest='channel', default='tt',choices=['mt','tt'])
    parser.add_argument('-full_sv_cov','--full_sv_cov',dest='full_sv_cov',action='store_true')
    args = parser.parse_args()

    
    samples = ['ggH','DY','Fakes']
    histnames_mt = ['dpt_mu','chi2_mu_a1','chi2sv_mu_a1','chi2met_mu_a1']
    histnames_tt = ['dpt_pi','dpt_rho','dpt_a1','chi2_pi_a1','chi2_rho_a1','chi2_a1_a1','chi2sv_pi_a1','chi2sv_rho_a1','chi2sv_a1_a1','chi2met_pi_a1','chi2met_rho_a1','chi2met_a1_a1',]
    
    channel = args.channel
    full_sv_cov = args.full_sv_cov

    if full_sv_cov:
        if os.path.isfile('kinfit_%s_svcov.root'%(channel)):
            os.system('rm kinfit_%s_svcov.root'%(channel))
        for sample in samples:
            filename = 'kinfit_%s_%s_svcov.root'%(channel,sample)
            if not os.path.isfile(filename):
                print('file %s not found'%(filename))
                print('run test.py --channel %s --sample %s --full_sv_cov'%(channel,sample))
                exit()
        os.system('hadd kinfit_%s_svcov.root kinfit_%s_ggH_svcov.root kinfit_%s_DY_svcov.root kinfit_%s_Fakes_svcov.root'%(channel,channel,channel,channel))
    else:
        if os.path.isfile('kinfit_%s.root'%(channel)):
            os.system('rm kinfit_%s.root'%(channel))
        for sample in samples:
            filename = 'kinfit_%s_%s.root'%(channel,sample)
            if not os.path.isfile(filename):
                print('file %s not found'%(filename))
                print('run test.py --channel %s --sample %s'%(channel,sample))
                exit()
        os.system('hadd kinfit_%s.root kinfit_%s_ggH.root kinfit_%s_DY.root kinfit_%s_Fakes.root'%(channel,channel,channel,channel))
        

    filename = 'kinfit_%s'%(channel)
    if full_sv_cov:
        filename += '_svcov'
    filename += '.root'
    inputfile = ROOT.TFile(filename,'READ')
    
    hists = {}
    for sample in samples:
        if channel=='tt':
            for histname in histnames_tt:
                name = '%s%s'%(sample,histname)
                hists[name] = inputfile.Get(name)
                #                print(name,hists[name])
        else:
            for histname in histnames_mt:
                name = '%s%s'%(sample,histname) 
                hists[name] = inputfile.Get(name)
                #                print(name,hists[name])


    if channel=='tt':
        for chi2_name in ['chi2','chi2sv','chi2met']:
            for dm_name in ['pi_a1','rho_a1','a1_a1']:
                Plot_chi2(hists,channel=dm_name,chi2=chi2_name)
        for dm_name in ['pi','rho','a1']:
            Plot_dpt(hists,mode=dm_name)
    elif channel=='mt':
        for chi2_name in ['chi2','chi2sv','chi2met']:
            for dm_name in ['mu_a1']:
                Plot_chi2(hists,channel=dm_name,chi2=chi2_name)
        Plot_dpt(hists,mode='mu')

    
    
