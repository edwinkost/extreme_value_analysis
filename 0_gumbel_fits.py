#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import datetime

import netCDF4 as nc
import numpy as np
import pcraster as pcr

# utility module:
import virtualOS as vos
import glofris_postprocess_edwin_modified.py as glofris

# netcdf reporting module:
import output_netcdf_cf_convention.py

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
input_files['file_name']['channelStorage'] = input_files['folder'] + "/" + "channel_storage_annual_flood_maxima.nc" 
input_files['file_name']['floodVolume']    = input_files['folder'] + "/" + "flood_innundation_volume_annual_flood_maxima.nc" 
input_files['file_name']['dynamicFracWat'] = input_files['folder'] + "/" + "fraction_of_surface_water_annual_flood_maxima.nc" 
#
# general input files
# - clone map
input_files['clone_map_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
# - cell area, ldd maps
input_files['cell_area_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['ldd_map_05min']   = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"

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


for var_name in ['channelStorage', 'floodVolume', 'dynamicFracWat', "surfaceWaterLevel"]: 
    #
    netcdf_file[var_name] = {}
    #
    # return periods
    return_period_in_year = ["2", "5", "10", "25", "50", "100", "250", "500", "1000"]
    

    
    
    
    # gumbel fits parameters
    # - probability of zero flood volume                             
    # - gumbel distribution location parameter of flood volume
    # - gumbel distribution scale parameter of flood volume
    gumbel_par_name = ['p_zero', 'location_parameter', 'scale_parameter']
    #
    # all gumbel fit parameters in one netcdf file:
    # - file name
    netcdf_file[var_name]['file_name'] = output_files['folder'] + "/" + "gumbel_fit_parameters_for_" + varDict.netcdf_short_name[var_name] + ".nc"
    # - attribute information:
    netcdf_file[var_name]['description'] = netcdf_setup['description']
    netcdf_file[var_name]['institution'] = netcdf_setup['institution']
    netcdf_file[var_name]['title'      ] = netcdf_setup['title'      ]
    netcdf_file[var_name]['created by' ] = netcdf_setup['created by' ]
    netcdf_file[var_name]['source'     ] = netcdf_setup['source'     ]
    netcdf_file[var_name]['references' ] = netcdf_setup['references' ]
    # - resolution (unit: arc-minutes)
    netcdf_file[var_name]['resolution_arcmin'] = 5. 
    if var_name == "surfaceWaterLevel":
    
    # 
    
    for par_name in gumbel_par_name:
        
        # attribute/information for netcdf file
        netcdf_file[var_name][par_name] = {}
        netcdf_file[var_name][par_name]['short_name'] = str() + varDict.netcdf_short_name[var_name]
        
        output_files[var_name]['par_name']['unit']              = varDict.netcdf_unit[var_name]
        output_files[var_name]['par_name']['long_name']         = varDict.netcdf_long_name[var_name]          
        output_files[var_name]['par_name']['comment']           = varDict.comment[var_name]               
        output_files[var_name]['par_name']['description']       = varDict.description[var_name]
        # - add more information 
        if output_files[var_name]['par_name']['long_name']   == None: output_files[var_name]['long_name']   = output_files[var_name]['short_name']
        if output_files[var_name]['par_name']['comment']     == None: output_files[var_name]['comment'] = ""
        if output_files[var_name]['par_name']['description'] == None: output_files[var_name]['description'] = ""
        output_files[var_name]['par_name']['description']       = netcdf_setup['description'] + " " + output_files[var_name]['description']
        output_files[var_name]['par_name']['institution']       = netcdf_setup['institution']
        output_files[var_name]['par_name']['title'      ]       = netcdf_setup['title'      ]
        output_files[var_name]['par_name']['created by' ]       = netcdf_setup['created by' ]
        output_files[var_name]['par_name']['description']       = netcdf_setup['description']
        # - resolution (unit: arc-minutes)
        output_files[var_name]['par_name']['resolution_arcmin'] = 5. 
        if var == "surfaceWaterLevel": output_files[var_name]['par_name']['resolution_arcmin'] = 30.
        # - preparing netcdf files:
        output_files[var_name]['par_name']['file_name']         = output_files['folder'] + "/" + \
                                                                  varDict.netcdf_short_name[var_name] + \
                                                                  "_annual_flood_maxima.nc"
        msg = "Preparing the netcdf file: " + output_files[var_name]['par_name']['file_name']
        logger.info(msg)
        netcdf_report.createNetCDF(output_files[var_name]) 


# output of gumbel fits:
#
# PARAMETERS:
#
# For every return period
# - channel_storage
# - flood_innundation_volume
# -                             

# object for reporting/making netcdf files
netcdf_report = outputNetCDF.OutputNetCDF()




# the input (netcdf) file that will be used  
msg = "Using the following annual flood maxima (netcdf) files:"
logger.info(msg)
input_files['file_name']                           = {}
for var in ['channelStorage', 'dynamicFracWat', 'floodVolume']:
    input_files['file_name'][var] = glob.glob(input_files['folder'] + "/" + str(hydro_year) + "/" + str(var) + "*" + str(str_year) + "_to_" + str(end_year) + "*.nc")[0]
    msg = input_files['file_name'][var]
    logger.info(msg)


# set the pcraster clone, ldd, landmask, and cell area map 
msg = "Setting the clone, ldd, landmask, and cell area maps" + ":"
logger.info(msg)
# - clone 
clone_map_file = input_files['clone_map_05min']
pcr.setclone(clone_map_file)
# - ldd
ldd = vos.readPCRmapClone(input_files['ldd_map_05min'],
                          clone_map_file,
                          output_files['tmp_folder'],
                          None,
                          True)
ldd = pcr.lddrepair(pcr.ldd(ldd))
ldd = pcr.lddrepair(ldd)
# - landmask
landmask  = pcr.ifthen(pcr.defined(ldd), pcr.boolean(1.0))
# - cell area
cell_area = vos.readPCRmapClone(input_files['cell_area_05min'],
                          clone_map_file,
                          output_files['tmp_folder'])



# Get the gumbel fit parameters (derive_Gumbel)


# 




# loop through every year
msg = "Merging two hydrologyical years for the following variables:"
logger.info(msg)
#
for i_year in range(str_year, end_year + 1):
    
    for var in ['channelStorage', 'dynamicFracWat', 'floodVolume']:
        
        msg = "Merging for the variable " + str(var) + " for the year " + str(i_year)
        logger.info(msg)
        
        # time index for this year
        time_index_in_netcdf_file = i_year - str_year + 1
        
        value_from_the_hydrological_year_1 = vos.netcdf2PCRobjClone(input_files['file_name']["hydrological_year_1"][var], \
                                                                    varDict.netcdf_short_name[var], time_index_in_netcdf_file,\
                                                                    useDoy = "Yes",
                                                                    cloneMapFileName  = clone_map_file,\
                                                                    LatitudeLongitude = True,\
                                                                    specificFillValue = None)
        
        value_from_the_hydrological_year_2 = vos.netcdf2PCRobjClone(input_files['file_name']["hydrological_year_2"][var], \
                                                                    varDict.netcdf_short_name[var], time_index_in_netcdf_file,\
                                                                    useDoy = "Yes",
                                                                    cloneMapFileName  = clone_map_file,\
                                                                    LatitudeLongitude = True,\
                                                                    specificFillValue = None)
        
        # merging two hydrological years 
        value_for_this_year = pcr.ifthenelse(pcr.scalar(hydro_year_type) == 1, value_from_the_hydrological_year_1, \
                                                                               value_from_the_hydrological_year_2)
        value_for_this_year = pcr.cover(value_for_this_year, 0.0)
        
        if landmask_only: value_for_this_year = pcr.ifthen(landmask, value_for_this_year)
        
        # report to a netcdf file
        ncFileName = output_files[var]['file_name']
        msg = "Saving to the netcdf file: " + str(ncFileName)
        logger.info(msg)
        time_stamp_used = datetime.datetime(i_year, 12, 31, 0)
        netcdf_report.data2NetCDF(ncFileName, varDict.netcdf_short_name[var], pcr.pcr2numpy(value_for_this_year, vos.MV), time_stamp_used)

        
# - apply the gumbel fit

