#!/bin/bash
#SBATCH -N 1
#SBATCH -t 119:59:00 
#SBATCH -p normal

# mail alert at start, end and abortion of execution
#SBATCH --mail-type=ALL

# send mail to this address
#SBATCH --mail-user=edwinkost@gmail.com

#SBATCH -J rcp4p5_archive_from_pcrglobwb_runs_2016_oct_nov

TARGET_DIRECTORY="/projects/0/dfguu2/users/edwinhs/temporary_aqueduct/rcp4p5/pcrglobwb_runs_2016_oct_nov/"
SOURCE_DIRECTORY="/projects/0/aqueduct/users/edwinsut/pcrglobwb_runs_2016_oct_nov/"

set -x 

module load p7zip

# preparing the target directory
mkdir -p ${TARGET_DIRECTORY}

# archiving 
cd ${SOURCE_DIRECTORY}
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z                        pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m/no_correction/rcp4p5                        &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z                        pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es/no_correction/rcp4p5                        &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z                      pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr/no_correction/rcp4p5                      &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z                    pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem/no_correction/rcp4p5                    &
7za a ${TARGET_DIRECTORY}/pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z                         pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m/no_correction/rcp4p5                         &
wait

# test archive
cd ${TARGET_DIRECTORY}
7za l pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.7z                        > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_gfdl-esm2m.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.7z                        > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_hadgem2-es.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.7z                      > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_ipsl-cm5a-lr.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.7z                    > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_miroc-esm-chem.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.7z                         > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_noresm1-m.txt
7za l pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.7z               > list_7za-l_pcrglobwb_4_land_covers_edwin_parameter_set_watch_kinematicwave.txt

set +x

