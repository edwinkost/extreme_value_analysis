#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00
#SBATCH -p normal
#SBATCH --constraint=haswell
#~ #SBATCH -p fat

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

# job name
#SBATCH -J watch_downscaling_sorder_3_edwinhs


set -x

# go to the main working folder (containing the scripts):
cd /home/edwinhs/github/edwinkost/extreme_value_analysis/
# 
# 
###################################################################################


###################################################################################
#
# Set the following variables:
#
STRAHLER_ORDER=3
#
MAIN_OUTPUT_FOLDER=/scratch-shared/edwinhs/flood_analyzer_sorder_sensitivity_analysis_2018_05_XX/strahler_order_${STRAHLER_ORDER}
#
MAIN_INPUT_FOLDER=/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/
#
RCP_CODE=historical
#
GCM_SMALL_LETTERS=watch
#
GCM_CONVENTION_NAME=000000000WATCH
GCM_CAPITAL_LETTERS=WATCH
#
TYPE_OF_EXTREME_VALUE_FILE=normal
#
PCRGLOBWB_OUTPUT_FOLDER=/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave/no_correction/non-natural/merged_1958_to_2001/global/netcdf/
#
echo $PCRGLOBWB_OUTPUT_FOLDER
# 
# 
###################################################################################



# derive/downscale flood inundation maps at 30 arc-second resolution
#
# 1960-1999 (1980) 
#~ python 6_downscaling_parallel.py ${MAIN_INPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/extreme_values/channel_storage/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/inundation_30sec/before_merged/ ${TYPE_OF_EXTREME_VALUE_FILE} channel_storage.map ${MAIN_INPUT_FOLDER}/historical/1960-1999/WATCH/extreme_values/channel_storage/2-year_of_channel_storage_used_as_bankfull_capacity.map ${STRAHLER_ORDER}
# merging all downscaled maps
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/inundation_30sec/before_merged/ ${MAIN_OUTPUT_FOLDER}/${RCP_CODE}/1960-1999/${GCM_CAPITAL_LETTERS}/inundation_30sec/merged/ inunriver_${RCP_CODE}_${GCM_CONVENTION_NAME}_1980 1960 1999 channel_storage.map 0${STRAHLER_ORDER}
#
#
###################################################################################


