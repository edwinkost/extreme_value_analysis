#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00
#SBATCH -p normal
#SBATCH --constraint=haswell
#~ #SBATCH -p fat

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL
# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

# job name
#SBATCH -J checking_results


set -x

cd /home/edwin/github/edwinkost/extreme_value_analysis/

echo "historical (WATCH only)"
cdo infon /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/*.nc
python checking_results.py "/projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/*mask*.map" historical



echo "rcp4p5"

echo "rcp4p5 - checking channel storage"
cdo infon /projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/*/*/extreme_values/channel_storage/bias_corrected_additive_extreme_values_*.nc

echo "rcp4p5 - checking channel storage, comparing to the reference values at the same return period"
cdo infon /projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/*/*/extreme_values/channel_storage/bias_corrected_additive_above_reference_at_the_same_return_period_extreme_values_*.nc

echo "rcp4p5 - checking surface water level"
cdo infon /projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/*/*/extreme_values/surface_water_level/bias_corrected_additive_extreme_values_*.nc

echo "rcp4p5 - checking surface water level, comparing to the reference values at the same return period"
cdo infon /projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/*/*/extreme_values/surface_water_level/bias_corrected_additive_above_reference_at_the_same_return_period_extreme_values_*.nc

echo "rcp4p5 - checking surface water level, per return period map"
cdo infon /projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/*/*/extreme_values/surface_water_level/*rp*.nc

python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2010-*/GFDL*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2010-*/HadG*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2010-*/IPSL*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2010-*/MIRO*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2010-*/NorE*/extreme_values/surface_water_level/bias_corrected_*mask*.map"

python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2030-*/GFDL*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2030-*/HadG*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2030-*/IPSL*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2030-*/MIRO*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2030-*/NorE*/extreme_values/surface_water_level/bias_corrected_*mask*.map"

python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2060-*/GFDL*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2060-*/HadG*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2060-*/IPSL*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2060-*/MIRO*/extreme_values/surface_water_level/bias_corrected_*mask*.map"
python checking_results.py "/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/rcp4p5/2060-*/NorE*/extreme_values/surface_water_level/bias_corrected_*mask*.map"


