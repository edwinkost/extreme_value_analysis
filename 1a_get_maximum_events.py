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
#
#~ # - WATCH historical
#~ input_files['folder']                 = "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave/no_correction/non-natural/merged_1958_to_2001/global/netcdf/"
#~ input_files['channelStorageMonthMax'] = input_files['folder'] + "channelStorage_monthMax_output_1958-01-31_to_2001-12-31.nc"                                    # unit: m3
#~ input_files['dynamicFracWatMonthMax'] = input_files['folder'] + "dynamicFracWat_monthMax_output_1958-01-31_to_2001-12-31.nc"                                    # unit: dimensionless
#~ input_files['floodVolumeMonthMax']    = input_files['folder'] + "floodVolume_monthMax_output_1958-01-31_to_2001-12-31.nc"                                       # unit: m3
#~ #
#~ # - GCM historical: noresm1-m 
#~ input_files['folder']                 = "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m/no_correction/non-natural/merged_1951-2005/global/netcdf/"
#~ input_files['channelStorageMonthMax'] = input_files['folder'] + "channelStorage_monthMax_output_1951-01-31_to_2005-12-31.nc"                                    # unit: m3
#~ input_files['dynamicFracWatMonthMax'] = input_files['folder'] + "dynamicFracWat_monthMax_output_1951-01-31_to_2005-12-31.nc"                                    # unit: dimensionless
#~ input_files['floodVolumeMonthMax']    = input_files['folder'] + "floodVolume_monthMax_output_1951-01-31_to_2005-12-31.nc"                                       # unit: m3
#
# - cru-ts3.23_era-20c_kinematicwave 
input_files['folder']                 = "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave/no_correction/non-natural/merged_1958-2010/global/netcdf/"
input_files['channelStorageMonthMax'] = input_files['folder'] + "channelStorage_monthMax_output_1958-01-31_to_2010-12-31.nc"                                    # unit: m3
input_files['dynamicFracWatMonthMax'] = input_files['folder'] + "dynamicFracWat_monthMax_output_1958-01-31_to_2010-12-31.nc"                                    # unit: dimensionless
input_files['floodVolumeMonthMax']    = input_files['folder'] + "floodVolume_monthMax_output_1958-01-31_to_2010-12-31.nc"                                       # unit: m3
#
#~ # pcrglobwb result folder based on the system argument
#~ pcrglobwb_result_folder                  = os.path.abspath(sys.argv[1])
#~ input_files['folder']                    = pcrglobwb_result_folder + "/"
#~ input_files['channelStorageMonthMax']    = input_files['folder'] + "channelStorage_monthMax_output_2006-01-31_to_2099-12-31.nc"                                    # unit: m3
#~ input_files['dynamicFracWatMonthMax']    = input_files['folder'] + "dynamicFracWat_monthMax_output_2006-01-31_to_2099-12-31.nc"                                    # unit: dimensionless
#~ input_files['floodVolumeMonthMax']       = input_files['folder'] + "floodVolume_monthMax_output_2006-01-31_to_2099-12-31.nc"                                       # unit: m3


# type of hydrological year
# - hydrological year 1: October to September 
# - hydrological year 2: July to June
#~ type_of_hydrological_year = 1         
#
# type of hydrological year based on the system argument
type_of_hydrological_year        = np.int(sys.argv[2])
print type_of_hydrological_year
print type_of_hydrological_year
print type_of_hydrological_year



# number of months to be shifted (based on hydrological year)
num_of_shift_month = 9                                                  # hydrological year 1: October to September 
if type_of_hydrological_year == 2: num_of_shift_month = 6               # hydrological year 2: July to June


# output files
output_files                         = {}
# - output folder
#
#~ # - WATCH historical
#~ output_files['folder']            = "/scratch-shared/edwinsut/flood_analyzer_analysis/maximum_events/watch_1960-1999/hydrological_year_" + str(type_of_hydrological_year) + "/"
#~ #
#~ # - GCM historical: noresm1-m
#~ output_files['folder']            = "/scratch-shared/edwinsut/flood_analyzer_analysis/maximum_events/noresm1-m_1960-1999/hydrological_year_" + str(type_of_hydrological_year) + "/"
#
# - cru-ts3.23_era-20c_kinematicwave 
output_files['folder']               = "/scratch-shared/edwinsut/flood_analyzer_analysis/maximum_events/cru-ts3.23_era-20c_kinematicwave/hydrological_year_" + str(type_of_hydrological_year) + "/"
#
#~ # output folder based on the system argument
#~ output_folder_for_this_analysis   = sys.argv[3]
#~ output_files['folder']            = output_folder_for_this_analysis + "/hydrological_year_" + str(type_of_hydrological_year) + "/" 
#
#
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


# start and end years for this analysis:
# - for historical runs
str_year = 1960
end_year = 1999
#~ # - for the year 2030
#~ str_year = 2010
#~ end_year = 2049
#~ # - for the year 2050
#~ str_year = 2030
#~ end_year = 2069
#~ # - for the year 2080
#~ str_year = 2060
#~ end_year = 2099
#
# - based on the system argument
str_year = int(sys.argv[4])
end_year = int(sys.argv[5])


# STEP 1: Using cdo shiftime to shift netcf file
msg = "Shifting netcdf time series to match the hydrological year " + str(type_of_hydrological_year) + " "
if type_of_hydrological_year == 1: msg = msg + "(October to September)"
if type_of_hydrological_year == 2: msg = msg + "(July to June)"
#
# - shifted input files
shifted_input_files           = {}
cmd = ""
for var in ['channelStorageMonthMax', 'dynamicFracWatMonthMax', 'floodVolumeMonthMax']: 
    # - cdo shifttime
    inp_file = input_files[var]
    out_file = output_files['folder'] + "/" + os.path.basename(input_files[var]) + "_shifted_hydrological_year_" + str(type_of_hydrological_year) + ".nc"
    cmd += "cdo shifttime,-" + str(num_of_shift_month) + "mon " + inp_file + " " + out_file
    cmd += " & "
    shifted_input_files[var] = out_file
cmd += " wait "
print(""); print(cmd); os.system(cmd); print("")

# STEP 2: Using cdo yearmax to find the annual maxima
#
# - annual maxima input files
annual_maxima_files           = {}
for var in ['channelStorageMonthMax', 'dynamicFracWatMonthMax', 'floodVolumeMonthMax']: 
    msg = "Find the annual maxima from the file " + str(shifted_input_files[var])
    logger.info(msg)
    # - cdo yearmax
    inp_file = shifted_input_files[var]
    out_file = shifted_input_files[var] + "_annual_maxima.nc"
    cmd = "cdo yearmax " + str(inp_file) + " " + str(out_file)
    print(""); print(cmd); os.system(cmd); print("")
    # - cdo selyear
    inp_file = out_file
    out_file = inp_file + "_" + str(str_year) + "_to_" + str(end_year) + ".nc"
    cmd = "cdo selyear," + str(str_year) + "/" + str(end_year) + " " + inp_file + " " + out_file
    print(""); print(cmd); os.system(cmd); print("")






