#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import datetime

from multiprocessing import Pool

import netCDF4 as nc
import numpy as np
import pcraster as pcr

# utility module:
import virtualOS as vos
import glofris_postprocess_edwin_modified as glofris

# netcdf reporting module:
import output_netcdf_cf_convention as outputNetCDF

# variable dictionaries:
import aqueduct_flood_analyzer_variable_list as varDict

import logging
logger = logging.getLogger(__name__)


#######################################################################################
# The script to derive gumbel parameters based on the Annual Flood Maxima time series #
#######################################################################################

# input files
input_files                    = {}
#
# The annual flood maxima based on the PCR-GLOBWB 5 arcmin results:
#
# - input file based on the system argument for the variable channelStorage
#~ channelStorageInputFolder    = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/watch_1960-1999/"
channelStorageInputFolder       = os.path.abspath(sys.argv[1]) + "/"
input_files['file_name']        = {}
input_files['file_name']['channelStorage']    = channelStorageInputFolder + "/" + "channel_storage_annual_flood_maxima.nc" 
#
# - input file based on the system argument for the variable surfaceWaterLevel
#~ surfaceWaterLevelInputFolder = "/scratch-shared/edwinhs-last/flood_analyzer_output/surface_water_level_maximum/watch_1960-1999/"
surfaceWaterLevelInputFolder    = os.path.abspath(sys.argv[2]) + "/"
input_files['file_name']['surfaceWaterLevel'] = surfaceWaterLevelInputFolder + "/" + "surface_water_level_annual_maxima.nc" 

