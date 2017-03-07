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
# - input folder that contain extreme values (in pcraster format):
input_folder         = os.path.abspath(sys.argv[1])
# - global output folder
global_output_folder = os.path.abspath(sys.argv[2])
# - master ini file
ini_file             = os.path.abspath(sys.argv[3])
# - mask/code for this clone
mask_code            = str(sys.argv[4])
# - type of files (options are: "normal"; "bias_corrected"; and "including_bias")
type_of_files        = str(sys.argv[5])
# - option for map types: *flood_inundation_volume.map or *channel_storage.map
map_type_name        = "channel_storage.map"
map_type_name        = str(sys.argv[6])

# - option for masking out permanent water bodies (valid only if map_type_name = "channel_storage.map")
masking_out_permanent_water_bodies = False
masking_out_permanent_water_bodies = sys.argv[7] == "masking_out_permanent_water_bodies" 

# output folder for this mask only
output_folder = global_output_folder + "/" + str(mask_code) + "/"

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

# permanent water bodies files:
reservoir_capacity_file = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/reservoirs/waterBodiesFinal_version15Sept2013/maps/reservoircapacity_2010.map"
fracwat_file            = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/reservoirs/waterBodiesFinal_version15Sept2013/maps/fracwat_2010.map"
water_body_id_file      = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/reservoirs/waterBodiesFinal_version15Sept2013/maps/waterbodyid_2010.map"

# cell_area_file
cell_area_file = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"

# read all extreme value maps (low resolution maps), resample them, and save them to the output folder
msg = "Resampling extreme value maps."
logger.info(msg)
file_names = [   '2-year_of_flood_inundation_volume.map',
                 '5-year_of_flood_inundation_volume.map',
                '10-year_of_flood_inundation_volume.map',
                '25-year_of_flood_inundation_volume.map',
                '50-year_of_flood_inundation_volume.map',
               '100-year_of_flood_inundation_volume.map',
               '250-year_of_flood_inundation_volume.map',
               '500-year_of_flood_inundation_volume.map',
              '1000-year_of_flood_inundation_volume.map']
if map_type_name == "channel_storage.map":
   file_names = [   '2-year_of_channel_storage.map',
                    '5-year_of_channel_storage.map',
                   '10-year_of_channel_storage.map',
                   '25-year_of_channel_storage.map',
                   '50-year_of_channel_storage.map',
                  '100-year_of_channel_storage.map',
                  '250-year_of_channel_storage.map',
                  '500-year_of_channel_storage.map',
                 '1000-year_of_channel_storage.map']
front_name = ""
if type_of_files != "normal": front_name = type_of_files + "_"
for i_file in range(0, len(file_names)):
#~ for i_file in range(0, 1):
    file_name = file_names[i_file]
    complete_file_name = input_folder + "/" + front_name + file_name
    extreme_value_map = pcr.cover(
                        vos.readPCRmapClone(complete_file_name, \
                                            clone_map_file, \
                                            tmp_folder, \
                                            None, False, None, False), 0.0)
    # - focus only to the landmask area. We have to do this so that only flood in the landmask that will be downscaled/routed. 
    extreme_value_map = pcr.ifthen(landmask, extreme_value_map)
    #
    # - masking out permanent water bodies
    if masking_out_permanent_water_bodies:
        cell_area = pcr.ifthen(landmask, \
                    pcr.cover(\
                    vos.readPCRmapClone(cell_area_file, \
                                        clone_map_file, \
                                        tmp_folder, \
                                        None, False, None, False), 0.0))
        # read the properties of permanent water bodies
        fracwat            = pcr.ifthen(landmask, \
                             pcr.cover(\
                             vos.readPCRmapClone(fracwat_file, \
                                                 clone_map_file, \
                                                 tmp_folder, \
                                                 None, False, None, False), 0.0))
        reservoir_capacity = pcr.ifthen(landmask, \
                             pcr.cover(\
                             vos.readPCRmapClone(reservoir_capacity_file, \
                                                 clone_map_file, \
                                                 tmp_folder, \
                                                 None, False, None, False), 0.0)) * 1000. * 1000.
        water_body_id      = vos.readPCRmapClone(water_body_id_file, \
                                                 clone_map_file, \
                                                 tmp_folder, \
                                                 None, False, None, True )
        water_body_id      = pcr.ifthen(pcr.scalar(water_body_id) > 0.00, water_body_id)
        water_body_id      = pcr.ifthen( landmask, water_body_id)                                         
        #
        # calculate overbank volume from lakes and reservoirs
        lake_reservoir_volume          = pcr.areatotal(extreme_value_map, water_body_id)
        lake_reservoir_overbank_volume = pcr.cover(
                                         pcr.max(0.0, lake_reservoir_volume - reservoir_capacity), 0.0)
        #~ pcr.aguila(lake_reservoir_overbank_volume)
        land_area = cell_area * pcr.max(0.0, 1.0 - fracwat)
        # distribute spills from reservoirs only in their shores 
        land_area_average = pcr.areaaverage(land_area, water_body_id) 
        land_area_weight  = pcr.ifthenelse(land_area < land_area_average, 0.0, land_area_average)
        distributed_lake_reservoir_overbank_volume = pcr.cover(\
                                                     lake_reservoir_overbank_volume * land_area / pcr.max(0.00, pcr.areatotal(land_area_weight, water_body_id)), 0.0)
        extreme_value_map = pcr.ifthenelse(reservoir_capacity > 0.0, distributed_lake_reservoir_overbank_volume, extreme_value_map)
        #~ pcr.aguila(extreme_value_map)
        #
        #~ # masking out all water above lakes and reservoirs
        #~ masked_out = pcr.boolean(0)
        #~ masked_out = pcr.defined(water_body_id)
        #~ # masking out all cells with fracwat > 0.20
        #~ masked_out = pcr.cover(
                     #~ pcr.ifthen(fracwat > 0.20, pcr.boolean(1)), masked_out)
        #~ masked_out = pcr.cover(masked_out, pcr.boolean(0))
        #~ masked_out_scalar = pcr.ifthen(masked_out, pcr.scalar(1.0))
        #~ pcr.report(masked_out_scalar, "permanent_water_bodies.map")
        #~ extreme_value_map = pcr.ifthenelse(masked_out, 0.0, extreme_value_map)
    #
    # - cover the rests to zero (so they will not contribute to any flood/inundation)
    extreme_value_map = pcr.cover(extreme_value_map, 0.0)
    #
    # - make sure that extreme value maps increasing over return period 
    if i_file == 0: previous_return_period_map = extreme_value_map
    if i_file >  0: extreme_value_map = pcr.max(previous_return_period_map, extreme_value_map) 
    pcr.report(extreme_value_map, file_name)

