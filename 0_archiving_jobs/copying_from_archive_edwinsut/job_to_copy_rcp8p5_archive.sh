#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00 
#SBATCH -p staging

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH -J copy_rcp8p5_archive

date

MAIN_SOURCE_FOLDER="/archive/edwinsut/aqueduct_flood_analyzer/pcrglobwb_runs/rcp8p5/"
MAIN_TARGET_FOLDER="/archive/edwin/aqueduct_projects/pcrglobwb_runs/for_flood_analyzer/rcp8p5/pcrglobwb_runs_2016_oct_nov/tar_archive_edwinsut/"

bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.tar     ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.tar     ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.tar   ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.tar ${MAIN_TARGET_FOLDER} &
bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.tar      ${MAIN_TARGET_FOLDER} &
wait

date
