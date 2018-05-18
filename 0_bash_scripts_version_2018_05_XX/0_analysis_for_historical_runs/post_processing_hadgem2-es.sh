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
#SBATCH -J historical_1980_hadgem2-es


set -x

###################################################################################
#
# Set the following variables:
#
MAIN_OUTPUT_FOLDER=/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/
#
RCP_CODE=historical
#
GCM_SMALL_LETTERS=hadgem2-es
#
GCM_CONVENTION_NAME=0000HadGEM2-ES
GCM_CAPITAL_LETTERS=HadGEM2-ES
#
TYPE_OF_EXTREME_VALUE_FILE=normal
#
PCRGLOBWB_OUTPUT_FOLDER=/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_${GCM_SMALL_LETTERS}/no_correction/non-natural/merged_1951-2005/global/netcdf/
#
echo $PCRGLOBWB_OUTPUT_FOLDER
# 
# 
###################################################################################



# get maximum events for the hydrological year types 1 and 2
# 
# 1960-1999 (1980)
python 1a_get_maximum_events.py ${PCRGLOBWB_OUTPUT_FOLDER} 1 ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/ 1960 1999 channelStorage_monthMax_output_1951-01-31_to_2005-12-31.nc dynamicFracWat_monthMax_output_1951-01-31_to_2005-12-31.nc &
python 1a_get_maximum_events.py ${PCRGLOBWB_OUTPUT_FOLDER} 2 ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/ 1960 1999 channelStorage_monthMax_output_1951-01-31_to_2005-12-31.nc dynamicFracWat_monthMax_output_1951-01-31_to_2005-12-31.nc &
# 
wait
# 
# 
###################################################################################



# derive hydro year type (ONLY FOR WATCH (baseline) RUN)
# 
# NOT NEEDED
# 
# 
###################################################################################



# get annual maximum events based on a defined/given hydrological year tipe map
#
# 1960-1999 (1980)
python 2_merge_two_hydrological_year_result.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/ ${MAIN_OUTPUT_FOLDER}/historical/1960-1999/WATCH/hydrological_year_types_1960-1999/hydrological_year_type.map ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/merged/ 1960 1999 &
# 
wait
# 
# 
###################################################################################



# calculate maximum surface water level (river depth)
#
# 1960-1999 (1980)
python 3_calculate_maximum_river_depth_without_upscaling.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/merged/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/surface_water_level_maximum/ 1960 1999 &
# 
wait
#
# 
###################################################################################



# gumbel fits for annual flood maxima variables: ['channelStorage', 'surfaceWaterLevel']
#
# 1960-1999 (1980)
#
# gumbel fits for the annual flood maxima variable 'channelStorage'
python 4_gumbel_fits_get_gumbel_parameters.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/merged/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/surface_water_level_maximum/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/gumbel_fits/channel_storage/ 1960 1999 channelStorage &
# 
# gumbel fits for the annual flood maxima variable 'surfaceWaterLevel'
python 4_gumbel_fits_get_gumbel_parameters.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/merged/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/surface_water_level_maximum/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/gumbel_fits/surface_water_level/ 1960 1999 surfaceWaterLevel &
# 
wait
# 
#
# 
###################################################################################



# apply gumbel parameters without/with and with bias correction, for annual flood maxima variables: ['channelStorage', 'surfaceWaterLevel']
#
# 1960-1999 (1980) 
# - without bias correction for the variables ['channelStorage'] - this should be without parallelization as this consumes huge memory
python 5a_gumbel_fits_apply_gumbel_parameters_without_bias_correction_for_historical_and_baseline_runs.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/gumbel_fits/channel_storage/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/gumbel_fits/surface_water_level/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/extreme_values/channel_storage/ 1960 1999 None channelStorage
# - without bias correction for the variables ['surfaceWaterLevel'] - this should be without parallelization as this consumes huge memory
python 5a_gumbel_fits_apply_gumbel_parameters_without_bias_correction_for_historical_and_baseline_runs.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/gumbel_fits/channel_storage/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/gumbel_fits/surface_water_level/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/extreme_values/surface_water_level/ 1960 1999 surface_water_level_${RCP_CODE}_${GCM_CONVENTION_NAME}_1980 surfaceWaterLevel
#
#
###################################################################################



# set the (channel storage) bankfull capacity for downscaling (NOTE: FOR WATCH ONLY)	
# 
# NOT NEEDED
# 
# 
###################################################################################




# derive/downscale flood inundation maps at 30 arc-second resolution
# 
# NOT NEEDED
# 
# 
###################################################################################



