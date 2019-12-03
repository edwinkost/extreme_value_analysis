#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00 
#SBATCH -p staging

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH -J copy_base-hist_archive_from_pcrglobwb_runs_2016_oct_nov

date

#~ edwin@srv5.bullx:/archive/edwinsut/aqueduct_flood_analyzer/pcrglobwb_runs/baseline_historical_incl_additional_spinup$ ls -lah
#~ total 798G
#~ drwxr-xr-x 2 edwinsut edwinsut 4.0K Oct 28  2017 .
#~ drwxr-xr-x 8 edwinsut edwinsut  124 Oct 29  2017 ..
#~ -rw-r--r-- 1 edwinsut edwinsut 798G Oct 28  2017 pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime.tar
#~ -rw-r--r-- 1 edwinsut edwinsut 1.3T Oct 28  2017 pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave.tar
#~ -rw-r--r-- 1 edwinsut edwinsut 972G Oct 28  2017 pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.tar
#~ -rw-r--r-- 1 edwinsut edwinsut 963G Oct 28  2017 pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.tar
#~ -rw-r--r-- 1 edwinsut edwinsut 966G Oct 28  2017 pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.tar
#~ -rw-r--r-- 1 edwinsut edwinsut 956G Oct 28  2017 pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.tar
#~ -rw-r--r-- 1 edwinsut edwinsut 969G Oct 28  2017 pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.tar
#~ -rw-r--r-- 1 edwinsut edwinsut 1.2T Oct 28  2017 pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.tar

MAIN_SOURCE_FOLDER="/archive/edwinsut/aqueduct_flood_analyzer/pcrglobwb_runs/baseline_historical_incl_additional_spinup/"
MAIN_TARGET_FOLDER="/archive/edwin/aqueduct_projects/pcrglobwb_runs/for_flood_analyzer/baseline_historical_incl_additional_spinup/pcrglobwb_runs_2016_oct_nov/tar_archive_edwinsut/"

bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime.tar ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave.tar  ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.tar                        ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.tar                        ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.tar                      ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.tar                    ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.tar                         ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.tar               ${MAIN_TARGET_FOLDER} &
wait

date
