#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import datetime

import netCDF4 as nc
import numpy as np
import pcraster as pcr

# netcdf reporting module:
import outputNetCDF

# utility module:
import virtualOS as vos

# variable dictionaries:
import aqueduct_flood_analyzer_variable_list as varDict

import logging
logger = logging.getLogger(__name__)


########################################################################
# The script to merge the results from two hydrological years
########################################################################



# input files
input_files                     = {}
#
# PCR-GLOBWB 5 arcmin results
#~ # - WATCH historical
#~ input_files['folder']        = "/scratch-shared/edwinsut/flood_analyzer_analysis/maximum_events/watch_1960-1999/"
#~ # - gfdl-esm2m historical
#~ input_files['folder']        = "/scratch-shared/edwinsut/flood_analyzer_analysis/maximum_events/gfdl-esm2m_1960-1999/"
#~ # - hadgem2-es historical
#~ input_files['folder']        = "/scratch-shared/edwinsut/flood_analyzer_analysis/maximum_events/hadgem2-es_1960-1999/"
#~ # - ipsl-cm5a-lr historical
#~ input_files['folder']        = "/scratch-shared/edwinsut/flood_analyzer_analysis/maximum_events/ipsl-cm5a-lr_1960-1999/"
#~ # - miroc-esm-chem historical
#~ input_files['folder']        = "/scratch-shared/edwinsut/flood_analyzer_analysis/maximum_events/miroc-esm-chem_1960-1999/"
#~ # - noresm1-m historical
#~ input_files['folder']        = "/scratch-shared/edwinsut/flood_analyzer_analysis/maximum_events/noresm1-m_1960-1999"
#
# - input folder based on the system argument
input_files['folder']           = os.path.abspath(sys.argv[1]) + "/"
#
#
# general input files
# - clone map
input_files['clone_map_05min']  = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
# - cell area, ldd maps
input_files['cell_area_05min']  = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['ldd_map_05min']    = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
#
#
# - hydrological year type (based on the WATCH data)
input_files['hydro_year_05min'] = "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/hydrological_year/watch_1960-1999/hydrological_year_type.map"
input_files['hydro_year_05min'] = sys.argv[2]

# option to save/present results at the landmask region only:
landmask_only = True

# output files
output_files                    = {}
#
# - output folder
#~ # - WATCH historical
#~ output_files['folder']       = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/watch_1960-1999/"
#~ # - gfdl-esm2m historical
#~ output_files['folder']       = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/gfdl-esm2m_1960-1999/"
#~ # - hadgem2-es historical
#~ output_files['folder']       = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/hadgem2-es_1960-1999/"
#~ # - ipsl-cm5a-lr historical
#~ output_files['folder']       = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/ipsl-cm5a-lr_1960-1999/"
#~ # - miroc-esm-chem historical
#~ output_files['folder']       = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/miroc-esm-chem_1960-1999/"
#~ # - noresm1-m historical
#~ output_files['folder']       = "/scratch-shared/edwinhs-last/flood_analyzer_output/maximum_events_merged/noresm1-m_1960-1999/"
#
# output folder based on the system argument
output_folder_for_this_analysis      = sys.argv[3]
output_files['folder']               = output_folder_for_this_analysis + "/" 
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

# start and end years for this analysis:
#~ # - for historical runs
#~ str_year = 1960
#~ end_year = 1999
#~ # - for the year 2030
#~ str_year = 2010
#~ end_year = 2049
#~ # - for the year 2050
#~ str_year = 2030
#~ end_year = 2069
#~ # - for the year 2080
#~ str_year = 2060
#~ end_year = 2099
# - based on the system arguments:
str_year = int(sys.argv[4])
end_year = int(sys.argv[5])

# netcdf general setup:
netcdf_setup = {}
netcdf_setup['format']          = "NETCDF4"
netcdf_setup['zlib']            = True
netcdf_setup['institution']     = "Department of Physical Geography, Utrecht University"
netcdf_setup['title'      ]     = "PCR-GLOBWB 2 output (post-processed for the Aqueduct Flood Analyzer): Annual Flood Maxima"
netcdf_setup['created by' ]     = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['description']     = 'The annual flood maxima for each year/period starting from October of the year until September of its following year (for normal hydrological years) or ' +\
                                                          'for each year/period starting from July of the year until June of its following year (for alternative hydrological years)."'
netcdf_setup['source'     ]     = "Utrecht University, Department of Physical Geography - contact: Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['references' ]     = "Sutanudjaja et al., in prep."


# change to the output folder (use it as the working folder) 
os.chdir(output_files['folder'])


# object for reporting/making netcdf files
netcdf_report = outputNetCDF.OutputNetCDF()

