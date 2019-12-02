#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00 
#SBATCH -p staging

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH -J 1st-spinup_archive_from_pcrglobwb_runs_2016_aug_oct
#SBATCH --nodelist=srv5

set -x 

module load p7zip

# go to the correct folder where the script is stored
cd /home/edwin/github/edwinkost/extreme_value_analysis/0_archiving_jobs/

# preparing the target directory and go there
mkdir -p /archive/edwin/aqueduct_projects/pcrglobwb_runs/for_flood_analyzer/1st-spinup/spinup_from_pcrglobwb_runs_2016_aug_oct/
cd /archive/edwin/aqueduct_projects/pcrglobwb_runs/for_flood_analyzer/1st-spinup/spinup_from_pcrglobwb_runs_2016_aug_oct/

# archiving 
7za a pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z           /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_aug_oct/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m          &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z           /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_aug_oct/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es          &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z         /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_aug_oct/pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr        &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z       /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_aug_oct/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem      &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z            /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_aug_oct/pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m           &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.7z  /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_aug_oct/pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave &
wait

# test archive
7za l pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z           > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z           > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z         > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z       > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z            > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.7z  > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.txt

set +x

