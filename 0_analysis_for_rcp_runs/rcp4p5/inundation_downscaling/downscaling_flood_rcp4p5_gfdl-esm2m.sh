

############################################################################################
#
# Downscaling BIAS-CORRECTED floods - rcp4p5 - gfdl-esm2m - inunriver_rcp4p5_0000GFDL-ESM2M
#
############################################################################################
#
# 2010-2049 (2030)
# DONE
#
# 2030-2069 (2050)
# DONE
#
# 2050-2099 (2080)
# - derive/downscale flood inundation maps at 30 arc-second resolution
python 6_downscaling_parallel.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/gfdl-esm2m/extreme_values/channel_storage/" /scratch/shared/edwin/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/gfdl-esm2m/inundation_downscaled/ "bias_corrected" channel_storage.map 6
# - merging all downscaled map
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py "/scratch/shared/edwin/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/gfdl-esm2m/inundation_downscaled/" "/scratch/shared/edwin/flood_analyzer_analysis_june_2017/rcp4p5/2050-2099/gfdl-esm2m/inundation_downscaled/" inunriver_rcp4p5_0000GFDL-ESM2M_2080 2050 2099 channel_storage.map 06


############################################################################################


