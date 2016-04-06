#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Edwin Husni Sutanudjaja (EHS, 29 Sep 2014): This is the script for estimating aquifer thickness based on de Graaf et al. (2014). 
#                                             This estimate is then corrected based on the table of Margat (2006). 

import os
import sys
import shutil

import numpy as np

from pcraster.framework import *
import pcraster as pcr

import outputNetCDF
import virtualOS as vos

# input directory, file name
input_directory  = "/nfsarchive/edwin-emergency-backup-DO-NOT-DELETE/cartesius/05min_runs_january_2016_merged/pcrglobwb_only_from_1958_4LCs_edwin_parameter_set_kinematic_wave/daily/"
file_name_front  = "floodVolume_dailyTot_output_"          # example: floodVolume_dailyTot_output_2000.nc
variable_name    = "flood_innundation_volume"

# start year and end year:
start_year = 1958 
end_year   = 2010

# output directory: 
output_directory = "/nfsarchive/edwin-emergency-backup-DO-NOT-DELETE/cartesius/05min_runs_january_2016_merged/pcrglobwb_only_from_1958_4LCs_edwin_parameter_set_kinematic_wave/daily/maximum/" 
cleanOutputDir = False
if cleanOutputDir:
    if os.path.exists(output_directory): shutil.rmtree(output_directory)
    os.makedirs(output_directory)
# - temporary directory
tmp_directory = output_directory + "/tmp/"
if os.path.exists(tmp_directory): shutil.rmtree(tmp_directory)
os.makedirs(tmp_directory)

# 5 min clone map
clone_map_05min_file = "/data/hydroworld/others/RhineMeuse/RhineMeuse05min.clone.map"
#~ clone_map_05min_file = "/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
pcr.setclone(clone_map_05min_file)

# 5 min cell area (unit: m2) 
cell_area_05min_file = "/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
cell_area_05min = vos.readPCRmapClone(cell_area_05min_file, clone_map_05min_file, \
                                      tmp_directory)

# 30 min cell ids
cell_ids_30min_file = "/data/hydroworld/others/irrigationZones/half_arc_degree/uniqueIds30min.nom.map"
cell_ids_30min = vos.readPCRmapClone(cell_ids_30min_file , clone_map_05min_file, \
                                     tmp_directory, \
                                     None, False, True)

# reporting objects
# - for 5 arcmin resolution
cloneMap = pcr.boolean(1.0)
latlonDict05min = {}
latlonDict05min['lat'] = np.unique(pcr.pcr2numpy(pcr.ycoordinate(cloneMap), vos.MV))[::-1] 
latlonDict05min['lon'] = np.unique(pcr.pcr2numpy(pcr.xcoordinate(cloneMap), vos.MV))
report_netcdf_05min = outputNetCDF.OutputNetCDF(latlonDict05min)
# - for 30 arcmin resolution
latlonDict30min = {}
latlonDict30min['lat'] = np.arange(latlonDict05min['lat'][0], latlonDict05min['lat'][-1] - 0.5/2, -0.5)
latlonDict30min['lon'] = np.arange(latlonDict05min['lon'][0], latlonDict05min['lon'][-1] + 0.5/2,  0.5)
report_netcdf_30min = outputNetCDF.OutputNetCDF(latlonDict30min)
# TODO: Make this module writes for CF convention (see Hessel's document)

# preparing the file at  5 arcmin resolution:
output_file_05min = output_directory + "/" + file_name_front + "maximum_05min.nc"
report_netcdf_05min.createNetCDF(output_file_05min, variable_name, "m3")

# preparing the file at 30 arcmin resolution:
output_file_30min = output_directory + "/" + file_name_front + "maximum_30min.nc"
report_netcdf_30min.createNetCDF(output_file_30min, variable_name, "m3")

# loop for all year
for year in range(start_year, end_year + 1, 1):
    
    # cdo for every year
    inp_file_name =  input_directory + file_name_front + str(year) + ".nc"
    out_file_name = output_directory + file_name_front + str(year) + "_maximum.nc"
    cmd = 'cdo timmax ' + inp_file_name + " " + out_file_name 
    
    # read value and report it at 5 arcmin resolution
    value_at_05_min = vos.netcdf2PCRobjClone(ncFile = out_file_name, varName = variable_name, dateInput = str(year) + "-12-31", \
                                             useDoy = None, \
                                             cloneMapFileName  = clone_map, \
                                             LatitudeLongitude = True, \
                                             specificFillValue = None)
    value_at_05_min = pcr.cover(value_at_05_min, 0.0)
    numpy_at_05_min = pcr.pcr2numpy(value_at_05_min, vos.MV)
    report_netcdf_05min.data2NetCDF(output_file_05min, \
                                    variable_name, \
                                    numpy_at_05_min)
    
    # upscale it to 30 arcmin resolution and report it
    value_at_30_min = pcr.areatotal(value_at_05_min * cell_area_05min, cell_ids_30min) /\
                      pcr.areatotal(                  cell_area_05min, cell_ids_30min)
    numpy_at_30_min = vos.regridToCoarse(value_at_30_min, \
                                         int(30./5.), "average", vos.MV)
    report_netcdf_30min.data2NetCDF(output_file_30min, \
                                    variable_name, \
                                    numpy_at_30_min)
