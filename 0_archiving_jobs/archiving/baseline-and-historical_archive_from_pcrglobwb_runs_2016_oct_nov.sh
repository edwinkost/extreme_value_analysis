#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00 
#SBATCH -p normal

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH -J baseline-and-historical_archive_from_pcrglobwb_runs_2016_aug_oct

TARGET_DIRECTORY="/projects/0/wtrcycle/users/edwinhs/temporary_aqueduct/baseline_historical_incl_additional_spinup/pcrglobwb_runs_2016_oct_nov/"
SOURCE_DIRECTORY="/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/"

#~ edwinhs@tcn700.bullx:/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov$ ls -lah
#~ total 52K
#~ drwxr-sr-x 10 edwinsut aqueduct 4.0K Dec  1  2018 .
#~ drwxr-sr-x 18 edwinsut aqueduct 4.0K Nov 29 23:46 ..
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m
#~ drwxr-sr-x  3 edwinsut aqueduct 4.0K Dec  1  2018 pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave
#~ -rw-r--r--  1 edwinsut aqueduct 2.3K Dec  1  2018 tar_historical_and_baseline.sh
#~ -rw-r--r--  1 edwinsut aqueduct 2.5K Dec  1  2018 tar_rcp4p5_and_rcp8p5.sh
#~ -rw-r--r--  1 edwinsut aqueduct 1.3K Dec  1  2018 tar_rcp4p5_only.sh

set -x 

module load p7zip

# preparing the target directory
mkdir -p ${TARGET_DIRECTORY}

# archiving 
cd ${SOURCE_DIRECTORY}
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime.7z pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime/no_correction/n* &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave.7z  pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave/no_correction/n*  &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z                        pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m/no_correction/n*                        &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z                        pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es/no_correction/n*                        &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z                      pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr/no_correction/n*                      &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z                    pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem/no_correction/n*                    &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z                         pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m/no_correction/n*                         &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.7z               pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave/no_correction/n*               &
wait

# test archive
cd ${TARGET_DIRECTORY}
7za l pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime.7z > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_accutraveltime.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave.7z  > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_cru-ts3.23_era-20c_kinematicwave.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z                        > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z                        > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z                      > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z                    > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z                         > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.7z               > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.txt

set +x

