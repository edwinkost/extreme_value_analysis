set -x 
pwd

RCP_CODE=rcp2p6

SOURCE_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_02_XX/river/inundation_30sec/${RCP_CODE}/

# NOTE that we used the folder name 2050-2099 to store the values for the time period 2060-2099 (2080 as its mid year), see the file important_read_me_for_2050-2099.txt. 

GCM_CODE=GFDL-ESM2M
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2010-2049/${GCM_CODE}/*.nc 2010-2049/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2030-2069/${GCM_CODE}/*.nc 2030-2069/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2060-2099/${GCM_CODE}/*.nc 2050-2099/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf

GCM_CODE=HadGEM2-ES
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2010-2049/${GCM_CODE}/*.nc 2010-2049/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2030-2069/${GCM_CODE}/*.nc 2030-2069/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2060-2099/${GCM_CODE}/*.nc 2050-2099/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf

GCM_CODE=IPSL-CM5A-LR
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2010-2049/${GCM_CODE}/*.nc 2010-2049/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2030-2069/${GCM_CODE}/*.nc 2030-2069/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2060-2099/${GCM_CODE}/*.nc 2050-2099/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf

GCM_CODE=MIROC-ESM-CHEM
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2010-2049/${GCM_CODE}/*.nc 2010-2049/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2030-2069/${GCM_CODE}/*.nc 2030-2069/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2060-2099/${GCM_CODE}/*.nc 2050-2099/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf

GCM_CODE=NorESM1-M
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2010-2049/${GCM_CODE}/*.nc 2010-2049/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2030-2069/${GCM_CODE}/*.nc 2030-2069/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
rsync --progress -h -r --size-only ${SOURCE_FOLDER}/2060-2099/${GCM_CODE}/*.nc 2050-2099/inundation_downscaled_from_bias_corrected_floods/${GCM_CODE}/global/netcdf
