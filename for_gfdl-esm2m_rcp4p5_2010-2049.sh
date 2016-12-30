
# get maximum events for two hydrological year types
python 1a_get_maximum_events.py /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m/no_correction/rcp4p5/merged_2006-2099/ 1 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events/gfdl-esm2m_2010-2049/ &
python 1a_get_maximum_events.py /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m/no_correction/rcp4p5/merged_2006-2099/ 2 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events/gfdl-esm2m_2010-2049/ &
wait

# merging two hydrological years
python 2_merge_two_hydrological_year_result.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events/gfdl-esm2m_2010-2049/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events_merged/gfdl-esm2m_2010-2049/

# calculate annual maxima of river depth (surface water level) at half arc-degree resolution
python 3_calculate_maximum_river_depth.py /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/maximum_events_merged/gfdl-esm2m_2010-2049/ /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp4p5_runs/surface_water_level_maximum/gfdl-esm2m_2010-2049/

