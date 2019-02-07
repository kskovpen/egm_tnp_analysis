#############################################################
########## General settings
#############################################################
import sys
type = sys.modules['__main__'].args.settingsOpt

# flag to be Tested
flags = {
    'passingL1TEle23Ele12' : '(passL1TEle23Ele12 == 1)',
    'passingEtLeg1Ele23Ele12' : '(passEtLeg1Ele23Ele12 == 1)',
    'passingEtLeg2Ele23Ele12' : '(passEtLeg2Ele23Ele12 == 1)',
    'passingPixelMatchLeg1Ele23Ele12' : '(passPixelMatchLeg1Ele23Ele12 == 1)',
    'passingPixelMatchLeg2Ele23Ele12' : '(passPixelMatchLeg2Ele23Ele12 == 1)',
    }
baseOutDir = 'results/2018/tnpEleTrig/Ele23Ele12/' + type

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples

tnpTreeDir = 'tnpEleTrig' # tree name of the input root files 

samplesDef = {
    'data'   : tnpSamples.samples2018['Run2018A'].clone(),
    'mcNom'  : tnpSamples.samples2018['DY'].clone(),
    'mcAlt'  : None, 
    'tagSel' : None,
}
samplesDef['data'].add_sample( tnpSamples.samples2018['Run2018B'] )
samplesDef['data'].add_sample( tnpSamples.samples2018['Run2018C'] )
samplesDef['data'].add_sample( tnpSamples.samples2018['Run2018D'] )

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph_ele')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 33  && tag_Ele_nonTrigMVA > 0.90')

## set MC weight, simple way (use tree weight)
weightName = 'totWeight'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

#############################################################
########## bining definition  [can be nD bining]
#############################################################
if type=='pt_vs_eta':
  biningDef = [
     { 'var' : 'el_sc_eta' , 'type': 'abs_float', 'bins': [0.0, 1.479, 2.5] },
     { 'var' : 'el_sc_et' , 'type': 'float', 'bins': [10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 27.0, 28.5, 30.0, 35.0, 40.0, 45.0, 50.0,60.0,70.0,80.0,100.0, 150.0, 200.0, 250.0] },
  ]
elif type=='pt_vs_eta':
  biningDef = [
     { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.2,-1.566,-1.4442, -1.0, -0.6,-0.3,-0.1, 0.1, 0.3,0.6,1.0, 1.4442, 1.566, 2.2, 2.5] },
     { 'var' : 'el_sc_et' , 'type': 'float', 'bins': [30,250] },
  ]
elif type=='eta_vs_phi':
  biningDef = [
     { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-1.479, 0.0, 1.479, 2.5] },
     { 'var' : 'el_sc_phi' , 'type': 'float', 'bins': [ -3.15, -2.4, -1.8, -1.2, -0.6, 0., 0.6, 1.2, 1.8, 2.4, 3.15] },
  ]
elif type=='eta_vs_nvtx':
  biningDef = [
     { 'var' : 'el_sc_eta' , 'type': 'abs_float', 'bins': [0.0, 1.479, 2.5] },
     { 'var' : 'event_nPV' , 'type': 'float', 'bins': [0., 3., 6., 9., 12., 15., 18., 21., 24., 27., 30., 33., 36., 39., 42., 45., 48., 51., 54., 57., 60., 63., 66., 69.] },
  ]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut

cutBase = 'tag_sc_et > 35 && abs(tag_sc_eta) < 2.1 && passL1TEle23Ele12 == 1'
if type!='pt_vs_eta': cutBase += ' && el_sc_et > 30'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
#additionalCuts = {i : 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45' for i in range(20)}

#### or remove any additional cut (default)
additionalCuts = None

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0, 1]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0, 1]","peakF[90.0]",
    ]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
     
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.5,0.1,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]
        
