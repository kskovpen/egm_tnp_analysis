#!bin/bash 

# Setup for lxplus
if [[ $(hostname -s) = lxp* ]]; then
  . /opt/rh/python27/enable
  export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64/:$LD_LIBRARY_PATH
  export PYTHONPATH=.:$PYTHONPATH

# Setup for somewhere else (just get some CMSSW release which works, slow but it gets the job done)
else
  returnPath=$(pwd)
  tempDir=$(mktemp -d /tmp/XXXXXXXXX)
  cd $tempDir
  scram p CMSSW CMSSW_10_2_22
  cd CMSSW_10_2_22/src
  eval `scram runtime -sh`
  cd $returnPath
fi
