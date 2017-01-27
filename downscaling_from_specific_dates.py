#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
import shutil
import glob
import datetime
import numpy as np

import pcraster as pcr

import virtualOS as vos

import logging
logger = logging.getLogger(__name__)

# from the system arguments, read the following:
# - netcdf input file
input_netcdf_file = "/projects/0/dfguu/users/edwinhs/data/from_niko_inundation_paper/simulation_result/channelStorage/Global_2000_landCover/netcdf/channelStorage_dailyTot.nc"
input_netcdf_file = os.path.abspath(sys.argv[1])
# - netcdf variable name
nc_variable_name  = "channelStorage"
nc_variable_name  = str(sys.argv[2])
# - date (YYYY-MM-DD) that will be analyzed/downscaled
chosen_date       = "1993-07-27"
chosen_date       = str(sys.argv[3])
# - output folder
output_folder     = "output_folder"
output_folder     = str(sys.argv[4])
# - landmask/clone map
landmask_map      = "/projects/0/dfguu/data/hydroworld/others/Mississippi/Mississippi30min.clone.map"
# - bankfull channel capacity file (in pcraster format)
channel_capacity  = "/projects/0/dfguu/users/edwinhs/data/from_niko_inundation_paper/simulation_result/maps/channel_capacity.map"
# - ldd map at low resolution
ldd_map_low_resolution_file_name = "/projects/0/dfguu/users/edwinhs/data/from_niko_inundation_paper/simulation_result/maps/"
# - netcdf file for water bodies (lakes/reservoirs, low resolution)
water_body_file   = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input30min/routing/reservoirs/fromRensJune2013/reservoirparameterization/waterBodies30min.nc"
# - year used for water body
water_body_year   = 1993

# clean any files exists on the ouput directory
clean_previous_output = True
if clean_previous_output and os.path.exists(output_folder): shutil.rmtree(output_folder)

# make output and log folders, and initialize logging:
log_file_folder = output_folder + "/log/"
if os.path.exists(log_file_folder): shutil.rmtree(log_file_folder)
os.makedirs(log_file_folder)
vos.initialize_logging(log_file_folder)

# make tmp folder:
tmp_folder = output_folder + "/tmp/"
if os.path.exists(tmp_folder): shutil.rmtree(tmp_folder)
os.makedirs(tmp_folder)

# copy ini file 
cmd = "cp downscaling.ini " + output_folder + "/downscaling.ini" 
vos.cmd_line(cmd, using_subprocess = False)

# change the working directory to the output folder 
os.chdir(output_folder)

# clone and landmask files at low resolution (e.g. 5 arc-minutes)
# - set clone map
clone_map_file    = landmask_map
msg = "Set the pcraster clone map to : " + str(clone_map_file)
logger.info(msg)
pcr.setclone(clone_map_file)
# - set the landmask
landmask_map_file = landmask_map
msg = "Set the landmask to : " + str(landmask_map_file)
logger.info(msg)
landmask = pcr.readmap(landmask_map_file)

# read the event map (low resolution), resample, and save to the output folder
msg = "Resampling the event map."
logger.info(msg)
extreme_value_map = vos.netcdf2PCRobjClone(ncFile = input_netcdf_file, varName = nc_variable_name, dateInput = chosen_date,\
                                           useDoy = None,
                                           cloneMapFileName  = clone_map_file,\
                                           LatitudeLongitude = True,\
                                           specificFillValue = None,\
                                           automaticMatchingVariableName = True)
# - focus only to the landmask area. We have to do this so that only flood in the landmask that will be downscaled/routed. 
extreme_value_map = pcr.ifthen(landmask, extreme_value_map)
# - cover the rests to zero (so they will not contribute to any flood/inundation)
extreme_value_map = pcr.cover(extreme_value_map, 0.0)
event_file_name   = "channel_storage_" + chosen_date + ".map"
pcr.report(extreme_value_map, event_file_name)

# resampling low resolution ldd map
msg = "Resample the low resolution ldd map."
logger.info(msg)
ldd_map_low_resolution_file_name = ldd_map_low_resolution_file_name
ldd_map_low_resolution = vos.readPCRmapClone(ldd_map_low_resolution_file_name, \
                                             clone_map_file, \
                                             tmp_folder, \
                                             None, True, None, False)
#~ ldd_map_low_resolution = pcr.ifthen(landmask, ldd_map_low_resolution)    # NOTE THAT YOU SHOULD NOT MASK-OUT THE LDD.
ldd_map_low_resolution = pcr.lddrepair(pcr.ldd(ldd_map_low_resolution))
ldd_map_low_resolution = pcr.lddrepair(ldd_map_low_resolution)
pcr.report(ldd_map_low_resolution, "resampled_low_resolution_ldd.map")

# resampling river length and width files (actually, we don't need these):
msg = "Resample the low resolution river length and width maps."
logger.info(msg)
# - river length
river_length_file_name = "/projects/0/dfguu/users/edwin/data/data_for_glofris_downscaling/input_data/maps_05min/celldiagonal05min.map"
river_length_low_resolution = vos.readPCRmapClone(river_length_file_name, \
                                                  clone_map_file, \
                                                  tmp_folder, \
                                                  None, False, None, False)
