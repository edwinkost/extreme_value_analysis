
#~ bash 0_analysis_for_rcp_runs/rcp2p6/extreme_value_analysis/extreme_value_analysis_rcp2p6_gfdl-esm2m.sh &
#~ wait
bash 0_analysis_for_rcp_runs/rcp2p6/extreme_value_analysis/extreme_value_analysis_rcp2p6_hadgem2-es.sh &
bash 0_analysis_for_rcp_runs/rcp2p6/extreme_value_analysis/extreme_value_analysis_rcp2p6_ipsl-cm5a-lr.sh & 
bash 0_analysis_for_rcp_runs/rcp2p6/extreme_value_analysis/extreme_value_analysis_rcp2p6_miroc-esm-chem.sh &
wait
bash 0_analysis_for_rcp_runs/rcp2p6/extreme_value_analysis/extreme_value_analysis_rcp2p6_noresm1-m.sh
