
set -x

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_05_29/

cp -rf directory_structure.txt ${TARGET_FOLDER}
cd ${TARGET_FOLDER}
xargs mkdir -p < directory_structure.txt

