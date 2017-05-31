
# Using strahler order 6
# - downscaling inundation
python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/rcp4p5/flood_analyzer_analysis_rcp4p5_runs_2030-2069/extreme_values/ipsl-cm5a-lr_2030-2069/ /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2017_05_XX/downscaling_including_bias_climate_runs/rcp4p5/ipsl-cm5a-lr_2030-2069_using_strahler_order_6/ normal channel_storage.map 6
# - merging all downscaled maps
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2017_05_XX/downscaling_including_bias_climate_runs/rcp4p5/ipsl-cm5a-lr_2030-2069_using_strahler_order_6/ /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2017_05_XX/downscaling_including_bias_climate_runs/rcp4p5/ipsl-cm5a-lr_2030-2069_using_strahler_order_6/ inunriver_rcp4p5_00IPSL-CM5A-LR_2050 2030 2069 channel_storage.map 06