# general input files
# - clone map
input_files['clone_map_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
pcr.setclone(input_files['clone_map_05min'])
# - cell area, ldd maps
input_files['cell_area_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['ldd_map_05min'  ] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"


# output files
output_files                   = {}

# output folder
#
#~ # - WATCH historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/gumbel_fits/watch_1960-1999/"
#~ # - gfdl-esm2m historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/gumbel_fits/gfdl-esm2m_1960-1999/"
#~ # - hadgem2-es historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/gumbel_fits/hadgem2-es_1960-1999/"
#~ # - ipsl-cm5a-lr historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/gumbel_fits/ipsl-cm5a-lr_1960-1999/"
#~ # - miroc-esm-chem historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/gumbel_fits/miroc-esm-chem_1960-1999/"
#~ # - miroc-esm-chem historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/gumbel_fits/noresm1-m_1960-1999/"
#
# output folder based on the system argument
output_folder_for_this_analysis = sys.argv[3]
output_files['folder']          = output_folder_for_this_analysis + "/" 
#
#
try:
    os.makedirs(output_files['folder'])
except:
    os.system('rm -r ' + output_files['folder']  + "/*")
    pass
# - temporary output folder (e.g. needed for resampling/gdalwarp)
output_files['tmp_folder']       = output_files['folder'] + "/tmp/"
try:
    os.makedirs(output_files['tmp_folder'])
except:
    os.system('rm -r ' + output_files['tmp_folder'] + "/*")
    pass
# - prepare logger and its directory
log_file_location = output_files['folder'] + "/log/"
try:
    os.makedirs(log_file_location)
except:
    pass
vos.initialize_logging(log_file_location)


# start and end years for this analysis:
#~ # - for historical runs
#~ str_year = 1960
#~ end_year = 1999
#~ # - for the year 2030
#~ str_year = 2010
#~ end_year = 2049
# - for the year 2050
#~ str_year = 2030
#~ end_year = 2069
#~ # - for the year 2080
#~ str_year = 2060
#~ end_year = 2099
# - based on the system arguments:
str_year = int(sys.argv[4])
end_year = int(sys.argv[5])


# option to limit only certain variables being processed
option_to_limit_variables = "None"
try:
    option_to_limit_variables = sys.argv[6]
except:
    pass
variable_name_list = ['channelStorage', 'surfaceWaterLevel']
if option_to_limit_variables != "None": variable_name_list = [option_to_limit_variables]



# netcdf general setup:
netcdf_setup = {}
netcdf_setup['format']          = "NETCDF4"
netcdf_setup['zlib']            = True
netcdf_setup['institution']     = "Utrecht University, Department of Physical Geography ; Deltares ; World Resources Institute"
netcdf_setup['title'      ]     = "PCR-GLOBWB 2 output (post-processed for the Aqueduct Flood Analyzer): Gumbel Fit to Annual Flood Maxima"
netcdf_setup['created by' ]     = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['description']     = "The gumbel fit parameters based on the annual flood maxima."
netcdf_setup['source'     ]     = "Utrecht University, Department of Physical Geography - contact: Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['references' ]     = "Sutanudjaja et al., in prep."


# change to the output folder (use it as the working folder) 
os.chdir(output_files['folder'])

# object for reporting/making netcdf files
netcdf_report = outputNetCDF.OutputNetCDF()
# - dictionary for netcdf output files 
netcdf_file = {}

msg = "Preparing netcdf output files."
logger.info(msg)
for var_name in variable_name_list: 
    #
    netcdf_file[var_name] = {}
    #
    # gumbel fits parameters
    # - probability of zero flood volume                             
    # - gumbel distribution location parameter of flood volume
    # - gumbel distribution scale parameter of flood volume
    gumbel_par_name = ['p_zero', 'location_parameter', 'scale_parameter']
    #
    # all gumbel fit parameters in a netcdf file:
    # - file name
    netcdf_file[var_name]['file_name'] = output_files['folder'] + "/" + "gumbel_analysis_output_for_" + varDict.netcdf_short_name[var_name] + ".nc"
    #
    # - general attribute information:
    netcdf_file[var_name]['description'] = netcdf_setup['description']
    netcdf_file[var_name]['institution'] = netcdf_setup['institution']
    netcdf_file[var_name]['title'      ] = netcdf_setup['title'      ]
    netcdf_file[var_name]['created by' ] = netcdf_setup['created by' ]
    netcdf_file[var_name]['source'     ] = netcdf_setup['source'     ]
    netcdf_file[var_name]['references' ] = netcdf_setup['references' ]
    #
    # - resolution (unit: arc-minutes)
    netcdf_file[var_name]['resolution_arcmin'] = 5. 
    #
    # - preparing netcdf file:
    msg = "Preparing the netcdf file: " + netcdf_file[var_name]['file_name']
    logger.info(msg)
    netcdf_report.create_netcdf_file(netcdf_file[var_name]) 

# number of cores used 
n_cores = 24    

# derive gumbel parameters
msg = "Deriving gumbel parameters."
logger.info(msg)
#
for var_name in variable_name_list: 
    
    msg = "Deriving gumbel parameters based on the annual flood maxima file: " + str(input_files['file_name'][var_name])
    logger.info(msg)

    # open input file
    netcdf_input_file = nc.Dataset(input_files['file_name'][var_name], "r")
    
    # read data
    input_data_all = netcdf_input_file.variables[varDict.netcdf_short_name[var_name]]
    number_of_rows = input_data_all.shape[1]
    number_of_cols = input_data_all.shape[2]
    
    # split input data into several rows
    input_data_splitted = []
    #
    for i_core in range(n_cores):
        #
        if i_core == 0:
            str_row = 0
        else:
            str_row = end_row
        end_row = str_row + number_of_rows / n_cores
        #~ end_row = str_row + 5                                           # for testing only
        #
        # put the input in a dictionary
        input_data = {}
        input_data['1strow'] = str_row
        input_data['values'] = input_data_all[:,str_row:end_row,:].copy()
        input_data_splitted.append(input_data) 
        
    # start multiple process to get gumbel parameters
    pool = Pool(processes = n_cores)                                                              # start "ncores" of worker processes 
    gumbel_parameter_list = []
    gumbel_parameter_list = pool.map(glofris.get_gumbel_parameters, input_data_splitted)          # multicore processing
    
    # merge all gumbel parameters 
    zero_prob    = np.zeros([number_of_rows, number_of_cols]) + vos.MV
    gumbel_loc   = np.zeros([number_of_rows, number_of_cols]) + vos.MV
    gumbel_scale = np.zeros([number_of_rows, number_of_cols]) + vos.MV
    for i_list in range(len(gumbel_parameter_list)):
        str_row = gumbel_parameter_list[i_list]['starting_row']
        end_row = str_row + gumbel_parameter_list[i_list]['p_zero'].shape[0]
        
        zero_prob[str_row:end_row,:]    = gumbel_parameter_list[i_list]['p_zero']
        gumbel_loc[str_row:end_row,:]   = gumbel_parameter_list[i_list]['gumbel_loc']
        gumbel_scale[str_row:end_row,:] = gumbel_parameter_list[i_list]['gumbel_scale']    
    
    print "zero_prob " 
    print zero_prob
    print "gumbel_loc " 
    print gumbel_loc
    print "gumbel_scale " 
    print gumbel_scale
    
    # write the gumbel parameters to netcdf file
    lowerTimeBound = datetime.datetime(str_year,  1,  1, 0)
    upperTimeBound = datetime.datetime(end_year, 12, 31, 0)
    timeBounds = [lowerTimeBound, upperTimeBound]
    
    msg = "Writing the gumbel parameters to a netcdf file: " + str(netcdf_file[var_name]['file_name'])
    logger.info(msg)

    # preparing the variables in the netcdf file:
    for par_name in gumbel_par_name:
        # variable names and unit 
        variable_name = str(par_name) + "_of_" + varDict.netcdf_short_name[var_name]
        variable_unit = varDict.netcdf_unit[var_name]
        if par_name == "p_zero": variable_unit = "1"
        var_long_name = str(par_name) + "_of_" + varDict.netcdf_long_name[var_name]
        # 
        netcdf_report.create_variable(\
                                      ncFileName = netcdf_file[var_name]['file_name'], \
                                      varName    = variable_name, \
                                      varUnit    = variable_unit, \
                                      longName   = var_long_name, \
                                      comment    = varDict.comment[var_name]
                                      )

    # store the variables in the netcdf file:
    data_dictionary = {}
    for par_name in gumbel_par_name:
        
        # variable name
        variable_name = str(par_name) + "_of_" + varDict.netcdf_short_name[var_name]
        
        # variable fields 
        # - note that we have to flip the variable 
        if par_name == 'p_zero'            : data_dictionary[variable_name] = np.flipud(zero_prob)
        if par_name == 'location_parameter': data_dictionary[variable_name] = np.flipud(gumbel_loc)  
        if par_name == 'scale_parameter'   : data_dictionary[variable_name] = np.flipud(gumbel_scale)
    #
    # save the variables to a netcdf file
    netcdf_report.dictionary_of_data_to_netcdf(netcdf_file[var_name]['file_name'], \
                                               data_dictionary, \
                                               timeBounds)
    netcdf_input_file.close()
