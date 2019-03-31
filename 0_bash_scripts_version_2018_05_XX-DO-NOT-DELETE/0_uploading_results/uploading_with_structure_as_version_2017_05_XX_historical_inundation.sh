set -x 
pwd


SOURCE_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_05_29/river/inundation_30sec/historical/1960-1999/WATCH

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_05_29_structured_as_version_2017_05_XX/river/inundation/historical/inundation_downscaled/WATCH/1960-1999/global/
cd ${TARGET_FOLDER}

# remove the "netcdf" folder as it will be replaced with links
rm -r netcdf

# make the link
ln -s ${SOURCE_FOLDER} netcdf
