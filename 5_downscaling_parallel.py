#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
import shutil
import glob
import datetime

import pcraster as pcr

import configuration
import virtualOS as vos

import logging
logger = logging.getLogger(__name__)

# print disclaimer
disclaimer.print_disclaimer()

# input folder that contain extreme values (in pcraster format):
input_folder = 

# output folder
general_output_folder = 

# clean any files exists on the ouput directory (this can be done for global runs)
clean_previous_output = True
if clean_previous_output and os.path.exists(general_output_folder): shutil.rmtree(general_output_folder)

# make log folder and initialize logging
log_file_folder = general_output_folder + "/global/log/"
if os.path.exists(log_file_folder) and clean_previous_output:  
    shutil.rmtree(log_file_folder)
    os.makedirs(log_file_folder)
if os.path.exists(log_file_folder) == False: 
    os.makedirs(log_file_folder)
vos.initialize_logging(log_file_folder)

# change working folder to the output folder 


# run the downscaling scripts parallelly
# - the first part: the relative big ones
clone_codes  = ["M17","M19","M26","M13","M18","M20","M05","M03","M21","M46","M27","M49","M16","M44","M52","M25","M09","M08","M11","M42","M12","M39"]
i_clone = 0
# - command lines for running the downscling script parallely
cmd = ''
for clone_code in clone_codes:
   cmd += "python downscaling.py " + iniFileName  + " " + debug_option + " " + clone_code + " "
   cmd = cmd + " & "
   i_clone += 1
cmd = cmd + " wait "
# - execute the command
print cmd
msg = "Call: "+str(cmd)
logger.debug(msg)



if clone_codes[0] == "part_two": 
    # the relative small ones
    clone_codes = ["M07","M15","M38","M48","M40","M41","M22","M14","M23","M51","M04","M06","M10","M02","M45","M35","M47","M50","M24","M01","M36","M53","M33","M43","M34","M37","M31","M32","M28","M30","M29"]
    #~ # the relative small ones minus one of the the two smallest ones
    #~ clone_codes = ["M07","M15","M38","M48","M40","M41","M22","M14","M23","M51","M04","M06","M10","M02","M45","M35","M47","M50","M24","M01","M36","M53","M33","M43","M34","M37","M31","M32","M28","M30"]
    #~ # the relative small ones minus two of the smallest ones
    #~ clone_codes = ["M07","M15","M38","M48","M40","M41","M22","M14","M23","M51","M04","M06","M10","M02","M45","M35","M47","M50","M24","M01","M36","M53","M33","M43","M34","M37","M31","M32","M28"]
#

# merging the results and save them in netcdf files

# pcr-globwb clone areas (for pcr-globwb multiple runs)
clone_codes = list(set(generalConfiguration.globalOptions['cloneAreas'].split(",")))
#
# - for one global run (that should be using a fat node):
if clone_codes[0] == "Global": 
    clone_codes = ['M%02d'%i for i in range(1,54,1)]
#
# - using two (thick) nodes:




# Note that for runs with spin-up, we should not combine it with modflow 


# command line(s) for merging and MODFLOW processes:       
if with_merging_or_modflow:

   logger.info('Also with merging and/or MODFLOW processes ')
   
   cmd += "python deterministic_runner_for_monthly_modflow_and_merging.py " + iniFileName +" "+debug_option +" transient"

   cmd = cmd + " & "       


# don't foget to add the following line
cmd = cmd + "wait"       



# execute PCR-GLOBWB and MODFLOW
vos.cmd_line(cmd, using_subprocess = False)      
