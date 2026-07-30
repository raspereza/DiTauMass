# C++ Wrapper of KinFit routines (kinematic fit in the channels involving 3-prong tau decay)

## Content

This package contains the following components:
* `kinfit_3pr.cpp` - C++ wrapper of kinematic fit for tau(X)+tau(a1) decays
* `kinfit_3pr_3pr.cpp` - C++ wrapper of kinematic fit for tau(a1)+tau(a1) decay
* `functions.h` - collection of functions used in kinfit routines
* `KinFit.cpp` - C++ code used for compilation of the package
* `compile_kinfit.bash` - compilation script (creates shared library)
* `test.py` - testing script
* `pybind11` - folder of pybind11 package (C++ binding to python)
* `Plot.py` - plotting macro
* `utils/python/stylesKinFit.py` - python file defining RooT styles

## Getting code from git

```
cd $CMSSW_BASE/src
git clone --recurse-submodules https://github.com/raspereza/DiTauMass.git
cd $CMSSW_BASE/
scramv1 b -j 4
```

## Compiling shared library

```
cd $CMSSW_BASE/src/
./compile_kinfit.bash
```

## Routines

### Kinematic fit in the final states where only one tau decays via 3-prong mode
```python
#######################
# Calling  kinfit_3pr #
#######################
# The tau decaying to a1(3-prong) should be passed
# to the routine first (pt1,eta1,phi1,mass1)
# all inputs except full_sv_cov and mX are numpy or awkward columns 
results = kinfit_3pr(
	pt1,eta1,phi1,mass1, # 4P of the 1st tau(->3-prong)
	pt2,eta2,phi2,mass2, # 4P of the 2nd tau(->pi,rho,a1)
	met_pt,met_phi, # MET
	metcovxx,metcovxy,metcovyy, # MET covariance
	svx1,svy1,svz1, # SV-PV vector of the 1st tau
	svcovxx1,svcovxy1,svcovxz1, # SV covariance of the 1st tau
	svcovyy1,svcovyz1,svcovzz1, # SV covariance of the 1st tau
	full_sv_cov, # boolean (True : use full SV covariance including non-diagonal entries)
	mX # mass of the resonance (Higgs mass in CP H->tautau analysis : 125.1 GeV)
)
```

### Kinematic fit in the final state where both taus decay via 3-prong mode
```python
##########################
# Calling kinfit_3pr_3pr #
##########################
# Both taus to decay to a1(3-prong)
# all inputs except full_sv_cov	and mX are numpy or awkward columns
results = kinfit_3pr_3pr(
	pt1,eta1,phi1,mass1, # 4P of the 1st tau
	pt2,eta2,phi2,mass2, # 4P of the 2nd tau
	met_pt,met_phi, # MET
	metcovxx,metcovxy,metcovyy, # MET covariance
	svx1,svy1,svz1, # SV-PV vector of the 1st tau
	svcovxx1,svcovxy1,svcovxz1, # SV covariance of the 1st tau
	svcovyy1,svcovyz1,svcovzz1, # SV covariance of the 1st tau
	svx2,svy2,svz2, # SV-PV vector of the 2nd tau
	svcovxx1,svcovxy1,svcovxz1, # SV covariance of the 2nd tau
	svcovyy1,svcovyz1,svcovzz1, # SV covariance of the 2nd tau
	full_sv_cov, # boolean (True : use full SV covariance including non-diagonal entries)
	mX # mass of the resonance (Higgs mass in CP H->tautau analysis : 125.1 GeV)
)

```

Both routines output the dictionary of columns:

```
results['px_1']     - Px of the total momentum of the 1st tau
results['py_1']     - Py of the total momentum of the 1st tau
results['px_1']     - Pz of the total momentum of the 1st tau
results['px_2']     - Px of the total momentum of the 2nd tau
results['py_2']     - Py of the total momentum of the 2nd tau
results['pz_2']     - Pz of the total momentum of the 2nd tau
results['chi2']     - total chi2 of the kinematic fit
results['chi2_sv']  - chi2(SV) of the kinematic fit
results['chi2_met'] - chi2(SV) of the kinematic fit
```

