#!/bin/bash
HEPTutorialDIR=../HEPTutorial

for object in `echo "MyElectron MyJet MyMuon MyPhoton"`
do
	ln -s ${HEPTutorialDIR}/${object}.{C,h} .
	echo .L ${object}.C+ | root.exe -l -b
done
