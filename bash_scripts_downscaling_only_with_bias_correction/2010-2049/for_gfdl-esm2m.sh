#!/bin/bash
#SBATCH -N 1
#SBATCH -t 72:59:00 
#SBATCH -p normal
#SBATCH --constraint=haswell


# go to the script directory
cd /home/edwinsut/github/edwinkost/extreme_value_analysis/

# analysis for 2010 to 2049

# done using other scripts:
# get maximum events for two hydrological year types
# merging two hydrological years
# calculate annual maxima of river depth (surface water level) at half arc-degree resolution
# calculate gumbel parameters for flood inundation volume and channel storage
# calculate gumbel parameters for surface water level
# apply gumbel fits with bias correction for inundation
# apply gumbel fits for surface water level for surface water level
# downscaling flood inundation volume and merging the downscaled maps

# downscaling inundation based on channel storage and merging the downscaled maps
# - rcp4p5
python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp4p5_runs_2010-2049/rcp4p5/extreme_values_bias_corrected/gfdl-esm2m_2010-2049/ /scratch-shared/edwinhs/inundation_downscaled_using_channel_storage/rcp4p5/gfdl-esm2m_2010-2049/ bias_corrected channel_storage.map
# - rcp8p5
python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2010-2049/rcp8p5/extreme_values_bias_corrected/gfdl-esm2m_2010-2049/ /scratch-shared/edwinhs/inundation_downscaled_using_channel_storage/rcp8p5/gfdl-esm2m_2010-2049/ bias_corrected channel_storage.map
