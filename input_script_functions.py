__author__ = 'Max'


# this function writes the initial setting lines for AERMOD
# currently setup to do a yearly average
def write_control_lines(input_file):
    #'''Writing COntrol Pathway Lines'''
    # The only things that might change between runs is the pollutant ID or possible adding 'FLAT' to the MODELOPT kewyword
    title = 'INPUT FILE'
    input_file.write('CO STARTING\n   TITLEONE ' + title + '\n   MODELOPT DFAULT CONC\n')
    # Pathway start, title, and model options
    input_file.write('   AVERTIME 1 ANNUAL\n')
    # Average time periods
    ID = 'POLLUTANT'
    input_file.write('   POLLUTID ' + ID + '\n')
    # Pollutant ID
    input_file.write('   ERRORFIL ERRORS.AER\n')
    input_file.write('   RUNORNOT RUN\nCO FINISHED\n\n')
    # Error file name, run specification, pathway ending


# this function writes lines to establish the receptors for AERMOD
# this function works only with discrete receptor coordinates
# all parameters are defined in run_framework.py
def write_receptor_lines_discrete(disccart_coordinate_list_x,disccart_coordinate_list_y,aermap_receptor_output,input_file):
    input_file.write('RE STARTING\n')
    # Extracting the 'DISCCART' keyword lines from the AERMAP receptor output if available
    if aermap_receptor_output:
        aermap_receptor_output_lines = []

        # Copying the lines we need from the aermap output file
        for line in open(aermap_receptor_output):
            if '**' not in line:
                aermap_receptor_output_lines.append(line)
        del aermap_receptor_output_lines[0]

        # Writing these lines to the input file
        for receptor_line in aermap_receptor_output_lines:
            input_file.write(receptor_line)

    # Writing discrete cartesian points if no AERMAP output is available
    else:
        for coordinate in range(len(disccart_coordinate_list_x)):
            disccart_x_coord = str(disccart_coordinate_list_x[coordinate])
            disccart_y_coord = str(disccart_coordinate_list_y[coordinate])
            input_file.write('   DISCCART ' + disccart_x_coord + ' ' + disccart_y_coord + '\n')

    input_file.write('RE FINISHED\n\n')
    # Pathway ending


# this function writes the input section for a grid receptor system
# inputs are defined in run_framework.py
def write_receptor_lines_grid(receptor_grid_starting_point_x,
                              receptor_grid_starting_point_y,
                              receptor_grid_number_receptors_x,
                              receptor_grid_number_receptors_y,
                              receptor_grid_spacing_x,
                              receptor_grid_spacing_y,
                              input_file):
    input_file.write('RE STARTING\n')
    # Pathway start
    receptor_network_name = 'NETWORK'
    # Grid receptor network creation start
    input_file.write('   GRIDCART ' + receptor_network_name + ' STA\n   ')
    input_file.write(
        'GRIDCART ' + str(receptor_network_name) + ' XYINC ' + str(receptor_grid_starting_point_x) + ' '
        + str(receptor_grid_number_receptors_x) + ' ' + str(receptor_grid_spacing_x) + ' '
        + str(receptor_grid_starting_point_y) + ' ' + str(receptor_grid_number_receptors_y) + ' '
        + str(receptor_grid_spacing_y) + '\n   ')
    input_file.write('GRIDCART ' + receptor_network_name + ' END\n')
    # Receptor network ending
    input_file.write('RE FINISHED\n\n')


# this function writes area source emitter lines for AERMOD
# all parameters are defined in run_framework.py
def write_source_location_lines(source_x_points, source_y_points, source_x_coordinates_for_naming,
                                source_y_coordinates_for_naming, source_type, aermap_source_output, input_file):
    # Writing SOurce Pathway Location Lines
    input_file.write('SO STARTING\n')
    # Pathway start

    # Extracting the 'location' keyword lines from the AERMAP source output if available
    if aermap_source_output:
        aermap_source_output_lines = []

        for line in open(aermap_source_output):
            if '**' not in line:
                aermap_source_output_lines.append(line)
        del aermap_source_output_lines[0]

        for receptor_line in aermap_source_output_lines:
            input_file.write(receptor_line)

    else:
        for point in range(len(source_x_points)):
            source_name = str(source_x_coordinates_for_naming[point]) + str(source_y_coordinates_for_naming[point])
            # Name of pollutant source
            if source_type == 'point':
                # Type of pollutant source (point, volume, area, etc.)
                source_type_for_file = 'POINT'
            if source_type == 'area':
                source_type_for_file = 'AREA'
            source_x_coord = str(source_x_points[point])
            source_y_coord = str(source_y_points[point])
            source_z_coord = '0'
            # Coordinates of source
            input_file.write(
                '   LOCATION ' + source_name + ' ' + source_type_for_file + ' ' + source_x_coord + ' ' + source_y_coord + ' ' + source_z_coord + '\n')
            # LOCATION keyword line


