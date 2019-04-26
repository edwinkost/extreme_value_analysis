
set -x 
pwd


RCP_CODE=rcp2p6

SOURCE_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2019_03_XX/river/surface_water_level_05min/${RCP_CODE}/

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2019_03_XX_structured_as_version_2017_05_XX/river/surface_water_level/${RCP_CODE}/
cd ${TARGET_FOLDER}

# remove the all folders within the TARGET_FOLDER as they will be replaced with links
rm -r *

# copy an important read me file
cd -
cp -r important_read_me_for_2050-2099.txt ${TARGET_FOLDER}

# NOTE that we used the link/folder "2050-2099" to store the values for the time period 2060-2099 (2080 as its mid year), see the file important_read_me_for_2050-2099.txt. 

cd ${TARGET_FOLDER}

ln -s ${SOURCE_FOLDER}/2010-2049 2010-2049
ln -s ${SOURCE_FOLDER}/2030-2069 2030-2069
ln -s ${SOURCE_FOLDER}/2060-2099 2050-2099
                                             
set +x

