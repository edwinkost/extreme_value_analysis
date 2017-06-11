
# get maximum events for the hydrological year types 1 and 2
# 2010-2049 (2030)
# DONE
# 2030-2069 (2050)
# DONE
# 2050-2099 (2080)
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m/no_correction/rcp4p5/merged_2006-2099/" 1 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/gfdl-esm2m/maximum_events/ 2050 2099 &
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m/no_correction/rcp4p5/merged_2006-2099/" 2 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/gfdl-esm2m/maximum_events/ 2050 2099 &
wait
#
#
###################################################################################
#
# derive hydro year type (based on the baseline/historical run using WATCH forcing data)
# DONE
#
#
###################################################################################

# get annual maximum events based on a defined/given hydrological year tipe map



###################################################################################

#~ # calculate maximum surface water level (river depth)
#~ python 3_calculate_maximum_river_depth_without_upscaling.py "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/rcp4p5/flood_analyzer_analysis_rcp4p5_runs_2010-2049/maximum_events_merged/gfdl-esm2m_2010-2049/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/gfdl-esm2m/1960-1999/surface_water_level_maximum/" 1960 1999 
#~ 
#~ 
#~ ###################################################################################
#~ 
#~ # gumbel fits for annual flood maxima variables: ['surfaceWaterLevel']
#~ python 4_gumbel_fits_get_gumbel_parameters.py "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/gfdl-esm2m/1960-1999/maximum_events/merged/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/gfdl-esm2m/1960-1999/surface_water_level_maximum/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/gfdl-esm2m/1960-1999/gumbel_fits/" 1960 1999 surfaceWaterLevel
#~ 
#~ 
#~ ###################################################################################
#~ 
#~ # apply gumbel parameters without/with and with bias correction, for annual flood maxima variables: ['surfaceWaterLevel'] 
#~ python  5a_gumbel_fits_apply_gumbel_parameters_without_bias_correction_for_historical_and_baseline_runs.py "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/gfdl-esm2m/1960-1999/gumbel_fits/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/gfdl-esm2m/1960-1999/extreme_values/" 1960 1999 surface_water_level_historical_gfdl-esm2m_1980 surfaceWaterLevel


###################################################################################

#~ # derive/downscale flood inundation maps at 30 arc-second resolution
#~ DONE

#~ # merging all downscaled map
#~ DONE


###################################################################################