# this function writes the source params for area source emitters for AERMOD
# all parameters are defined in run_framework.py
def write_source_data_area_lines(source_x_coordinates_for_naming, source_y_coordinates_for_naming,
                                 source_emission_rate_list, source_release_height_list,
                                 source_area_x_direction_length_list, source_area_y_direction_length_list,
                                 input_file):
    for value in range(len(source_x_coordinates_for_naming)):
        source_name = str(source_x_coordinates_for_naming[value]) + str(source_y_coordinates_for_naming[value])
        source_emission_rate = source_emission_rate_list[value]
        # Source emission rate (g/(s-m^2))
        source_height = source_release_height_list[value]
        # Source release height above ground
        x_direction_length = source_area_x_direction_length_list[value]
        # Length of side of area source in x-direction (m)
        y_direction_length = source_area_y_direction_length_list[value]
        input_file.write('   SRCPARAM '+source_name+' '+str(source_emission_rate)+' '+str(source_height)+' '+str(x_direction_length)+' '+str(y_direction_length)+'\n')

    input_file.write('   SRCGROUP ALL\nSO FINISHED\n\n')
    # Source group name and pathway ending


# this function writes the source params for point source emitters for AERMOD
# all parameters are defined in run_framework.py
def write_source_data_point_lines(source_x_coordinates_for_naming, source_y_coordinates_for_naming,
                                  source_emission_rate_list, source_height_list,
                                  stack_gas_exit_temperature_list, stack_gas_exit_velocity_list,
                                  stack_inside_diameter_list, input_file):
    for value in range(len(source_x_coordinates_for_naming)):
        # BPIP Input
        source_name = str(source_x_coordinates_for_naming[value]) + str(source_y_coordinates_for_naming[value])
        source_emission_rate = source_emission_rate_list[value]
        # Source emission rate (g/s)
        source_height = source_height_list[value]
        # Source physical release height above ground
        stack_gas_exit_temperature = stack_gas_exit_temperature_list[value]
        # Source stack gas exit temperature
        stack_gas_exit_velocity = stack_gas_exit_velocity_list[value]
        # Source stack gas exit velocity
        stack_inside_diameter = stack_inside_diameter_list[value]
        # Source stack inside diameter
        input_file.write(
            '   SRCPARAM ' + source_name + ' ' + str(source_emission_rate) + ' ' + str(source_height) + ' ' + str(
                stack_gas_exit_temperature) + ' ' + str(stack_gas_exit_velocity) + ' ' + str(
                stack_inside_diameter) + '\n')
    input_file.write('   SRCGROUP ALL\nSO FINISHED\n\n')


# this function writes the meteorological data settings for the AERMOD input file
# all parameters are defined in run_framework.py
def write_met_data_lines(surface_observations_file, upper_air_data_file,
                   met_data_start_year,uairdata_station_number,surfdata_station_number,base_elevation, input_file):
    # '''Writing MEteorological Data pathway lines'''
    # These lines will vary depending on meteorological data
    surffile = surface_observations_file
    # Surface data file, must end with .SFC
    proffile = upper_air_data_file
    # Profile data file, must end with .PFL
    input_file.write('ME STARTING\n   SURFFILE ' + surffile + '\n   PROFFILE ' + proffile + '\n   ')
    # Pathway start, specification of MET Data files
    surfdata_year = met_data_start_year
    input_file.write('SURFDATA ' + surfdata_station_number + ' ' + surfdata_year + '\n   ')
    # Surface data details
    uairdata_year = met_data_start_year
    input_file.write('UAIRDATA ' + uairdata_station_number + ' ' + uairdata_year + '\n   ')
    # Upper air data details
    input_file.write('PROFBASE ' + str(base_elevation) + '\nME FINISHED\n\n')
    # Base elevation of temperature profile and pathway ending


# this function writes the output settings for the AERMOD input file
# if you want to change what information aermod displays do it here
# currently configured to just printing hourly averages for a year
def write_output_option_lines(run_aerplot, input_file):
    input_file.write('OU STARTING\n')
    input_file.write('   DAYTABLE ALLAVE\n')
    if run_aerplot == 'yes':
        input_file.write('   PLOTFILE ANNUAL ALL aerplot_data.PLT\n')
    input_file.write('OU FINISHED')


