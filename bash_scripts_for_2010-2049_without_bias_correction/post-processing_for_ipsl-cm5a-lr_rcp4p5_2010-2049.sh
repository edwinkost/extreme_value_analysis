
# get maximum events for two hydrological year types
python 1a_get_maximum_events.py /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr/no_correction/rcp4p5/merged_2006-2099/ 1 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events/ipsl-cm5a-lr_2010-2049/ &
python 1a_get_maximum_events.py /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr/no_correction/rcp4p5/merged_2006-2099/ 2 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events/ipsl-cm5a-lr_2010-2049/ &
wait

# merging two hydrological years
python 2_merge_two_hydrological_year_result.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events/ipsl-cm5a-lr_2010-2049/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events_merged/ipsl-cm5a-lr_2010-2049/

# calculate annual maxima of river depth (surface water level) at half arc-degree resolution
python 3_calculate_maximum_river_depth.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events_merged/ipsl-cm5a-lr_2010-2049/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/surface_water_level_maximum/ipsl-cm5a-lr_2010-2049/

# calculate gumbel parameters for inundation
python 4a_gumbel_fits_get_gumbel_parameters_for_inundation.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events_merged/ipsl-cm5a-lr_2010-2049/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/gumbel_fits/ipsl-cm5a-lr_2010-2049/

# calculate gumbel parameters for surface water level
python 4b_gumbel_fits_get_gumbel_parameters_for_surface_water_level.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/surface_water_level_maximum/ipsl-cm5a-lr_2010-2049/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/gumbel_fits_surface_water_level/ipsl-cm5a-lr_2010-2049/

# apply gumbel fits for inundation
python 5a_gumbel_fits_apply_gumbel_parameters_for_inundation.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/gumbel_fits/ipsl-cm5a-lr_2010-2049/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/extreme_values/ipsl-cm5a-lr_2010-2049/

# apply gumbel fits for surface water level
python 5b_gumbel_fits_apply_gumbel_parameters_for_surface_water_level.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/gumbel_fits_surface_water_level/ipsl-cm5a-lr_2010-2049/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/extreme_values_surface_water_level/ipsl-cm5a-lr_2010-2049/

# downscaling inundation
python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/extreme_values/ipsl-cm5a-lr_2010-2049/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/inundation_downscaled/ipsl-cm5a-lr_2010-2049/

# merging the downscaled maps
python 7_merging_downscaled_maps.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/inundation_downscaled/ipsl-cm5a-lr_2010-2049/ inunriver_rcp4p5_ipsl-cm5a-lr_2010-2049.nc
