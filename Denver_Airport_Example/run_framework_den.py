from mainframe import run_aermod_framework
# # imports for randomly assigning source data example
# from random import random
# from random import seed
# from math import pi
# from math import cos
# from math import sin
# from time import time
__author__ = 'Max'

# DENVER INTERNATIONAL AIRPORT EXAMPLE PROGRAM
# The meteorological data in this script comes from the Denver Airport weather station
# There is currently a grid system setup to show functionality of aerplot plotting.

# @@@ RANDOM SOURCE COORDINATE AND EMISSION MAKER @@@
# to activate this section of code, uncomment lines 3-8 and lines 209-235
# this randomly creates source emittors in a circular radius around the origin, with a specified emission range
# parameters for setting up this section start at line 209

# run_framework.py is the interface for the framework, and calls the run_framework function that runs mainframe
# mainframe.py is the framework, it checks inputs, writes the input files, runs AERMOD and processes the outputs
# input_script_functions contains all functions to write AERMOD/AERPLOT input files and check inputs
# output_processing_functions contains all functions to process AERMOD output files
#   more details about output processing are presented below, refer to the receptor_style and run_aerplot variables

# the overview of the framework is easily allowing one to add emission sources in discrete locations and assigning
#   them emission rates, which AERMOD will use to predict concentrations at locations also specified by the user. This
#   framework also processes the output data, currently set to hourly averages for a year of data, into a spreadsheet
#   to easily be used to create graphs, analyze maxima or anything else. The output spreadsheet is currently configured
#   to neatly display the time information and yearly average information. If wanted, one can easily go into excel and
#   delete all the columns that don't contain emission concentration data.
# concentration data that aermod produces is in the form *****micrograms per meter cubed******

# meteorological data comes from AERMET processor
# AERMET will be needed to obtain meteorological data used for AERMOD
# processing meteorological data with AERMET is the *only* requirement to run this framework
# AERMOD is currently set to calculate all 1-hour concentration averages for a given year of meteorological data
# To change this, go to the writing control and output lines functions in input_script_functions.py

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@ INPUT OPTIONS @@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Name of the surface observations file
# Mandatory, file type: SFC
# Enter as string data type
surface_observations_file = 'DEN_2016.SFC'

# Name of the upper air observations file
# Mandatory, file type: PFL
# Enter as string data type
upper_air_data_file = 'DEN_2016.PFL'

# list of pollutant source points coordinates in meters
# INPUT LIST OF X COORDINATES IN source_x_points AND Y COORDINATES IN source_y_points
# INDEXES WILL CORRESPOND TO EACH OTHER IN THE TWO LISTS
# LISTS MUST BE MATCHING LENGTH
source_coordinate_list_x = [100, 200, -1032.2, -370.6]
source_coordinate_list_y = [100, -489, 55.6, -622.2]

# list of pollutant source release heights in meters
# can be a single data point in which case the value will be applied to EVERY pollutant source
# if manually entering each height, must be the exact same length as the source_x_points/source_y_points
#   each height will be associated to the source with the same index as in the coordinate list
source_release_height_list = [2]

# list of emission rates that will correspond to the source points list
# can be a single data point in which case the value will be applied to EVERY pollutant source
# if manually entering each rate, must be the exact same length as the source_x_points/source_y_points
#   each rate will be associated to the source with the same index as in the coordinate list
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# $$**** IF USING POINT SOURCE, WILL BE INTERPRETED IN GRAMS PER SECOND ***********************$$
# $$**** IF USING AREA SOURCE, WILL BE INTERPRETED IN GRAMS PER SECOND PER METER SQUARED ******$$
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
source_emission_rate_list = [.6232, .2132, 1.004, .1401]

# determines what pollutant source type you want
# data required for simulation depends on what type is chosen
# if point is chosen, all 'source_point_...' data is needed
# if area is chosen, all 'source_area_...' data is needed
# MUST BE EITHER 'point' OR 'area' OR FRAMEWORK WILL NOT WORK
# Enter as string data type
source_type = 'point'

# area source dimensions of area source polluters, in meters
# this will determine the size of the pollutant source and the emission rate,
#   since emissions for area sources are in g/s/m^2,
# ONLY NEEDED IF USING AREA SOURCE, IF NOT NEEDED SET EQUAL TO 'None'
# can be a single data point in which case the value will be applied to EVERY pollutant source
# if manually entering each value, must be the exact same length as the source_x_points/source_y_points
#   each value will be associated to the source with the same index as in the coordinate list
source_area_x_direction_length_list = [15.6]
source_area_y_direction_length_list = [18.3]

