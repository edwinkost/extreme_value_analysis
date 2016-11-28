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
# The script to derive and apply gumbel fits to the Annual Flood Maxima time series
###################################################################################

# input files
input_files                    = {}
# The annual flood maxima based on the PCR-GLOBWB 5 arcmin results:
# - WATCH historical
input_files['folder'] = "/scratch-shared/edwinsut/flood_analyzer_analysis/maximum_events_merged/watch_1960-1999/"
input_files['file_name'] = {}
input_files['file_name']['channelStorage'] = input_files['folder'] + "/" + "channel_storage_annual_flood_maxima.nc" 
input_files['file_name']['floodVolume'   ] = input_files['folder'] + "/" + "flood_innundation_volume_annual_flood_maxima.nc" 
input_files['file_name']['dynamicFracWat'] = input_files['folder'] + "/" + "fraction_of_surface_water_annual_flood_maxima.nc" 
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
output_files['folder']         = "/scratch-shared/edwinsut/flood_analyzer_analysis/gumbel_fits/watch_1960-1999/"
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
netcdf_setup['format']          = "NETCDF4"
netcdf_setup['zlib']            = True
netcdf_setup['institution']     = "Utrecht University, Department of Physical Geography ; Deltares ; World Resources Institute"
netcdf_setup['title'      ]     = "PCR-GLOBWB 2 output (post-processed for the Aqueduct Flood Analyzer): Gumbel Fit to Annual Flood Maxima"
netcdf_setup['created by' ]     = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['description']     = "The gumbel fit/analysis output for the annual flood maxima."
netcdf_setup['source'     ]     = "Utrecht University, Department of Physical Geography - contact: Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['references' ]     = "Sutanudjaja et al., in prep."


# change to the output folder (use it as the working folder) 
os.chdir(output_files['folder'])

# object for reporting/making netcdf files
netcdf_report = outputNetCDF.OutputNetCDF()
# - dictionary for netcdf output files 
netcdf_file = {}

for var_name in ['channelStorage', 'floodVolume', 'dynamicFracWat', "surfaceWaterLevel"]: 
    #
    netcdf_file[var_name] = {}
    #
    # gumbel fits parameters
    # - probability of zero flood volume                             
    # - gumbel distribution location parameter of flood volume
    # - gumbel distribution scale parameter of flood volume
    gumbel_par_name = ['p_zero', 'location_parameter', 'scale_parameter']
    #
    # return periods
    return_period_in_year = ["2-year", "5-year", "10-year", "25-year", "50-year", "100-year", "250-year", "500-year", "1000-year"]
    #
    # all gumbel fit parameters and return period values in one netcdf file:
    # - file name
    netcdf_file[var_name]['file_name'] = output_files['folder'] + "/" + "gumbel_analysis_ouput_for_" + varDict.netcdf_short_name[var_name] + ".nc"
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
    if var_name == "surfaceWaterLevel": netcdf_file[var_name]['resolution_arcmin'] = 30.
    #
    # - preparing netcdf file:
    msg = "Preparing the netcdf file: " + netcdf_file[var_name]['file_name']
    logger.info(msg)
    netcdf_report.create_netcdf_file(netcdf_file[var_name]) 
    #
    # - creating all variables in the netcdf file:
    for return_period in return_period_in_year: 
        
        netcdf_report.create_variable(ncFileName = netcdf_file[var_name]['file_name'], \
                                      varName    = str(return_period) + "_" + varDict.netcdf_short_name[var_name], \
                                      varUnit    = varDict.netcdf_unit[var_name],
                                      longName   = str(return_period) + "_" + varDict.netcdf_long_name[var_name] , \
                                      comment    = varDict.comment[var_name])
    for par_name in gumbel_par_name:
        # gumbel fit parameters will not be calculated for the surfaceWaterLevel
        if var_name != "surfaceWaterLevel":
            netcdf_report.create_variable(\
                                      ncFileName = netcdf_file[var_name]['file_name'], \
                                      varName    = str(par_name) + "_of_" + varDict.netcdf_short_name[var_name], \
                                      varUnit    = varDict.netcdf_unit[var_name],
                                      longName   = str(par_name) + "_of_" + varDict.netcdf_long_name[var_name] , \
                                      comment    = varDict.comment[var_name])

# n_cores
n    

# NEXT: derive and apply Gumbel
for var_name in ['channelStorage', 'floodVolume', 'dynamicFracWat']: 
    
    # open input file
    netcdf_input_file = nc.Dataset(input_files['file_name'][var_name], "r")
    
    # read data
    
    print
    print varDict.netcdf_short_name[var_name]
    
    input_data_all = netcdf_input_file.variables[varDict.netcdf_short_name[var_name]]
    
    # split input data
    input_data_splitted = {}
    for i_core in range(n_core)
    
    # start multiple process to get gumbel parameters
    ll = []
    for ncName in netcdfList:
    	ll.append((ncName, latMin, latMax, lonMin, lonMax, deltaLat, deltaLon, startDate, endDate, ncFormat, using_zlib))
    pool = Pool(processes = ncores)    # start "ncores" of worker processes 
    pool.map(mergeNetCDF, ll)          # multicore processing
    
    # get gumbel paramaters
    zero_prob, gumbel_loc, gumbel_scale = glofris.get_gumbel_parameters(input_data)
    
    # write the gumbel parameters to netcdf file
    lowerTimeBound = datetime.datetime(str_year,  1,  1, 0)
    upperTimeBound = datetime.datetime(end_year, 12, 31, 0)
    
    for par_name in gumbel_par_name:

        if par_name == 'p_zero'            : varField = zero_prob
        if par_name == 'location_parameter': varField = gumbel_loc  
        if par_name == 'scale_parameter'   : varField = gumbel_scale
        
        netcdf_report.data_to_netcdf(netcdf_file[var_name]['file_name'], \
                                     str(par_name) + "_of_" + varDict.netcdf_short_name[var_name], \
                                     varField, 
                                     timeBounds)
        
    netcdf_input_file.close()
