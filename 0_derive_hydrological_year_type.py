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


########################################################################
# The script to derive the type of hydrological year:
# - hydrological year 1: October to September 
# - hydrological year 2: July to June
########################################################################

# input files
input_files                           = {}
# PCR-GLOBWB 5 arcmin results
# - WATCH historical
input_files['folder']            = "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave/no_correction/non-natural/merged_1958_to_2001/global/netcdf/"
input_files['dischargeMonthAvg'] = input_files['folder'] + "discharge_monthAvg_output_1958-01-31_to_2001-12-31.nc"                                    # unit: m3/s
#
# General input files
# - clone map
input_files['clone_map_05min']   = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
# - cell area, ldd maps
input_files['cell_area_05min']   = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['ldd_map_05min']     = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
# - basin classification (raw file) 
input_files['basin_map_05min']   = "/projects/0/dfguu/users/edwin/data/aqueduct_gis_layers/aqueduct_shp_from_marta/Aqueduct_GDBD.map"

# start and end years for this analysis (PS: after shifted)
str_year = 1960
end_year = 1999

# output files
output_files                     = {}
# - output folder
output_files['folder']           = "/scratch-shared/edwinsut/flood_analyzer_analysis/hydrological_year/watch_1960-1999/"
#
try:
    os.makedirs(output_files['folder'])
except:
    #~ os.system('rm -r ' + output_files['folder']  + "/*")
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


# change to the output folder (use it as the working folder 
os.chdir(output_files['folder'])


# using cdo selyear to select the years that we choose: 
msg = "Selecting only the years " + str(str_year) + " to " + str(end_year) + ":"
logger.info(msg)
# - cdo selyear
inp_file = input_files['dischargeMonthAvg']
out_file = output_files['folder'] + "/monthly_discharge" + "_" + str(str_year) + "_to_" + str(end_year) + ".nc"
cmd = "cdo selyear," + str(str_year) + "/" + str(end_year) + " " + inp_file + " " + out_file
#~ print(""); print(cmd); os.system(cmd); print("")


# using cdo yearmax for calculating the climatology monthly discharge:
msg = "Calculating the climatology monthly discharge " + str(str_year) + " to " + str(end_year) + ":"
logger.info(msg)
# - cdo yearmax
inp_file = out_file
out_file = inp_file + "_climatology.nc"
cmd = "cdo ymonavg " + inp_file + " " + out_file
#~ print(""); print(cmd); os.system(cmd); print("")
input_files['climatologyDischargeMonthAvg'] = out_file


# using cdo timmax and timmax for calculating the maximum and average climatology monthly discharge
msg = "Calculating the maximum dicharge and average discharge from the climatology time series" + ":"
logger.info(msg)
# - cdo timmax
inp_file = input_files['climatologyDischargeMonthAvg']
out_file = inp_file + "_climatology_maximum.nc"
cmd = "cdo timmax " + inp_file + " " + out_file
#~ print(""); print(cmd); os.system(cmd); print("")
input_files['maximumClimatologyDischargeMonthAvg'] = out_file
# - cdo timavg
inp_file = input_files['climatologyDischargeMonthAvg']
out_file = inp_file + "_climatology_average.nc"
cmd = "cdo timavg " + inp_file + " " + out_file
#~ print(""); print(cmd); os.system(cmd); print("")
input_files['averageClimatologyDischargeMonthAvg'] = out_file


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


# set the basin map
msg = "Setting the basin map" + ":"
logger.info(msg)
basin_map = pcr.nominal(\
            vos.readPCRmapClone(input_files['basin_map_05min'],
                                input_files['clone_map_05min'],
                                output_files['tmp_folder'],
                                None, False, None, True))
pcr.aguila(basin_map)
# - extend/extrapolate the basin
basin_map = pcr.cover(basin_map, pcr.windowmajority(basin_map, 0.5))
basin_map = pcr.cover(basin_map, pcr.windowmajority(basin_map, 0.5))
basin_map = pcr.cover(basin_map, pcr.windowmajority(basin_map, 0.5))
basin_map = pcr.cover(basin_map, pcr.windowmajority(basin_map, 1.0))
basin_map = pcr.cover(basin_map, pcr.windowmajority(basin_map, 1.5))
basin_map = pcr.ifthen(landmask, basin_map)
pcr.aguila(basin_map)

msg = "Redefining the basin map (so that it is consistent with the ldd map used in PCR-GLOBWB):"
logger.info(msg)
# - Calculate the catchment area of every basin:
basin_area = pcr.areatotal(cell_area, basin_map)
# - Calculate the upstream area of every pixeL:
upstream_area = pcr.catchmenttotal(cell_area, ldd)
# - Identify the outlet of every basin (in order to rederive the basin so that it is consistent with the ldd)
outlet = pcr.nominal(pcr.uniqueid(pcr.ifthen(upstream_area == basin_area, pcr.boolean(1.0))))
pcr.aguila(outlet)
# - recalculate the basin
basin_map = pcr.ifthen(landmask, pcr.subcatchment(ldd, outlet))
pcr.aguila(basin_map)


# finding the month that give the maximum discharge (from the climatology time series)
msg = "Identifying the month with peak discharge (from climatology time series):"
logger.info(msg)
# - read the maximum monthly discharge for every basin
maximum_discharge = vos.netcdf2PCRobjClone(input_files['maximumClimatologyDischargeMonthAvg'], \
                                           "discharge", 1,\
                                           useDoy = "Yes",
                                           cloneMapFileName  = clone_map_file,\
                                           LatitudeLongitude = True,\
                                           specificFillValue = None)
maximum_discharge = pcr.areamaximum(\
                  pcr.cover(maximum_discharge, 0.0), basin_map)
# - find the month with maximum discharge
maximum_month = pcr.spatial(pcr.scalar(1.0))
for i_month in range(1, 12 + 1):
    # read the climatology discharge time series
    discharge_for_this_month = vos.netcdf2PCRobjClone(input_files['climatologyDischargeMonthAvg'], \
                                                      "discharge", i_month,\
                                                      useDoy = "Yes",
                                                      cloneMapFileName  = clone_map_file,\
                                                      LatitudeLongitude = True,\
                                                      specificFillValue = None)
    # upscale it to the basin scale
    discharge_for_this_month = pcr.areamaximum(maximum_discharge, basin_map)
    maximum_month = pcr.ifthenelse(discharge_for_this_month == maximum_discharge, pcr.scalar(i_month +1), maximum_month)
    	
# defining the hydrological year type
msg = "Defining the type of hydrological year:"
logger.info(msg)
hydrological_year_type = pcr.spatial(pcr.nominal(1))
hydrological_year_type = pcr.ifthenelse(maximum_month ==  9, pcr.nominal(2), hydrological_year_type)
hydrological_year_type = pcr.ifthenelse(maximum_month == 10, pcr.nominal(2), hydrological_year_type)
hydrological_year_type = pcr.ifthenelse(maximum_month == 11, pcr.nominal(2), hydrological_year_type)
pcr.aguila(hydrological_year_type)
pcr.report(hydrological_year_type, "hydrological_year_type.map")

