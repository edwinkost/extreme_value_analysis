set -x 
pwd


RCP_CODE=rcp4p5

SOURCE_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_05_29/river/inundation_30sec/${RCP_CODE}/

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_05_29_structured_as_version_2017_05_XX/river/inundation/${RCP_CODE}/
cd ${TARGET_FOLDER}

# remove all "netcdf" folders as they will be replaced with links
rm -r */inundation_downscaled_from_bias_corrected_floods/*/global/netcdf

# copy an important read me file
cp -r /home/edwinsut/github/edwinkost/extreme_value_analysis/0_bash_scripts_version_2018_05_XX/0_uploading_results/important_read_me_for_2050-2099.txt ${TARGET_FOLDER}

# NOTE that we used the link/folder "2050-2099" to store the values for the time period 2060-2099 (2080 as its mid year), see the file important_read_me_for_2050-2099.txt. 

GCM_CODE=GFDL-ESM2M
ln -s ${SOURCE_FOLDER}/2010-2049/${GCM_CODE} 2010-2049/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
ln -s ${SOURCE_FOLDER}/2030-2069/${GCM_CODE} 2030-2069/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
ln -s ${SOURCE_FOLDER}/2060-2099/${GCM_CODE} 2050-2099/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf

GCM_CODE=HadGEM2-ES
ln -s ${SOURCE_FOLDER}/2010-2049/${GCM_CODE} 2010-2049/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
ln -s ${SOURCE_FOLDER}/2030-2069/${GCM_CODE} 2030-2069/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
ln -s ${SOURCE_FOLDER}/2060-2099/${GCM_CODE} 2050-2099/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf

GCM_CODE=IPSL-CM5A-LR
ln -s ${SOURCE_FOLDER}/2010-2049/${GCM_CODE} 2010-2049/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
ln -s ${SOURCE_FOLDER}/2030-2069/${GCM_CODE} 2030-2069/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
ln -s ${SOURCE_FOLDER}/2060-2099/${GCM_CODE} 2050-2099/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf

GCM_CODE=MIROC-ESM-CHEM
ln -s ${SOURCE_FOLDER}/2010-2049/${GCM_CODE} 2010-2049/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
ln -s ${SOURCE_FOLDER}/2030-2069/${GCM_CODE} 2030-2069/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
ln -s ${SOURCE_FOLDER}/2060-2099/${GCM_CODE} 2050-2099/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf

GCM_CODE=NorESM1-M
ln -s ${SOURCE_FOLDER}/2010-2049/${GCM_CODE} 2010-2049/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
ln -s ${SOURCE_FOLDER}/2030-2069/${GCM_CODE} 2030-2069/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
ln -s ${SOURCE_FOLDER}/2060-2099/${GCM_CODE} 2050-2099/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
