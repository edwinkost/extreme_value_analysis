
# PS: There are no changes in the historical output, from the versions 2018_05_29 to 2019_03_XX.

set -x

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2019_03_XX/river/surface_water_level_05min

cp -rf uploading_surface_water_level_historical.sh ${TARGET_FOLDER}
cd ${TARGET_FOLDER}

cp -r /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/surface_water_level_historical_000000000WATCH_1980_rp00002.nc         ${TARGET_FOLDER}/historical/1960-1999/WATCH///surface_water_level_historical_000000000WATCH_1980_rp00002.nc        
cp -r /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/surface_water_level_historical_000000000WATCH_1980_rp00005.nc         ${TARGET_FOLDER}/historical/1960-1999/WATCH///surface_water_level_historical_000000000WATCH_1980_rp00005.nc        
cp -r /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/surface_water_level_historical_000000000WATCH_1980_rp00010.nc         ${TARGET_FOLDER}/historical/1960-1999/WATCH///surface_water_level_historical_000000000WATCH_1980_rp00010.nc        
cp -r /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/surface_water_level_historical_000000000WATCH_1980_rp00025.nc         ${TARGET_FOLDER}/historical/1960-1999/WATCH///surface_water_level_historical_000000000WATCH_1980_rp00025.nc        
cp -r /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/surface_water_level_historical_000000000WATCH_1980_rp00050.nc         ${TARGET_FOLDER}/historical/1960-1999/WATCH///surface_water_level_historical_000000000WATCH_1980_rp00050.nc        
cp -r /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/surface_water_level_historical_000000000WATCH_1980_rp00100.nc         ${TARGET_FOLDER}/historical/1960-1999/WATCH///surface_water_level_historical_000000000WATCH_1980_rp00100.nc        
cp -r /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/surface_water_level_historical_000000000WATCH_1980_rp00250.nc         ${TARGET_FOLDER}/historical/1960-1999/WATCH///surface_water_level_historical_000000000WATCH_1980_rp00250.nc        
cp -r /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/surface_water_level_historical_000000000WATCH_1980_rp00500.nc         ${TARGET_FOLDER}/historical/1960-1999/WATCH///surface_water_level_historical_000000000WATCH_1980_rp00500.nc        
cp -r /projects/0/aqueduct/users/edwinsut/flood_analyzer_analysis_2018_05_XX/historical/1960-1999/WATCH/extreme_values/surface_water_level/surface_water_level_historical_000000000WATCH_1980_rp01000.nc         ${TARGET_FOLDER}/historical/1960-1999/WATCH///surface_water_level_historical_000000000WATCH_1980_rp01000.nc        

cd -

set +x

