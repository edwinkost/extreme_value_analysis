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


###################################################################################
# The script to apply gumbel fits to the Annual Flood Maxima time series
###################################################################################

# input files
input_files                    = {}
# The gumbel fit parameters based on the annual flood maxima based on the PCR-GLOBWB 5 arcmin results:
# - WATCH historical
input_files['folder'] = "/scratch-shared/edwinsut/flood_analyzer_analysis/gumbel_fits/watch_1960-1999_example"
input_files['file_name'] = {}
input_files['file_name']['channelStorage'] = input_files['folder'] + "/" + "gumbel_analysis_output_for_channel_storage.nc" 
input_files['file_name']['floodVolume'   ] = input_files['folder'] + "/" + "gumbel_analysis_output_for_flood_innundation_volume.nc" 
input_files['file_name']['dynamicFracWat'] = input_files['folder'] + "/" + "gumbel_analysis_output_for_fraction_of_surface_water.nc" 
#
# general input files
# - clone map
input_files['clone_map_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
pcr.setclone(input_files['clone_map_05min'])
# - cell area, ldd maps
input_files['cell_area_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['ldd_map_05min'  ] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"

# option to save/present results at the landmask region only:
landmask_only = True

# start and end years for this analysis:
str_year = 1960
end_year = 1999

# output files
output_files                   = {}
# - WATCH historical
# output folder
output_files['folder']         = "/scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/"
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


# netcdf general setup:
netcdf_setup = {}
netcdf_setup['format']      = "NETCDF4"
netcdf_setup['zlib']        = True
netcdf_setup['institution'] = "Utrecht University, Department of Physical Geography ; Deltares ; World Resources Institute"
netcdf_setup['title'      ] = "PCR-GLOBWB 2 output (post-processed for the Aqueduct Flood Analyzer): Gumbel Fit to Annual Flood Maxima"
netcdf_setup['created by' ] = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['description'] = "The extreme values based on the gumbel fits of the annual flood maxima."
netcdf_setup['source'     ] = "Utrecht University, Department of Physical Geography - contact: Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['references' ] = "Sutanudjaja et al., in prep."


# change to the output folder (use it as the working folder) 
os.chdir(output_files['folder'])

# object for reporting/making netcdf files
netcdf_report = outputNetCDF.OutputNetCDF()
# - dictionary for netcdf output files 
netcdf_file = {}

msg = "Preparing netcdf output files."
logger.info(msg)
for var_name in ['channelStorage', 'floodVolume', 'dynamicFracWat']: 
    #
    netcdf_file[var_name] = {}
    #
    # return periods
    return_periods = ["2-year", "5-year", "10-year", "25-year", "50-year", "100-year", "250-year", "500-year", "1000-year"]
    #
    # all gumbel fit parameters in a netcdf file:
    # - file name
    netcdf_file[var_name]['file_name'] = output_files['folder'] + "/" + "extreme_values_based_on_gumbel_fit_for_" + varDict.netcdf_short_name[var_name] + ".nc"
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

# derive gumbel parameters
msg = "Applying gumbel parameters."
logger.info(msg)
#
for var_name in ['channelStorage', 'floodVolume', 'dynamicFracWat']: 
    
    msg = "Applying gumbel parameters from the file: " + str(input_files['file_name'][var_name])
    logger.info(msg)

    netcdf_input_file = input_files['file_name'][var_name]
    
    # read gumbel parameters: ['p_zero', 'location_parameter', 'scale_parameter']
    #
    variable_name = str('p_zero') + "_of_" + varDict.netcdf_short_name[var_name]
    p_zero   = vos.netcdf2PCRobjClone(netcdf_input_file,\
                                      variable_name,\
                                      1,\
                                      "Yes",\
                                      input_files['clone_map_05min'])
    #
    variable_name = str('location_parameter') + "_of_" + varDict.netcdf_short_name[var_name]
    location = vos.netcdf2PCRobjClone(netcdf_input_file,\
                                      variable_name,\
                                      1,\
                                      "Yes",\
                                      input_files['clone_map_05min'])
    #
    variable_name = str('scale_parameter') + "_of_" + varDict.netcdf_short_name[var_name]
    scale    = vos.netcdf2PCRobjClone(netcdf_input_file,\
                                      variable_name,\
                                      1,\
                                      "Yes",\
                                      input_files['clone_map_05min'])
    
    # applying gumbel parameters for every return period
    extreme_values = {}
    for return_period in return_periods:
        
        return_period_in_year = float(return_period.split("-")[0]) 
        
        extreme_values[return_period] = glofris.inverse_gumbel(p_zero, location, scale, return_period_in_year)
    
    # write the extreme values to a netcdf file
    lowerTimeBound = datetime.datetime(str_year,  1,  1, 0)
    upperTimeBound = datetime.datetime(end_year, 12, 31, 0)
    timeBounds = [lowerTimeBound, upperTimeBound]
    
    msg = "Writing extreme values to a netcdf file: " + str(netcdf_file[var_name]['file_name'])
    logger.info(msg)

    # preparing the variables in the netcdf file:
    for return_period in return_periods:
        # variable names and unit 
        variable_name = str(return_period) + "_of_" + varDict.netcdf_short_name[var_name]
        variable_unit = varDict.netcdf_unit[var_name]
        var_long_name = str(return_period) + "_of_" + varDict.netcdf_long_name[var_name]
        # 
        netcdf_report.create_variable(\
                                      ncFileName = netcdf_file[var_name]['file_name'], \
                                      varName    = variable_name, \
                                      varUnit    = variable_unit, \
                                      longName   = var_long_name, \
                                      comment    = varDict.comment[var_name]
                                      )

    # store the variables to pcraster map and netcdf files:
    data_dictionary = {}
    for return_period in return_periods:
        
        # variable name
        variable_name = str(return_period) + "_of_" + varDict.netcdf_short_name[var_name]
        
        # put it into a dictionary
        data_dictionary[variable_name] = pcr.pcr2numpy(extreme_values[return_period], vos.MV)

        # report to a pcraster map
        pcr.report(data_dictionary[variable_name], variable_name + ".map")

    # save the variables to a netcdf file
    netcdf_report.dictionary_of_data_to_netcdf(netcdf_file[var_name]['file_name'], \
                                               data_dictionary, \
                                               timeBounds)




