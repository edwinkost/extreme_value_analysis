#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
import shutil
import glob
import datetime
import numpy as np

import virtualOS as vos

import logging
logger = logging.getLogger(__name__)



# input folder that contain extreme values (in pcraster format):
#~ # - WATCH historical
#~ input_folder       = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/watch_1960-1999/"
#~ # - gfdl-esm2m historical
#~ input_folder       = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/gfdl-esm2m_1960-1999/"
#~ # - hadgem2-es historical
#~ input_folder       = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/hadgem2-es_1960-1999/"
#~ # - ipsl-cm5a-lr historical
#~ input_folder       = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/ipsl-cm5a-lr_1960-1999/"
#~ # - miroc-esm-chem historical
#~ input_folder       = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/miroc-esm-chem_1960-1999/"
#~ # - noresm1-m historical
#~ input_folder       = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/noresm1-m_1960-1999/"
#
# - input folder based on the system argument
input_folder          = os.path.abspath(sys.argv[1]) + "/"


# output folder
#~ # - WATCH historical
#~ general_output_folder = "/scratch-shared/edwinhs-last/flood_analyzer_output/inundation_downscaled/watch_1960-1999/"
#~ # - gfdl-esm2m historical
#~ general_output_folder = "/scratch-shared/edwinhs-last/flood_analyzer_output/inundation_downscaled/gfdl-esm2m_1960-1999/"
#~ # - hadgem2-es historical
#~ general_output_folder = "/scratch-shared/edwinhs-last/flood_analyzer_output/inundation_downscaled/hadgem2-es_1960-1999/"
#~ # - ipsl-cm5a-lr historical
#~ general_output_folder = "/scratch-shared/edwinhs-last/flood_analyzer_output/inundation_downscaled/ipsl-cm5a-lr_1960-1999/"
#~ # - miroc-esm-chem historical
#~ general_output_folder = "/scratch-shared/edwinhs-last/flood_analyzer_output/inundation_downscaled/miroc-esm-chem_1960-1999/"
#~ # - noresm1-m historical
#~ general_output_folder = "/scratch-shared/edwinhs-last/flood_analyzer_output/inundation_downscaled/noresm1-m_1960-1999/"
#
# output folder based on the system argument
output_folder_for_this_analysis = sys.argv[2]
general_output_folder           = output_folder_for_this_analysis + "/" 


# - type of files (options are: "normal"; "bias_corrected"; and "including_bias")
type_of_files  = str(sys.argv[3])

# - option for map types: *flood_inundation_volume.map or *channel_storage.map
map_type_name  = "HESSEL_RESULT"
map_type_name  = "channel_storage.map"
map_type_name  = str(sys.argv[4])

# - option with first upscaling model results to 30 arc-min model
try:
    with_upscaling = str(sys.argv[5]) == "with_upscaling"
except:
    with_upscaling = False

# clean any files exists on the ouput directory (this can be done for global runs)
clean_previous_output = True
if clean_previous_output and os.path.exists(general_output_folder): shutil.rmtree(general_output_folder)

# make log folder and initialize logging
log_file_folder = general_output_folder + "/global/log/"
if clean_previous_output and os.path.exists(log_file_folder): shutil.rmtree(log_file_folder)
if os.path.exists(log_file_folder) == False: os.makedirs(log_file_folder)
vos.initialize_logging(log_file_folder)


# run the downscaling scripts parallelly
msg = "Run the downscaling scripts."
logger.info(msg)
#
number_of_clone_maps = 53
all_clone_codes = ['M%02d'%i for i in range(1,number_of_clone_maps+1,1)]
#~ all_clone_codes = ['M09']
#
# - due to limited memory, we have to split the runs into several groups (assumption: a process takes maximum about 4.5 GB RAM and we will use normal nodes)
num_of_clones_in_a_grp = np.int(np.floor(64.0 / 4.5))
number_of_clone_groups = np.int(np.ceil(float(number_of_clone_maps)/ num_of_clones_in_a_grp))
start_clone = 0
for i_group in range(number_of_clone_groups):
    if i_group > 0: start_clone = last_clone
    last_clone = np.minimum(number_of_clone_maps, start_clone + num_of_clones_in_a_grp)
    clone_codes = all_clone_codes[start_clone:last_clone]
    print clone_codes
    msg = "Run the downscaling scripts for " + str(clone_codes)
    logger.info(msg)
    i_clone = 0
    # - command lines for running the downscling script parallely
    cmd = ''
    for clone_code in clone_codes:
       if with_upscaling:
          cmd += "python downscaling_with_30min_option.py " + input_folder  + " " + general_output_folder + " " + "downscaling.ini" + " " + clone_code + " " + type_of_files + " " + map_type_name + " with_upscaling"
       else:
          if map_type_name == "HESSEL_RESULT"
             cmd += "python downscaling_with_30min_option_for_hessel_results.py " + input_folder  + " " + general_output_folder + " " + "downscaling.ini" + " " + clone_code + " " + type_of_files + " " + map_type_name
          else:
             cmd += "python downscaling.py " + input_folder  + " " + general_output_folder + " " + "downscaling.ini" + " " + clone_code + " " + type_of_files + " " + map_type_name
       cmd = cmd + " & "
       i_clone += 1
    cmd = cmd + " wait "
    # - execute the command
    print cmd
    msg = "Call: "+str(cmd)
    logger.debug(msg)
    vos.cmd_line(cmd, using_subprocess = False)
    #
    # wait until all downscaling processes are done:
    status = False
    while status == False:
       status = vos.check_downscaling_status(general_output_folder, clone_codes)


# Finish
msg = "All downscaling calculations are done. "
logger.info(msg)

