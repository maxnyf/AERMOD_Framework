from input_script_functions import *
from output_processing_functions import *
from os import system
from sys import exit
from time import time
from openpyxl import Workbook
__author__ = 'Max'


# all parameters are defined in depth in run_framework.py
def run_aermod_framework(surface_observations_file,
                         upper_air_data_file,
                         source_coordinate_list_x,
                         source_coordinate_list_y,
                         source_release_height_list,
                         source_emission_rate_list,
                         source_type,
                         source_area_x_direction_length_list,
                         source_area_y_direction_length_list,
                         source_point_stack_gas_exit_temperature_list,
                         source_point_stack_gas_exit_velocity_list,
                         source_point_stack_inside_diameter_list,
                         met_data_start_year,
                         receptor_style,
                         receptor_coordinate_list_x,
                         receptor_coordinate_list_y,
                         receptor_grid_starting_point_x,
                         receptor_grid_starting_point_y,
                         receptor_grid_number_receptors_x,
                         receptor_grid_number_receptors_y,
                         receptor_grid_spacing_x,
                         receptor_grid_spacing_y,
                         base_elevation,
                         uair_data_station_number,
                         surf_data_station_number,
                         receptor_aermap_output_file_name=None,
                         source_aermap_output_file_name=None,
                         run_aerplot='no',
                         aerplot_northing=None,
                         aerplot_easting=None,
                         aerplot_UTM_zone=None,
                         aerplot_northern_hemisphere=None
                         ):


    # Simple setup to see time it took for program to run
    start_time = time()

    # ********* INPUT CHECKS **************
    number_sources = len(source_coordinate_list_x)
    number_receptors = len(receptor_coordinate_list_x)

    # running the check_source_data_for_length on parameters
    #   if there is only one data point, copies to correct number of source points
    #   also checks if data is valid, returns a string if data is not valid
    source_emission_rate_list = check_source_data_for_length(source_emission_rate_list, number_sources)
    source_release_height_list = check_source_data_for_length(source_release_height_list, number_sources)
    source_area_x_direction_length_list = check_source_data_for_length(source_area_x_direction_length_list,
                                                                       number_sources)
    source_area_y_direction_length_list = check_source_data_for_length(source_area_y_direction_length_list,
                                                                       number_sources)
    source_point_stack_gas_exit_temperature_list = \
        check_source_data_for_length(source_point_stack_gas_exit_temperature_list, number_sources)
    source_point_stack_gas_exit_velocity_list = \
        check_source_data_for_length(source_point_stack_gas_exit_velocity_list, number_sources)
    source_point_stack_inside_diameter_list = \
        check_source_data_for_length(source_point_stack_inside_diameter_list, number_sources)

    # runs check_for_valid_inputs to check if check_source_data_for_length returned an error for any input
    valid_inputs_result = check_for_valid_inputs(source_coordinate_list_x,
                                                 source_coordinate_list_y,
                                                 source_type,
                                                 source_emission_rate_list,
                                                 source_release_height_list,
                                                 source_area_x_direction_length_list,
                                                 source_area_y_direction_length_list,
                                                 source_point_stack_gas_exit_temperature_list,
                                                 source_point_stack_gas_exit_velocity_list,
                                                 source_point_stack_inside_diameter_list,
                                                 receptor_coordinate_list_y,
                                                 receptor_coordinate_list_x
                                                 )

    # exits the program if there is any problems in the inputs
    if not valid_inputs_result:
        print('errors exist in inputs, exiting program')
        exit()

    # ***** CREATING AERMOD INPUT FILE *****
    write_aermod_input_file(surface_observations_file,
                            upper_air_data_file,
                            source_coordinate_list_x,
                            source_coordinate_list_y,
                            source_release_height_list,
                            source_emission_rate_list,
                            source_type,
                            source_area_x_direction_length_list,
                            source_area_y_direction_length_list,
                            source_point_stack_gas_exit_temperature_list,
                            source_point_stack_gas_exit_velocity_list,
                            source_point_stack_inside_diameter_list,
                            met_data_start_year,
                            receptor_style,
                            receptor_coordinate_list_x,
                            receptor_coordinate_list_y,
                            receptor_grid_starting_point_x,
                            receptor_grid_starting_point_y,
                            receptor_grid_number_receptors_x,
                            receptor_grid_number_receptors_y,
                            receptor_grid_spacing_x,
                            receptor_grid_spacing_y,
                            base_elevation,
                            uair_data_station_number,
                            surf_data_station_number,
                            receptor_aermap_output_file_name[0],
                            source_aermap_output_file_name[0],
                            run_aerplot
                            )

    # ***** CREATING AERPLOT INPUT FILE *****
    if run_aerplot == 'yes':
        write_aerplot_input_file(easting=aerplot_easting,
                                 northing=aerplot_northing,
                                 utm_zone=aerplot_UTM_zone,
                                 northern_hemisphere=aerplot_northern_hemisphere,
                                 google_earth_display_name="aerplot_output",
                                 plot_file_name="aerplot_data.PLT",
                                 output_file_name="aerplot_output")

    # ***** RUNNING AERMOD *****
    # for running on linux you will need a version of aermod compiled for linux, add a ./ in front of aermod
    system("aermod.exe >nul")

    # if aerplot is set to run, runs aerplot as well
    if run_aerplot == 'yes':
        system("aerplot.exe >nul")

    # ***** PROCESSING OUTPUTS *****
    # @@@@@@@@ only processes outputs if in discrete receptor type @@@@@@@@@@@
    if receptor_style == 'discrete':
        # setting up spreadsheet and output file data
        output_file_name = 'aermod.out'
        output_workbook = Workbook()
        output_spreadsheet = output_workbook.active
        output_spreadsheet.title = "Data"

        # setting up spreadsheet headers
        spreadsheet_setup(number_receptors,output_spreadsheet, receptor_coordinate_list_x, receptor_coordinate_list_y)

        # setting up list of times that the concentration was analyzed at
        find_time_lines(output_file_name, output_spreadsheet)

        # adding concentrations from all receptors to excel spreadsheet
        find_concentration_lines(output_file_name, number_receptors, output_spreadsheet)

        # Saving workbook to excel file and printing runtime of program
        output_workbook.save("AERMOD concentration outputs.xlsx")
    run_time = time() - start_time
    print("Program runtime: " + str(int(run_time / 60)) + " minutes " + str(int(run_time % 60)) + " seconds")