# resampling low resolution ldd map
msg = "Resample the low resolution ldd map."
logger.info(msg)
ldd_map_low_resolution_file_name = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
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


# clone at high resolution (e.g. 30 arc-seconds)
msg = "Set the clone map at high resolution."
logger.info(msg)
num_of_rows = np.round(pcr.clone().nrRows() * 10   , 2)
num_of_cols = np.round(pcr.clone().nrCols() * 10   , 2)
x_min       = np.round(pcr.clone().west()          , 2)
y_max       = np.round(pcr.clone().north()         , 2)
cell_length = pcr.clone().cellSize() / 10.
# set the cell length manually
cell_length = '0.00833333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333'
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
#
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
#
# - masking out permanent water bodies (particularly from reservoirs)
if masking_out_permanent_water_bodies:
    reservoir_capacity  = pcr.cover(\
                          vos.readPCRmapClone(reservoir_capacity_file, \
                                              clone_map_file, \
                                              tmp_folder, \
                                              None, False, None, False), 0.0))
    non_reservoir_areas_scalar = pcr.ifthenelse(reservoir_capacity > 0.0, pcr.scalar(0.0), pcr.scalar(1.0)) 
    non_reservoir_areas_scalar = pcr.ifthen(non_reservoir_areas_scalar > 0.0, non_reservoir_areas_scalar ) 
    # extend these to 0.20 degree
    non_reservoir_areas_scalar = pcr.cover(non_reservoir_areas_scalar, \
                                 pcr.windowmaximum(non_reservoir_areas_scalar, 0.20))
    ldd_map_high_resolution = pcr.ifthen(non_reservoir_areas_scalar > 0.0, ldd_map_high_resolution)
    ldd_map_high_resolution = pcr.lddrepair(pcr.ldd(ldd_map_high_resolution))
    ldd_map_high_resolution = pcr.lddrepair(ldd_map_high_resolution)
    pcr.report(ldd_map_high_resolution, "resampled_high_resolution_ldd.map")

# - dem map
# -- using the dem from deltares
dem_map_high_resolution_file_name = "/projects/0/dfguu/users/edwinhs/data/HydroSHEDS/hydro_basin_without_lakes/integrating_ldd/version_9_december_2016/cover_SRTM_1km_merge_gtopo_masked.map"
#~ # -- using the gtopo30 dem
#~ dem_map_high_resolution_file_name = "/projects/0/dfguu/data/hydroworld/basedata/hydrography/GTOPO30/edwin_process/gtopo30_full.map"
#
# TODO: using the merged DEMs from HydroSHEDS and Deltares/GTOPO30
#
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
#
# strahler order option
strahler_order_used = 6
#
# TODO: ignore smaller rivers (< 10 m)
#
pcr.report(stream_order_map, "high_resolution_stream_order.map")


# execute downscaling scripts for every return period
msg = "Downscaling for every return period."
logger.info(msg)
for i_file in range(len(file_names)-1, 0, -1):       # starting from the highest return period
    file_name = file_names[i_file]
    cmd = ' python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py ' + \
          ' -i downscaling.ini ' + \
          ' -f ' + str(file_name) + \
          ' -b ' + str(file_names[0]) + \
          ' -c ' + str(strahler_order_used) + \
          ' -d output_folder'
    vos.cmd_line(cmd, using_subprocess = False)


# make an empty file to indicate that this downscaling script is done      
filename = "downscaling_is_done.txt"
if os.path.exists(filename): os.remove(filename)
open(filename, "w").close()    


