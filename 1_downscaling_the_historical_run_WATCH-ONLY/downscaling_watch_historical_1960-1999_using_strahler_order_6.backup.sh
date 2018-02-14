
# using strahler order 6

#~ # - downscaling inundation
#~ python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/extreme_values/watch_1960-1999/ /scratch-shared/edwinsut/flood_inundation_2018_02_XX/historical/watch/1960-1999/ normal channel_storage.map 6

# - merging all downscaled maps
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py /scratch-shared/edwinsut/flood_inundation_2018_02_XX/before_merged/historical/WATCH/1960-1999/ /scratch-shared/edwinsut/flood_inundation_2018_02_XX/merged/historical/WATCH/1960-1999/ inunriver_historical_000000000WATCH_1980 1960 1999 channel_storage.map 06

