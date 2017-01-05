
# done using other scripts:
# get maximum events for two hydrological year types
# merging two hydrological years
# calculate annual maxima of river depth (surface water level) at half arc-degree resolution
# calculate gumbel parameters for inundation
# calculate gumbel parameters for surface water level

# apply gumbel fits with bias correction for inundation
python 5ab_gumbel_fits_apply_gumbel_parameters_for_inundation_with_bias_correction.py 2010 2049 /scratch-shared/edwinhs/bias_correction_test/input/rcp8p5/gumbel_fits/gfdl-esm2m_2010-2049/ /scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits/gfdl-esm2m_1960-1999/ /scratch-shared/edwinhs/bias_correction_test/output/rcp8p5/extreme_values_bias_corrected/gfdl-esm2m_2010-2049/
 
# apply gumbel fits for surface water level for surface water level
python 5bb_gumbel_fits_apply_gumbel_parameters_for_surface_water_level_with_bias_correction.py 2010 2049 /scratch-shared/edwinhs/bias_correction_test/input/rcp8p5/gumbel_fits_surface_water_level/gfdl-esm2m_2010-2049/ /scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits_surface_water_level/gfdl-esm2m_1960-1999/ /scratch-shared/edwinhs/bias_correction_test/output/rcp8p5/extreme_values_surface_water_level_bias_corrected/gfdl-esm2m_2010-2049/

# downscaling inundation
python 6_downscaling_parallel.py /scratch-shared/edwinhs/bias_correction_test/output/rcp8p5/extreme_values_bias_corrected/gfdl-esm2m_2010-2049/ /scratch-shared/edwinhs/bias_correction_test/output/rcp8p5/inundation_downscaled_bias_corrected/gfdl-esm2m_2010-2049/ bias_corrected

# merging the downscaled maps
python 7_merging_downscaled_maps.py /scratch-shared/edwinhs/bias_correction_test/output/rcp8p5/inundation_downscaled_bias_corrected/gfdl-esm2m_2010-2049/ inunriver_rcp8p5_gfdl-esm2m_2010-2049.nc
