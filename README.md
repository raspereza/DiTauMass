# C++ Wrapper of KinFit routines (kinematic fit in  channels involving 3-prong decay)

## Content

This package contains the following components:
* `kinfit_3pr.cpp` - C++ wrapper of kinematic fit for tau(X)+tau(a1) decays
* `kinfit_3pr_3pr.cpp` - C++ wrapper of kinematic fit for tau(a1)+tau(a1) decays
* `functions.h` - collection of functions used in fastmtt and kinfit
* `KinFit.cpp` - C++ code used for compilation of 
* `compile_kinfit.bash` - compilation script (creates shared library)
* `test.py` - testing script
* `pybind11` - folder of pybind11 package (C++ binding to python)
* `Plot.py` - plotting macro

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
results = kinfit_3pr(pt1,eta1,phi1,mass1, # 4P of the 1st tau(->3-prong)
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
                      	 full_sv_cov, # boolean (True : use full SV covariance including non-diagonal entries)
			 mX # mass of the resonance (Higgs mass in CP H->tautau analysis : 125.1 GeV)
                         )

```

## Running test

```
./test.py --channel ${channel} --sample ${sample}
```
The script will create RooT file named `kinfit_${channel}_${sample}` which you can inspect.

