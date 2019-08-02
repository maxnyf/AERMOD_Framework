This folder contains supplemental scripts.

There is more information about how to run each script at the top of the 
script itself, but in general you need to import the function from the script 
in mainframe.py and then add a function call to the script's function at the
bottom of mainframe.py's run_aermod_framework() function. 

map_plotting.py:

DEPENDENCIES: openpyxl, matplotlib, numpy

map_plotting creates a heatmap of AERMOD concentration data from the Excel 
spreadsheet that this framework creates. There are instructions on how to 
run the script in map_plotting.py

Some code in this script comes from the matplotlib website, which I am not claiming is mine.
You can view the code at the link below.
Title: Creating annotated heatmaps,
Availability: https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html#sphx-glr-gallery-images-contours-and-fields-image-annotated-heatmap-py
