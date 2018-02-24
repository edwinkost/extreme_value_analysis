
RCP_CODE=rcp4p5

GCM_CONVENTION_NAME=0000GFDL-ESM2M
GCM_CAPITAL_LETTERS=GFDL-ESM2M
GCM_SMALL_LETTERS=gfdl-esm2m


#####################################################################################################
#
# get maximum events for the hydrological year types 1 and 2
# 2060-2099 (2080)
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_$GCM_SMALL_LETTERS/no_correction/$RCP_CODE/merged_2006-2099/" 1 /projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/maximum_events/ 2060 2099 &
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_$GCM_SMALL_LETTERS/no_correction/$RCP_CODE/merged_2006-2099/" 2 /projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/maximum_events/ 2060 2099 &
#
wait
#
#
#####################################################################################################


#####################################################################################################
#
# derive hydro year type (based on the baseline/historical run using WATCH forcing data)
# DONE
#
#
#####################################################################################################


#####################################################################################################
#
# get annual maximum events based on a defined/given hydrological year tipe map
# 2060-2099 (2080)
python 2_merge_two_hydrological_year_result.py "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/maximum_events//" /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/hydrological_year/watch_1960-1999/hydrological_year_type.map "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/maximum_events/merged/" 2060 2099 &
#
wait
#
#
#####################################################################################################


#####################################################################################################
#
# calculate maximum surface water level (river depth)
# 2060-2099 (2080)
python 3_calculate_maximum_river_depth_without_upscaling.py "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/maximum_events/merged/" /projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/maximum_events/surface_water_level_maximum/ 2060 2099 &
#
wait
#
#
#####################################################################################################


#####################################################################################################
#
# gumbel fits for the annual flood maxima variable 'channelStorage'
# 2060-2099 (2080)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/gumbel_fits/channel_storage/" 2060 2099 channelStorage &
# 
# gumbel fits for the annual flood maxima variable 'surfaceWaterLevel'
# 2060-2099 (2080)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/gumbel_fits/surface_water_level/" 2060 2099 surfaceWaterLevel &
# 
wait
# 
# 
#####################################################################################################



#####################################################################################################
#
# apply gumbel parameters with bias correction, for the variable 'channelStorage' 
# 2060-2099 (2080)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/gumbel_fits/channel_storage/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/gumbel_fits/$GCM_SMALL_LETTERS_1960-1999/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/gumbel_fits/watch_1960-1999/" "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/extreme_values/channel_storage/" 2060 2099 None channelStorage &
# 
# gumbel fits for the annual flood maxima variable 'surfaceWaterLevel'
# 2060-2099 (2080)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/gumbel_fits/surface_water_level/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_may_june_2017/historical/$GCM_CAPITAL_LETTERS/1960-1999/gumbel_fits/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_may_june_2017/historical/WATCH/1960-1999/gumbel_fits" "/projects/0/aqueduct/users/edwinsut/$RCP_CODE/2060-2099/$GCM_SMALL_LETTERS/extreme_values/surface_water_level/" 2060 2099 surface_water_level_$RCP_CODE_$GCM_CONVENTION_NAME_2080 surfaceWaterLevel &
# 
wait
# 
# 
#####################################################################################################

