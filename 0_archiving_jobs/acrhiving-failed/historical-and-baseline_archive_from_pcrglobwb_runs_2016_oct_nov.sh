#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00 
#~ #SBATCH -p staging
#SBATCH -p normal

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH -J hist-base_archive_from_pcrglobwb_runs_2016_oct_nov
#~ #SBATCH --nodelist=srv1

set -x 

module load p7zip

# go to the correct folder where the script is stored
cd /home/edwin/github/edwinkost/extreme_value_analysis/0_archiving_jobs/

# preparing the target directory and go there
TARGET_FOLDER="/archive/edwin/aqueduct_projects/pcrglobwb_runs/for_flood_analyzer/baseline_historical_incl_additional_spinup/pcrglobwb_runs_2016_oct_nov/"
TARGET_FOLDER="/projects/0/wtrcycle/users/edwin/temporary_aqueduct/baseline_historical_incl_additional_spinup/pcrglobwb_runs_2016_oct_nov/"
mkdir -p ${TARGET_FOLDER}
cd ${TARGET_FOLDER}

# archiving 
7za a pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime.7z  /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave.7z   /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave  &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z                         /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m                        &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z                         /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es                        &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z                       /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr                      &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z                     /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem                    &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z                          /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m                         &
7za a pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.7z                /projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave               &
wait

# test archive
7za l pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime.7z > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime.7z  
7za l pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave.7z  > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave.7z   
7za l pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z                        > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z                         
7za l pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z                        > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z                         
7za l pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z                      > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z                       
7za l pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z                    > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z                     
7za l pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z                         > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z                          
7za l pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.7z               > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.7z                


set +x

