#############################################################
########## General settings
#############################################################


# Hacky way to allow specifying the era as --configOpts="era=2016" in the tnpEGM_fitter.py
import __main__ as main
for option in main.args.configOpts.split(';'):
  if 'era' in option: era = option.split('=')[-1]


# flag to be Tested
if   era=='2016': flags = {'passEle27' : 'passHltEle27WPTightGsf'}
elif era=='2017': flags = {'passEle32' : 'passHltEle32DoubleEGWPTightGsf && passEGL1SingleEGOr'}
elif era=='2018': flags = {'passEle32' : 'passHltEle32WPTightGsf'}

baseOutDir = '/user/tomc/public_html/leptonSF/trigger_HNL/%s' % era

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
from etc.inputs.tnpSampleDef import getSample

# all the samples MUST have different names (i.e. sample.name must be different for all)
# if you need to use 2 times the same sample, then rename the second one
if era=='2016':
  samplesDef = {
      'data'   : getSample(['Run2016B', 'Run2016C', 'Run2016D', 'Run2016E', 'Run2016F', 'Run2016G', 'Run2016H'], rename='2016'),
      'mcNom'  : getSample('2016_DY_NLO'),
      'mcAlt'  : getSample('2016_DY_LO'),
      'tagSel' : getSample('2016_DY_NLO', rename='2016_DY_NLO_altTag'),
  }
elif era=='2017':
  samplesDef = {
      'data'   : getSample(['Run2017B', 'Run2017C', 'Run2017D', 'Run2017E', 'Run2017F'], rename='2017'),
      'mcNom'  : getSample(['2017_DY_NLO', '2017_DY_NLO_ext']),
      'mcAlt'  : getSample(['2017_DY_LO', '2017_DY_LO_ext']),
      'tagSel' : getSample(['2017_DY_NLO', '2017_DY_NLO_ext'], rename='2017_DY_NLO_altTag'),
  }
elif era=='2018':
  samplesDef = {
      'data'   : getSample(['Run2018A', 'Run2018B', 'Run2018C', 'Run2018D'], rename='2018'),
      'mcNom'  : getSample(['2018_DY_NLO', '2018_DY_NLO_ext']),
      'mcAlt'  : getSample('2018_DY_LO'),
      'tagSel' : getSample('2018_DY_NLO', rename='2018_DY_NLO_altTag'),
  }
else:
  print 'Unknown era, please fix'
  exit(1)




# Set the tree to use within the samples
for sample in samplesDef.values():
  sample.set_tnpTree('tnpEleTrig')

# Require MC truth on DY and set weight for MC
for mcSample in ['mcNom', 'mcAlt']:
  samplesDef[mcSample].set_mcTruth()
  samplesDef[mcSample].set_weight('totWeight')

# The totWeight in MC assumes a full year distribution, in case you only want to check a particular run, you need an external puTree
# if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree('/eos/cms/store/group/phys_egamma/swmukher/ntuple_2017/PU/DY_1j_madgraph_ele.pu.puTree.root')

# Alternative tag selection
if not samplesDef['tagSel'] is None:
  samplesDef['tagSel'].set_cut('tag_Ele_pt > %s' % ('35' if era=='2016' else '37'))

# Quickly doing a printout
for sample in samplesDef.values():
  sample.dump()

#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
   { 'var' : 'el_pt' , 'type': 'float', 'bins': [25,30,35,40,50,70,100,200,500]}, # in HNL analysis we use from 30 (2016) and 35 (2017-2018), just prepending some bins here to see possible trends
]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase  = 'tag_Ele_pt > %s && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0' % ('30' if era=='2016' else '35') # tag
cutBase += '&& abs(el_dxy) < 0.05 && abs(el_dz) < 0.1 && el_relIso_fall17 < 0.1 && passingMVA94Xwp90noisoV2' # Id of the single prompt electron we trigger on, see table 11 in AN-18-014

