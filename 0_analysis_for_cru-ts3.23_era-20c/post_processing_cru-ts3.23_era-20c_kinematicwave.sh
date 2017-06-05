
# get maximum events for the hydrological year types 1 and 2
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave/no_correction/non-natural/merged_1958-2010/global/netcdf/" 1 /scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/maximum_events/cru-ts3.23_era-20c_kinematicwave/ 1960 1999 &
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave/no_correction/non-natural/merged_1958-2010/global/netcdf/" 2 /scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/maximum_events/cru-ts3.23_era-20c_kinematicwave/ 1960 1999 &
wait

