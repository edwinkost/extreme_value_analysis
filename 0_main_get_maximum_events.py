#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob

# pcraster dynamic framework is used.
from pcraster.framework import DynamicFramework

# netcdf reporting module:
import outputNetCDF

# utility module:
import virtualOS as vos

# variable dictionaries:
import aqueduct_flood_analyzer_variable_list as varDict

import logging
logger = logging.getLogger(__name__)

# input files
input_files                           = {}
# PCR-GLOBWB 5 arcmin results
input_files['folder']                 = "/scratch/shared/edwinhs-last/scratch_flood_analyzer/watch_results/merged_1958-2001/global/netcdf/"
input_files['channelStorageMonthMax'] = glob.glob(input_files['folder'] + "channelStorage_monthMax*.nc")                                     # unit: m3
input_files['dynamicFracWatMonthMax'] = glob.glob(input_files['folder'] + "dynamicFracWat_monthMax*.nc")                                     # unit: dimensionless
input_files['floodVolumeMonthMax']    = glob.glob(input_files['folder'] + "floodVolume_monthMax*.nc"   )                                     # unit: m3
# - general input data
input_files['cellarea_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['clone_05min']    = input_files['cellarea_05min']
input_files['clone_30min']    = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"

# type of hydrological year
type_of_hydrological_year = 1         # hydrological year 1: October to September 
# - number of months to be shifted
num_of_shift_month = 9
if type_of_hydrological_year == 2:    # hydrological year 2: July to June
    num_of_shift_month = 6

# start and end years for this analysis (PS: after shifted)
str_year = 1960
end_year = 1999

# netcdf general setup:
netcdf_setup = {}
netcdf_setup['format']          = "NETCDF4"
netcdf_setup['zlib']            = True
netcdf_setup['institution']     = "Department of Physical Geography, Utrecht University"
netcdf_setup['title'      ]     = "PCR-GLOBWB 2 output - post-processed for Aqueduct Flood Analyzer"
netcdf_setup['created by' ]     = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['description']     = 'The annual flood maxima for each year/period starting from October of the year until September of its following year.'
if type_of_hydrological_year == 2:
    netcdf_setup['description'] = 'The annual flood maxima for each year/period starting from July of the year until June of its following year.'

# output files
output_files                      = {}
# - output folder
output_files['folder']            = "/scratch-shared/edwinhs-last/scratch_flood_analyzer/output/"
try:
    os.makedirs(output['folder'])
except:
    os.system('rm -r ' + output['folder'] + "/*")
    pass
# - temporary output folder (e.g. needed for resampling/gdalwarp)
output_files['tmp_folder']        = output_files['folder'] + "/tmp/"
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

# object for reporting/making netcdf files
netcdf_report = outputNetcdf.OutputNetcdf()

# - variables that will be reported:
variable_names = ['channelStorage', 'floodVolume', 'dynamicFracWat', 'surfaceWaterlevel']
#
for var_name in variable_names: 
    output_files[var_name] = {}
    # - attribute information for netcdf files
    output_files[var_name]['short_name']        = varDict.netcdf_short_name[var_name]
    output_files[var_name]['unit']              = varDict.netcdf_unit[var_name]
    output_files[var_name]['long_name']         = varDict.netcdf_long_name[var_name]          
    output_files[var_name]['comment']           = varDict.comment[var_name]               
    output_files[var_name]['description']       = varDict.description[var_name]
    # - add more information 
    if output_files[var_name]['long_name']   == None: output_files[var_name]['long_name']   = output_files[var_name]['short_name']
    if output_files[var_name]['comment']     == None: output_files[var_name]['comment'] = ""
    if output_files[var_name]['description'] == None: output_files[var_name]['description'] = ""
    output_files[var_name]['description']       = netcdf_setup['description'] + " " + output_files[var_name]['description']
    output_files[var_name]['institution']       = netcdf_setup['institution']
    output_files[var_name]['title'      ]       = netcdf_setup['title'      ]
    output_files[var_name]['created by' ]       = netcdf_setup['created by' ]
    output_files[var_name]['description']       = netcdf_setup['description']
    # - resolution
    output_files[var_name]['resolution_arcmin'] = 5. # unit: arc-minutes
    # - the surfaceWaterLevel will be reported at 30 arc-minute resolution
    if var_name == "surfaceWaterlevel": output_files[var_name]['resolution_arcmin'] = 30. 
    # - preparing netcdf files:
    output_files[var_name]['file_name']         = input_files['folder'] + "/" + \
                                                  varDict.netcdf_short_name[var_name] + \
                                                  "_annual_maxima_for_hydrological_year_" + str(type_of_hydrological_year) +  ".nc"
    netcdf_report.createNetCDF(output_files[var_name]['file_name']) 


# STEP 1: Using cdo shiftime to shift netcf file
msg = "Shifting netcdf time series to match the hydrological year " + str(type_of_hydrological_year) + ")"
logger.info(msg)
# - shifted input files
shifted_input_files                           = {}
shifted_input_files['folder']                 = output_files['folder']
for var in ['channelStorageMonthMax', 'dynamicFracWatMonthMax', 'floodVolumeMonthMax']: 
    # - cdo shifttime
    inp_file = input_files[var]
    out_file = shifted_input_files['folder'] + "/" + os.path.basename(input_files[var]) + "_shifted_hydrological_year_" + str(type_of_hydrological_year) + ".nc"
    cmd = "cdo shiftime,-" + str(num_of_shift_month) + "mon " + inp_file + " " + out_file
    print(cmd); os.system(cmd)
    # - cdo selyear
    inp_file = out_file
    out_file = inp_file + "_" + str(str_year) + "_" + str(end_year) + ".nc"
    cmd = "cdo selyear," + str(str_year) + "/" + str(end_year) + " " + inp_file + " " + out_file
    print(cmd); os.system(cmd)
    shifted_input_files[var] = out_file


# STEP 2: Find the annual maxima of channelStorage
msg = "Find the annua maxima of channelStorage from the file " + str(shifted_input_files['channelStorageMonthMax'])
logger.info(msg)
inp_file = shifted_input_files['channelStorageMonthMax']
out_file = shifted_input_files['channelStorageMonthMax'] + "_annual_maxima,nc"
cmd = "cdo yearmax" + str(inp_file) + " " + str(out_file)
print(cmd); os.system(cmd)
annual_maxima_channel_storage_file = out_file


