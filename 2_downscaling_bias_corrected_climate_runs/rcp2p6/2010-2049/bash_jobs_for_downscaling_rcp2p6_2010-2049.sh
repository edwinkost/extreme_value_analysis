
cd /home/edwinsut/github/edwinkost/extreme_value_analysis/2_downscaling_bias_corrected_climate_runs/rcp2p6/2010-2049/

bash downscaling_gfdl-esm2m_rcp2p6_2010-2049.sh &
bash downscaling_hadgem2-es_rcp2p6_2010-2049.sh &
bash downscaling_ipsl-cm5a-lr_rcp2p6_2010-2049.sh & 
bash downscaling_miroc-esm-chem_rcp2p6_2010-2049.sh & 
bash downscaling_noresm1-m_rcp2p6_2010-2049.sh &

wait
