
cd /home/edwinsut/github/edwinkost/extreme_value_analysis/2_downscaling_bias_corrected_climate_runs_rerun_for_2060-2099/rcp8p5/2060-2099/

bash downscaling_gfdl-esm2m_rcp8p5_2060-2099.sh &
bash downscaling_hadgem2-es_rcp8p5_2060-2099.sh &
bash downscaling_ipsl-cm5a-lr_rcp8p5_2060-2099.sh & 
bash downscaling_miroc-esm-chem_rcp8p5_2060-2099.sh & 
bash downscaling_noresm1-m_rcp8p5_2060-2099.sh &

wait
