#!/bin/bash                                                                                                                  
#SBATCH -N 1                                                                                                                 
#SBATCH -t 48:59:00                                                                                                         
#SBATCH -p normal                                                                                                            
#SBATCH --constraint=haswell                                                                                                 
                                                                                                                             
# mail alert at start, end and abortion of execution                                                                         
#SBATCH --mail-type=ALL                                                                                                      
                                                                                                                             
# send mail to this address                                                                                                  
#SBATCH --mail-user=edwinkost@gmail.com                                                                                      


# go to the scripts folder
cd /home/edwinsut/github/edwinkost/extreme_value_analysis


#~ #####################################################################################################
#~ #
#~ # get maximum events for the hydrological year types 1 and 2
#~ # 2010-2049 (2030)
#~ # DONE
#~ # 2030-2069 (2050)
#~ # DONE
#~ # 2050-2099 (2080)
#~ python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m/no_correction/rcp4p5/merged_2006-2099/" 1 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/maximum_events/ 2050 2099 &
#~ python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m/no_correction/rcp4p5/merged_2006-2099/" 2 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/maximum_events/ 2050 2099 &
#~ wait
#~ #
#~ #
#~ #####################################################################################################
#~ #
#~ # derive hydro year type (based on the baseline/historical run using WATCH forcing data)
#~ # DONE
#~ #
#~ #
#~ #####################################################################################################


#~ #####################################################################################################
#~ #
#~ # get annual maximum events based on a defined/given hydrological year tipe map
#~ # 2010-2049 (2030)
#~ # DONE
#~ # 2030-2069 (2050)
#~ # DONE
#~ # 2050-2099 (2080)
#~ python 2_merge_two_hydrological_year_result.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/maximum_events/" /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/hydrological_year/watch_1960-1999/hydrological_year_type.map "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/maximum_events/merged/" 2050 2099 &
#~ wait
#~ #
#~ #
#~ #####################################################################################################


#~ #####################################################################################################
#~ #
#~ # calculate maximum surface water level (river depth)
#~ # 2010-2049 (2030)
#~ python 3_calculate_maximum_river_depth_without_upscaling.py "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/rcp4p5/flood_analyzer_analysis_rcp4p5_runs_2010-2049/maximum_events_merged/noresm1-m_2010-2049/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2010-2049/noresm1-m/maximum_events/surface_water_level_maximum/ 2010 2049 &
#~ # 2030-2069 (2050)
#~ python 3_calculate_maximum_river_depth_without_upscaling.py "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/rcp4p5/flood_analyzer_analysis_rcp4p5_runs_2030-2069/maximum_events_merged/noresm1-m_2030-2069/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2030-2069/noresm1-m/maximum_events/surface_water_level_maximum/ 2030 2069 &
#~ # 2050-2099 (2080)
#~ python 3_calculate_maximum_river_depth_without_upscaling.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/maximum_events/surface_water_level_maximum/" 2050 2099 &
#~ wait
#~ #
#~ #
#~ #####################################################################################################


#####################################################################################################
#
# gumbel fits for the annual flood maxima variable 'channelStorage'
# 2010-2049 (2030)
# DONE
# 2030-2069 (2050)
# DONE
# 2050-2099 (2080)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/gumbel_fits/channel_storage/" 2050 2099 channelStorage &
wait
# 
# gumbel fits for the annual flood maxima variable 'surfaceWaterLevel'
# 2010-2049 (2030)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2010-2049/noresm1-m/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2010-2049/noresm1-m/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2010-2049/noresm1-m/gumbel_fits/surface_water_level/" 2010 2049 surfaceWaterLevel &
wait
# 2030-2069 (2050)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2030-2069/noresm1-m/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2030-2069/noresm1-m/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2030-2069/noresm1-m/gumbel_fits/surface_water_level/" 2030 2069 surfaceWaterLevel &
wait
# 2050-2099 (2080)
python 4_gumbel_fits_get_gumbel_parameters.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/maximum_events/merged/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/maximum_events/surface_water_level_maximum/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/gumbel_fits/surface_water_level/" 2050 2099 surfaceWaterLevel &
# 
wait
# 
# 
#####################################################################################################



#####################################################################################################
#
# apply gumbel parameters with bias correction, for the variable 'channelStorage' 
# 2010-2049 (2030)
# DONE
# 2030-2069 (2050)
# DONE
# 2050-2099 (2080)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/gumbel_fits/channel_storage/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/gumbel_fits/noresm1-m_1960-1999/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/gumbel_fits/watch_1960-1999/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/extreme_values/channel_storage/" 2050 2099 None channelStorage
# 
# gumbel fits for the annual flood maxima variable 'surfaceWaterLevel'
# 2010-2049 (2030)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2010-2049/noresm1-m/gumbel_fits/surface_water_level/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/baseline_and_historical/noresm1-m/1960-1999/gumbel_fits/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/baseline_and_historical/watch/1960-1999/gumbel_fits/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2010-2049/noresm1-m/extreme_values/surface_water_level/" 2010 2049 surface_water_level_rcp4p5_00000NorESM1-M_2030 surfaceWaterLevel &
# 2030-2069 (2050)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2030-2069/noresm1-m/gumbel_fits/surface_water_level/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/baseline_and_historical/noresm1-m/1960-1999/gumbel_fits/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/baseline_and_historical/watch/1960-1999/gumbel_fits/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2030-2069/noresm1-m/extreme_values/surface_water_level/" 2030 2069 surface_water_level_rcp4p5_00000NorESM1-M_2050 surfaceWaterLevel &
# 2050-2099 (2080)
python 5b_gumbel_fits_apply_gumbel_parameters_with_bias_correction_for_gcm_runs.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/gumbel_fits/surface_water_level/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/baseline_and_historical/noresm1-m/1960-1999/gumbel_fits/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/baseline_and_historical/watch/1960-1999/gumbel_fits/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/noresm1-m/extreme_values/surface_water_level/" 2050 2099 surface_water_level_rcp4p5_00000NorESM1-M_2080 surfaceWaterLevel &
wait
