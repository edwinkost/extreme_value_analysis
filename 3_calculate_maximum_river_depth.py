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
import glofris_postprocess_edwin_modified as glofris

# netcdf reporting module:
import outputNetCDF

# variable dictionaries:
import aqueduct_flood_analyzer_variable_list as varDict

import logging
logger = logging.getLogger(__name__)


#######################################################################################################################
# The script to derive/calculate annual maxima of river depth (at half arc-degree resolution, as requested by Philip) #
#######################################################################################################################

# input files
input_files                    = {}
#
# The annual flood maxima based on the PCR-GLOBWB 5 arcmin results:
#
#~ # - WATCH historical
#~ input_files['folder'] = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/watch_1960-1999/"
#~ # - gfdl-esm2m historical
#~ input_files['folder'] = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/gfdl-esm2m_1960-1999/"
#~ # - hadgem2-es historical
#~ input_files['folder'] = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/hadgem2-es_1960-1999/"
#~ # - ipsl-cm5a-lr historical
#~ input_files['folder'] = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/ipsl-cm5a-lr_1960-1999/"
#~ # - miroc-esm-chem historical
#~ input_files['folder'] = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/miroc-esm-chem_1960-1999/"
#~ # - noresm1-m historical
#~ input_files['folder']  = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/noresm1-m_1960-1999/"
#
# - input folder based on the system argument
input_files['folder']           = os.path.abspath(sys.argv[1]) + "/"
#
#
input_files['file_name'] = {}
input_files['file_name']['channelStorage'] = input_files['folder'] + "/" + "channel_storage_annual_flood_maxima.nc" 
input_files['file_name']['dynamicFracWat'] = input_files['folder'] + "/" + "fraction_of_surface_water_annual_flood_maxima.nc" 
#
# general input files
# - clone map
input_files['clone_map_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
pcr.setclone(input_files['clone_map_05min'])
# - cell area, ldd maps
input_files['cell_area_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['ldd_map_05min'  ] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
# - cell id for every half degree cell
input_files['cell_ids_30min' ] = "/projects/0/dfguu/data/hydroworld/others/irrigationZones/half_arc_degree/uniqueIds30min.nom.map"


# start and end years for this analysis:
#~ # - for historical runs
#~ str_year = 1960
#~ end_year = 1999
# - for the year 2030
str_year = 2010
end_year = 2049
#~ # - for the year 2050
#~ str_year = 2030
#~ end_year = 2069
#~ # - for the year 2080
#~ str_year = 2060
#~ end_year = 2099


# option to save/present results at the landmask region only (not working yet):
landmask_only = True


# output files
output_files                   = {}

# output folder
#
#~ # - WATCH historical
#~ output_files['folder']   = "/scratch-shared/edwinhs-last/flood_analyzer_output/surface_water_level_maximum/watch_1960-1999/"
#~ # - gfdl-esm2m historical
#~ output_files['folder']   = "/scratch-shared/edwinhs-last/flood_analyzer_output/surface_water_level_maximum/gfdl-esm2m_1960-1999/"
#~ # - hadgem2-es historical
#~ output_files['folder']   = "/scratch-shared/edwinhs-last/flood_analyzer_output/surface_water_level_maximum/hadgem2-es_1960-1999/"
#~ # - ipsl-cm5a-lr historical
#~ output_files['folder']   = "/scratch-shared/edwinhs-last/flood_analyzer_output/surface_water_level_maximum/ipsl-cm5a-lr_1960-1999/"
#~ # - miroc-esm-chem historical
#~ output_files['folder']   = "/scratch-shared/edwinhs-last/flood_analyzer_output/surface_water_level_maximum/miroc-esm-chem_1960-1999/"
#~ # - noresm1-m historical
#~ output_files['folder']   = "/scratch-shared/edwinhs-last/flood_analyzer_output/surface_water_level_maximum/noresm1-m_1960-1999/"
#
# output folder based on the system argument
output_folder_for_this_analysis = sys.argv[2]
output_files['folder']          = output_folder_for_this_analysis + "/" 
#
#
try:
    os.makedirs(output_files['folder'])
except:
    os.system('rm -r ' + output_files['folder']  + "/*")
    pass
# - temporary output folder (e.g. needed for resampling/gdalwarp)
output_files['tmp_folder']       = output_files['folder'] + "/tmp/"
try:
    os.makedirs(output_files['tmp_folder'])
except:
    os.system('rm -r ' + output_files['tmp_folder'] + "/*")
    pass
# - prepare logger and its directory
log_file_location = output_files['folder'] + "/log/"
try:
    os.makedirs(log_file_location)
except:
    pass
vos.initialize_logging(log_file_location)


# set the pcraster clone, ldd and landmask maps 
msg = "Setting the clone, ldd and landmask maps" + ":"
logger.info(msg)
# - clone 
clone_map_file = input_files['clone_map_05min']
pcr.setclone(clone_map_file)
# - ldd
ldd = vos.readPCRmapClone(input_files['ldd_map_05min'],
                          clone_map_file,
                          output_files['tmp_folder'],
                          None,
                          True)
ldd = pcr.lddrepair(pcr.ldd(ldd))
ldd = pcr.lddrepair(ldd)
# - landmask
landmask  = pcr.ifthen(pcr.defined(ldd), pcr.boolean(1.0))

# set the the cell id for every half arc-degree cell 
msg = "Setting the cell id for every half arc-degree cell" + ":"
logger.info(msg)
cell_ids_30min = pcr.nominal(\
                 vos.readPCRmapClone(input_files['cell_ids_30min' ],
                                     clone_map_file,
                                     output_files['tmp_folder'],
                                     None,
                                     False,
                                     None,
                                     True))

# set the cell areas for 5 arc-min and half arc-degree cells 
msg = "Setting the cell areas for 5 arc-min and half arc-degree cells" + ":"
logger.info(msg)
# - 5 arc-min
cell_area = vos.readPCRmapClone(input_files['cell_area_05min'],
                          clone_map_file,
                          output_files['tmp_folder'])
cell_area = pcr.ifthen(landmask, cell_area)
# - 30 arc-min
cell_area_30min = pcr.areatotal(cell_area, cell_ids_30min)

# upscaling factor
upscaling_factor = np.int(30.0 / 5.0)

# netcdf general setup:
netcdf_setup = {}
netcdf_setup['format']          = "NETCDF4"
netcdf_setup['zlib']            = True
netcdf_setup['institution']     = "Utrecht University, Department of Physical Geography ; Deltares ; World Resources Institute"
netcdf_setup['title'      ]     = "PCR-GLOBWB 2 output (post-processed for the Aqueduct Flood Analyzer): Annual Maxima of River Depth"
netcdf_setup['created by' ]     = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['description']     = 'The annual river depth maxima for each year/period starting from October of the year until September of its following year (for normal hydrological years) or ' +\
                                                          'for each year/period starting from July of the year until June of its following year (for alternative hydrological years). "'
netcdf_setup['source'     ]     = "Utrecht University, Department of Physical Geography - contact: Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['references' ]     = "Sutanudjaja et al., in prep."


# change to the output folder (use it as the working folder) 
os.chdir(output_files['folder'])

# object for reporting/making netcdf files
netcdf_report = outputNetCDF.OutputNetCDF()
# - dictionary for netcdf output files 
netcdf_file = {}

msg = "Preparing netcdf output files."
logger.info(msg)
#
var_name = 'surfaceWaterLevel' 
netcdf_file[var_name] = {}
#
# - file name
netcdf_file[var_name]['file_name']   = output_files['folder'] + "/" + varDict.netcdf_short_name[var_name] + "_annual_maxima.nc"
#
# - general attribute information:
netcdf_file[var_name]['description'] = netcdf_setup['description']
netcdf_file[var_name]['institution'] = netcdf_setup['institution']
netcdf_file[var_name]['title'      ] = netcdf_setup['title'      ]
netcdf_file[var_name]['created by' ] = netcdf_setup['created by' ]
netcdf_file[var_name]['source'     ] = netcdf_setup['source'     ]
netcdf_file[var_name]['references' ] = netcdf_setup['references' ]
#
netcdf_file[var_name]['short_name']  = varDict.netcdf_short_name[var_name]
netcdf_file[var_name]['unit']        = varDict.netcdf_unit[var_name]
netcdf_file[var_name]['long_name']   = varDict.netcdf_long_name[var_name]          
netcdf_file[var_name]['comment']     = varDict.comment[var_name]               
#
# - resolution (unit: arc-minutes)
netcdf_file[var_name]['resolution_arcmin'] = 30. 
if netcdf_file[var_name]['resolution_arcmin'] > 5.0:
    netcdf_file[var_name]['description'] += "We upscale the results of PCR-GLOBWB model used at 5 arc-minute resolution to the resolution of " + str(netcdf_file[var_name]['resolution_arcmin'])
#
# - preparing netcdf file (and variable):
msg = "Preparing the netcdf file: " + netcdf_file[var_name]['file_name']
logger.info(msg)
netcdf_report.createNetCDF(netcdf_file[var_name])


msg = "Calculate surface water level at half-arc degree resolution "
logger.info(msg)
#
# assumption for minimum surface water level
minimum_fraction_of_surface_water = 0.005
msg = "Using the assumption for minimum_fraction_of_surface_water: " + str(minimum_fraction_of_surface_water)
#
for i_year in range(str_year, end_year + 1):
    
    msg = "Calculate surface water level at half-arc degree resolution for the year: " + str(i_year)
    logger.info(msg)
    
    # time index for this year (for reading netcdf file
    time_index_in_netcdf_file = i_year - str_year + 1

    # read channel storage and upscale it to 30 arc-min (unit: m3)
    channel_storage = vos.netcdf2PCRobjClone(input_files['file_name']['channelStorage'], \
                                             "channel_storage", time_index_in_netcdf_file,\
                                             useDoy = "Yes", \
                                             cloneMapFileName  = clone_map_file,\
                                             LatitudeLongitude = True,\
                                             specificFillValue = None)
    channel_storage = pcr.ifthen(landmask, pcr.cover(channel_storage, 0.0))
    # - upscale it to 30 arc-min (unit: m3)
    channel_storage_30min = pcr.areatotal(channel_storage, cell_ids_30min)
    
    # read fraction_of_surface_water and upscale it to 30 arc-min (dimensionless)
    fraction_of_surface_water = vos.netcdf2PCRobjClone(input_files['file_name']['dynamicFracWat'], \
                                                       "fraction_of_surface_water", time_index_in_netcdf_file,\
                                                       useDoy = "Yes", \
                                                       cloneMapFileName  = clone_map_file,\
                                                       LatitudeLongitude = True,\
                                                       specificFillValue = None)
    fraction_of_surface_water = pcr.ifthen(landmask, pcr.cover(fraction_of_surface_water, 0.0))
    # - upscale it to 30 arc-min (dimensionless)
    fraction_of_surface_water_30min = pcr.areatotal(fraction_of_surface_water * cell_area, cell_ids_30min) / cell_area_30min
    
    # calculate surface water level at 30 arc-min resolution
    surface_water_level_30min = channel_storage_30min / (pcr.max(fraction_of_surface_water_30min, minimum_fraction_of_surface_water) * cell_area_30min)

    # convert it 30 arcmin arrays
    surface_water_level_30min_arrays = vos.regridToCoarse(pcr.pcr2numpy(surface_water_level_30min, vos.MV), upscaling_factor, "max", vos.MV)

    # save it to netcdf file
    ncFileName = netcdf_file[var_name]['file_name']
    msg = "Saving to the netcdf file: " + str(netcdf_file[var_name]['file_name'])
    logger.info(msg)
    time_stamp_used = datetime.datetime(i_year, 12, 31, 0)
    netcdf_report.data2NetCDF(ncFileName, varDict.netcdf_short_name[var_name], surface_water_level_30min_arrays, time_stamp_used)
    
