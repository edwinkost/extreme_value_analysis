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
# calculate gumbel parameters for inundation
# calculate gumbel parameters for surface water level

# apply gumbel fits with bias correction for inundation
python 5ab_gumbel_fits_apply_gumbel_parameters_for_inundation_with_bias_correction.py 2010 2049 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp8p5_runs_2010-2049/gumbel_fits/noresm1-m_2010-2049/ /scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits/noresm1-m_1960-1999/ /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2010-2049/rcp8p5/extreme_values_bias_corrected/noresm1-m_2010-2049/
 
# apply gumbel fits for surface water level for surface water level
python 5bb_gumbel_fits_apply_gumbel_parameters_for_surface_water_level_with_bias_correction.py 2010 2049 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp8p5_runs_2010-2049/gumbel_fits_surface_water_level/noresm1-m_2010-2049/ /scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits_surface_water_level/noresm1-m_1960-1999/ /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2010-2049/rcp8p5/extreme_values_surface_water_level_bias_corrected/noresm1-m_2010-2049/

# downscaling inundation
python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2010-2049/rcp8p5/extreme_values_bias_corrected/noresm1-m_2010-2049/ /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2010-2049/rcp8p5/inundation_downscaled_bias_corrected/noresm1-m_2010-2049/ bias_corrected

# merging the downscaled maps
python 7_merging_downscaled_maps.py /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2010-2049/rcp8p5/inundation_downscaled_bias_corrected/noresm1-m_2010-2049/ inunriver_rcp8p5_noresm1-m_2010-2049.nc 2010 2049


# analysis for 2030 to 2069

# done using other scripts:
# get maximum events for two hydrological year types
# merging two hydrological years
# calculate annual maxima of river depth (surface water level) at half arc-degree resolution
# calculate gumbel parameters for inundation
# calculate gumbel parameters for surface water level

# apply gumbel fits with bias correction for inundation
python 5ab_gumbel_fits_apply_gumbel_parameters_for_inundation_with_bias_correction.py 2030 2069 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp8p5_runs_2030-2069/gumbel_fits/noresm1-m_2030-2069/ /scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits/noresm1-m_1960-1999/ /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2030-2069/rcp8p5/extreme_values_bias_corrected/noresm1-m_2030-2069/
 
# apply gumbel fits for surface water level for surface water level
python 5bb_gumbel_fits_apply_gumbel_parameters_for_surface_water_level_with_bias_correction.py 2030 2069 /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_rcp8p5_runs_2030-2069/gumbel_fits_surface_water_level/noresm1-m_2030-2069/ /scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits_surface_water_level/noresm1-m_1960-1999/ /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2030-2069/rcp8p5/extreme_values_surface_water_level_bias_corrected/noresm1-m_2030-2069/

# downscaling inundation
python 6_downscaling_parallel.py /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2030-2069/rcp8p5/extreme_values_bias_corrected/noresm1-m_2030-2069/ /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2030-2069/rcp8p5/inundation_downscaled_bias_corrected/noresm1-m_2030-2069/ bias_corrected

# merging the downscaled maps
python 7_merging_downscaled_maps.py /projects/0/aqueduct/users/edwinsut/bias_corrected_flood_analyzer_analysis_rcp8p5_runs_2030-2069/rcp8p5/inundation_downscaled_bias_corrected/noresm1-m_2030-2069/ inunriver_rcp8p5_noresm1-m_2030-2069.nc 2030 2069
