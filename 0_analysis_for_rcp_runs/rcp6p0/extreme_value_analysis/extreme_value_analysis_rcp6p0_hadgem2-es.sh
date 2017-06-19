#!/bin/bash                                                                                                                  
#SBATCH -N 1                                                                                                                 
#SBATCH -t 17:30:00                                                                                                         
#SBATCH -p normal                                                                                                            
#SBATCH --constraint=haswell                                                                                                 
                                                                                                                             
# mail alert at start, end and abortion of execution                                                                         
#SBATCH --mail-type=ALL                                                                                                      
                                                                                                                             
# send mail to this address                                                                                                  
#SBATCH --mail-user=edwinkost@gmail.com                                                                                      


# go to the scripts folder
cd /home/edwinsut/github/edwinkost/extreme_value_analysis


#####################################################################################################
#
# get maximum events for the hydrological year types 1 and 2
#
# 2010-2049 (2030)
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_feb_rcp6p0/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es/no_correction/rcp6p0/merged_2006-2099/" 1 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/maximum_events/ 2010 2049 &
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_feb_rcp6p0/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es/no_correction/rcp6p0/merged_2006-2099/" 2 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/maximum_events/ 2010 2049 &
#
# 2030-2069 (2050)
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_feb_rcp6p0/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es/no_correction/rcp6p0/merged_2006-2099/" 1 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/maximum_events/ 2030 2069 &
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_feb_rcp6p0/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es/no_correction/rcp6p0/merged_2006-2099/" 2 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/maximum_events/ 2030 2069 &
#
# 2050-2099 (2080)
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_feb_rcp6p0/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es/no_correction/rcp6p0/merged_2006-2099/" 1 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/maximum_events/ 2050 2099 &
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_feb_rcp6p0/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es/no_correction/rcp6p0/merged_2006-2099/" 2 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/maximum_events/ 2050 2099 &
#
wait
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
# 2010-2049 (2030)
python 2_merge_two_hydrological_year_result.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/maximum_events/" /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/hydrological_year/watch_1960-1999/hydrological_year_type.map "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/maximum_events/merged/" 2010 2049 &
# 2030-2069 (2050)
python 2_merge_two_hydrological_year_result.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/maximum_events/" /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/hydrological_year/watch_1960-1999/hydrological_year_type.map "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/maximum_events/merged/" 2030 2069 &
# 2050-2099 (2080)
python 2_merge_two_hydrological_year_result.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/maximum_events/" /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/hydrological_year/watch_1960-1999/hydrological_year_type.map "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/maximum_events/merged/" 2050 2099 &
wait
#
#
#####################################################################################################


#####################################################################################################
#
# calculate maximum surface water level (river depth)
# 2010-2049 (2030)
python 3_calculate_maximum_river_depth_without_upscaling.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/maximum_events/merged/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/maximum_events/surface_water_level_maximum/ 2010 2049 &
# 2030-2069 (2050)
python 3_calculate_maximum_river_depth_without_upscaling.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/maximum_events/merged/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/maximum_events/surface_water_level_maximum/ 2030 2069 &
# 2050-2099 (2080)
python 3_calculate_maximum_river_depth_without_upscaling.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/maximum_events/merged/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/maximum_events/surface_water_level_maximum/ 2050 2099 &
wait
#
#
#####################################################################################################


#####################################################################################################
#
# gumbel fits for the annual flood maxima variable 'channelStorage'
# 2010-2049 (2030)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/gumbel_fits/channel_storage/" 2010 2049 channelStorage &
# 2030-2069 (2050)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/gumbel_fits/channel_storage/" 2030 2069 channelStorage &
# 2050-2099 (2080)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/gumbel_fits/channel_storage/" 2050 2099 channelStorage &
wait
#
#
#####################################################################################################


#####################################################################################################
# 
# gumbel fits for the annual flood maxima variable 'surfaceWaterLevel'
# 2010-2049 (2030)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/gumbel_fits/surface_water_level/" 2010 2049 surfaceWaterLevel &
wait
# 2030-2069 (2050)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/gumbel_fits/surface_water_level/" 2030 2069 surfaceWaterLevel &
wait
# 2050-2099 (2080)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/gumbel_fits/surface_water_level/" 2050 2099 surfaceWaterLevel &
wait
# 
# 
#####################################################################################################



#####################################################################################################
#
# apply gumbel parameters with bias correction, for the variable 'channelStorage' 
# 2010-2049 (2030)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/gumbel_fits/channel_storage/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/gumbel_fits/hadgem2-es_1960-1999/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/gumbel_fits/watch_1960-1999/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/extreme_values/channel_storage/" 2010 2049 None channelStorage &
# 2030-2069 (2050)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/gumbel_fits/channel_storage/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/gumbel_fits/hadgem2-es_1960-1999/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/gumbel_fits/watch_1960-1999/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/extreme_values/channel_storage/" 2030 2069 None channelStorage &
# 2050-2099 (2080)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/gumbel_fits/channel_storage/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/gumbel_fits/hadgem2-es_1960-1999/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/gumbel_fits/watch_1960-1999/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/extreme_values/channel_storage/" 2050 2099 None channelStorage &
# 
wait
# 
# 
#####################################################################################################


#####################################################################################################
# 
# apply gumbel parameters with bias correction, for the variable 'surfaceWaterLevel'
# 2010-2049 (2030)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/gumbel_fits/surface_water_level/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_may_june_2017/historical/HadGEM2-ES/1960-1999/gumbel_fits/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_may_june_2017/historical/WATCH/1960-1999/gumbel_fits/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/extreme_values/surface_water_level/" 2010 2049 surface_water_level_rcp6p0_0000HadGEM2-ES_2030 surfaceWaterLevel &
# 2030-2069 (2050)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/gumbel_fits/surface_water_level/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_may_june_2017/historical/HadGEM2-ES/1960-1999/gumbel_fits/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_may_june_2017/historical/WATCH/1960-1999/gumbel_fits/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/extreme_values/surface_water_level/" 2030 2069 surface_water_level_rcp6p0_0000HadGEM2-ES_2050 surfaceWaterLevel &
# 2050-2099 (2080)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/gumbel_fits/surface_water_level/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_may_june_2017/historical/HadGEM2-ES/1960-1999/gumbel_fits/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_may_june_2017/historical/WATCH/1960-1999/gumbel_fits/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/extreme_values/surface_water_level/" 2050 2099 surface_water_level_rcp6p0_0000HadGEM2-ES_2080 surfaceWaterLevel &
#
wait
#
#####################################################################################################


