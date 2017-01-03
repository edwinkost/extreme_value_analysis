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


#############################################################################################
# The script to apply gumbel fits WITH BIAS CORRECTION to the Annual Flood Maxima time series
#############################################################################################


# start and end years for this analysis:
str_year = np.int(sys.argv[1])
end_year = np.int(sys.argv[2])
#~ # - for the year 2030
#~ str_year = 2010
#~ end_year = 2049
#~ # - for the year 2050
#~ str_year = 2030
#~ end_year = 2069
#~ # - for the year 2080
#~ str_year = 2060
#~ end_year = 2099


# input files
input_files            = {}
#
# The gumbel fit parameters based on the annual flood maxima based on the FUTURE/CLIMATE/GCM run:
input_files["future"]  = {}
# - input folder based on the system argument
input_files["future"]['folder']    = os.path.abspath(sys.argv[3]) + "/"
#~ # - gfdl-esm2m future/climate (example)
#~ input_files["future"]['folder'] = "/scratch-shared/edwinhs/bias_correction_test/input/rcp4p5/gumbel_fits/gfdl-esm2m_2010-2049/"
#
input_files["future"]['file_name'] = {}
input_files["future"]['file_name']['channelStorage'] = input_files["future"]['folder'] + "/" + "gumbel_analysis_output_for_channel_storage.nc" 
input_files["future"]['file_name']['floodVolume'   ] = input_files["future"]['folder'] + "/" + "gumbel_analysis_output_for_flood_inundation_volume.nc" 
#
# The gumbel fit parameters based on the annual flood maxima based on the HISTORICAL run:
input_files["historical"]  = {}
# - input folder based on the system argument
input_files["historical"]['folder']    = os.path.abspath(sys.argv[4]) + "/"
#~ # - gfdl-esm2m historical (example)
#~ input_files["historical"]['folder'] = "/scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits/gfdl-esm2m_1960-1999/"
#
input_files["historical"]['file_name'] = {}
input_files["historical"]['file_name']['channelStorage'] = input_files["historical"]['folder'] + "/" + "gumbel_analysis_output_for_channel_storage.nc" 
input_files["historical"]['file_name']['floodVolume'   ] = input_files["historical"]['folder'] + "/" + "gumbel_analysis_output_for_flood_inundation_volume.nc" 
#
#
# general input files
# - clone map
input_files['clone_map_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
pcr.setclone(input_files['clone_map_05min'])
# - cell area, ldd maps
input_files['cell_area_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['ldd_map_05min'  ] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
#
# The gumbel fit parameters based on the annual flood maxima based on the BASELINE run: WATCH 1960-1999
input_files["baseline"]  = {}
input_files["baseline"]['folder']    = "/scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits/watch_1960-1999/"
input_files["baseline"]['file_name'] = {}
input_files["baseline"]['file_name']['channelStorage'] = input_files["baseline"]['folder'] + "/" + "gumbel_analysis_output_for_channel_storage.nc" 
input_files["baseline"]['file_name']['floodVolume'   ] = input_files["baseline"]['folder'] + "/" + "gumbel_analysis_output_for_flood_inundation_volume.nc" 


# option to save/present results at the landmask region only (not working yet):
landmask_only = True


# output files
output_files                   = {}
#
# - output folder
# output folder based on the system argument
output_folder_for_this_analysis = sys.argv[5]
output_files['folder']          = output_folder_for_this_analysis + "/" 
#~ # - gfdl-esm2m
#~ output_files['folder']      = "/scratch-shared/edwinhs/bias_correction_test/output/extreme_values_bias_corrected/gfdl-esm2m_1960-1999/"
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


# netcdf general setup:
netcdf_setup = {}
netcdf_setup['format']      = "NETCDF4"
netcdf_setup['zlib']        = True
netcdf_setup['institution'] = "Utrecht University, Department of Physical Geography ; Deltares ; World Resources Institute"
netcdf_setup['title'      ] = "PCR-GLOBWB 2 output (post-processed for the Aqueduct Flood Analyzer): Gumbel Fit to Annual Flood Maxima"
netcdf_setup['created by' ] = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['description'] = "The bias-corrected extreme values based on the gumbel fits of the annual flood maxima."
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
for bias_type in ['including_bias', 'bias_corrected']:
    netcdf_file[bias_type] = {}
    for var_name in ['channelStorage', 'floodVolume']: 
        #
        netcdf_file[bias_type][var_name] = {}
        #
        # all gumbel fit parameters in a netcdf file:
        # - file name
        netcdf_file[bias_type][var_name]['file_name']   = output_files['folder'] + "/" + str(bias_type) + "_" + "extreme_values_based_on_gumbel_fit_for_" + varDict.netcdf_short_name[var_name] + ".nc"
        #
        # - general attribute information:
        netcdf_file[bias_type][var_name]['description'] = netcdf_setup['description']
        netcdf_file[bias_type][var_name]['institution'] = netcdf_setup['institution']
        netcdf_file[bias_type][var_name]['title'      ] = netcdf_setup['title'      ]
        netcdf_file[bias_type][var_name]['created by' ] = netcdf_setup['created by' ]
        netcdf_file[bias_type][var_name]['source'     ] = netcdf_setup['source'     ]
        netcdf_file[bias_type][var_name]['references' ] = netcdf_setup['references' ]
        #
        # - resolution (unit: arc-minutes)
        netcdf_file[bias_type][var_name]['resolution_arcmin'] = 5. 
        #
        # - preparing netcdf file:
        msg = "Preparing the netcdf file: " + netcdf_file[bias_type][var_name]['file_name']
        logger.info(msg)
        netcdf_report.create_netcdf_file(netcdf_file[bias_type][var_name]) 


# applying gumbel parameters with bias correction to get extreme values for every return period:
msg = "Applying gumbel parameters with bias correction."
logger.info(msg)
#
# - a dictionary for input gumbel parameters:
p_zero = {}
location = {}
scale = {}
#
# - a dictionary for extreme value:
extreme_values = {}
#
# - a dictionary for return periods
return_periods = ["2-year", "5-year", "10-year", "25-year", "50-year", "100-year", "250-year", "500-year", "1000-year"]
#
for var_name in ['channelStorage', 'floodVolume']: 
    
    msg  = "Applying gumbel parameters from the climate run: " + str(input_files["future"]['file_name'][var_name])
    msg += "    that are bias corrected to the baseline run: " + str(input_files["baseline"]['file_name'][var_name])
    msg += "                         and the historical run: " + str(input_files["historical"]['file_name'][var_name])
    logger.info(msg)

    # read gumbel parameters from : ['p_zero', 'location_parameter', 'scale_parameter']
    for run_type in ["future", "historical", "baseline"]:

        netcdf_input_file = input_files[run_type]['file_name'][var_name]
        #
        variable_name = str('p_zero') + "_of_" + varDict.netcdf_short_name[var_name]
        p_zero[run_type]   = vos.netcdf2PCRobjClone(netcdf_input_file,\
                                          variable_name,\
                                          1,\
                                          "Yes",\
                                          input_files['clone_map_05min'])
        #
        variable_name = str('location_parameter') + "_of_" + varDict.netcdf_short_name[var_name]
        location[run_type] = vos.netcdf2PCRobjClone(netcdf_input_file,\
                                          variable_name,\
                                          1,\
                                          "Yes",\
                                          input_files['clone_map_05min'])
        #
        variable_name = str('scale_parameter') + "_of_" + varDict.netcdf_short_name[var_name]
        scale[run_type]    = vos.netcdf2PCRobjClone(netcdf_input_file,\
                                          variable_name,\
                                          1,\
                                          "Yes",\
                                          input_files['clone_map_05min'])
    
    # compute future extreme values (including bias correction):
    for return_period in return_periods:
        return_period_in_year = float(return_period.split("-")[0]) 

        # compute future extreme values (with bias): applying gumbel parameters
        msg = "Compute future/climate/gcm extreme values (biases are still included here)."
        logger.info(msg)
        extreme_values["including_bias"][return_period] = glofris.inverse_gumbel(p_zero["future"], location["future"], scale["future"], return_period_in_year)
    
        # lookup the return period in present days (historical run) belonging to future extreme values
        msg = "For the given future extreme values, obtain the return period based on the historical gumbel fit/parameters."
        logger.info(msg)
        return_period_historical = glofris.get_return_period_gumbel(p_zero["historical"], location["historical"], scale["historical"], extreme_values["with_bias"][return_period])
        
        # bias corrected extreme values
        msg = "Calculate the bias corrected extreme values: Using the return period based on the historical gumbel fit/parameters and the gumbel fit/parameters of the baseline run."
        logger.info(msg)
        extreme_values["bias_corrected"][return_period] = glofris.inverse_gumbel(p_zero["baseline"], location["baseline"], scale["baseline"], return_period_in_year)
    
    # time bounds in a netcdf file
    lowerTimeBound = datetime.datetime(str_year,  1,  1, 0)
    upperTimeBound = datetime.datetime(end_year, 12, 31, 0)
    timeBounds = [lowerTimeBound, upperTimeBound]
    
    for bias_type in ['including_bias', 'bias_corrected']:
    
        msg = "Writing extreme values to a netcdf file: " + str(netcdf_file[bias_type][var_name]['file_name'])
        logger.info(msg)
        
        # preparing the variables in the netcdf file:
        for return_period in return_periods:
            # variable names and unit 
            variable_name = str(return_period) + "_of_" + varDict.netcdf_short_name[var_name]
            variable_unit = varDict.netcdf_unit[var_name]
            var_long_name = str(return_period) + "_of_" + varDict.netcdf_long_name[var_name]
            # 
            netcdf_report.create_variable(\
                                          ncFileName = netcdf_file[bias_type][var_name]['file_name'], \
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
            
            # report to a pcraster map
            pcr.report(extreme_values[bias_type][return_period], bias_type + "_" + variable_name + ".map")
        
            # put it into a dictionary
            data_dictionary[variable_name] = pcr.pcr2numpy(extreme_values[bias_type][return_period], vos.MV)
        
        # save the variables to a netcdf file
        netcdf_report.dictionary_of_data_to_netcdf(netcdf_fileextreme_values[bias_type][var_name]['file_name'], \
                                                   data_dictionary, \
                                                   timeBounds)