# temperature of gas from the point source as it exits
# UNITS ARE IN ***KELVIN***, ENTER 0 TO JUST USE AMBIENT TEMPERATURE
# ONLY NEEDED IF USING POINT SOURCE, IF NOT NEEDED SET EQUAL TO 'None'
# can be a single data point in which case the value will be applied to EVERY pollutant source
# if manually entering each value, must be the exact same length as the source_x_points/source_y_points
#   each value will be associated to the source with the same index as in the coordinate list
source_point_stack_gas_exit_temperature_list = [0]

# velocity of gas from the point source as it exits
# units are in meters/second
# ONLY NEEDED IF USING POINT SOURCE, IF NOT NEEDED SET EQUAL TO 'None'
# can be a single data point in which case the value will be applied to EVERY pollutant source
# if manually entering each value, must be the exact same length as the source_x_points/source_y_points
#   each value will be associated to the source with the same index as in the coordinate list
source_point_stack_gas_exit_velocity_list = [20.1]

# diameter of pollutant stack from point source emittor
# units are in meters
# ONLY NEEDED IF USING POINT SOURCE, IF NOT NEEDED SET EQUAL TO 'None'
# can be a single data point in which case the value will be applied to EVERY pollutant source
# if manually entering each value, must be the exact same length as the source_x_points/source_y_points
#   each value will be associated to the source with the same index as in the coordinate list
source_point_stack_inside_diameter_list = [1.2]

# the year the meteorological data starts
# Should reflect meteorological data
met_data_start_year = '2016'

# there are two options for receptor styles
# the first is discrete in which you put in the coordinates you want AERMOD to calculate concentrations at
# the second is grid in which AERMOD calculates concentrations in a full grid
#   grid simulations can take a lot longer since there are much more receptor locations
# either enter 'discrete' or 'grid'
# for discrete you only have to enter the receptor_coordinate_list_... variables
# for grid you have to enter all receptor_grid_... variables
# EXTRACTING CONCENTRATION DATA TO EXCEL SPREADSHEET ONLY WORKS WITH DISCRETE COORDINATES
receptor_style = 'grid'

# coordinate list of discrete receptors in METERS
# enter as many as you want, enter as lists of numbers
# length of each list must match
# the index of each coordinate in each list will correspond to the index of the coordinate in the other list
# if using grid receptors, enter as None
receptor_coordinate_list_x = [0, 70.3,   225.5, -405.6, -334.1]
receptor_coordinate_list_y = [0, 101.1, -299.1, 368.7,  -545.2]

# the starting coordinate for the x and y receptors
# the first receptor will be at this location, followed by as many receptors specified at the spacing distance
# entered in meters
# hint: enter negative coordinate so receptors form a grid around the origin
receptor_grid_starting_point_x = -3000
receptor_grid_starting_point_y = -3000

# the number of receptors in the x and y location
# this will determine the size of the grid since there will be as many receptors as specified,
#   seperated by the spacing distance
receptor_grid_number_receptors_x = 21
receptor_grid_number_receptors_y = 21

# this determines the spacing distance between receptors in the x and y direction
# the distance between each receptor multiplied by the number of receptors minus one in each direction (x/y),
#    will determine the size of the grid
# units are in meters
# for example, starting point -1000, number receptors = 21, grid_spacing = 100, the x length of the grid is 2000
receptor_grid_spacing_x = 300
receptor_grid_spacing_y = 300

# the base elevation for the region in the study
# data is MANDATORY by AERMOD
# units are in METERS
base_elevation = '1418.6'

# the station number that the upper air data was collected at
# data is MANDATORY by AERMOD
uair_data_station_number = '72469'

# the station number that the surface data observations were collected at
# data is MANDATORY by AERMOD
surf_data_station_number = '725650'

# if you ran an AERMAP simulation for this scenario
#   enter the names of the source and receptor files that AERMAP outputted
#   these files should be in a txt format
#   example; receptor_aermap_output_file_name='aermap_receptor.txt'
# if AERMAP was not used set both variables to None and the program will run fine
receptor_aermap_output_file_name = None,
source_aermap_output_file_name = None,

# if you want to run AERPLOT to make contour plots of the results
# all you need is information about the location of the area of interest

# for running aerplot, set run_aerplot to 'yes' or 'no'
run_aerplot = 'yes'

# the northing and easting **UTM** coordinates of the location of interest
#  if you don't care about the location that the plot is overlayed in on google earth
#          you can enter 0 for the northing and easting and just see the contour plot on the ocean
# enter the coordinates, or set them to None if not running aerplot
aerplot_northing = '4409278.1'
aerplot_easting = '529264'

