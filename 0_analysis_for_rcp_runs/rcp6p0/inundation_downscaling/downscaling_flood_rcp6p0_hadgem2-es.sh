#!/bin/bash                                                                                                                 
#SBATCH -N 1                                                                                                                
#SBATCH -t 119:00:00                                                                                                        
#SBATCH -p normal                                                                                                           
#SBATCH --constraint=haswell                                                                                                
                                                                                                                            
# mail alert at start, end and abortion of execution                                                                        
#SBATCH --mail-type=ALL                                                                                                     
                                                                                                                            
# send mail to this address                                                                                                 
#SBATCH --mail-user=edwinkost@gmail.com                                                                                     



# move to the folder that contains the scripts
cd /home/edwinsut/github/edwinkost/extreme_value_analysis


################################################################################################
#
# Downscaling BIAS-CORRECTED floods - rcp6p0 - hadgem2-es - inunriver_rcp6p0_0000HadGEM2-ES
#
################################################################################################
#
# 2010-2049 (2030)
# - derive/downscale flood inundation maps at 30 arc-second resolution
python 6_downscaling_parallel.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/extreme_values/channel_storage/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/inundation_downscaled/bias_corrected/ "bias_corrected" channel_storage.map 6
# - merging all downscaled map
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/inundation_downscaled/bias_corrected/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/inundation_downscaled/bias_corrected/" inunriver_rcp6p0_0000HadGEM2-ES_2030 2010 2049 channel_storage.map 06
#
# 2030-2069 (2050)
# - derive/downscale flood inundation maps at 30 arc-second resolution
python 6_downscaling_parallel.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/extreme_values/channel_storage/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/inundation_downscaled/bias_corrected/ "bias_corrected" channel_storage.map 6
# - merging all downscaled map
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/inundation_downscaled/bias_corrected/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/inundation_downscaled/bias_corrected/" inunriver_rcp6p0_0000HadGEM2-ES_2050 2030 2069 channel_storage.map 06
#
# 2050-2099 (2080)
# - derive/downscale flood inundation maps at 30 arc-second resolution
python 6_downscaling_parallel.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/extreme_values/channel_storage/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/inundation_downscaled/bias_corrected/ "bias_corrected" channel_storage.map 6
# - merging all downscaled map
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/inundation_downscaled/bias_corrected/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/inundation_downscaled/bias_corrected/" inunriver_rcp6p0_0000HadGEM2-ES_2080 2050 2099 channel_storage.map 06
#
#
################################################################################################



################################################################################################
#
# Downscaling NON-bias_corrected floods - rcp6p0 - hadgem2-es - inunriver_rcp6p0_0000HadGEM2-ES
#
################################################################################################
#
# 2010-2049 (2030)
# - derive/downscale flood inundation maps at 30 arc-second resolution
python 6_downscaling_parallel.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/extreme_values/channel_storage/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/inundation_downscaled/including_bias/ "including_bias" channel_storage.map 6
# - merging all downscaled map
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/inundation_downscaled/including_bias/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2010-2049/hadgem2-es/inundation_downscaled/including_bias/" inunriver_rcp6p0_0000HadGEM2-ES_2030 2010 2049 channel_storage.map 06
#
# 2030-2069 (2050)
# - derive/downscale flood inundation maps at 30 arc-second resolution
python 6_downscaling_parallel.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/extreme_values/channel_storage/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/inundation_downscaled/including_bias/ "including_bias" channel_storage.map 6
# - merging all downscaled map
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/inundation_downscaled/including_bias/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2030-2069/hadgem2-es/inundation_downscaled/including_bias/" inunriver_rcp6p0_0000HadGEM2-ES_2050 2030 2069 channel_storage.map 06
#
# 2050-2099 (2080)
#~ # - derive/downscale flood inundation maps at 30 arc-second resolution
python 6_downscaling_parallel.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/extreme_values/channel_storage/" /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/inundation_downscaled/including_bias/ "including_bias" channel_storage.map 6
# - merging all downscaled map
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/inundation_downscaled/including_bias/" "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp6p0/2050-2099/hadgem2-es/inundation_downscaled/including_bias/" inunriver_rcp6p0_0000HadGEM2-ES_2080 2050 2099 channel_storage.map 06
#
#
################################################################################################

