
cd /home/edwinsut/github/edwinkost/extreme_value_analysis/2_downscaling_bias_corrected_climate_runs/rcp4p5/2050-2099/

bash downscaling_gfdl-esm2m_rcp4p5_2050-2099.sh &
bash downscaling_hadgem2-es_rcp4p5_2050-2099.sh &
bash downscaling_ipsl-cm5a-lr_rcp4p5_2050-2099.sh & 
bash downscaling_miroc-esm-chem_rcp4p5_2050-2099.sh & 
bash downscaling_noresm1-m_rcp4p5_2050-2099.sh &

wait
