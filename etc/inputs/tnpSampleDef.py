from libPython.tnpClassUtils import tnpSample

samples2018 = {
    'DY' : tnpSample('DY', '/user/tomc/eleHLT/tnpTuples/2018/DY.root', isMC = True, nEvts = -1),
    'Run2018A' : tnpSample('Run2018A', '/user/tomc/eleHLT/tnpTuples/2018/2018A.root', lumi = 13.48),  # lumi taken from https://twiki.cern.ch/twiki/bin/view/CMS/PdmV2018Analysis#DATA 
    'Run2018B' : tnpSample('Run2018B', '/user/tomc/eleHLT/tnpTuples/2018/2018B.root', lumi = 6.785),
    'Run2018C' : tnpSample('Run2018C', '/user/tomc/eleHLT/tnpTuples/2018/2018C.root', lumi = 6.612),
    'Run2018D' : tnpSample('Run2018D', '/user/tomc/eleHLT/tnpTuples/2018/2018D.root', lumi = 31.95),
    }
