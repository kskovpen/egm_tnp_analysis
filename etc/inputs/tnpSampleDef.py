from libPython.tnpClassUtils import tnpSample

### qll stat
#myinputDir = '/data1/EGM_TnP/TnPTree/Dalmin/HN/Moriond17_GainSwitch_newTnP_v3_test/'
myinputDir_leg1 = '/data1/EGM_TnP/TnPTree/Dalmin/HN/Moriond17_GainSwitch_newTnP_v3_leg1/'
myinputDir_leg2 = '/data1/EGM_TnP/TnPTree/Dalmin/HN/Moriond17_GainSwitch_newTnP_v3_leg2/'
myinputDir = '/data8/Users/jhkim/Moriond17_GainSwitch_newTnP_v5/'

myinputDir_2018 = '/data8/Users/jhkim/2018Data/2018Data/'

EGamma2018_test = {
    ### MiniAOD TnP for IDs scale factors
    'DY_madgraph_Winter17' : tnpSample('DY_madgraph_Winter17',
                                       myinputDir_2018 + 'mc/CRAB_UserFiles/crab_DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8.root',
                                       isMC = True, nEvts = 49144274 ),

    'data_Run2018Av1' : tnpSample('data_Run2018Av1' , myinputDir_2018 + 'data/EGamma/TnPTree_SingleElectron_2018rereco_RunAv1.root' , lumi = 5.788 ),
    }


Moriond17_80X_HN = {
    ### MiniAOD TnP for IDs scale factors
    'DY_madgraph_Winter17' : tnpSample('DY_madgraph_Winter17', 
                                       myinputDir + 'mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_DYToLL_madgraph_Moriond17.root',
                                       isMC = True, nEvts = 49144274 ),
    'DY_amcatnlo_Winter17' : tnpSample('DY_amcatnlo_Winter17', 
                                       myinputDir + 'mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_DYToLL_mcAtNLO_Moriond17.root',
                                       isMC = True, nEvts = 28968252 ),

    'data_Run2016B' : tnpSample('data_Run2016B' , myinputDir + 'data/SingleElectron/TnPTree_SingleElectron_2016rereco_RunB.root' , lumi = 5.788 ),
    'data_Run2016C' : tnpSample('data_Run2016C' , myinputDir + 'data/SingleElectron/TnPTree_SingleElectron_2016rereco_RunC.root' , lumi = 2.573 ),
    'data_Run2016D' : tnpSample('data_Run2016D' , myinputDir + 'data/SingleElectron/TnPTree_SingleElectron_2016rereco_RunD.root' , lumi = 4.248 ),
    'data_Run2016E' : tnpSample('data_Run2016E' , myinputDir + 'data/SingleElectron/TnPTree_SingleElectron_2016rereco_RunE.root' , lumi = 4.009 ),
    'data_Run2016F' : tnpSample('data_Run2016F' , myinputDir + 'data/SingleElectron/TnPTree_SingleElectron_2016rereco_RunF.root' , lumi = 3.102 ),
    'data_Run2016G' : tnpSample('data_Run2016G' , myinputDir + 'data/SingleElectron/TnPTree_SingleElectron_2016rereco_RunG.root' , lumi = 7.540 ),
    'data_Run2016H' : tnpSample('data_Run2016H' , myinputDir + 'data/SingleElectron/TnPTree_SingleElectron_2016prompt_RunH.root' , lumi = 8.606 ),
    }

Moriond17_80X_HN_leg1 = {
    ### MiniAOD TnP for IDs scale factors
    'DY_madgraph_Winter17' : tnpSample('DY_madgraph_Winter17', 
                                       myinputDir_leg1 + 'mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_DYToLL_madgraph_Moriond17.root',
                                       isMC = True, nEvts = 49144274 ),
    'DY_amcatnlo_Winter17' : tnpSample('DY_amcatnlo_Winter17', 
                                       myinputDir_leg1 + 'mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_DYToLL_mcAtNLO_Moriond17.root',
                                       isMC = True, nEvts = 28968252 ),

    'data_Run2016B' : tnpSample('data_Run2016B' , myinputDir_leg1 + 'data/TnPTree_SingleElectron_2016rereco_RunB.root' , lumi = 5.788 ),
    'data_Run2016C' : tnpSample('data_Run2016C' , myinputDir_leg1 + 'data/TnPTree_SingleElectron_2016rereco_RunC.root' , lumi = 2.573 ),
    'data_Run2016D' : tnpSample('data_Run2016D' , myinputDir_leg1 + 'data/TnPTree_SingleElectron_2016rereco_RunD.root' , lumi = 4.248 ),
    'data_Run2016E' : tnpSample('data_Run2016E' , myinputDir_leg1 + 'data/TnPTree_SingleElectron_2016rereco_RunE.root' , lumi = 4.009 ),
    'data_Run2016F' : tnpSample('data_Run2016F' , myinputDir_leg1 + 'data/TnPTree_SingleElectron_2016rereco_RunF.root' , lumi = 3.102 ),
    'data_Run2016G' : tnpSample('data_Run2016G' , myinputDir_leg1 + 'data/TnPTree_SingleElectron_2016rereco_RunG.root' , lumi = 7.540 ),
    'data_Run2016H' : tnpSample('data_Run2016H' , myinputDir_leg1 + 'data/TnPTree_SingleElectron_2016prompt_RunH.root' , lumi = 8.606 ),
    }

Moriond17_80X_HN_leg2 = {
    ### MiniAOD TnP for IDs scale factors
    'DY_madgraph_Winter17' : tnpSample('DY_madgraph_Winter17', 
                                       myinputDir_leg2 + 'mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_DYToLL_madgraph_Moriond17.root',
                                       isMC = True, nEvts = 49144274 ),
    'DY_amcatnlo_Winter17' : tnpSample('DY_amcatnlo_Winter17', 
                                       myinputDir_leg2 + 'mc/TnPTree_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_DYToLL_mcAtNLO_Moriond17.root',
                                       isMC = True, nEvts = 28968252 ),

    'data_Run2016B' : tnpSample('data_Run2016B' , myinputDir_leg2 + 'data/TnPTree_SingleElectron_2016rereco_RunB.root' , lumi = 5.788 ),
    'data_Run2016C' : tnpSample('data_Run2016C' , myinputDir_leg2 + 'data/TnPTree_SingleElectron_2016rereco_RunC.root' , lumi = 2.573 ),
    'data_Run2016D' : tnpSample('data_Run2016D' , myinputDir_leg2 + 'data/TnPTree_SingleElectron_2016rereco_RunD.root' , lumi = 4.248 ),
    'data_Run2016E' : tnpSample('data_Run2016E' , myinputDir_leg2 + 'data/TnPTree_SingleElectron_2016rereco_RunE.root' , lumi = 4.009 ),
    'data_Run2016F' : tnpSample('data_Run2016F' , myinputDir_leg2 + 'data/TnPTree_SingleElectron_2016rereco_RunF.root' , lumi = 3.102 ),
    'data_Run2016G' : tnpSample('data_Run2016G' , myinputDir_leg2 + 'data/TnPTree_SingleElectron_2016rereco_RunG.root' , lumi = 7.540 ),
    'data_Run2016H' : tnpSample('data_Run2016H' , myinputDir_leg2 + 'data/TnPTree_SingleElectron_2016prompt_RunH.root' , lumi = 8.606 ),
    }
