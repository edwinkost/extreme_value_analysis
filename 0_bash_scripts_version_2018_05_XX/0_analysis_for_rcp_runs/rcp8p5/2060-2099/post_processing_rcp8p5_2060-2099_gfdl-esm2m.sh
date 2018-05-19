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
#SBATCH -J rcp8p5_2080_gfdl-esm2m


set -x

# go to the main working folder (containing the scripts):
cd /home/edwinsut/github/edwinkost/extreme_value_analysis/
# 
# 
###################################################################################


###################################################################################
#
# Set the following variables:
#
MAIN_OUTPUT_FOLDER=/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/
#
RCP_CODE=rcp8p5
#
STA_PERIOD=2060
END_PERIOD=2099
MID_PERIOD=2080
#
GCM_SMALL_LETTERS=gfdl-esm2m
#
GCM_CONVENTION_NAME=0000GFDL-ESM2M_${MID_PERIOD}
GCM_CAPITAL_LETTERS=GFDL-ESM2M
#
TYPE_OF_EXTREME_VALUE_FILE=bias_corrected
#
PCRGLOBWB_OUTPUT_FOLDER=/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_${GCM_SMALL_LETTERS}/no_correction/${RCP_CODE}/merged_2006-2099/
#
echo ${PCRGLOBWB_OUTPUT_FOLDER}
# 
# 
HYDRO_YEAR_TYPE_MAP=${MAIN_OUTPUT_FOLDER}/historical/1960-1999/WATCH/hydrological_year_types_1960-1999/hydrological_year_type.map
#
#
###################################################################################



#~ # get maximum events for the hydrological year types 1 and 2
#~ # 
#~ # ${STA_PERIOD} - ${END_PERIOD} ( ${MID_PERIOD} )
#~ python 1a_get_maximum_events.py ${PCRGLOBWB_OUTPUT_FOLDER} 1 ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/maximum_events/ ${STA_PERIOD} ${END_PERIOD} channelStorage_monthMax_output_2006-01-31_to_2099-12-31.nc dynamicFracWat_monthMax_output_2006-01-31_to_2099-12-31.nc &
#~ python 1a_get_maximum_events.py ${PCRGLOBWB_OUTPUT_FOLDER} 2 ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/maximum_events/ ${STA_PERIOD} ${END_PERIOD} channelStorage_monthMax_output_2006-01-31_to_2099-12-31.nc dynamicFracWat_monthMax_output_2006-01-31_to_2099-12-31.nc &
#~ # 
#~ wait
#~ # 
#~ # 
#~ ###################################################################################
#~ 
#~ 
#~ 
#~ # derive hydro year type (ONLY FOR WATCH (baseline) RUN)
#~ # 
#~ # NOT NEEDED
#~ # 
#~ # 
#~ ###################################################################################
#~ 
#~ 
#~ 
#~ # get annual maximum events based on a defined/given hydrological year tipe map
#~ #
#~ # ${STA_PERIOD} - ${END_PERIOD} ( ${MID_PERIOD} )
#~ python 2_merge_two_hydrological_year_result.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/maximum_events/ ${HYDRO_YEAR_TYPE_MAP} ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/maximum_events/merged/ ${STA_PERIOD} ${END_PERIOD} &
#~ # 
#~ wait
#~ # 
#~ # 
#~ ###################################################################################
#~ 
#~ 
#~ 
#~ # calculate maximum surface water level (river depth)
#~ #
#~ # ${STA_PERIOD} - ${END_PERIOD} ( ${MID_PERIOD} )
#~ python 3_calculate_maximum_river_depth_without_upscaling.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/maximum_events/merged/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/maximum_events/surface_water_level_maximum/ ${STA_PERIOD} ${END_PERIOD} &
#~ # 
#~ wait
#~ #
#~ # 
#~ ###################################################################################
#~ 
#~ 
#~ 
#~ # gumbel fits for annual flood maxima variables: ['channelStorage', 'surfaceWaterLevel']
#~ #
#~ # ${STA_PERIOD} - ${END_PERIOD} ( ${MID_PERIOD} )
#~ #
#~ # gumbel fits for the annual flood maxima variable 'channelStorage'
#~ python 4_gumbel_fits_get_gumbel_parameters.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/maximum_events/merged/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/maximum_events/surface_water_level_maximum/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/gumbel_fits/channel_storage/ ${STA_PERIOD} ${END_PERIOD} channelStorage &
#~ # 
#~ # gumbel fits for the annual flood maxima variable 'surfaceWaterLevel'
#~ python 4_gumbel_fits_get_gumbel_parameters.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/maximum_events/merged/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/maximum_events/surface_water_level_maximum/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/gumbel_fits/surface_water_level/ ${STA_PERIOD} ${END_PERIOD} surfaceWaterLevel &
#~ # 
#~ wait
#~ # 
#~ #
#~ # 
#~ ###################################################################################



# apply gumbel parameters without/with and with bias correction, for annual flood maxima variables: ['channelStorage', 'surfaceWaterLevel']
#
# ${STA_PERIOD} - ${END_PERIOD} ( ${MID_PERIOD} )
#
FUTURE_RCP_GCM_FOLDER=${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/gumbel_fits/
HISTORICAL_GCM_FOLDER=${MAIN_OUTPUT_FOLDER}/historical/1960-1999/${GCM_CAPITAL_LETTERS}/gumbel_fits/
BASELINE_WATCH_FOLDER=${MAIN_OUTPUT_FOLDER}/historical/1960-1999/WATCH/gumbel_fits/
#
# - with bias correction for the variables ['channelStorage'] - this should be without parallelization as this consumes huge memory
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py ${FUTURE_RCP_GCM_FOLDER}/channel_storage/ ${HISTORICAL_GCM_FOLDER}/channel_storage ${BASELINE_WATCH_FOLDER}/channel_storage/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/extreme_values/channel_storage/ ${STA_PERIOD} ${END_PERIOD} None channelStorage
#
# - with bias correction for the variables ['surfaceWaterLevel'] - this should be without parallelization as this consumes huge memory
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py ${FUTURE_RCP_GCM_FOLDER}/surface_water_level/ ${HISTORICAL_GCM_FOLDER}/surface_water_level ${BASELINE_WATCH_FOLDER}/surface_water_level/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/${STA_PERIOD}-${END_PERIOD}/${GCM_CAPITAL_LETTERS}/extreme_values/surface_water_level/ ${STA_PERIOD} ${END_PERIOD} surface_water_level_${RCP_CODE}_${GCM_CONVENTION_NAME} surfaceWaterLevel
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
# NEEDED
# 
# 
###################################################################################



