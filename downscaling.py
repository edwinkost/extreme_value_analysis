#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
import shutil
import glob
import datetime

import pcraster as pcr

import virtualOS as vos

import logging
logger = logging.getLogger(__name__)

# from the system arguments, read the following:
# - input folder that contain extreme values (in pcraster format):
input_folder         = os.path.abspath(sys.argv[1])
# - global output folder
global_output_folder = os.path.abspath(sys.argv[2])
# - master ini file
ini_file             = os.path.abspath(sys.argv[3])
# - mask/code for this clone
mask_code            = str(sys.argv[4])

# output folder for this mask only
output_folder = global_output_folder + "/" + str(mask_code) + "/"

# clean any files exists on the ouput directory
clean_previous_output = True
if clean_previous_output and os.path.exists(output_folder): shutil.rmtree(output_folder)

# make output and log folders, and initialize logging:
log_file_folder = output_folder + "/log/"
if os.path.exists(log_file_folder) and clean_previous_output:  
    shutil.rmtree(log_file_folder)
    os.makedirs(log_file_folder)
if os.path.exists(log_file_folder) == False: 
    os.makedirs(log_file_folder)
vos.initialize_logging(log_file_folder)

# make tmp folder:
tmp_folder = general_output_folder + "/tmp/"
os.makedirs(tmp_folder)

# change the working directory to the output folder 
os.chdir(output_folder)

# copy ini file 
cmd = "cp " + str(ini_file) + " downscaling.ini" 
vos.cmd_line(cmd, using_subprocess = False)

# clone and landmask files at low resolution (e.g. 5 arc-minutes)
# - set clone map
clone_map_file    = "/projects/0/dfguu/data/hydroworld/others/05ArcMinCloneMaps/new_masks_from_top/clone_" + str(mask_code) + ".map" 
msg = "Set the pcraster clone map to : " + str(clone_map_file)
logger.info(msg)
pcr.setclone(clone_map_file)
# - set the landmask
landmask_map_file = "/projects/0/dfguu/data/hydroworld/others/05ArcMinCloneMaps/new_masks_from_top/mask_"  + str(mask_code) + ".map"
msg = "Set the landmask to : " + str(landmask_map_file)
logger.info(msg)
landmask = pcr.readmap(landmask_map_file)

# read all extreme value maps (low resolution maps), resample them, and save them to the output folder
msg = "Resampling extreme value maps."
logger.info(msg)
file_names = [   2-year_of_flood_innundation_volume.map,
                 5-year_of_flood_innundation_volume.map,
                10-year_of_flood_innundation_volume.map,
                25-year_of_flood_innundation_volume.map,
                50-year_of_flood_innundation_volume.map,
               100-year_of_flood_innundation_volume.map,
               250-year_of_flood_innundation_volume.map,
               500-year_of_flood_innundation_volume.map,
              1000-year_of_flood_innundation_volume.map]
for file_name in file_names:
    complete_file_name = input_folder + "/" + file_name
    extreme_value_map = vos.readPCRmapClone(complete_file_name, \
                                            clone_map_file, \
                                            tmp_folder, \
                                            None, False, None, False)
    # - focus only to the landmask area. We have to do this so that only flood in the landmask that will be downscaled/routed. 
    extreme_value_map = pcr.ifthen(landmask, extreme_value_map)
    # - cover the rests to zero (so they will not contribute to any flood/inundation)
    extreme_value_map = pcr.cover(extreme_value_map, 0.0)
    pcr.report(extreme_value_map, file_name)

# resampling low resolution ldd map
msg = "Resample the low resolution ldd map."
logger.info(msg)
ldd_map_low_resolution_file_name = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
ldd_map_low_resolution = vos.readPCRmapClone(ldd_map_low_resolution_file_name, \
                                             clone_map_file, \
                                             tmp_folder, \
                                             None, True, None, False)
#~ ldd_map_low_resolution = pcr.ifthen(landmask, ldd_map_low_resolution)  # NOTE THAT YOU SHOULD NOT MASK-OUT THE LDD.
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
                                                  True, False, None, False)
river_length_low_resolution = pcr.ifthen(landmask, river_length_low_resolution)
river_length_low_resolution = pcr.cover(river_length_low_resolution, 0.0)
pcr.report(river_length_low_resolution, "resampled_low_resolution_channel_length.map") 
# - river width
river_width_file_name = "/projects/0/dfguu/users/edwin/data/data_for_glofris_downscaling/input_data/maps_05min/celldiagonal05min.map"
river_width_low_resolution = vos.readPCRmapClone(river_width_file_name, \
                                                 clone_map_file, \
                                                 tmp_folder, \
                                                 True, False, None, False)
river_width_low_resolution = pcr.ifthen(landmask, river_width_low_resolution)
river_width_low_resolution = pcr.cover(river_width_low_resolution, 0.0)
pcr.report(river_width_low_resolution, "resampled_low_resolution_bankfull_width.map") 


# clone at high resolution (e.g. 30 arc-seconds)
msg = "Set the clone map at high resolution."
logger.info(msg)
num_of_rows = pcr.clone().nrRows() * 10
num_of_cols = pcr.clone().nrCols() * 10
x_min       = pcr.clone().west()
y_max       = pcr.clone().north()
cell_length = pcr.clone().cellSize() / 10.
# set the cell length manually
cell_length = 0.00833333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
#
# - make the map using 'mapattr' command 
cmd = 'mapattr -s -R ' + str(num_of_rows) + \
                ' -C ' + str(num_of_cols) + \
                ' -B -P yb2t ' + \
                ' -x ' + str(x_min) + \
                ' -y ' + str(y_max) + \
                ' -l ' + str() + \
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
# - dem map
dem_map_high_resolution_file_name = ""
dem_map_high_resolution = vos.readPCRmapClone(dem_map_high_resolution_file_name, \
                                              clone_map_file, \
                                              tmp_folder, \
                                              None, True, None, False)
dem_map_high_resolution = pcr.demrepair(pcr.dem(dem_map_high_resolution))
dem_map_high_resolution = pcr.demrepair(dem_map_high_resolution)
pcr.report(dem_map_high_resolution, "resampled_high_resolution_dem.map")
# - ldd map
ldd_map_high_resolution_file_name = ""
ldd_map_high_resolution = vos.readPCRmapClone(ldd_map_high_resolution_file_name, \
                                              clone_map_file, \
                                              tmp_folder, \
                                              None, True, None, False)
ldd_map_high_resolution = pcr.lddrepair(pcr.ldd(ldd_map_high_resolution))
ldd_map_high_resolution = pcr.lddrepair(ldd_map_high_resolution)
pcr.report(ldd_map_high_resolution, "resampled_high_resolution_ldd.map")


# calculating high resolution stream order maps
msg = "Calculating a high resolution stream order map."
logger.info(msg)
stream_order_map = pcr.streamorder(ldd_map_high_resolution)
pcr.report(stream_order_map, "resampled_high_resolution_ldd.map")


# execute downscaling scripts for every return period
msg = "Downscaling for every return period."
logger.info(msg)
for i_file in range(1, length(file_names)):
    file_name = file_name[i_file]
    cmd = ' python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py ' + \
          ' -i downscaling.ini ' + \
          ' -f ' + str(file_name) + \
          ' -b 2-year_of_flood_innundation_volume.map -c 4 -d output_folder'
    vos.cmd_line(cmd, using_subprocess = False)      