# this function is used to make source inputs the correct length if only one data point is entered
def check_source_data_for_length(input, number_terms):
    if input is None:
        return None
    elif type(input) == list:
        if len(input) == 1:
            return copy_number_to_list_length(input[0], number_terms)
        elif len(input) == number_terms:
            return input
        else:
            return 'error'
    elif type(input) == int or type(input) == float:
        return copy_number_to_list_length(input, number_terms)
    else:
        return 'error'


# this function is used to copy a single data point to a list for a specific number
def copy_number_to_list_length(data_value, number_terms):
    data_list = []
    for i in range(number_terms):
        data_list.append(data_value)
    return data_list


# this function checks the inputs to see if they were inputted correctly
# returns true if all data is correct, false if there is a problem with the data
# all parameters are defined in run_framework.py
def check_for_valid_inputs(source_x_points,
                           source_y_points,
                           source_type,
                           source_emission_rate_list,
                           source_release_height_list,
                           source_area_x_direction_length_list,
                           source_area_y_direction_length_list,
                           source_point_stack_gas_exit_temperature_list,
                           source_point_stack_gas_exit_velocity_list,
                           source_point_stack_inside_diameter_list,
                           receptor_coordinate_list_y,
                           receptor_coordinate_list_x,
                           receptor_style
                           ):

    number_errors = 0
    # checking if number of x and y coordinates for sources match
    if len(source_x_points) != len(source_y_points):
        print("x and y source coordinate lists don't have matching lengths")
        number_errors += 1

    if source_type != 'point' and source_type != 'area':
        number_errors += 1
        print("source_type is not 'area' or 'point'")

    # if the following data is a string it was inputted correctly via check_source_data_for_length(...) function

    if type(source_emission_rate_list) == str:
        number_errors += 1
        print("source_emission_rate_list inputted incorrectly")

    if type(source_release_height_list) == str:
        number_errors += 1
        print("source_release_height_list inputted incorrectly")

    if source_type == 'area':

        if type(source_area_x_direction_length_list) == str or source_area_x_direction_length_list is None:
            number_errors += 1
            print("source_area_x_direction_length_list inputted incorrectly")

        if type(source_area_y_direction_length_list) == str or source_area_y_direction_length_list is None:
            number_errors += 1
            print("source_area_y_direction_length_list inputted incorrectly")

    if source_type == 'point':

        if type(source_point_stack_gas_exit_temperature_list) == str or source_point_stack_gas_exit_temperature_list\
                is None:
            number_errors += 1
            print("source_point_stack_gas_exit_temperature_list inputted incorrectly")

        if type(source_point_stack_gas_exit_velocity_list) == str or source_point_stack_gas_exit_velocity_list is None:
            number_errors += 1
            print("source_point_stack_gas_exit_velocity_list inputted incorrectly")

        if type(source_point_stack_inside_diameter_list) == str or source_point_stack_inside_diameter_list is None:
            number_errors += 1
            print("source_point_stack_inside_diameter_list inputted incorrectly")
    if receptor_style == 'discrete':
        if len(receptor_coordinate_list_y) != len(receptor_coordinate_list_x):
            number_errors += 1
            print("number of receptor y coordinates does not equal number of receptor x coordinates")

    # Returns false if there are any errors, otherwise true
    if number_errors > 0:
        return False
    else:
        return True