# - variables that will be reported:
#~ variable_names = ['channelStorage', 'floodVolume', 'dynamicFracWat']
variable_names = ['channelStorage', 'dynamicFracWat']
for var_name in variable_names: 
    output_files[var_name] = {}
    # - attribute information for netcdf files
    output_files[var_name]['short_name']        = varDict.netcdf_short_name[var_name]
    output_files[var_name]['unit']              = varDict.netcdf_unit[var_name]
    output_files[var_name]['long_name']         = varDict.netcdf_long_name[var_name]          
    output_files[var_name]['comment']           = varDict.comment[var_name]               
    output_files[var_name]['description']       = varDict.description[var_name]
    # - add more information 
    if output_files[var_name]['long_name']   == None: output_files[var_name]['long_name']   = output_files[var_name]['short_name']
    if output_files[var_name]['comment']     == None: output_files[var_name]['comment'] = ""
    output_files[var_name]['institution']       = netcdf_setup['institution']
    output_files[var_name]['title'      ]       = netcdf_setup['title'      ]
    output_files[var_name]['created by' ]       = netcdf_setup['created by' ]
    if output_files[var_name]['description'] == None: output_files[var_name]['description'] = ""
    output_files[var_name]['description']       = netcdf_setup['description'] + " " + output_files[var_name]['description']
    output_files[var_name]['source'     ]       = netcdf_setup['source'     ]
    output_files[var_name]['references' ]       = netcdf_setup['references' ]
    # - resolution
    output_files[var_name]['resolution_arcmin'] = 5. # unit: arc-minutes
    # - preparing netcdf files:
    output_files[var_name]['file_name']         = output_files['folder'] + "/" + \
                                                  varDict.netcdf_short_name[var_name] + \
                                                  "_annual_flood_maxima.nc"
    msg = "Preparing the netcdf file: " + output_files[var_name]['file_name']
    logger.info(msg)
    netcdf_report.createNetCDF(output_files[var_name]) 


# the input (netcdf) file that will be used  
msg = "Using the following PCR-GLOBWB simulation output (netcdf) files:"
logger.info(msg)
input_files['file_name']                           = {}
for hydro_year in ["hydrological_year_1", "hydrological_year_2"]:
    input_files['file_name'][hydro_year]           = {} 
    for var in variable_names:
        input_files['file_name'][hydro_year][var] = glob.glob(input_files['folder'] + "/" + str(hydro_year) + "/" + str(var) + "*" + str(str_year) + "_to_" + str(end_year) + "*.nc")[0]
        msg = input_files['file_name'][hydro_year][var]
        logger.info(msg)


# set the pcraster clone, ldd, landmask, and cell area map 
msg = "Setting the clone, ldd, landmask, and cell area maps" + ":"
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
# - cell area
cell_area = vos.readPCRmapClone(input_files['cell_area_05min'],
                          clone_map_file,
                          output_files['tmp_folder'])


# read the hydrological year 
msg = "Reading the hydrological year types" + ":"
logger.info(msg)
hydro_year_type = pcr.nominal(\
                  vos.readPCRmapClone(input_files['hydro_year_05min'],
                                      input_files['clone_map_05min'],
                                      output_files['tmp_folder'],
                                      None, False, None, True))
hydro_year_type = pcr.cover(hydro_year_type, pcr.nominal(1.0))




# loop through every year
msg = "Merging two hydrologyical years for the following variables:"
logger.info(msg)
#
for i_year in range(str_year, end_year + 1):
    
    for var in variable_names:
        
        msg = "Merging for the variable " + str(var) + " for the year " + str(i_year)
        logger.info(msg)
        
        # time index for this year
        time_index_in_netcdf_file = i_year - str_year + 1
        
        value_from_the_hydrological_year_1 = vos.netcdf2PCRobjClone(input_files['file_name']["hydrological_year_1"][var], \
                                                                    varDict.netcdf_short_name[var], time_index_in_netcdf_file,\
                                                                    useDoy = "Yes",
                                                                    cloneMapFileName  = clone_map_file,\
                                                                    LatitudeLongitude = True,\
                                                                    specificFillValue = None)
        
        value_from_the_hydrological_year_2 = vos.netcdf2PCRobjClone(input_files['file_name']["hydrological_year_2"][var], \
                                                                    varDict.netcdf_short_name[var], time_index_in_netcdf_file,\
                                                                    useDoy = "Yes",
                                                                    cloneMapFileName  = clone_map_file,\
                                                                    LatitudeLongitude = True,\
                                                                    specificFillValue = None)
        
        # merging two hydrological years 
        value_for_this_year = pcr.ifthenelse(pcr.scalar(hydro_year_type) == 1, value_from_the_hydrological_year_1, \
                                                                               value_from_the_hydrological_year_2)
        value_for_this_year = pcr.cover(value_for_this_year, 0.0)
        
        if landmask_only: value_for_this_year = pcr.ifthen(landmask, value_for_this_year)
        
        # report to a netcdf file
        ncFileName = output_files[var]['file_name']
        msg = "Saving to the netcdf file: " + str(ncFileName)
        logger.info(msg)
        time_stamp_used = datetime.datetime(i_year, 12, 31, 0)
        netcdf_report.data2NetCDF(ncFileName, varDict.netcdf_short_name[var], pcr.pcr2numpy(value_for_this_year, vos.MV), time_stamp_used)

