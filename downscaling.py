#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
import shutil
import glob
import datetime

import pcraster as pcr

import logging
logger = logging.getLogger(__name__)

# print disclaimer
disclaimer.print_disclaimer()

# from the system arguments, read the following:
# - input folder that contain extreme values (in pcraster format):
input_folder = 
# - globa; output folder
global_output_folder = 
# - mask/code for this clone
mask_code = 

# output folder for this mask only
output_folder = global_output_folder + "/" + str(mask_code) + "/"

# clean any files exists on the ouput directory (this can be done for global runs)
clean_previous_output = True
if clean_previous_output and os.path.exists(general_output_folder): shutil.rmtree(general_output_folder)

# make log folder and initialize logging
log_file_folder = general_output_folder + "/log/"
if os.path.exists(log_file_folder) and clean_previous_output:  
    shutil.rmtree(log_file_folder)
    os.makedirs(log_file_folder)
if os.path.exists(log_file_folder) == False: 
    os.makedirs(log_file_folder)
vos.initialize_logging(log_file_folder)

# change the working directory to the output folder 

# clone and landmask files at low resolution (5 arc minute)
clone_map_file    = 
# - set clone map:
pcr.setclone(clone_map_file)
# - set the landmask
landmask_map_file = 
landmask = pcr.readmap(landmask_map_file)

# read all extreme value maps (5 arc-min maps), resample them, and save them to the output folder
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
    complete_file_name = "/" + file_name
    extreme_value_map = 
    # - focus only to the landmask area
    extreme_value_map = pcr.ifthen(landmask, extreme_value_map)
    # - cover the rests to zero (so they will not contribute to any flood/inundation)
    extreme_value_map = pcr.cover(extreme_value_map, 0.0)
    pcr.report(complete_file_name, file_name)



# clone and landmask files at high resolution (30 arc second)
    


# copy 

# pcr-globwb clone areas (for pcr-globwb multiple runs)
clone_codes = list(set(generalConfiguration.globalOptions['cloneAreas'].split(",")))
#
# - for one global run (that should be using a fat node):
if clone_codes[0] == "Global": 
    clone_codes = ['M%02d'%i for i in range(1,54,1)]
#
# - using two (thick) nodes:
if clone_codes[0] == "part_one": 
     # the relative big ones
    clone_codes  = ["M17","M19","M26","M13","M18","M20","M05","M03","M21","M46","M27","M49","M16","M44","M52","M25","M09","M08","M11","M42","M12","M39"]
    #~ # - and plus one of the two smallest ones
    #~ clone_codes += ["M29"]
    #~ # - and plus two of the smallest ones 
    #~ clone_codes += ["M30","M29"]
if clone_codes[0] == "part_two": 
    # the relative small ones
    clone_codes = ["M07","M15","M38","M48","M40","M41","M22","M14","M23","M51","M04","M06","M10","M02","M45","M35","M47","M50","M24","M01","M36","M53","M33","M43","M34","M37","M31","M32","M28","M30","M29"]
    #~ # the relative small ones minus one of the the two smallest ones
    #~ clone_codes = ["M07","M15","M38","M48","M40","M41","M22","M14","M23","M51","M04","M06","M10","M02","M45","M35","M47","M50","M24","M01","M36","M53","M33","M43","M34","M37","M31","M32","M28","M30"]
    #~ # the relative small ones minus two of the smallest ones
    #~ clone_codes = ["M07","M15","M38","M48","M40","M41","M22","M14","M23","M51","M04","M06","M10","M02","M45","M35","M47","M50","M24","M01","M36","M53","M33","M43","M34","M37","M31","M32","M28"]
    # the execution of merging and modflow processes are done in another node
    with_merging_or_modflow = False


# command line(s) for PCR-GLOBWB 
logger.info('Running transient PCR-GLOBWB with/without MODFLOW ')
i_clone = 0
cmd = ''
for clone_code in clone_codes:

   cmd += "python deterministic_runner_glue_with_parallel_and_modflow_options.py " + iniFileName  + " " + debug_option + " " + clone_code + " "
   cmd = cmd + " & "
   i_clone += 1


# Note that for runs with spin-up, we should not combine it with modflow 


# command line(s) for merging and MODFLOW processes:       
if with_merging_or_modflow:

   logger.info('Also with merging and/or MODFLOW processes ')
   
   cmd += "python deterministic_runner_for_monthly_modflow_and_merging.py " + iniFileName +" "+debug_option +" transient"

   cmd = cmd + " & "       


# don't foget to add the following line
cmd = cmd + "wait"       

print cmd
msg = "Call: "+str(cmd)
logger.debug(msg)


# execute PCR-GLOBWB and MODFLOW
vos.cmd_line(cmd, using_subprocess = False)      
