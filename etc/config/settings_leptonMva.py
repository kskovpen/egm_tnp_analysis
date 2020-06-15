#############################################################
########## General settings
#############################################################


# Hacky way to allow specifying the era as --configOpts="era=2016" in the tnpEGM_fitter.py
import __main__ as main
for option in main.args.configOpts.split(';'):
  if 'era' in option: era = option.split('=')[-1]



# Baseline selection as defined in https://indico.cern.ch/event/923174/contributions/3889049/attachments/2050271/3436370/kskovpenLeptonMVA20200603.pdf (slide 5)
baseline = 'el_miniIsoAll_fall17 < 0.4 && el_mHits < 2 && abs(el_sip) < 8 && abs(el_dxy) < 0.05 && abs(el_dz) < 0.1'

# Baseline selection tZq (need new TnPTree's and especially someone needs to come up with an explanation why you need such a complicated baseline when you apply an mva)
# Bullshit alert
baselineTZQ  = 'el_mHits==0 && abs(el_sip) < 8 && abs(el_dxy) < 0.05 && abs(el_dz) < 0.1'
baselineTZQ += 'CONEPT > 10 && CONVERSIONREJECTION && passingMVA94Xwp80noisoV2 && DEEPCSV < ??'
baselineTZQ += 'RELISO < 0.4'
baselineTZQ += '&& ((abs(el_eta) < 1.4442 && el_sieie < 0.011) || (abs(el_eta) > 1.4442 && el_sieie < 0.030))'
baselineTZQ += '&& el_hoe < 0.10 && el_1overEminus1overP > -0.04'
# End bullshit alert

# flag to be Tested
flags = {
    'passingLeptonMvaTight'  : '(%s && el_leptonMva_TOP > 0.9)' % baseline,
    'passingLeptonMvaMedium' : '(%s && el_leptonMva_TOP > 0.4)' % baseline,
    'passingLeptonMvaLoose'  : '(%s && el_leptonMva_TOP > 0.0)' % baseline,
    'passingLeptonMvaVLoose' : '(%s && el_leptonMva_TOP > -.55)' % baseline,
    }


baseOutDir = '/user/tomc/public_html/leptonSF/electrons/%s' % era

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
      'tagSel' : getSample('2017_DY_NLO', rename='2017_DY_NLO_altTag'),
  }
elif era=='2018':
  samplesDef = {
      'data'   : getSample(['Run2018A', 'Run2018B', 'Run2018C', 'Run2018D'], rename='2018'),
      'mcNom'  : getSample('2018_DY_NLO'),
      'mcAlt'  : getSample('2018_DY_pow'),
      'tagSel' : getSample('2018_DY_NLO', rename='2018_DY_NLO_altTag'),
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
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 37')

# Quickly doing a printout
for sample in samplesDef.values():
  sample.dump()

#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
   { 'var' : 'el_pt' , 'type': 'float', 'bins': [10,20,35,50,100,200,500] },


]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = { 
#    0 : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
}


#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
    ]

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
        
