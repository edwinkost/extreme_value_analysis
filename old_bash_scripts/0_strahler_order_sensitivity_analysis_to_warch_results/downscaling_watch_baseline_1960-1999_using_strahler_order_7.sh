
# Using strahler order 7
# - downscaling inundation
python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/extreme_values/watch_1960-1999/ /scratch-shared/edwinsut/finalizing_downscaling/using_strahler_order_7/ normal channel_storage.map 7
# - merging all downscaled maps
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py /scratch-shared/edwinsut/finalizing_downscaling/using_strahler_order_7/ /scratch-shared/edwinsut/finalizing_downscaling/using_strahler_order_7/ inunriver_historical_WATCH_1999 1960 1999 channel_storage.map 07
