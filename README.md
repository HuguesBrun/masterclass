How to use : 
===========

### Get the HEPTutorial tarball and untar it ###

		wget http://ippog.web.cern.ch/sites/ippog.web.cern.ch/files/HEPTutorial.tar_.gz
		tar -xvzf HEPTutorial.tar_.gz

### Setup root and pyroot ###
		
		source setup.sh

### link and compile the classes, it also links the root input files ###

		source mk_links.sh

### run the python script (here for mc_dy.root) ###

		python analysis.py mc_dy

### contemplate the wonderful histogram you did (here in histos_mc_dy.root) ###
