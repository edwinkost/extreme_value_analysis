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
#
# - input folders based on the system argument
input_files['folder'] = {}
input_files['folder']['channelStorage']    = os.path.abspath(sys.argv[1]) + "/"
input_files['folder']['surfaceWaterLevel'] = os.path.abspath(sys.argv[2]) + "/"
# -- an example: WATCH historical: "/scratch-shared/edwinhs-last/flood_analyzer_output/gumbel_fits/watch_1960-1999/"
#
input_files['file_name'] = {}
input_files['file_name']['channelStorage']    = input_files['folder']['channelStorage']    + "/" + "gumbel_analysis_output_for_channel_storage.nc" 
input_files['file_name']['surfaceWaterLevel'] = input_files['folder']['surfaceWaterLevel'] + "/" + "gumbel_analysis_output_for_surface_water_level.nc" 
#
# general input files
# - clone map
input_files['clone_map_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
pcr.setclone(input_files['clone_map_05min'])
# - cell area, ldd maps
input_files['cell_area_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['ldd_map_05min'  ] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
# - landmask
# -- default based on ldd
landmask = pcr.defined(pcr.readmap(input_files['ldd_map_05min']))
# -- additional landmask (to exclude river basins with limited meteo forcing coverage)
input_files['landmask_file']   = "/projects/0/aqueduct/users/edwinsut/data/landmasks_for_extreme_value_analysis_and_downscaling/landmask_extreme_value_analysis/landmask_extreme_value_analysis_05min.map"
if input_files['landmask_file'] != None:
    landmask = pcr.ifthen(landmask, pcr.readmap(input_files['landmask_file']))
#~ pcr.aguila(landmask)

# output files
output_files                   = {}
#
# output folder
#
#~ # - WATCH historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/watch_1960-1999/"
#~ # - gfdl-esm2m historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/gfdl-esm2m_1960-1999/"
#~ # - hadgem2-es historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/hadgem2-es_1960-1999/"
#~ # - ipsl-cm5a-lr historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/ipsl-cm5a-lr_1960-1999/"
#~ # - miroc-esm-chem historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/miroc-esm-chem_1960-1999/"
#~ # - noresm1-m historical
#~ output_files['folder']      = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/noresm1-m_1960-1999/"
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

# output netcdf file name (without extension) for the variable 'surfaceWaterLevel'
output_netcdf_file_name = "surface_water_level_historical_000000000WATCH_1999"
output_netcdf_file_name = str(sys.argv[6])

# option to limit only certain variables being processed
option_to_limit_variables = "None"
try:
    option_to_limit_variables = sys.argv[7]
except:
    pass
variable_name_list = ['channelStorage', 'surfaceWaterLevel']
if option_to_limit_variables != "None": variable_name_list = [option_to_limit_variables]


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
for var_name in variable_name_list: 
    #
    netcdf_file[var_name] = {}
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
    netcdf_file[var_name]['created on' ] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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




# applying gumbel parameters to get extrme values for every return period:
msg = "Applying gumbel parameters."
logger.info(msg)
#
# return periods
return_periods = ["2-year", "5-year", "10-year", "25-year", "50-year", "100-year", "250-year", "500-year", "1000-year"]
#
for var_name in variable_name_list: 
    
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
    
    # time bounds in a netcdf file
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
        
        # report to a pcraster map
        pcr.report(extreme_values[return_period], variable_name + ".map")

        # masking out based on the landmask
        extreme_values[return_period] = pcr.ifthen(landmask, extreme_values[return_period])
        pcr.report(extreme_values[return_period], variable_name + ".masked_out.map")
        
        # put it into a dictionary
        data_dictionary[variable_name] = pcr.pcr2numpy(extreme_values[return_period], vos.MV)

    # save the variables to a netcdf file
    netcdf_report.dictionary_of_data_to_netcdf(netcdf_file[var_name]['file_name'], \
                                               data_dictionary, \
                                               timeBounds)


###################################################################################


if 'surfaceWaterLevel' not in variable_name_list: sys.exit()

# masking out permanent water bodies
msg = "Preparing final netcdf files, one for every return period, as requested by Philip."
logger.info(msg)

#~ # permanent water bodies files (at 5 arc-minute resolution) 
#~ fracwat_file            = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/reservoirs/waterBodiesFinal_version15Sept2013/maps/fracwat_2010.map"
#~ water_body_id_file      = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/reservoirs/waterBodiesFinal_version15Sept2013/maps/waterbodyid_2010.map"
#~ 
#~ # read the properties of permanent water bodies
#~ fracwat            = pcr.cover(pcr.readmap(fracwat_file), 0.0)
#~ water_body_id      = pcr.readmap(water_body_id_file)
#~ water_body_id      = pcr.ifthen(pcr.scalar(water_body_id) > 0.00, water_body_id)
#~ water_body_area    = pcr.areatotal(input_files['cell_area_05min'] * fracwat, water_body_id)
#~ water_body_area    = pcr.cover(water_body_area, 0.0)
#~ water_body_id      = pcr.cover(water_body_id, pcr.nominal(0.0))
#~ water_body_id      = pcr.ifthen( landmask, water_body_id)                                         
#~ non_permanent_water_bodies = pcr.boolean(1.0)
#~ non_permanent_water_bodies = pcr.ifthenelse(water_body_area > 50. * 1000. * 1000., pcr.boolean(0.0), non_permanent_water_bodies)
#~ non_permanent_water_bodies = pcr.ifthen(landmask, non_permanent_water_bodies)
#~ pcr.aguila(non_permanent_water_bodies)

# - time bounds for netcdf files
lowerTimeBound = datetime.datetime(str_year,  1,  1, 0)
upperTimeBound = datetime.datetime(end_year, 12, 31, 0)
timeBounds = [lowerTimeBound, upperTimeBound]

# - variable name according to the PCR-GLOBWB variable dictionary
var_name = 'surfaceWaterLevel' 

# - return periods
return_periods      = [ "2-year",  "5-year", "10-year", "25-year", "50-year", "100-year", "250-year", "500-year", "1000-year"]
return_period_codes = ["rp00002", "rp00005", "rp00010", "rp00025", "rp00050",  "rp00100",  "rp00250",  "rp00500",   "rp01000"]

# preparing netcdf files and their variables:
var_name = "surfaceWaterLevel"
for i_return_period in range(0, len(return_periods)):
    # 
    return_period      = return_periods[i_return_period]
    return_period_code = return_period_codes[i_return_period]
    # 
    # - preparing netcdf file:
    file_name = output_files['folder'] + "/" + output_netcdf_file_name + "_" + return_period_code + ".nc"
    msg = "Preparing the netcdf file: " + file_name
    logger.info(msg)
    netcdf_file[var_name]['file_name'] = file_name
    netcdf_report.create_netcdf_file(netcdf_file[var_name]) 
    #
    # - variable name and unit 
    variable_name = str(return_period) + "_of_" + varDict.netcdf_short_name[var_name]
    var_long_name = str(return_period) + "_of_" + varDict.netcdf_long_name[var_name]
    variable_unit = varDict.netcdf_unit[var_name]
    # 
    # - creating variable 
    netcdf_report.create_variable(\
                                  ncFileName = file_name, \
                                  varName    = variable_name, \
                                  varUnit    = variable_unit, \
                                  longName   = var_long_name, \
                                  comment    = varDict.comment[var_name]
                                  )

    # read from pcraster files
    surface_water_level_file_name = output_files['folder'] + "/" + str(return_period) + "_of_surface_water_level" + ".map"
    surface_water_level = pcr.readmap(surface_water_level_file_name)
    surface_water_level = pcr.cover(surface_water_level, 0.0)
    
    # masking out based on the landmask
    surface_water_level = pcr.ifthen(landmask, surface_water_level)

    #~ # masking out permanent water bodies
    #~ surface_water_level = pcr.ifthen(non_permanent_water_bodies, surface_water_level)

    # report in pcraster maps
    pcr.report(surface_water_level, surface_water_level_file_name + ".masked_out.map")
    
    # write to netcdf files
    netcdf_report.data_to_netcdf(file_name, variable_name, pcr.pcr2numpy(surface_water_level, vos.MV), timeBounds, timeStamp = None, posCnt = 0)
