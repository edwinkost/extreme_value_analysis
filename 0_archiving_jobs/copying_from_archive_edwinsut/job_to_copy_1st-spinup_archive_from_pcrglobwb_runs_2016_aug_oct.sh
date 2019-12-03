#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00 
#SBATCH -p staging

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH -J copy_1st-spinup_archive_from_pcrglobwb_runs_2016_aug_oct

date

MAIN_SOURCE_FOLDER="/archive/edwinsut/aqueduct_flood_analyzer/pcrglobwb_runs/1st_spinup/"
MAIN_TARGET_FOLDER="/archive/edwin/aqueduct_projects/pcrglobwb_runs/for_flood_analyzer/1st-spinup/spinup_from_pcrglobwb_runs_2016_aug_oct/tar_archive_edwinsut/"

bash copying_from_archive_edwinsut.sh ${MAIN_SOURCE_FOLDER} spinup_from_pcrglobwb_runs_2016_aug_oct.tar ${MAIN_TARGET_FOLDER}

date
