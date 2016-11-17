#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob

# pcraster dynamic framework is used.
from pcraster.framework import DynamicFramework

# The calculation script (engine) is imported from the following module.
from dynamic_calc_framework import CalcFramework

# time object
from currTimeStep import ModelTime

# utility modules:
import outputNetCDF
import virtualOS as vos

# variable dictionaries:
import aqueduct_flood_analyzer_variable_list_final as varDict

import logging
logger = logging.getLogger(__name__)

# input files
input_files                           = {}
# PCR-GLOBWB 5 arcmin results
input_files['folder']                 = "/scratch/shared/edwinhs-last/scratch_flood_analyzer/watch_results/merged_1958-2001/global/netcdf/"
input_files['channelStorageMonthMax'] = glob.glob(self.input_files['folder'] + "channelStorage_monthMax*.nc")                                     # unit: m3
input_files['dynamicFracWatMonthMax'] = glob.glob(self.input_files['folder'] + "dynamicFracWat_monthMax*.nc")                                     # unit: dimensionless
input_files['floodVolumeMonthMax']    = glob.glob(self.input_files['folder'] + "floodVolume_monthMax*.nc"   )                                     # unit: m3
# - general input data
input_files['cellarea_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['clone_05min']    = input_files['cellarea_05min']
input_files['clone_30min']    = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"

# type of hydrological year
type_of_hydrological_year = 1         # hydrological year 1: October to September 
# - number of months to be shifted
num_of_shift_month = 2
if type_of_hydrological_year == 2: num_of_shift_month = 6

# start and end years for this analysis (PS: after shifted)
start_year = 1960
end_year   = 1999

# netcdf general setup:
netcdf_setup = {}
netcdf_setup['format']          = "NETCDF4"
netcdf_setup['zlib']            = True
netcdf_setup['institution']     = "Department of Physical Geography, Utrecht University"
netcdf_setup['title'      ]     = "PCR-GLOBWB 2 output - post-processed for Aqueduct Flood Analyzer"
netcdf_setup['created by' ]     = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['description']     = 'The annual flood maxima for each year/period starting from October of the year until September of its following year.'
if type_of_hydrological_year == 2:
    netcdf_setup['description'] = 'The annual flood maxima for each year/period starting from July of the year until June of its following year.'

# output files
output_files                      = {}
# - output folder
output_files['folder']            = "/scratch-shared/edwinsut/scratch_flood_analyzer/output/"
try:
    os.makedirs(output['folder'])
except:
    os.system('rm -r ' + output['folder'] + "/*")
    pass
# - temporary output folder (e.g. needed for resampling/gdalwarp)
output_files['tmp_folder']        = output_files['folder'] + "/tmp/"
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

# object for reporting/making netcdf files
netcdf_report = OutputNetcdf(cloneMapFileName, self.output['description'])

# - variables that will be reported:
variable_names = ['channelStorage', 'floodVolume', 'dynamicFracWat', 'surfaceWaterlevel']
           


for var_name in variable_names: 
    output_files[var_name] = {}
    output_files[var_name]['short_name']        = varDict.netcdf_short_name[var_name]
    output_files[var_name]['unit']              = varDict.netcdf_unit[var_name]
    output_files[var_name]['long_name']         = varDict.netcdf_long_name[var_name]          
    output_files[var_name]['comment']           = varDict.comment[var_name]               
    output_files[var_name]['description']       = varDict.description[var_name]
    # - add more information 
    if output_files[var_name]['long_name']   == None: output_files[var_name]['long_name']   = output_files[var_name]['short_name']
    if output_files[var_name]['comment']     == None: output_files[var_name]['comment'] = ""
    if output_files[var_name]['description'] == None: output_files[var_name]['description'] = ""
    output_files[var_name]['description'] = netcdf_setup['description'] + " " + output_files[var_name]['description']
    output_files[var_name]['institution'] = netcdf_setup['institution']
    output_files[var_name]['title'      ] = netcdf_setup['title'      ]
    output_files[var_name]['created by' ] = netcdf_setup['created by' ]
    output_files[var_name]['description'] = netcdf_setup['description']
    # - resolution
    output_files[var_name]['resolution_arcmin'] = 5. # unit: arc-minutes
    # - the surfaceWaterLevel will be reported at 30 ar
    if var_name == "surfaceWaterlevel": output_files[var_name]['resolution_arcmin'] = 30. 
    # - preparing netcdf files:
     


    # make a netcdf file
    self.netcdf_report.createNetCDF(self.output['file_name'],\
                                    self.output['variable_name'],\
                                    self.output['unit'],\
                                    self.output['long_name'])

def main():
    
    
    # time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate,endDate,nrOfTimeSteps)
    
    calculationModel = CalcFramework(cloneMapFileName,\
                                     pcraster_files, \
                                     modelTime, \
                                     output, inputEPSG, outputEPSG, resample_method)

    dynamic_framework = DynamicFramework(calculationModel,modelTime.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    dynamic_framework.run()

if __name__ == '__main__':
    sys.exit(main())
