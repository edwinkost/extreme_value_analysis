#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Edwin Husni Sutanudjaja (EHS, 29 Sep 2014): This is the script for estimating aquifer thickness based on de Graaf et al. (2014). 
#                                             This estimate is then corrected based on the table of Margat (2006). 

import os
import sys
import shutil

import datetime

import numpy as np

from pcraster.framework import *
import pcraster as pcr

import outputNetCDF
import virtualOS as vos

# input directory, file name
input_directory  = "/nfsarchive/edwin-emergency-backup-DO-NOT-DELETE/cartesius/05min_runs_january_2016_merged/pcrglobwb_only_from_1958_4LCs_edwin_parameter_set_kinematic_wave/daily/"
file_name_front  = "floodVolume_dailyTot_output_"          # example: floodVolume_dailyTot_output_2000.nc
variable_name    = "flood_innundation_volume"
file_name_front  = str(sys.argv[1]) + "_"
variable_name    = str(sys.argv[2])

# start year and end year:
start_year = 1958 
end_year   = 2010
start_year = int(sys.argv[3]) ; print(start_year)
end_year   = int(sys.argv[4]) ; print(end_year)

# output directory: 
output_directory = input_directory + "/maximum/" + str(start_year) + "to" + str(end_year) + "/"
cleanOutputDir = False
if cleanOutputDir:
    if os.path.exists(output_directory): shutil.rmtree(output_directory)
    os.makedirs(output_directory)
# - temporary directory
tmp_directory = output_directory + "/tmp/"
if os.path.exists(tmp_directory): shutil.rmtree(tmp_directory)
os.makedirs(tmp_directory)

# 5 min clone map
#~ clone_map_05min_file = "/data/hydroworld/others/RhineMeuse/RhineMeuse05min.clone.map"         # TODO: FIXME: Resampling seems NOT really working.  
clone_map_05min_file = "/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
pcr.setclone(clone_map_05min_file)

# 5 min cell area (unit: m2) 
cell_area_05min_file = "/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
cell_area_05min = vos.readPCRmapClone(cell_area_05min_file, clone_map_05min_file, \
                                      tmp_directory)

# 30 min cell ids
cell_ids_30min_file = "/data/hydroworld/others/irrigationZones/half_arc_degree/uniqueIds30min.nom.map"
cell_ids_30min = vos.readPCRmapClone(cell_ids_30min_file , clone_map_05min_file, \
                                     tmp_directory, \
                                     None, False, None, True)
cell_ids_30min = pcr.nominal(cell_ids_30min)

# reporting objects
# - for 5 arcmin resolution
latlonDict05min = {}
cloneMap = pcr.boolean(1.0)
latlonDict05min['lat'] = np.unique(pcr.pcr2numpy(pcr.ycoordinate(cloneMap), vos.MV))[::-1] 
latlonDict05min['lon'] = np.unique(pcr.pcr2numpy(pcr.xcoordinate(cloneMap), vos.MV))
report_netcdf_05min = outputNetCDF.OutputNetCDF(latlonDict05min)
# - for 30 arcmin resolution
latlonDict30min = {}
latlonDict30min['lat'] = np.arange(np.round(latlonDict05min['lat'][0] + 2.5/60 - 0.25 , 2), latlonDict05min['lat'][-1] - 2.5/60, -0.5)
latlonDict30min['lon'] = np.arange(np.round(latlonDict05min['lon'][0] - 2.5/60 + 0.25 , 2), latlonDict05min['lon'][-1] + 2.5/60,  0.5)
report_netcdf_30min = outputNetCDF.OutputNetCDF(latlonDict30min)
# TODO: Make this module writes for CF convention (see Hessel's document)

# preparing the file at  5 arcmin resolution:
output_file_05min = output_directory + "/" + file_name_front + "maximum_05min_" + str(start_year) + "_to_" + str(end_year) + ".nc"
report_netcdf_05min.createNetCDF(output_file_05min, variable_name, "m", variable_name, True)

# preparing the file at 30 arcmin resolution:
output_file_30min = output_directory + "/" + file_name_front + "maximum_30min_" + str(start_year) + "_to_" + str(end_year) + ".nc"
report_netcdf_30min.createNetCDF(output_file_30min, variable_name, "m", variable_name, True)

# loop for all year
for year in range(start_year, end_year + 1, 1):
    
    # cdo for every year
    inp_file_name =  input_directory + file_name_front + str(year) + ".nc"
    out_file_name = output_directory + file_name_front + str(year) + "_maximum.nc"
    cmd = 'cdo timmax ' + inp_file_name + " " + out_file_name 
    print(cmd)
    os.system(cmd)
    
    # time stamp for netcdf reporting
    timeStamp = datetime.datetime(year, 12, 31, 0)
    
    # read value and report it at 5 arcmin resolution
    print("Reading values at 5 arcmin resolution.")
    value_at_05_min = vos.netcdf2PCRobjCloneWithoutTime(ncFile = out_file_name, varName = variable_name, \
                                                         cloneMapFileName  = clone_map_05min_file)
    value_at_05_min = pcr.cover(value_at_05_min, 0.0)
    numpy_at_05_min = pcr.pcr2numpy(value_at_05_min, vos.MV)
    report_netcdf_05min.data2NetCDF(output_file_05min, \
                                    variable_name, \
                                    numpy_at_05_min, \
                                    timeStamp)
    
    # upscale it to 30 arcmin resolution and report it
    print("Upscale to 30 arcmin resolution.")
    value_at_30_min = pcr.areatotal(value_at_05_min * cell_area_05min, cell_ids_30min) /\
                      pcr.areatotal(                  cell_area_05min, cell_ids_30min)
    value_at_30_min = pcr.cover(value_at_30_min, 0.0)
    numpy_at_30_min = vos.regridToCoarse(pcr.pcr2numpy(value_at_30_min, vos.MV), \
                                         int(30./5.), "average", vos.MV)
    report_netcdf_30min.data2NetCDF(output_file_30min, \
                                    variable_name, \
                                    numpy_at_30_min, \
                                    timeStamp)
