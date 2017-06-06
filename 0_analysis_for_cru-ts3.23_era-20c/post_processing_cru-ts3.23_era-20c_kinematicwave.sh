
#~ # get maximum events for the hydrological year types 1 and 2
#~ python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave/no_correction/non-natural/merged_1958-2010/global/netcdf/" 1 /scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/maximum_events/ 1960 1999 &
#~ python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave/no_correction/non-natural/merged_1958-2010/global/netcdf/" 2 /scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/maximum_events/ 1960 1999 &
#~ 
#~ # derive hydro year type (only for the baseline run)
#~ python 1b_for_baseline_only_derive_hydrological_year_type.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave/no_correction/non-natural/merged_1958-2010/global/netcdf/" discharge_monthAvg_output_1958-01-31_to_2010-12-31.nc 1960 1999 /scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/hydrological_year_types_1960-1999/ &
#~ 
#~ wait
#~ 
#~ ###################################################################################
#~ 
#~ # get annual maximum events based on a defined/given hydrological year tipe map
#~ python 2_merge_two_hydrological_year_result.py "/scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/maximum_events/" /scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/hydrological_year_types_1960-1999/hydrological_year_type.map "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/maximum_events/merged/" 1960 1999 
#~ 
#~ 
#~ ###################################################################################
#~ 
#~ # calculate maximum surface water level (river depth)
#~ python 3_calculate_maximum_river_depth_without_upscaling.py "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/maximum_events/merged/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/surface_water_level_maximum/" 1960 1999 
#~ 
#~ 
###################################################################################
#~ 
#~ # gumbel fits for annual flood maxima variables: ['channelStorage', 'surfaceWaterLevel']
#~ python 4_gumbel_fits_get_gumbel_parameters_for_inundation_and_surface_water_level_variables.py "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/maximum_events/merged/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/surface_water_level_maximum/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/gumbel_fits/" 1960 1999 


###################################################################################

#~ # apply gumbel parameters without/with and with bias correction, for annual flood maxima variables: ['channelStorage', 'surfaceWaterLevel'] 
#~ python  5a_gumbel_fits_apply_gumbel_parameters_without_bias_correction_for_historical_and_baseline_runs.py "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/gumbel_fits/" "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/extreme_values/" 1960 1999


###################################################################################

#~ # derive/downscale flood inundation maps at 30 arc-second resolution
#~ python 6_downscaling_parallel.py "/scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/extreme_values/" "/scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/inundation_downscaled/" normal "channel_storage.map" 6

# merging all downscaled map
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py "/scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/inundation_downscaled/" "/scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/inundation_downscaled/" inunriver_historical_0_cru-ts3.23_era-20c_1980 1960 1999 channel_storage.map 06


###################################################################################