# this function writes an aerplot input file
def write_aerplot_input_file(easting, northing, utm_zone, northern_hemisphere, google_earth_display_name,
                             plot_file_name, output_file_name):
    '''Write aerplot.inp file'''
    # Create file
    input_file = open('aerplot.inp', 'w')

    # Version line and other comment information
    # Do not edit the version line
    input_file.write('version=1\n; This line must be the first non-comment line\n\n; Altitude options\n')

    # Altitude choice
    # Comment out one of the following two lines within the write command
    # To do so add a ';' directly after the ' in the write command
    # This makes it easier to remember the options when looking at the input file later on
    # The first is relative to ground and the second is height above sea level
    input_file.write('altitudeChoice=relativeToGround\n')
    input_file.write(';altitudeChoice=absolute\n')

    # The height can offset from the height indicated in the .plt file from AERMOD
    input_file.write('altitude=0\n\n')

    # Input utm zone and utm coordinates of location to display on Google Earth
    input_file.write('; UTM Location Information\n')
    input_file.write('easting='+str(easting)+'\n')
    input_file.write('northing='+str(northing)+'\n')
    input_file.write('utmZone='+str(utm_zone)+'\n')

    # Specifying hemisphere
    # If right on the equator, set this to True
    input_file.write('inNorthernHemisphere='+str(northern_hemisphere)+'\n\n')
    # Name of kmz file in Google Earth
    input_file.write('; File naming\n')
    input_file.write('NameDisplayedInGoogleEarth=' + google_earth_display_name + '\n')

    # Name of plot file from AERMOD
    input_file.write('PlotFileName=' + plot_file_name + '\n')

    # Name of kmz file in file directory
    input_file.write('OutputFileNameBase=' + output_file_name + '\n\n')

    # Binning choice
    # The options are "Linear" and "Log"
    input_file.write('; Binning choice\n')
    input_file.write('binningChoice=Log\n\n')

    # Comment out one of the following lines within the write command to choose the color scheme
    input_file.write('; Contour display options\n')
    input_file.write('sIconSetChoice=redBlue\n')
    input_file.write(';sIconSetChoice=redGreen\n')

    # .7 is the recommended scale for Google Earth
    input_file.write('IconScale = 0.70\n')

    # The program will automatically pick the maximum and minimum values for the color scale if "DATA" is specified
    # The min and max can be manually set below if desired
    input_file.write('minbin=DATA\n')
    input_file.write('maxbin=DATA\n')

    # if "FALSE" Google Earth will launch after AERPLOT finishes running
    # if "True" it will not
    input_file.write('sDisableEarthBrowser = TRUE\n')

    # Creating contours
    input_file.write('makeContours                        = True\n')

    # Number of times to perform contour smoothing
    # One smoothing can make the contours much less chaotic
    # A second one can move the contours farther from their proper locations according to the receptor values
    # However, a setting greater than one may be beneficial when there is greater spacing between receptors
    input_file.write('numberOfTimesToSmoothContourSurface = 1\n')

    # Number of columns and rows is generally good at 400 but may need to be increased for particularly large domains
    input_file.write('numberOfGridCols                    = 400\n')
    input_file.write('numberOfGridRows                    = 400\n\n')
    input_file.close()


# main function that writes AERMOD input file
# all parameters are defined in run_framework.py
# aermap files are defaulted to None since there is no aermap framework for creating and running aermap.exe
#   aermap will run and be used if the files are given, the inputs are configured to use aermap data if provided
def write_aermod_input_file(surface_observations_file,
                            upper_air_data_file,
                            source_x_points,
                            source_y_points,
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
                            surfdata_station_number,
                            aermap_receptor_output=None,
                            aermap_source_output=None,
                            run_aerplot='no'
                            ):
    input_file = open('aermod.inp', 'w')

    '''Writing COntrol lines'''
    write_control_lines(input_file)

    # creating names for each well that AERMOD will use to identify
    # name of each well is just the integer of the x coord followed by the y coord
    # for example, a well at location [501.134, -25.3] will have the name '501-25'
    source_x_coordinates_for_naming = []
    source_y_coordinates_for_naming = []
    for x_coord in source_x_points:
        source_x_coordinates_for_naming.append(int(x_coord))
    for y_coord in source_y_points:
        source_y_coordinates_for_naming.append(int(y_coord))

    '''Writing SOurce data pathway lines'''
    write_source_location_lines(source_x_points, source_y_points, source_x_coordinates_for_naming,
                                source_y_coordinates_for_naming, source_type, aermap_source_output, input_file)

    # POINT SOURCE CURRENTLY NOT WORKING
    if source_type == 'point':
        write_source_data_point_lines(source_x_coordinates_for_naming, source_y_coordinates_for_naming,
                                      source_emission_rate_list, source_release_height_list,
                                      source_point_stack_gas_exit_temperature_list,
                                      source_point_stack_gas_exit_velocity_list,
                                      source_point_stack_inside_diameter_list, input_file)
    if source_type == 'area':
        write_source_data_area_lines(source_x_coordinates_for_naming, source_y_coordinates_for_naming,
                                     source_emission_rate_list, source_release_height_list,
                                     source_area_x_direction_length_list, source_area_y_direction_length_list,
                                     input_file)

    '''Writing REceptor pathway lines'''
    if receptor_style == 'discrete':
        write_receptor_lines_discrete(receptor_coordinate_list_x, receptor_coordinate_list_y,
                                      aermap_receptor_output, input_file)
    elif receptor_style == 'grid':
        write_receptor_lines_grid(receptor_grid_starting_point_x,
                                  receptor_grid_starting_point_y,
                                  receptor_grid_number_receptors_x,
                                  receptor_grid_number_receptors_y,
                                  receptor_grid_spacing_x,
                                  receptor_grid_spacing_y,
                                  input_file)
    else:
        print('receptor_style inputted incorrectly, program will not run')

    '''Writing MEteorological Data pathway lines'''
    write_met_data_lines(surface_observations_file, upper_air_data_file, str(met_data_start_year),
                         str(uair_data_station_number), str(surfdata_station_number), str(base_elevation), input_file)

    '''Writing OUtput options pathway lines'''
    # currently set up for just hourly concentrations
    write_output_option_lines(run_aerplot, input_file)
    input_file.close()