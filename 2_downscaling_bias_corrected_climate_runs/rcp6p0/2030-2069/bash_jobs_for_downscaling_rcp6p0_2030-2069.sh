
cd /home/edwinsut/github/edwinkost/extreme_value_analysis/2_downscaling_bias_corrected_climate_runs/rcp6p0/2030-2069/

bash downscaling_gfdl-esm2m_rcp6p0_2030-2069.sh &
bash downscaling_hadgem2-es_rcp6p0_2030-2069.sh &
bash downscaling_ipsl-cm5a-lr_rcp6p0_2030-2069.sh & 
bash downscaling_miroc-esm-chem_rcp6p0_2030-2069.sh & 
bash downscaling_noresm1-m_rcp6p0_2030-2069.sh &

wait
