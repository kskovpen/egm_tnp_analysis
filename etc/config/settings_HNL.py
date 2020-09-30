#############################################################
########## General settings
#############################################################


# Hacky way to allow specifying the era as --configOpts="era=2016" in the tnpEGM_fitter.py
import __main__ as main
for option in main.args.configOpts.split(';'):
  if 'era' in option: era = option.split('=')[-1]


# flag to be Tested
flags = {'HNLprompt' : 'abs(el_dxy) < 0.05 && abs(el_dz) < 0.1 && el_relIso_fall17 < 0.1 && passingMVA94Xwp90noisoV2',
         'HNLprompt_noIP' : 'el_relIso_fall17 < 0.1 && passingMVA94Xwp90noisoV2',
         'HNLprompt_noIso' : 'abs(el_dxy) < 0.05 && abs(el_dz) < 0.1 && passingMVA94Xwp90noisoV2',
         'HNLprompt_noIPnoIso' : 'passingMVA94Xwp90noisoV2'}

baseOutDir = '/user/tomc/public_html/leptonSF/HNLprompt/%s' % era

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
      'tagSel' : getSample(['2018_DY_NLO', '2018_DY_NLO_ext'], rename='2018_DY_NLO_altTag'),
  }
else:
  print 'Unknown era, please fix'
  exit(1)




# Set the tree to use within the samples
for sample in samplesDef.values():
  sample.set_tnpTree('tnpEleIDs')

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

additionalCuts = {i : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45' for i in range(0, 15)}


#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = {'default' : [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
    ]}

if era=='2016':
  tnpParNomFit['bin58'] = ["meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,1.1]",
                           "meanF[-0.0,-1.0,.1]","sigmaF[0.7,0.5,1.1]",
                           "acmsP[60.,50.,90.]","betaP[0.05,0.01,0.9]","gammaP[0.1, -2, 2]","peakP[90.0]",
                           "acmsF[60.,50.,90.]","betaF[0.05,0.01,0.9]","gammaF[0.1, -2, 2]","peakF[90.0]"]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
     
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]
