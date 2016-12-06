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
input_folder = "/scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/"

# output folder
general_output_folder = "/scratch-shared/edwinhs-last/test_global/"

# clean any files exists on the ouput directory (this can be done for global runs)
clean_previous_output = False
if clean_previous_output and os.path.exists(general_output_folder): shutil.rmtree(general_output_folder)

# make log folder and initialize logging
log_file_folder = general_output_folder + "/global/log/"
if os.path.exists(log_file_folder) and clean_previous_output: 
    shutil.rmtree(log_file_folder)
    os.makedirs(log_file_folder)
vos.initialize_logging(log_file_folder)


#~ # run the downscaling scripts parallelly
#~ msg = "Run the downscaling scripts."
#~ logger.info(msg)
#~ #
#~ # - the first part: the relative big ones
clone_codes  = ["M17","M19","M26","M13","M18","M20","M05","M03","M21","M46","M27","M49","M16","M44","M52","M25","M09","M08","M11","M42","M12","M39"]
#~ msg = "Run the downscaling scripts for " + str(clone_codes)
#~ logger.info(msg)
#~ i_clone = 0
#~ # - command lines for running the downscling script parallely
#~ cmd = ''
#~ for clone_code in clone_codes:
   #~ cmd += "python downscaling.py " + input_folder  + " " + general_output_folder + " " + "downscaling.ini" + " " + clone_code + " "
   #~ cmd = cmd + " & "
   #~ i_clone += 1
#~ cmd = cmd + " wait "
#~ # - execute the command
#~ print cmd
#~ msg = "Call: "+str(cmd)
#~ logger.debug(msg)
#~ vos.cmd_line(cmd, using_subprocess = False)
#
# wait until all downscaling processes are done:
status = False
while status == False:
   status = vos.check_downscaling_status(general_output_folder, clone_codes)


#~ # - the second part: # the relative small ones
#~ clone_codes = ["M07","M15","M38","M48","M40","M41","M22","M14","M23","M51","M04","M06","M10","M02","M45","M35","M47","M50","M24","M01","M36","M53","M33","M43","M34","M37","M31","M32","M28","M30","M29"]
#~ msg = "Run the downscaling scripts for " + str(clone_codes)
#~ logger.info(msg)
#~ i_clone = 0
#~ # - command lines for running the downscling script parallely
#~ cmd = ''
#~ for clone_code in clone_codes:
   #~ cmd += "python downscaling.py " + input_folder  + " " + general_output_folder + " " + "downscaling.ini" + " " + clone_code + " "
   #~ cmd = cmd + " & "
   #~ i_clone += 1
#~ cmd = cmd + " wait "
#~ # - execute the command
#~ print cmd
#~ msg = "Call: "+str(cmd)
#~ logger.debug(msg)
#~ vos.cmd_line(cmd, using_subprocess = False)
#~ #
#~ # wait until all downscaling processes are done:
#~ status = False
#~ while status == False:
   #~ status = vos.check_downscaling_status(general_output_folder, clone_codes)

