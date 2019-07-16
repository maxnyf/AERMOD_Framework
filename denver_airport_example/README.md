This is an example of the framework working with meteorological data from the
denver international airport. The coordinates for aerplot also plot to the 
denver international airport. The framework is currently set to a grid 
receptor system and to run aerplot to create a contour plot of the 
emission concentration data over the airport

You will need to add the following files to the folder with the
run_framework_den.py file and the '.pfl' and '.sfc' files:
aermod.exe
aerplot.exe
mainframe.py
output_processing_functions.py
input_script_functions.py

There is an example of a random source coordinate and random emission rate
maker in the code. To activate the part, remove all the comments, '#'s in front 
of the code below the section labeled 
"RANDOMLY ASSIGNING SOURCE COORDINATES AND EMISSION RATES EXAMPLES"
You will also need to remove all the comment statements before *all* the 
import statements at the top of the page