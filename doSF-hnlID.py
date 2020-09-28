#!/bin/env python3
import subprocess, os, argparse,time

#
# Argparser
#
parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--createHists', action='store_true', help = 'Create histograms')
parser.add_argument('--all', action='store_true', help = 'Do all type of fits (nominal, altBkg and altSig)')
parser.add_argument('--altSig', action='store_true', help = 'Do altSig fits')
parser.add_argument('--altBkg', action='store_true', help = 'Do altBkg fits') 
parser.add_argument('--nominal', action='store_true', help = 'Do nominal fits')
parser.add_argument('--sumUp', action='store_true', help = 'Create the final SF plots')
parser.add_argument('--year', default=None, help = 'Only for specific era')
parser.add_argument('--iBin', type = int, default=-1, help='bin number (to refit individual bin)')
args = parser.parse_args()


#
# System and cream02 commands
#
def system(command):
  print(command)
  return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()

def makeDir(filename):
  dirname = os.path.dirname(filename)
  try:    os.makedirs(dirname)
  except: pass

def cream02(command, logFile):
  dir = os.getcwd()
  qsubOptions = ['-v dir=%s,command="%s"' % (dir, 'source etc/scripts/setup.sh;%s' % command),
                 '-q localgrid@cream02',
                 '-e %s' % logFile,
                 '-o %s' % logFile,
                 '-l walltime=15:00:00']
  makeDir(logFile)
  try:
    out = system('qsub %s etc/scripts/runOnCream02.sh' % ' '.join(qsubOptions))
    if not out.count('.cream02.iihe.ac.be'):
      time.sleep(10)
      cream02(command, logFile)
  except subprocess.CalledProcessError as e:
    time.sleep(10)
    cream02(command, logFile)


#
# Settings
#
settings      = 'settings_HNL.py'
workingpoints = {'2016': 'HNLprompt', '2017': 'HNLprompt', '2018': 'HNLprompt'}

#
# Workflow
#
for era, workingpoint in workingpoints.items():
    if args.year and args.year != era: continue

    baseCommand = 'python tnpEGM_fitter.py etc/config/%s --flag=%s --configOpts="era=%s"' % (settings, workingpoint, era)
    selectBin   = ('--iBin %s' % args.iBin) if args.iBin >= 0 else ''

    if args.createHists:
      system('%s --checkBins' % (baseCommand))
      system('%s --createBins' % (baseCommand))
      for sample in ['data' , 'mcNom', 'mcAlt', 'tagSel']:
        logFile = 'log/createHists/%s-%s-%s' % (workingpoint, sample, era)
        cream02('%s --createHists --sample=%s' % (baseCommand, sample), logFile)

    if args.all or args.nominal:
      logFile = 'log/fits-nominal/%s-%s' % (workingpoint, era)
      cream02('%s --doFit %s' % (baseCommand, selectBin), logFile)
    if args.all or args.altSig:
      logFile = 'log/fits-altSig-mc/%s-%s' % (workingpoint, era)
      cream02('%s --doFit --mcSig --altSig %s;%s --doFit --altSig %s' % (baseCommand, selectBin, baseCommand, selectBin), logFile)
    if args.all or args.altBkg:
      logFile = 'log/fits-altBkg/%s-%s' % (workingpoint, era)
      cream02('%s --doFit --altBkg %s' % (baseCommand, selectBin), logFile)
     
    # Then sum up
    if args.sumUp:
      system('%s --sumUp' % (baseCommand))
