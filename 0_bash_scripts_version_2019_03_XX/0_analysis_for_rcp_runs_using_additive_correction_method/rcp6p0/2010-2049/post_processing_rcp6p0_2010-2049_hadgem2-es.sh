#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00
#SBATCH -p normal
#SBATCH --constraint=haswell
#~ #SBATCH -p fat

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

# job name
#SBATCH -J rcp6p0_2030_hadgem2-es


########################################################################################################################################
# Set the following variables:
#
RCP_CODE=rcp6p0
#
STA_PERIOD=2010
END_PERIOD=2049
MID_PERIOD=2030
#
GCM_SMALL_LETTERS=hadgem2-es
#
GCM_CONVENTION_NAME=0000HadGEM2-ES_${MID_PERIOD}
GCM_CAPITAL_LETTERS=HadGEM2-ES
#
########################################################################################################################################


set -x

# load a compatible python version
. /home/edwin/opt/anaconda2_5.1_for_flood_analyzer/bashrc_anaconda2_5.1_for_flood_analyzer

# go to the main working folder (containing the scripts):
cd /home/edwin/github/edwinkost/extreme_value_analysis/


########################################################################################################################################
# NOTE: READ THE FOLLOWING 
# Some processes were already done in the previous version: /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX 
# In this new version, we change the bias correction procedure to an "additive correction" method. 
# Downscaling is also performed in this script as new extreme volume maps are derived in this script.  
########################################################################################################################################


###################################################################################
#
HISTORICAL_GCM_FOLDER=/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/${GCM_CAPITAL_LETTERS}/gumbel_fits/
#
BASELINE_WATCH_FOLDER=/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/gumbel_fits/
#
BANKFULL_CAPACITY=/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/channel_storage/2-year_of_channel_storage_used_as_bankfull_capacity.map
#
FUTURE_RCP_GCM_FOLDER=/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX//${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/gumbel_fits/
#
MAIN_OUTPUT_FOLDER=/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/
#
TYPE_OF_EXTREME_VALUE_FILE=bias_corrected
#
###################################################################################



# apply gumbel parameters without/with and with bias correction, for annual flood maxima variables: ['channelStorage', 'surfaceWaterLevel']
#
# ${STA_PERIOD} - ${END_PERIOD} ( ${MID_PERIOD} )
#
# - with bias correction for the variables ['channelStorage'] - this should be without parallelization as this consumes huge memory
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py ${FUTURE_RCP_GCM_FOLDER}/channel_storage/ ${HISTORICAL_GCM_FOLDER}/channel_storage ${BASELINE_WATCH_FOLDER}/channel_storage/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/extreme_values/channel_storage/ ${STA_PERIOD} ${END_PERIOD} None channelStorage
#
# - with bias correction for the variables ['surfaceWaterLevel'] - this should be without parallelization as this consumes huge memory
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py ${FUTURE_RCP_GCM_FOLDER}/surface_water_level/ ${HISTORICAL_GCM_FOLDER}/surface_water_level ${BASELINE_WATCH_FOLDER}/surface_water_level/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/extreme_values/surface_water_level/ ${STA_PERIOD} ${END_PERIOD} surface_water_level_${RCP_CODE}_${GCM_CONVENTION_NAME} surfaceWaterLevel
#
#
###################################################################################



# derive/downscale flood inundation maps at 30 arc-second resolution
# 
# ${STA_PERIOD} - ${END_PERIOD} ( ${MID_PERIOD} )
python 6_downscaling_parallel.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/extreme_values/channel_storage/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/inundation_30sec/before_merged/ ${TYPE_OF_EXTREME_VALUE_FILE} channel_storage.map ${BANKFULL_CAPACITY} 6
# merging all downscaled maps
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/inundation_30sec/before_merged/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/inundation_30sec/merged/ inunriver_${RCP_CODE}_${GCM_CONVENTION_NAME} ${STA_PERIOD} ${END_PERIOD} channel_storage.map 06
# 
# 
###################################################################################


