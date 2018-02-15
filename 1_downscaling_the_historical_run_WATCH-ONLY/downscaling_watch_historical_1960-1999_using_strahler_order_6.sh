#!/bin/bash
#SBATCH -N 1
#~ #SBATCH -t 29:00:00
#~ #SBATCH -p normal
#SBATCH -p short

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

# job name
#SBATCH -J historical_WATCH_1980

STA_PERIOD=1960
END_PERIOD=1999
MID_PERIOD=1980

NETCDF_OUTPUT_CONVENTION=inunriver_historical_000000000WATCH_$MID_PERIOD

MERGED_MAP_OUTPUT_FOLDER=/scratch-shared/edwinsut/flood_inundation_2018_02_XX/merged/historical/WATCH/$STA_PERIOD-$END_PERIOD/

UNMERGED_MAP_OUTPUT_FOLDER=/scratch-shared/edwinsut/flood_inundation_2018_02_XX/before_merged/historical/WATCH/$STA_PERIOD-$END_PERIOD/

EXTREME_VALUE_INPUT_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/historical/extreme_values/watch_1960-1999/

TYPE_OF_EXTREME_VALUE_FILE=normal

# other options: using strahler order 6 to downscale channel_storage.map

###################################################################################################################################


# - cleaning up previous folders
rm -r $UNMERGED_MAP_OUTPUT_FOLDER
rm -r $MERGED_MAP_OUTPUT_FOLDER

# - go to the script folder
cd /home/edwinsut/github/edwinkost/extreme_value_analysis

# - downscaling inundation
echo python 6_downscaling_parallel.py $EXTREME_VALUE_INPUT_FOLDER $UNMERGED_MAP_OUTPUT_FOLDER $TYPE_OF_EXTREME_VALUE_FILE channel_storage.map 6

# - merging all downscaled maps
echo python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py $UNMERGED_MAP_OUTPUT_FOLDER $MERGED_MAP_OUTPUT_FOLDER $NETCDF_OUTPUT_CONVENTION $STA_PERIOD $END_PERIOD channel_storage.map 06
