#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import datetime

from multiprocessing import Pool

import netCDF4 as nc
import numpy as np
import pcraster as pcr

# utility module:
import virtualOS as vos

import logging
logger = logging.getLogger(__name__)


#############################################################################################
# The script to check that maximum values increasing over return period
#############################################################################################


# the pattern of files and directories:
file_pattern = str(sys.argv[1])

# list of files
input_pcraster_files = glob.glob(file_pattern)
print input_pcraster_files

# return periods
return_periods      = [ "_2-year_",  "_5-year_", "_10-year_", "_25-year_", "_50-year_", "_100-year_", "_250-year_", "_500-year_", "_1000-year_"]


for i_return_period in range(0, len(return_periods)):

    return_period = return_periods[i_return_period]
    
    # loop the file list to get the correct file
    for pcraster_file in input_pcraster_files:
        if return_period in pcraster_file:
            selected_pcraster_file = pcraster_file
            map_for_this_return_period = pcr.readmap(pcraster_file)
    
    map_for_this_return_period = pcr.cover(map_for_this_return_period, 0.0)
    
    if i_return_period > 0:
        check_map = pcr.ifthenelse(map_for_this_return_period >= previous_map, pcr.scalar(0.0), pcr.scalar(-1.0))
        
        minimum_value, maximum_value, average_value = vos.getMinMaxMean(check_map)
        
        msg  = ""
        msg += "Checkting that the values in the file %s are equal to or bigger than the file %s : Min %f Max %f Mean %f" %(selected_pcraster_file, previous_file, minimum_value, maximum_value, average_value)
        msg += "\n"
        print(msg)
    
    previous_map = map_for_this_return_period
    previous_file = selected_pcraster_file
