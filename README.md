# AERMOD_Framework
This framework is designed around AERMOD to fully streamline emissions modeling. 
This framework will write the input file, run AERMOD, and process the outputs into 
an excel spreadsheet or into a contour plot using AERPLOT.

OPERATING SYSTEM: Windows (versions of AERPLOT and AERMOD needed for other OS)
PYTHON VERSION: Python 3.x
DEPENDENCIES: openpyxl

The requirements to run this framework is that you need to have meteorological data
already processed by AERMET. Once you have processed AERMET data, this framework is
fully ready to be used. AERMAP isn't required to run this framework, but the program
can accept AERMAP data and use it in AERMOD runs if specified.