additionalCuts = {}

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
# Some documentation which goes in way too much detail as you are supposed to do in CMS, but I'll do it anyway:
# --> signal shape is described by a gaussian function
#   this shape of this gaussian is as usual defined by a mean and a variance (sigma),
#   convoluted with the Z shape as obtained from egm_tnp_analysis/etc/inputs/ZeeGenLevel.root
#   i.e. the mean parameter shifts the Z peak (in GeV), and sigma makes it more or less wide
#   probably we should keep the ranges for these parameters small enough to avoid incorporating background in the Z peak
#   Note: the sigmaF parameter is useless, the code automatically fits in the range [0.8*sigmaP, 3*sigmaP]
# --> background is described by a
#   an exponential defined as exp((peak-x)*gamma)
#   which is then multiplied with the error function erfc((alpha-x)*beta)
#   so probably we want to have alpha not in the Z peak range, otherwise you risk to construct a background shape which looks
#   a bit like a strange Z peak, especially in combination with a small beta (unless we're in a low pt bin where we only expect to construct background anyway)
#   I guess it is good to allow for a large beta in case we have minimal/flat background
#   I still do not fully understand all the strange situations you can get out of these shapes though....
tnpParNomFit = {'default':            ["meanP[-0.0,-1.0,1.0]","sigmaP[0.9,0.3,2.]",
                                       "meanF[-0.0,-1.0,1.0]","sigmaF[0.9,0.3,2.]",
                                       "acmsP[60.,50.,75.]","betaP[0.5,0.01,5]","gammaP[0.1, -5, 5]","peakP[90.0]",
                                       "acmsF[60.,50.,75.]","betaF[0.5,0.01,5]","gammaF[0.1, -5, 5]","peakF[90.0]"]
               }

if era=='2018' or era=='2017':
  tnpParNomFit['bin00'] =             ["meanP[-0.0,-1.0,1.0]","sigmaP[0.9,0.7,1.2]",
                                       "meanF[-0.0,-1.0,1.0]","sigmaF[0.9,0.3,2.]",
                                       "acmsP[85.,70.,90.]","betaP[0.127,0.01,0.2]","gammaP[0.252, .2, .5]","peakP[90.0]",
                                       "acmsF[60.,50.,85.]","betaF[0.5,0.01,5]","gammaF[0.1, -5, 5]","peakF[90.0]"]
  tnpParNomFit['bin09'] =             ["meanP[-0.0,-1.0,1.0]","sigmaP[0.9,0.7,1.2]",
                                       "meanF[-0.0,-1.0,1.0]","sigmaF[0.9,0.3,2.]",
                                       "acmsP[85.,70.,90.]","betaP[0.127,0.01,0.2]","gammaP[0.252, .2, .5]","peakP[90.0]",
                                       "acmsF[60.,50.,85.]","betaF[0.5,0.01,5]","gammaF[0.1, -5, 5]","peakF[90.0]"]


# AltSigFit
tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]


# AltBkgFit
tnpParAltBkgFit = {'default':         ["meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,3.0]",
                                       "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,3.0]",
                                       "alphaP[0.,-5.,5.]",
                                       "alphaF[0.,-5.,5.]",
                                      ]
                  }

if era=='2017':
  tnpParAltBkgFit['bin00'] =          ["meanP[-0.0,-3.0,3.0]","sigmaP[0.9,0.5,3.0]",
                                       "meanF[-0.0,-3.0,3.0]","sigmaF[1.3,0.5,3.0]",
                                       "alphaP[0.,-5.,5.]",
                                       "alphaF[0.1,-5.,5.]"]
  tnpParAltBkgFit['bin09'] =          ["meanP[-0.0,-3.0,3.0]","sigmaP[0.9,0.5,3.0]",
                                       "meanF[-0.0,-3.0,3.0]","sigmaF[0.9,0.5,3.0]",
                                       "alphaP[0.,-5.,5.]",
                                       "alphaF[0.4,-5.,5.]"]


