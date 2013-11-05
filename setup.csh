#!/bin/csh
source /afs/cern.ch/sw/lcg/contrib/gcc/4.3/x86_64-slc5/setup.csh
source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.32.00/x86_64-slc5-gcc43-opt/root/bin/thisroot.csh 
setenv PYTHONDIR /afs/cern.ch/sw/lcg/external/Python/2.6.5p2/x86_64-slc5-gcc43-opt
setenv PATH ${PYTHONDIR}/bin:${PATH}
setenv LD_LIBRARY_PATH $ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH
setenv PYTHONPATH $ROOTSYS/lib:$PYTHONPATH
