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

cd /home/edwinsut/github/edwinkost/extreme_value_analysis/

echo "historical (WATCH only)"
cdo infon /scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/inundation_30sec/merged/global/netcdf/*.nc
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/inundation_30sec/merged/global/maps/*mask*.map" historical_inundation


echo "rcp2p6"
cdo infon /scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/*/*/inundation_30sec/merged/global/netcdf/*.nc

python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2010-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2010-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2010-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2010-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2010-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"
                            
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2030-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2030-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2030-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2030-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2030-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"
                            
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2060-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2060-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2060-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2060-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py  "/scratch-shared/edwinhs/flood_analyzer_analysis_2018_05_XX/rcp2p6/2060-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"


echo "rcp4p5"
cdo infon /scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/*/*/inundation_30sec/merged/global/netcdf/*.nc

python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2010-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2010-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2010-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2010-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2010-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"

python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2030-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2030-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2030-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2030-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2030-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"

python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2060-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2060-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2060-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2060-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp4p5/2060-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"


echo "rcp6p0"
cdo infon /scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/*/*/inundation_30sec/merged/global/netcdf/*.nc

python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2010-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2010-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2010-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2010-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2010-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"

python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2030-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2030-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2030-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2030-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2030-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"

python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2060-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2060-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2060-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2060-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp6p0/2060-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"


echo "rcp8p5"
cdo infon /scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/*/*/inundation_30sec/merged/global/netcdf/*.nc

python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2010-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2010-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2010-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2010-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2010-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"

python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2030-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2030-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2030-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2030-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2030-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"

python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2060-*/GFDL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2060-*/HadG*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2060-*/IPSL*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2060-*/MIRO*/inundation_30sec/merged/global/maps/*mask*.map"
python checking_results.py "/scratch-shared/edwinsut/flood_analyzer_analysis_2018_05_XX/rcp8p5/2060-*/NorE*/inundation_30sec/merged/global/maps/*mask*.map"
