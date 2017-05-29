
# Using strahler order 6
# - downscaling inundation
python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/extreme_values/gfdl-esm2m_1960-1999/ /scratch-shared/edwinsut/finalizing_downscaling_historical/gfdl-esm2m_1960-1999_using_strahler_order_6/ normal channel_storage.map 6
# - merging all downscaled maps
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py /scratch-shared/edwinsut/finalizing_downscaling_historical/gfdl-esm2m_1960-1999_using_strahler_order_6/ /scratch-shared/edwinsut/finalizing_downscaling_historical/gfdl-esm2m_1960-1999_using_strahler_order_6/ inunriver_historical_GFDL-ESM2M 1960 1999 channel_storage.map 06




