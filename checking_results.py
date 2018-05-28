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
file_pattern = sys.argv[1]

# list of files
input_pcraster_files = glob.glob(file_pattern)
print input_pcraster_files

# return periods
return_periods      = [ "2-year",  "5-year", "10-year", "25-year", "50-year", "100-year", "250-year", "500-year", "1000-year"]


for i_return_period in range(0, len(return_periods)):

    return_period = return_periods[i_return_period]
    
    # loop the file list to get the correct file
    for pcraster_file in input_pcraster_files:
        if return_period in pcraster_file:
            selected_pcraster_file = pcraster_file
            map_for_this_return_period = pcr.readmap(pcraster_file)
    
    map_for_this_return_period = pcr.cover(map_for_this_return_period, 0.0)
    
    if i_return_period > 0:
        check_map = pcr.ifthenelse(pcraster_file_for_this_return_period >= previous_map, pcr.scalar(0.0), pcr.scalar(-1.0))
        
        minimum_value, maximum_value, average_value = vos.getMinMaxMean(check_map)
        
        msg = "Checkting that the values in the file %s are equal to or bigger than the file %s : Min %f Max %f Mean %f" %(selected_pcraster_file, previous_file, minimum_value, maximum_value, average_value)
        print(msg)
    
    previous_map = pcraster_file_for_this_return_period
    previous_file = selected_pcraster_file
