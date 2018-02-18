#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00
#SBATCH -p fat
#~ #SBATCH -p short

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

# job name
#SBATCH -J rcp6p0_ALL-GCMs_ALL-PERIODS


cd /home/edwinsut/github/edwinkost/extreme_value_analysis/2_downscaling_bias_corrected_climate_runs/rcp6p0/

bash 2010-2049/bash_jobs_for_downscaling_rcp6p0_2010-2049.sh

cd /home/edwinsut/github/edwinkost/extreme_value_analysis/2_downscaling_bias_corrected_climate_runs/rcp6p0/

bash 2030-2069/bash_jobs_for_downscaling_rcp6p0_2030-2069.sh

cd /home/edwinsut/github/edwinkost/extreme_value_analysis/2_downscaling_bias_corrected_climate_runs/rcp6p0/

bash 2050-2099/bash_jobs_for_downscaling_rcp6p0_2050-2099.sh

