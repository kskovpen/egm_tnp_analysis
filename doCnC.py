import os

#python tnpEGM_fitter.py etc/config/settings_et_HLT.py --flag passTrackIsoLeg1 --doCutCount --onlyDoPlot --plotX et

variables = ['eta','nvtx','et']
#variables = ['et']
procedure = ['--checkBins --onlyDoPlot --plotX', '--createBins --onlyDoPlot --plotX', '--doCutCount --onlyDoPlot --plotX']

for var in variables:

	for step in procedure:

		os.system('python tnpEGM_fitter.py etc/config/settings_' + var + '_HLT.py --flag passTrackIsoLeg1' + ' ' + step + ' ' + var)
