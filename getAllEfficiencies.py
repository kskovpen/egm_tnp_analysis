#! /usr/bin/env python
import os

filesAndFlags = [('settings_HLT_Ele23_Ele12.py',      'passingEtLeg1Ele23Ele12'),
                 ('settings_HLT_Ele23_Ele12.py',      'passingEtLeg2Ele23Ele12'),
                 ('settings_HLT_DoubleEle33.py',      'passingSeededDouble33'),
                 ('settings_HLT_DoubleEle33.py',      'passingUnseededDouble33'),
                 ('settings_HLT_Ele32.py',            'passingEtEle32WPTight'),
                ]

for f, flag in filesAndFlags:
  for binning in ['pt_vs_eta', 'eta_vs_pt', 'eta_vs_phi', 'eta_vs_nvtx']:
    os.system("python tnpEGM_fitter.py etc/config/" + f + " --flag " + flag + " --settingsOpt='" + binning + "' --checkBins")
    os.system("python tnpEGM_fitter.py etc/config/" + f + " --flag " + flag + " --settingsOpt='" + binning + "' --createBins")
    os.system("python tnpEGM_fitter.py etc/config/" + f + " --flag " + flag + " --settingsOpt='" + binning + "' --createHists")
