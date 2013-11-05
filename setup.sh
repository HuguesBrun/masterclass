#!/bin/bash
# SETUP ROOT
source /afs/cern.ch/sw/lcg/contrib/gcc/4.6/x86_64-slc5/setup.sh
source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.34.09/x86_64-slc5-gcc46-opt/root/bin/thisroot.sh
# SETUP PYTHON & PYROOT
export PYTHONDIR=/afs/cern.ch/sw/lcg/external/Python/2.6.5p2/x86_64-slc5-gcc46-opt
export PATH=${PYTHONDIR}/bin:${PATH}
export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH