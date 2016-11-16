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

# utility module:
import virtualOS as vos

# variable dictionaries:
import efas_variable_list_final as varDict

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

# type of hydrological year
type_of_hydrological_year = 1         # hydrological year 

# - number of 

# start and end years for this analysis (PS: after shifted)
start_year = 1960
end_year   = 1999

# output files
output_files                      = {}
output_files['folder']            = 
# - variable names (that will be reported at 5 arc min resolution
variable_name = ['channelStorage', 'dynamicFracWat', ]

output_files['channelStorageMax'] = {}
output_files['channelStorageMax']['file_name'] = 
output_files['channelStorageMax']['variable_name'] = 
 

# intermediate netcds files: for the 'shifted' netcdf files (to consider the start of hydrological year)


# netcdf file attribute


###########################################################################################################

# efas_variable_code in a list
efas_variable_name = ["pd","pr","rg","ta","ws"]

# obtain efas_variable_code from the system argurment
try:
   efas_variable_name = sys.argv[1]
except:
   pass

# file name of the clone map defining the scope of output
cloneMapFileName = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/clone_maps/RhineMeuse3min.clone.map"

# directory where the original pcraster files are stored
pcraster_files = {}
pcraster_files['directory'] = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/source/pcraster/"
pcraster_files['file_name'] = efas_variable_name # "pr"

# output folder
output = {}
output['folder']        = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/netcdf_latlon/3min/"
output['variable_name'] = varDict.netcdf_short_name[efas_variable_name] 
output['file_name']     = output['variable_name']+"_efas_rhine-meuse"+".nc"
output['unit']          = varDict.netcdf_unit[efas_variable_name]
output['long_name']     = varDict.netcdf_long_name[efas_variable_name] 
output['description']   = varDict.description[efas_variable_name]      

# put output at different folder
output['folder'] += output['variable_name']+"/"

# prepare the output directory
try:
    os.makedirs(output['folder'])
except:
    os.system('rm -r ')
    pass

startDate     = "1990-01-01" # YYYY-MM-DD
endDate       = None
nrOfTimeSteps = 9070         # based on the last file provided by Ad 

# projection/coordinate sy
inputEPSG  = "EPSG:3035" 
outputEPSG = "EPSG:4326"
resample_method = "near"

###########################################################################################################

def main():
    
    # prepare logger and its directory
    log_file_location = output['folder']+"/log/"
    try:
        os.makedirs(log_file_location)
    except:
        pass
    vos.initialize_logging(log_file_location)
    
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
