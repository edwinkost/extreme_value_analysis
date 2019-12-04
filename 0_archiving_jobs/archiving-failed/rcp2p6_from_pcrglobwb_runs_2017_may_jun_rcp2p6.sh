#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00 
#SBATCH -p staging

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH -J rcp2p6_from_pcrglobwb_runs_2017_may_jun_rcp2p6
#SBATCH --nodelist=srv2

set -x 

module load p7zip

# go to the correct folder where the script is stored
cd /home/edwin/github/edwinkost/extreme_value_analysis/0_archiving_jobs/

# preparing the target directory and go there
TARGET_FOLDER="/archive/edwin/aqueduct_projects/pcrglobwb_runs/for_flood_analyzer/rcp2p6/pcrglobwb_runs_2017_may_jun_rcp2p6/"
mkdir -p ${TARGET_FOLDER}
cd ${TARGET_FOLDER}

#~ edwin@srv5.bullx:/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_may_jun_rcp2p6$ ls -lah  
#~ total 36K
#~ drwxr-sr-x  7 edwinsut aqueduct 4.0K Dec  1  2018 .
#~ drwxr-sr-x 18 edwinsut aqueduct 4.0K Nov 29 23:46 ..
#~ -rw-r--r--  1 edwinsut aqueduct 2.9K Dec  1  2018 merging.sh
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m
#~ -rw-r--r--  1 edwinsut aqueduct 1.3K Dec  1  2018 tar_rcp2p6.sh

# archiving 
7za a pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z                         /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_may_jun_rcp2p6/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m     &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z                         /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_may_jun_rcp2p6/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es     &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z                       /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_may_jun_rcp2p6/pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr   &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z                     /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_may_jun_rcp2p6/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z                          /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2017_may_jun_rcp2p6/pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m      &
wait

# test archive
7za l pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z     > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z    
7za l pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z     > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z    
7za l pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z   > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z  
7za l pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z
7za l pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z      > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z     

set +x

