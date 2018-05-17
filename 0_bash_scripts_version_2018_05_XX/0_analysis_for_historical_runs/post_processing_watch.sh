
set -x

###################################################################################
#
# Set the following variables:
#
MAIN_OUTPUT_FOLDER=/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/
#
RCP_CODE=historical
#
GCM_SMALL_LETTERS=watch
#
GCM_CONVENTION_NAME=000000000WATCH
GCM_CAPITAL_LETTERS=WATCH
#
PCRGLOBWB_OUTPUT_FOLDER=/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave/no_correction/non-natural/merged_1958_to_2001/global/netcdf/
#
echo $PCRGLOBWB_OUTPUT_FOLDER
# 
# 
###################################################################################



#~ # get maximum events for the hydrological year types 1 and 2
#~ # 
#~ # 1960-1999 (1980)
#~ python 1a_get_maximum_events.py ${PCRGLOBWB_OUTPUT_FOLDER} 1 ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/ 1960 1999 channelStorage_monthMax_output_1958-01-31_to_2001-12-31.nc dynamicFracWat_monthMax_output_1958-01-31_to_2001-12-31.nc &
#~ python 1a_get_maximum_events.py ${PCRGLOBWB_OUTPUT_FOLDER} 2 ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/ 1960 1999 channelStorage_monthMax_output_1958-01-31_to_2001-12-31.nc dynamicFracWat_monthMax_output_1958-01-31_to_2001-12-31.nc &
#~ wait
#~ # 
#~ # 
#~ ###################################################################################


#~ # derive hydro year type (only for the baseline run)
#~ # 
#~ # based on the period 1960-1999
#~ python 1b_for_baseline_only_derive_hydrological_year_type.py ${PCRGLOBWB_OUTPUT_FOLDER} discharge_monthAvg_output_1958-01-31_to_2001-12-31.nc 1960 1999 ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}//hydrological_year_types_1960-1999/ &
#~ wait
#~ # 
#~ # 
#~ ###################################################################################


# get annual maximum events based on a defined/given hydrological year tipe map
# 1960-1999 (1980)
python 2_merge_two_hydrological_year_result.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}//hydrological_year_types_1960-1999/hydrological_year_type.map ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/maximum_events/merged/ 1960 1999 &
# 
# 
###################################################################################









#~ 
#~ # calculate maximum surface water level (river depth)
#~ NOT YET 
#~ 
#~ 
#~ ###################################################################################
#~ 
#~ # gumbel fits for annual flood maxima variables: ['channelStorage', 'surfaceWaterLevel']
#~ NOT YET 
#~ 
#~ 
#~ ###################################################################################


#~ # apply gumbel parameters without/with and with bias correction, for annual flood maxima variables: ['channelStorage', 'surfaceWaterLevel']
#~ python  5a_gumbel_fits_apply_gumbel_parameters_without_bias_correction_for_historical_and_baseline_runs.py "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/watch/1960-1999/gumbel_fits/" "/scratch-shared/edwinsut/flood_analyzer_analysis_may_2018/historical/1960-1999/WATCH/extreme_values/" 1960 1999 surface_water_level_historical_000000000WATCH_1980


###################################################################################

#~ # derive/downscale flood inundation maps at 30 arc-second resolution
#~ NOT YET

#~ # merging all downscaled map
#~ DONE


###################################################################################


