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
# - WATCH historical
input_folder          = "/scratch-shared/edwinhs-last/flood_analyzer_output/extreme_values/watch_1960-1999/"

# output folder
# - WATCH historical
general_output_folder = "/scratch-shared/edwinhs-last/flood_analyzer_output/inundation_downscaled/watch_1960-1999/"

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
#
# - due to limited memory, we have to split the runs into several groups (assumption: a process takes maximum about 3.5 GB RAM and we will use normal nodes)
num_of_clones_in_a_grp = np.int(np.floor(64.0 / 3.5))
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
       cmd += "python downscaling.py " + input_folder  + " " + general_output_folder + " " + "downscaling.ini" + " " + clone_code + " "
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

