from libPython.tnpClassUtils import tnpSample

UL = {
    'data' :  tnpSample('UL',     '/user/tomc/eleHLT/tnpTuples/UL/TnPTree_mc.root', isMC = True),
    '94X' :   tnpSample('94X',    '/user/tomc/eleHLT/tnpTuples/UL/comparison.root', isMC = True),
    '102X':   tnpSample('102X',   '/user/tomc/eleHLT/tnpTuples/UL/TnPTree_mc_PUpmx25ns_102X_upgrade2018_realistic_v15_ECAL-v1.root', isMC = True),
    '106Xv4': tnpSample('106Xv4', '/user/tomc/eleHLT/tnpTuples/UL/TnPTree_mc_PUpmx25ns_106X_upgrade2018_realistic_v4-v1.root', isMC = True),
    '106Xv6': tnpSample('106Xv6', '/user/tomc/eleHLT/tnpTuples/UL/TnPTree_mc_PUpmx25ns_106X_upgrade2018_realistic_v6_ul18hlt_premix_hs-v1.root', isMC = True),
    '106Xv6rs': tnpSample('106Xv6(rs)', '/user/tomc/eleHLT/tnpTuples/UL/TnPTree_mc_PUpmx25ns_106X_upgrade2018_realistic_v6_ul18hlt_premix_rs-v1.root', isMC = True),
    }

UL['data'].is2018def = True   # neede for all the newly produced samples to catch for a change in tree variable name
UL['94X'].is2018def = True
UL['102X'].is2018def = True
UL['106Xv4'].is2018def = True
UL['106Xv6'].is2018def = True
UL['106Xv6rs'].is2018def = True

EGamma2018 = {
    'DY' : tnpSample('DY', '/user/tomc/eleHLT/tnpTuples/2018/DY.root', isMC = True),
    'data_Run2018' : tnpSample('data_Run2018' , '/user/tomc/eleHLT/tnpTuples/2018/2018.root', lumi = 58.9),
    }

EGamma2018['DY'].is2018def = True
EGamma2018['data_Run2018'].is2018def = True

EGamma2017 = {
    'data_Run2017' : tnpSample('data_Run2017' , '/user/tomc/eleHLT/tnpTuples/2017/2017SE.root', lumi = 1.0),
    }

EGamma2016 = {
    'data_Run2016' : tnpSample('data_Run2016' , '/user/tomc/eleHLT/tnpTuples/2016/2016SE.root', lumi = 1.0),
    }

EGamma2016['data_Run2016'].set_cut('!(run >= 276453 && run <=278822)')
