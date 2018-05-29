set -x 
pwd


RCP_CODE=rcp2p6

SOURCE_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_05_29/river/surface_water_level_05min/${RCP_CODE}/

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_05_29_structured_as_version_2017_05_XX/river/surface_water_level/${RCP_CODE}/
cd ${TARGET_FOLDER}

# copy an important read me file
cp -r /home/edwinsut/github/edwinkost/extreme_value_analysis/0_bash_scripts_version_2018_05_XX/0_uploading_results/important_read_me_for_2050-2099.txt ${TARGET_FOLDER}

# NOTE that we used the link/folder "2050-2099" to store the values for the time period 2060-2099 (2080 as its mid year), see the file important_read_me_for_2050-2099.txt. 

# remove the GCM_CODE folders as they will be replaced with links
rm -r */*

GCM_CODE=GFDL-ESM2M
ln -s ${SOURCE_FOLDER}/2010-2049/${GCM_CODE} 2010-2049/${GCM_CODE}
ln -s ${SOURCE_FOLDER}/2030-2069/${GCM_CODE} 2030-2069/${GCM_CODE}
ln -s ${SOURCE_FOLDER}/2060-2099/${GCM_CODE} 2050-2099/${GCM_CODE}
                                             
GCM_CODE=HadGEM2-ES                          
ln -s ${SOURCE_FOLDER}/2010-2049/${GCM_CODE} 2010-2049/${GCM_CODE}
ln -s ${SOURCE_FOLDER}/2030-2069/${GCM_CODE} 2030-2069/${GCM_CODE}
ln -s ${SOURCE_FOLDER}/2060-2099/${GCM_CODE} 2050-2099/${GCM_CODE}
                                             
GCM_CODE=IPSL-CM5A-LR                        
ln -s ${SOURCE_FOLDER}/2010-2049/${GCM_CODE} 2010-2049/${GCM_CODE}
ln -s ${SOURCE_FOLDER}/2030-2069/${GCM_CODE} 2030-2069/${GCM_CODE}
ln -s ${SOURCE_FOLDER}/2060-2099/${GCM_CODE} 2050-2099/${GCM_CODE}
                                             
GCM_CODE=MIROC-ESM-CHEM                      
ln -s ${SOURCE_FOLDER}/2010-2049/${GCM_CODE} 2010-2049/${GCM_CODE}
ln -s ${SOURCE_FOLDER}/2030-2069/${GCM_CODE} 2030-2069/${GCM_CODE}
ln -s ${SOURCE_FOLDER}/2060-2099/${GCM_CODE} 2050-2099/${GCM_CODE}
                                             
GCM_CODE=NorESM1-M                           
ln -s ${SOURCE_FOLDER}/2010-2049/${GCM_CODE} 2010-2049/${GCM_CODE}/
ln -s ${SOURCE_FOLDER}/2030-2069/${GCM_CODE} 2030-2069/${GCM_CODE}/
ln -s ${SOURCE_FOLDER}/2060-2099/${GCM_CODE} 2050-2099/${GCM_CODE}/
