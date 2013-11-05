#!/bin/bash
HEPTutorialDIR=../HEPTutorial

for object in `echo "MyElectron MyJet MyMuon MyPhoton"`
do
	if [[ ! -f ${object}.C ]] 
	then
		ln -s ${HEPTutorialDIR}/${object}.{C,h} .
		echo .L ${object}.C+ | root.exe -l -b
	fi
done

ln -s -d ${HEPTutorialDIR}/files .

