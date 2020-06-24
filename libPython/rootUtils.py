import ROOT
import math
from fitUtils import *
#from fitSimultaneousUtils import *

from ROOT import RooFit,RooFitResult
from libPython.logger import getLogger
log = getLogger()

def readRootFile(fname):
  if not os.path.exists(os.path.expandvars(fname)):
    log.error('Filename %s does not exist' % fname)
  f = ROOT.TFile(fname, 'read')
  if (f.IsZombie() or f.TestBit(ROOT.TFile.kRecovered) or f.GetListOfKeys().IsEmpty()):
    log.warning('Something wrong with this file: %s' % fname)
  return f

def histPlotter( filename, tnpBin, plotDir ):
    log.info('opening %s' % filename)
    log.info('  get canvas: %s_Canv' % tnpBin['name'])
    rootfile = readRootFile(filename)

    c = rootfile.Get( '%s_Canv' % tnpBin['name'] )
    c.Print( '%s/%s.png' % (plotDir,tnpBin['name']))


def computeEffi( n1,n2,e1,e2):
    if not (n1+n2):
      log.warning('Bin found with no events')
      return [0., 1.]
    effout = []
    eff   = n1/(n1+n2)
    e_eff = 1/(n1+n2)*math.sqrt(e1*e1*n2*n2+e2*e2*n1*n1)/(n1+n2)
    if e_eff < 0.001 : e_eff = 0.001

    effout.append(eff)
    effout.append(e_eff)
    
    return effout

def getEffiFromCutAndCount(fname, bindef):
    rootfile = readRootFile(fname)
    hP = rootfile.Get('%s_Pass'%bindef['name'])
    hF = rootfile.Get('%s_Fail'%bindef['name'])
    bin1 = 11
    bin2 = 70
    eP = ROOT.Double(-1.0)
    eF = ROOT.Double(-1.0)
    nP = hP.IntegralAndError(bin1,bin2,eP)
    nF = hF.IntegralAndError(bin1,bin2,eF)
    rootfile.Close()

    return computeEffi(nP,nF,eP,eF)

def getFitParameter(fnameFit, fit, paramName):
    rootFile = readRootFile(fnameFit)
    fitRes = rootFile.Get(fit)
    try:
      param = fitRes.floatParsFinal().find(paramName)
      return param.getVal(), param.getError()
    except:
      log.error('Did not find %s in fitresults %s in file %s' % (paramName, fit, fnameFit))
    finally:
      rootFile.Close()

def getEffiFromFit(fnameFit, fnameHist, bindef):
    rootfile = readRootFile(fnameFit)

    nP, eP = getFitParameter(fnameFit, '%s_resP' % bindef['name'], 'nSigP')
    nF, eF = getFitParameter(fnameFit, '%s_resF' % bindef['name'], 'nSigF')

    rootfile = readRootFile(fnameHist)
    hP = rootfile.Get('%s_Pass'%bindef['name'])
    hF = rootfile.Get('%s_Fail'%bindef['name'])

    eP = min(eP, math.sqrt(hP.Integral()))
    eF = min(eF, math.sqrt(hF.Integral()))
    rootfile.Close()

    return computeEffi(nP,nF,eP,eF)

import os.path
def getAllEffi(info, bindef):
    effis = {}
    for x in ['mcNominal', 'tagSel', 'mcAlt']:
      effis[x] = getEffiFromCutAndCount(info[x], bindef) if info[x] else [-1, -1]

    for x in ['dataNominal', 'dataAltSig', 'dataAltBkg']:
      effis[x] = getEffiFromFit(info[x], info['data'], bindef) if info[x] else [-1, -1]

    return effis
