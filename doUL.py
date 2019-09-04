import os, time

#python tnpEGM_fitter.py etc/config/settings_et_HLT.py --flag passTrackIsoLeg1 --doCutCount --onlyDoPlot --plotX et

#variables = ['eta','nvtx','et', 'phi']
variables = ['phi']
procedure = ['--checkBins --onlyDoPlot --plotX', '--createBins --onlyDoPlot --plotX', '--doCutCount --onlyDoPlot --plotX']

#### HLT_Ele32_WPTight
base = 'hltEle32WPTight'
filters  = ['hltEGL1SingleEGOr', 'hltEG32L1SingleEGOrEt', base + 'ClusterShape', base + 'HE', base + 'EcalIso', base + 'HcalIso', base + 'PixelMatch', base + 'PMS2', base + 'GsfOneOEMinusOneOP', base + 'GsfMissingHits', base + 'GsfDeta', base + 'GsfDphi', base + 'GsfTrackIso']

#### HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL
base = 'hltEle23Ele12CaloIdLTrackIdLIsoVL'
filters += ['hltEGL1SingleAndDoubleEGOrPair', base + 'EtLeg1', base + 'ClusterShapeLeg1', base + 'HELeg1', base + 'EcalIsoLeg1', base + 'HcalIsoLeg1', base + 'PixelMatchLeg1', base + 'OneOEMinusOneOPLeg1', base + 'DetaLeg1', base + 'DphiLeg1', base + 'TrackIsoLeg1',
                                              base + 'EtLeg2', base + 'ClusterShapeLeg2', base + 'HELeg2', base + 'EcalIsoLeg2', base + 'HcalIsoLeg2', base + 'PixelMatchLeg2', base + 'OneOEMinusOneOPLeg2', base + 'DetaLeg2', base + 'DphiLeg2', base + 'TrackIsoLeg2']


for var in variables:
  for filter in filters: 
    commands = []
    for step in procedure:
      commands.append('python tnpEGM_fitter.py etc/config/settings_' + var + '_HLT_UL.py --flag pass' + filter[0].capitalize() + filter[1:] + ' ' + step + ' ' + var)
    os.system('(' + ';'.join(commands) + ') &')
    time.sleep(30)