## Running test

```
./test.py --channel ${channel} --sample ${sample}
```
Steering cards are:

* `--channel : available options [tt,mt]`
* `--sample  : available options [ggH,DY,Fakes]`, where
  * `ggH : gg->H with H->tautau`;
  * `DY  : Drell-Yan with Z->tautau`;
  * `Fakes : data from same-sign sideband`;
* `--full_sv_cov : optional flag to enable the usage of full SV covariance matrix, if False only diagonal elements are used in computation of chi2(SV)`

The script will create RooT file named `kinfit_${channel}_${sample}.root` (or `kinfit_${channel}_${sample}_svcov.root` if flag `--full_sv_cov` is specified) which you can inspect.

When running `test.py` with the option `--channel mt` the following histograms are output to the RooT file:

* `${sample}dpt_mu`         : (pT(reco)-pT(gen))/pT(gen) of the tau decaying to muon
* `${sample}dpt_a1`         : (pT(reco)-pT(gen))/pT(gen) of the tau decaying to 3-prong mode
* `${sample}chi2_mu_a1`     : chi2 of the kinematic fit in the mu+a1(3-prong) decay mode
* `${sample}chi2sv_mu_a1`   : chi2(SV) of the kinematic fit in the mu+a1(3-prong) decay mode
* `${sample}chi2met_mu_a1`  : chi2(MET) of the kinematic fit in the mu+a1(3-prong) decay mode

When running `test.py` with the option `--channel tt` the following histograms are output to the RooT file:

* `${sample}dpt_pi`         : (pT(reco)-pT(gen))/pT(gen) of the tau decaying to pi+v mode
* `${sample}dpt_rho`        : (pT(reco)-pT(gen))/pT(gen) of the tau decaying to rho+v mode
* `${sample}dpt_a1`         : (pT(reco)-pT(gen))/pT(gen) of the tau decaying to 3-prong mode
* `${sample}chi2_pi_a1`     : chi2 of the kinematic fit in the pi+a1 decay mode
* `${sample}chi2sv_pi_a1`   : chi2(SV) of the kinematic fit in the pi+a1 decay modd
* `${sample}chi2met_pi_a1`  : chi2(MET) of the kinematic fit in the pi+a1 decay mode
* `${sample}chi2_rho_a1`    : chi2 of the kinematic fit in the rho+a1 decay mode
* `${sample}chi2sv_rho_a1`  : chi2(SV) of the kinematic fit in the rho+a1 decay mode
* `${sample}chi2met_rho_a1` : chi2(MET) of the kinematic fit in the rho+a1 decay mode
* `${sample}chi2_a1_a1`    : chi2 of the kinematic fit in the a1+a1 decay mode
* `${sample}chi2sv_a1_a1`  : chi2(SV) of the kinematic fit in the a1+a1 decay mode
* `${sample}chi2met_a1_a1` : chi2(MET) of the kinematic fit in the a1+a1 decay mode

## Plotting

Plotting macro should be run once you've created output RooT files for all samples: `ggH`, `DY`, `Fakes`.
```
./Plot.py --channel ${channel}
```
When flag `--full_sv_cov` is specified, the routine accesses RooT files with results of kinematic fit obtained with full SV covariance matrix (i.e. including nondiagonal elements).

When run with option `--channel tt`, the macro produces the following list of plots:
```
pi_a1_chi2.png
rho_a1_chi2.png
a1_a1_chi2.png
pi_a1_chi2sv.png
rho_a1_chi2sv.png
a1_a1_chi2sv.png
pi_a1_chi2met.png
rho_a1_chi2met.png
a1_a1_chi2met.png
dpt_pi.png
dpt_rho.png
dpt_a1.png
```

When run with the option `--channel mt`, the macro produces the following list of plots:
```
mu_a1_chi2.png
mu_a1_chi2sv.png
mu_a1_chi2met.png
dpt_mu.png
```
