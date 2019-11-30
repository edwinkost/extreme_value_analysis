
set -x

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2019_03_XX/

mkdir -p ${TARGET_FOLDER}

cp -rf directory_structure.txt ${TARGET_FOLDER}
cd ${TARGET_FOLDER}
xargs mkdir -p < directory_structure.txt

set +x
