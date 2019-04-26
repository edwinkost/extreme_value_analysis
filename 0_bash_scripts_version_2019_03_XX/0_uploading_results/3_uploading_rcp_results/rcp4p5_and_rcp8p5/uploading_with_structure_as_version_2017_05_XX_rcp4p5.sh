
set -x 
pwd

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2019_03_XX_structured_as_version_2017_05_XX/

echo "rcp4p5"
# uploading/making links for the rcp4p5
bash uploading_with_structure_as_version_2017_05_XX_rcp4p5_inundation.sh
bash uploading_with_structure_as_version_2017_05_XX_rcp4p5_water_level.sh

set +x


