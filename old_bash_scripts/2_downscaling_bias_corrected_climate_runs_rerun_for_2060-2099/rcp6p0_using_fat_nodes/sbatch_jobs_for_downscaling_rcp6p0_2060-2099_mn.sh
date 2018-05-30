#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00
#SBATCH -p fat

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

# job name
#~ #SBATCH -J rcp6p0_2080_ghi
#SBATCH -J rcp6p0_2080_mn

#~ bash downscaling_gfdl-esm2m_rcp6p0_2060-2099.sh &
#~ bash downscaling_hadgem2-es_rcp6p0_2060-2099.sh &
#~ bash downscaling_ipsl-cm5a-lr_rcp6p0_2060-2099.sh & 
bash downscaling_miroc-esm-chem_rcp6p0_2060-2099.sh & 
bash downscaling_noresm1-m_rcp6p0_2060-2099.sh &

wait
