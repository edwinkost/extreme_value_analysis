
# get maximum events for the hydrological year types 1 and 2
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave/no_correction/non-natural/merged_1958-2010/global/netcdf/" 1 /scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/maximum_events/1960-1999/ 1960 1999 &
python 1a_get_maximum_events.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave/no_correction/non-natural/merged_1958-2010/global/netcdf/" 2 /scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/maximum_events/1960-1999/ 1960 1999 &

# derive hydro year type (only for the baseline run)
python 1b_for_baseline_only_derive_hydrological_year_type.py "/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave/no_correction/non-natural/merged_1958-2010/global/netcdf/" discharge_monthAvg_output_1958-01-31_to_2010-12-31.nc 1960 1999 /scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/hydrological_year_types_1960-1999/ &

wait

###################################################################################

# get annual maximum events based on a defined/given hydrological year tipe map
python 2_merge_two_hydrological_year_result.py "/scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/maximum_events/1960-1999/" /scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/1960-1999/hydrological_year_types_1960-1999/hydrological_year_type.map "/scratch-shared/edwinsut/flood_analyzer_analysis_june_2017/cru-ts3.23_era-20c_kinematicwave/maximum_events/1960-1999/merged/" 1960 1999 &

wait

###################################################################################