# the utm zone for the location of interest
# set to None if not using aerplot
aerplot_UTM_zone = '13'

# if using aerplot, define if in the northern hemisphere or not
# **ENTER ARGUMENT AS A STRING**
# if not using aerplot, set as None. Otherwise, set *ONLY* to 'True' or 'False' with quotations
aerplot_northern_hemisphere = 'True'


####################################################################################
####### RANDOMLY ASSIGNING SOURCE COORDINATES AND EMISSION RATES EXAMPLES ##########
####################################################################################
# # @@@@@@@@@@@@@ UNCOMMENT THE SECTION STARTING HERE @@@@@@@@@@@@@@@@@@@@@@@@@@@
# # parameters
# # assigns coordinates in a circle around the origin with radius of maximum_range
# # @@@ PARAMETERS LIST @@@
# # the total number of emittor sources 
# number_sources = 10  # enter integer
# # the radius around the origin that sources will appear in
# maximum_range = 5280 * .3048  # a mile in meters
# # the range of emissions that will be randomly assigned to each source
# source_emission_rate_range = [.1, 1.3]  # entered as [lower bound, upper bound]
#
# # setup - clearing previous source coordinates and emission entries
# source_coordinate_list_y = []
# source_coordinate_list_x = []
# source_emission_rate_list = []
# emission_rate_range = source_emission_rate_range[1] - source_emission_rate_range[0]
# seed(time())
# for coord in range(number_sources):
#     theta = 2 * pi * random()
#     radius = random() * maximum_range
#     x_coord_temp = cos(theta) * radius
#     y_coord_temp = sin(theta) * radius
#     source_coordinate_list_x.append(x_coord_temp)
#     source_coordinate_list_y.append(y_coord_temp)
#     # randomly assigning emission rates in specified range
#     emission_rate_val_temp = emission_rate_range * random() + source_emission_rate_range[0]
#     source_emission_rate_list.append(emission_rate_val_temp)

# # @@@@@@@@@@@@@@ STOP UNCOMMENTING HERE @@@@@@@@@@@@@@@@@@@
#
# # print(source_coordinate_list_x)
# # print(source_coordinate_list_y)
# # print(source_emission_rate_list)


####################################################################################
####################################################################################
####################################################################################
################################### FUNCTION CALL ##################################
####################################################################################
####################################################################################
####################################################################################

run_aermod_framework(surface_observations_file=surface_observations_file,
                     upper_air_data_file=upper_air_data_file,
                     source_coordinate_list_x=source_coordinate_list_x,
                     source_coordinate_list_y=source_coordinate_list_y,
                     source_release_height_list=source_release_height_list,
                     source_emission_rate_list=source_emission_rate_list,
                     source_type=source_type,
                     source_area_x_direction_length_list=source_area_x_direction_length_list,
                     source_area_y_direction_length_list=source_area_y_direction_length_list,
                     source_point_stack_gas_exit_temperature_list=source_point_stack_gas_exit_temperature_list,
                     source_point_stack_gas_exit_velocity_list=source_point_stack_gas_exit_velocity_list,
                     source_point_stack_inside_diameter_list=source_point_stack_inside_diameter_list,
                     met_data_start_year=met_data_start_year,
                     receptor_style=receptor_style,
                     receptor_coordinate_list_x=receptor_coordinate_list_x,
                     receptor_coordinate_list_y=receptor_coordinate_list_y,
                     receptor_grid_starting_point_x=receptor_grid_starting_point_x,
                     receptor_grid_starting_point_y=receptor_grid_starting_point_y,
                     receptor_grid_number_receptors_x=receptor_grid_number_receptors_x,
                     receptor_grid_number_receptors_y=receptor_grid_number_receptors_y,
                     receptor_grid_spacing_x=receptor_grid_spacing_x,
                     receptor_grid_spacing_y=receptor_grid_spacing_y,
                     base_elevation=base_elevation,
                     uair_data_station_number=uair_data_station_number,
                     surf_data_station_number=surf_data_station_number,
                     receptor_aermap_output_file_name=receptor_aermap_output_file_name,
                     source_aermap_output_file_name=source_aermap_output_file_name,
                     run_aerplot=run_aerplot,
                     aerplot_northing=aerplot_northing,
                     aerplot_easting=aerplot_easting,
                     aerplot_UTM_zone=aerplot_UTM_zone,
                     aerplot_northern_hemisphere=aerplot_northern_hemisphere
                     )