river_length_low_resolution = pcr.ifthen(landmask, river_length_low_resolution)
river_length_low_resolution = pcr.cover(river_length_low_resolution, 0.0)
pcr.report(river_length_low_resolution, "resampled_low_resolution_channel_length.map") 
# - river width
river_width_file_name = "/projects/0/dfguu/users/edwin/data/data_for_glofris_downscaling/input_data/maps_05min/bankfull_width.map"
river_width_low_resolution = vos.readPCRmapClone(river_width_file_name, \
                                                 clone_map_file, \
                                                 tmp_folder, \
                                                 None, False, None, False)
river_width_low_resolution = pcr.ifthen(landmask, river_width_low_resolution)
river_width_low_resolution = pcr.cover(river_width_low_resolution, 0.0)
pcr.report(river_width_low_resolution, "resampled_low_resolution_bankfull_width.map") 


# resampling bankfull channel capacity file
msg = "Resample the channel capacity maps."
logger.info(msg)
channel_capacity_file_name = ldd_map_low_resolution_file_name
channel_capacity = vos.readPCRmapClone(channel_capacity_file_name, \
                                       clone_map_file, \
                                       tmp_folder, \
                                       None, True, None, False)
channel_capacity = pcr.ifthen(landmask, channel_capacity)
channel_capacity = pcr.cover(channel_capacity, 0.0)
pcr.report(channel_capacity, "channel_capacity.map")

# - TODO: ADD capacities of lakes/reservoies 

# clone at high resolution (e.g. 30 arc-seconds)
msg = "Set the clone map at high resolution."
logger.info(msg)
# set the cell length manually
cell_length = '0.00833333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333'
factor = np.round(
         vos.getMapAttributes(ldd_map_high_resolution_file_name, "cellsize") / cell_length, 2)
# numbers of rows and columns
num_of_rows = np.round(pcr.clone().nrRows() * factor   , 2)
num_of_cols = np.round(pcr.clone().nrCols() * factor   , 2)
# upper left corner coordinate
x_min       = np.round(pcr.clone().west()          , 2)
y_max       = np.round(pcr.clone().north()         , 2)
#
# - make the map using 'mapattr' command 
cmd = 'mapattr -s -R ' + str(num_of_rows) + \
                ' -C ' + str(num_of_cols) + \
                ' -B -P yb2t ' + \
                ' -x ' + str(x_min) + \
                ' -y ' + str(y_max) + \
                ' -l ' + str(cell_length) + \
                ' clone_high_resolution.map'
vos.cmd_line(cmd, using_subprocess = False)
#
# - set the clone map
clone_map_file = os.path.abspath("clone_high_resolution.map")
msg = "Set the clone map at high resolution to the file: " + str(clone_map_file)
logger.info(msg)
pcr.setclone(clone_map_file)
 

# resampling high resolution dem and ldd maps
msg = "Resampling high resolution dem and ldd maps."
logger.info(msg)
# - ldd map
ldd_map_high_resolution_file_name = "/projects/0/dfguu/users/edwinhs/data/HydroSHEDS/hydro_basin_without_lakes/integrating_ldd/version_9_december_2016/merged_ldd.map"
ldd_map_high_resolution = vos.readPCRmapClone(ldd_map_high_resolution_file_name, \
                                              clone_map_file, \
                                              tmp_folder, \
                                              None, True, None, False)
#~ ldd_map_high_resolution = pcr.cover(ldd_map_high_resolution, pcr.ldd(5))	# YOU SHOULD NOT DO THIS
ldd_map_high_resolution = pcr.lddrepair(pcr.ldd(ldd_map_high_resolution))
ldd_map_high_resolution = pcr.lddrepair(ldd_map_high_resolution)
pcr.report(ldd_map_high_resolution, "resampled_high_resolution_ldd.map")
# - dem map
dem_map_high_resolution_file_name = "/projects/0/dfguu/users/edwinhs/data/HydroSHEDS/hydro_basin_without_lakes/integrating_ldd/version_9_december_2016/cover_SRTM_1km_merge_gtopo_masked.map"
dem_map_high_resolution = vos.readPCRmapClone(dem_map_high_resolution_file_name, \
                                              clone_map_file, \
                                              tmp_folder, \
                                              None, False, None, False)
dem_map_high_resolution = pcr.cover(dem_map_high_resolution, 0.0)
# - use dem only where ldd are defined
dem_map_high_resolution = pcr.ifthen(pcr.defined(ldd_map_high_resolution) , dem_map_high_resolution)
pcr.report(dem_map_high_resolution, "resampled_high_resolution_dem.map")


# calculating high resolution stream order maps
msg = "Calculating a high resolution stream order map."
logger.info(msg)
stream_order_map = pcr.streamorder(ldd_map_high_resolution)
pcr.report(stream_order_map, "high_resolution_stream_order.map")


# execute downscaling script
msg = "Downscaling."
logger.info(msg)
file_name = file_names[i_file]
cmd = ' python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py ' + \
      ' -i downscaling.ini ' + \
      ' -f ' + str(event_file_name) + \
      ' -b channel_capacity.map ' + \
      ' -c 4 -d output_folder'
vos.cmd_line(cmd, using_subprocess = False)

# make an empty file to indicate that this downscaling script is done      
filename = "downscaling_is_done.txt"
if os.path.exists(filename): os.remove(filename)
open(filename, "w").close()    


