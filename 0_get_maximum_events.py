#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob

import netCDF4 as nc
import numpy as np
import pcraster as pcr

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
input_files['channelStorageMonthMax'] = input_files['folder'] + "/channelStorage_monthMax_output_1958-01-31_to_2001-12-31.nc"                                    # unit: m3
input_files['dynamicFracWatMonthMax'] = input_files['folder'] + "/dynamicFracWat_monthMax_output_1958-01-31_to_2001-12-31.nc"                                    # unit: dimensionless
input_files['floodVolumeMonthMax']    = input_files['folder'] + "/floodVolume_monthMax_output_1958-01-31_to_2001-12-31.nc"                                       # unit: m3

# type of hydrological year
type_of_hydrological_year = 2         # hydrological year 1: October to September 
# - number of months to be shifted
num_of_shift_month = 9
if type_of_hydrological_year == 2:    # hydrological year 2: July to June
    num_of_shift_month = 6

# start and end years for this analysis (PS: after shifted)
str_year = 1960
end_year = 1999

# output files
output_files                      = {}
# - output folder
output_files['folder']            = "/scratch-shared/edwinsut/scratch_flood_analyzer/output/hydrological_year_" + str(type_of_hydrological_year) + "/"
try:
    os.makedirs(output_files['folder'] )
except:
    os.system('rm -r ' + output_files['folder']  + "/*")
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


# STEP 1: Using cdo shiftime to shift netcf file
msg = "Shifting netcdf time series to match the hydrological year " + str(type_of_hydrological_year) + " "
if type_of_hydrological_year == 1: msg = msg + "(October to September)"
if type_of_hydrological_year == 2: msg = msg + "(July to June)"
#
# - shifted input files
shifted_input_files           = {}
for var in ['channelStorageMonthMax', 'dynamicFracWatMonthMax', 'floodVolumeMonthMax']: 
    # - cdo shifttime
    inp_file = input_files[var]
    out_file = output_files['folder'] + "/" + os.path.basename(input_files[var]) + "_shifted_hydrological_year_" + str(type_of_hydrological_year) + ".nc"
    cmd = "cdo shifttime,-" + str(num_of_shift_month) + "mon " + inp_file + " " + out_file
    print(""); print(cmd); os.system(cmd); print("")
    shifted_input_files[var] = out_file


# STEP 2: Using cdo yearmax to find the annual maxima
#
# - annual maxima input files
annual_maxima_files           = {}
for var in ['channelStorageMonthMax', 'dynamicFracWatMonthMax', 'floodVolumeMonthMax']: 
    msg = "Find the annual maxima from the file " + str(shifted_input_files[var])
    logger.info(msg)
    # - cdo yearmax
    inp_file = shifted_input_files[var]
    out_file = shifted_input_files[var] + "_annual_maxima,nc"
    cmd = "cdo yearmax " + str(inp_file) + " " + str(out_file)
    print(""); print(cmd); os.system(cmd); print("")
    # - cdo selyear
    inp_file = out_file
    out_file = inp_file + "_" + str(str_year) + "_to_" + str(end_year) + ".nc"
    cmd = "cdo selyear," + str(str_year) + "/" + str(end_year) + " " + inp_file + " " + out_file
    print(""); print(cmd); os.system(cmd); print("")






