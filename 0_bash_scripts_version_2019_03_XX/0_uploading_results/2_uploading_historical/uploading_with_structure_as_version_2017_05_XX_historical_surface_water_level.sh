set -x 
pwd
	

SOURCE_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2019_03_XX/river/surface_water_level_05min/historical/1960-1999/WATCH

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2019_03_XX_structured_as_version_2017_05_XX/river/surface_water_level/historical/1960-1999/
cd ${TARGET_FOLDER}

# remove the "WATCH" folder as it will be replaced with a link
rm -r WATCH

# make the link
ln -s ${SOURCE_FOLDER} WATCH
	
