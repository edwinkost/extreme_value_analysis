#!/bin/bash                                                                                                                 
#SBATCH -N 1                                                                                                                
#SBATCH -t 49:49:49                                                                                                        
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
# Downscaling BIAS-CORRECTED floods - rcp8p5 - noresm1-m - inunriver_rcp8p5_00000NorESM1-M
#
################################################################################################
#
# 2010-2049 (2030)
# DONE
#
# 2030-2069 (2050)
# DONE
#
# 2050-2099 (2080)
#~ # - derive/downscale flood inundation maps at 30 arc-second resolution
#~ python 6_downscaling_parallel.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp8p5/2050-2099/noresm1-m/extreme_values/channel_storage/" /scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/rcp8p5/2050-2099/noresm1-m/inundation_downscaled/bias_corrected/ "bias_corrected" channel_storage.map 6
# - merging all downscaled map
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py "/scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/rcp8p5/2050-2099/noresm1-m/inundation_downscaled/bias_corrected/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2017_05_XX/river/inundation/rcp8p5/2050-2099/inundation_downscaled_from_bias_corrected_floods/NorESM1-M/" inunriver_rcp8p5_00000NorESM1-M_2080 2050 2099 channel_storage.map 06
#
#
################################################################################################



################################################################################################
#
# Downscaling NON-bias_corrected floods - rcp8p5 - noresm1-m - inunriver_rcp8p5_00000NorESM1-M
#
################################################################################################
#
# 2010-2049 (2030)
# DONE
#
# 2030-2069 (2050)
# DONE
#
# 2050-2099 (2080)
#~ # - derive/downscale flood inundation maps at 30 arc-second resolution
#~ python 6_downscaling_parallel.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_june_2017/rcp8p5/2050-2099/noresm1-m/extreme_values/channel_storage/" /scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/rcp8p5/2050-2099/noresm1-m/inundation_downscaled/including_bias/ "including_bias" channel_storage.map 6
# - merging all downscaled map
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py "/scratch/shared/edwinsut/flood_analyzer_analysis_june_2017/rcp8p5/2050-2099/noresm1-m/inundation_downscaled/including_bias/" "/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2017_05_XX/river/inundation/rcp8p5/2050-2099/inundation_downscaled_from_non_bias_corrected_floods/NorESM1-M/" inunriver_rcp8p5_00000NorESM1-M_2080 2050 2099 channel_storage.map 06
#
#
################################################################################################

