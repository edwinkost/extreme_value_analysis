
# Using strahler order 6
# - downscaling inundation
python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/rcp8p5/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2010-2049/rcp8p5/extreme_values_bias_corrected/gfdl-esm2m_2010-2049/ /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2017_05_XX/downscaling_bias_corrected_climate_runs/rcp8p5/gfdl-esm2m_2010-2049_using_strahler_order_6/ bias_corrected channel_storage.map 6
# - merging all downscaled maps
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2017_05_XX/downscaling_bias_corrected_climate_runs/rcp8p5/gfdl-esm2m_2010-2049_using_strahler_order_6/ /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2017_05_XX/downscaling_bias_corrected_climate_runs/rcp8p5/gfdl-esm2m_2010-2049_using_strahler_order_6/ inunriver_rcp8p5_0000GFDL-ESM2M_2030 2010 2049 channel_storage.map 06

