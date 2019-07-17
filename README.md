# AERMOD_Framework
This framework is designed to help people who are doing air quality analysis 
simulations to simply set parameters to write the inputs, run, and process 
the outputs of AERMOD. 

OPERATING SYSTEM: Windows (versions of AERPLOT and AERMOD needed for other OS)

PYTHON VERSION: Python 3.x (should work with 2.7 also)

DEPENDENCIES: openpyxl

The requirements to run this framework is that you need to have meteorological data
already processed by AERMET. Once you have processed AERMET data, this framework is
fully ready to be used. AERMAP isn't required to run this framework, but the program
can accept AERMAP data and use it in AERMOD runs if specified.

run_framework.py contains in depth detail about the parameters used to run the framework,
and should be used as a reference for how the framework works and for more information
about the outputs.

Denver_Airport_Example contains a fully running example of the framework that is ready 
to run as is. There is more information in the README in the Denver_Airport_Example 
folder.

Authors:
Max Nyffenegger,
Matthew Alongi,
Joseph Kasprzyk.

AERMOD.exe version: 18081

AERPLOT.exe version: 13329

AERMOD and AERPLOT are published by the U.S. Environmental Protection Agency and are publicly
available to download on their website (epa.gov).
