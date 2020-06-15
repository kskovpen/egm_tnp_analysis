from libPython.tnpClassUtils import tnpSample
import os

# tnpTuple top directory
tnpTuplesDirectory = '/eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-06-09' # on lxplus
tnpTuplesDirectory = '/pnfs/iihe/cms/store/user/tomc/tnpTuples/2020-06-09'        # on T2_BE_IIHE

# 2016
dir2016 = os.path.join(tnpTuplesDirectory, '2016/merged')
samples = [
  tnpSample('2016_DY_LO',  os.path.join(dir2016, 'DY_LO.root'),    isMC = True),
  tnpSample('2016_DY_NLO', os.path.join(dir2016, 'DY_NLO.root'),   isMC = True),
  tnpSample('Run2016B',    os.path.join(dir2016, 'Run2016B.root'), lumi = 5.785),
  tnpSample('Run2016C',    os.path.join(dir2016, 'Run2016C.root'), lumi = 2.573),
  tnpSample('Run2016D',    os.path.join(dir2016, 'Run2016D.root'), lumi = 4.248),
  tnpSample('Run2016E',    os.path.join(dir2016, 'Run2016E.root'), lumi = 3.947),
  tnpSample('Run2016F',    os.path.join(dir2016, 'Run2016F.root'), lumi = 3.102),
  tnpSample('Run2016G',    os.path.join(dir2016, 'Run2016G.root'), lumi = 7.540),
  tnpSample('Run2016H',    os.path.join(dir2016, 'Run2016H.root'), lumi = 7.813),
]

# 2017
dir2017 = os.path.join(tnpTuplesDirectory, '2017/merged')
samples += [
  tnpSample('2017_DY_LO',      os.path.join(dir2017, 'DY_LO.root'),     isMC = True),
  tnpSample('2017_DY_LO_ext',  os.path.join(dir2017, 'DY_LO_ext.root'), isMC = True),
  tnpSample('2017_DY_NLO',     os.path.join(dir2017, 'DY_NLO.root'),     isMC = True),
  tnpSample('2017_DY_NLO_ext', os.path.join(dir2017, 'DY_NLO_ext.root'), isMC = True),
  tnpSample('Run2017B',        os.path.join(dir2017, 'Run2017B.root'),   lumi = 4.793),
  tnpSample('Run2017C',        os.path.join(dir2017, 'Run2017C.root'),   lumi = 9.753),
  tnpSample('Run2017D',        os.path.join(dir2017, 'Run2017D.root'),   lumi = 4.320),
  tnpSample('Run2017E',        os.path.join(dir2017, 'Run2017E.root'),   lumi = 8.802),
  tnpSample('Run2017F',        os.path.join(dir2017, 'Run2017F.root'),   lumi = 13.567),
]

# 2018
dir2018 = os.path.join(tnpTuplesDirectory, '2018/merged')
samples += [
  tnpSample('2018_DY_NLO', os.path.join(dir2018, 'DY_NLO.root'),   isMC = True),
  tnpSample('2018_DY_pow', os.path.join(dir2018, 'DY_pow.root'),   isMC = True),
  tnpSample('Run2018A' ,   os.path.join(dir2018, 'Run2018A.root'), lumi = 10.723),
  tnpSample('Run2018B' ,   os.path.join(dir2018, 'Run2018B.root'), lumi = 5.964),
  tnpSample('Run2018C' ,   os.path.join(dir2018, 'Run2018C.root'), lumi = 6.382),
  tnpSample('Run2018D' ,   os.path.join(dir2018, 'Run2018D.root'), lumi = 29.181),
]

# UL2017
  # to add (they are already available at /eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-05-20)

# UL2018
  # to add (they are already available at /eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-05-20)

#
# This function returns one of the above tnpSample based on the name (first argument in each tnpSample)
# If you give it a list, it adds them up (useful for adding multiple data runs)
#
def getSample(name, rename=None):
  if isinstance(name, list):
    summedSample = getSample(name[0]).clone()
    for i in name[1:]:
      summedSample.add_sample(getSample(i))
    toReturn = summedSample
  else:
    for i in samples:
      if i.name==name:
        toReturn = i.clone()
        break
  if rename: toReturn.rename(rename)
  return toReturn
