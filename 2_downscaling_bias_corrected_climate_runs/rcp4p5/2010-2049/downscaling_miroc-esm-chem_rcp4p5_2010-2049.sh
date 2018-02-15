#!/bin/bash
#SBATCH -N 1
#SBATCH -t 29:00:00
#SBATCH -p normal
#~ #SBATCH -p short

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#################################################################################################################################################

# steps:
# - Check whether it is from rcp or historical runs?
# - Check the type of extreme value maps: bias_corrected? 
# - Which rcp?
# - Which gcm? There are three formats: MIROC-ESM-CHEM and MIROC-ESM-CHEM and miroc-esm-chem (please be careful during find and replace-ing). 
# - Which time period?
# - Check the output folders: MERGED_MAP_OUTPUT_FOLDER and UNMERGED_MAP_OUTPUT_FOLDER (be careful here, do NOT write to your input folder).
# - Set the input folder: EXTREME_VALUE_INPUT_FOLDER (this varies among rcps).
# - Set/check the job name.

#################################################################################################################################################

# job name
#SBATCH -J rcp4p5_MIROC-ESM-CHEM_2030

TYPE_OF_EXTREME_VALUE_FILE=bias_corrected

STA_PERIOD=2010
END_PERIOD=2049
MID_PERIOD=2030

# nc filename convention:inunriver_rcp4p5_00000000000000_$MID_PERIOD
NETCDF_OUTPUT_CONVENTION=inunriver_rcp4p5_MIROC-ESM-CHEM_$MID_PERIOD

MERGED_MAP_OUTPUT_FOLDER=/scratch-shared/edwinsut/flood_inundation_2018_02_XX/merged/rcp4p5/MIROC-ESM-CHEM/$STA_PERIOD-$END_PERIOD/

UNMERGED_MAP_OUTPUT_FOLDER=/scratch-shared/edwinsut/flood_inundation_2018_02_XX/before_merged/rcp4p5/MIROC-ESM-CHEM/$STA_PERIOD-$END_PERIOD/

EXTREME_VALUE_INPUT_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2016_12_11/flood_analyzer_analysis/rcp4p5/bias_corrected_flood_analyzer_analysis_rcp4p5_runs_2010-2049/rcp4p5/extreme_values_bias_corrected/miroc-esm-chem_2010-2049/

# other options: using strahler order 6 to downscale channel_storage.map

###################################################################################################################################


# - cleaning up previous folders (if exists)
rm -r $UNMERGED_MAP_OUTPUT_FOLDER/*
rm -r $MERGED_MAP_OUTPUT_FOLDER/*

# - go to the script folder
cd /home/edwinsut/github/edwinkost/extreme_value_analysis

# - downscaling inundation
python 6_downscaling_parallel.py $EXTREME_VALUE_INPUT_FOLDER $UNMERGED_MAP_OUTPUT_FOLDER $TYPE_OF_EXTREME_VALUE_FILE channel_storage.map 6

# - merging all downscaled maps
python 7_merging_downscaled_maps_with_masking_out_and_following_name_convention.py $UNMERGED_MAP_OUTPUT_FOLDER $MERGED_MAP_OUTPUT_FOLDER $NETCDF_OUTPUT_CONVENTION $STA_PERIOD $END_PERIOD channel_storage.map 06




