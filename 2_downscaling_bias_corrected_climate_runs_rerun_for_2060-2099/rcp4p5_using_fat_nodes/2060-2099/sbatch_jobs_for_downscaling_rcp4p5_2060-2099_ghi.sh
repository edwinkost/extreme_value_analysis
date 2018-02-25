#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00
#SBATCH -p fat
#SBATCH -J rcp4p5-2080-ghi
#~ #SBATCH -J rcp4p5-2080-mn

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

bash downscaling_gfdl-esm2m_rcp4p5_2060-2099.sh &
bash downscaling_hadgem2-es_rcp4p5_2060-2099.sh &
bash downscaling_ipsl-cm5a-lr_rcp4p5_2060-2099.sh & 
#~ bash downscaling_miroc-esm-chem_rcp4p5_2060-2099.sh & 
#~ bash downscaling_noresm1-m_rcp4p5_2060-2099.sh &

wait
