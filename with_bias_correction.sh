
python 5ab_gumbel_fits_apply_gumbel_parameters_for_inundation_with_bias_correction.py 2010 2049 /scratch-shared/edwinhs/bias_correction_test/input/rcp4p5/gumbel_fits/gfdl-esm2m_2010-2049/ /scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits/gfdl-esm2m_1960-1999/ /scratch-shared/edwinhs/bias_correction_test/output/extreme_values_bias_corrected/gfdl-esm2m_2010-2049/
 
python 5bb_gumbel_fits_apply_gumbel_parameters_for_surface_water_level_with_bias_correction.py 2010 2049 /scratch-shared/edwinhs/bias_correction_test/input/rcp4p5/gumbel_fits_surface_water_level/gfdl-esm2m_2010-2049/ /scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits_surface_water_level/gfdl-esm2m_1960-1999/ /scratch-shared/edwinhs/bias_correction_test/output/extreme_values_surface_water_level_bias_corrected/gfdl-esm2m_2010-2049/

python 6_downscaling_parallel.py /scratch-shared/edwinhs/bias_correction_test/output/extreme_values_bias_corrected/gfdl-esm2m_2010-2049/ /scratch-shared/edwinhs/bias_correction_test/output/extreme_values_bias_corrected/gfdl-esm2m_2010-2049/ /scratch-shared/edwinhs/bias_correction_test/output/inundation_downscaled_bias_corrected/gfdl-esm2m_2010-2049/ bias_corrected

