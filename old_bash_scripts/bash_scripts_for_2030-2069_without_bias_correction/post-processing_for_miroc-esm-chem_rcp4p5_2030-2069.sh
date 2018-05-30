
# get maximum events for two hydrological year types
python 1a_get_maximum_events.py /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem/no_correction/rcp4p5/merged_2006-2099/ 1 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/maximum_events/miroc-esm-chem_2060-2069/ &
python 1a_get_maximum_events.py /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem/no_correction/rcp4p5/merged_2006-2099/ 2 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/maximum_events/miroc-esm-chem_2060-2069/ &
wait

# merging two hydrological years
python 2_merge_two_hydrological_year_result.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/maximum_events/miroc-esm-chem_2060-2069/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/maximum_events_merged/miroc-esm-chem_2060-2069/

# calculate annual maxima of river depth (surface water level) at half arc-degree resolution
python 3_calculate_maximum_river_depth.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/maximum_events_merged/miroc-esm-chem_2060-2069/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/surface_water_level_maximum/miroc-esm-chem_2060-2069/

# calculate gumbel parameters for inundation
python 4a_gumbel_fits_get_gumbel_parameters_for_inundation.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/maximum_events_merged/miroc-esm-chem_2060-2069/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/gumbel_fits/miroc-esm-chem_2060-2069/

# calculate gumbel parameters for surface water level
python 4b_gumbel_fits_get_gumbel_parameters_for_surface_water_level.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/surface_water_level_maximum/miroc-esm-chem_2060-2069/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/gumbel_fits_surface_water_level/miroc-esm-chem_2060-2069/

# apply gumbel fits for inundation
python 5a_gumbel_fits_apply_gumbel_parameters_for_inundation.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/gumbel_fits/miroc-esm-chem_2060-2069/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/extreme_values/miroc-esm-chem_2060-2069/

# apply gumbel fits for surface water level
python 5b_gumbel_fits_apply_gumbel_parameters_for_surface_water_level.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/gumbel_fits_surface_water_level/miroc-esm-chem_2060-2069/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/extreme_values_surface_water_level/miroc-esm-chem_2060-2069/

# downscaling inundation
python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/extreme_values/miroc-esm-chem_2060-2069/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/inundation_downscaled/miroc-esm-chem_2060-2069/

# merging the downscaled maps
python 7_merging_downscaled_maps.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs_2060-2069/inundation_downscaled/miroc-esm-chem_2060-2069/ inunriver_rcp4p5_miroc-esm-chem_2060-2069.nc
