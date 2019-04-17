
set -x

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2019_03_XX_structured_as_version_2017_05_XX/
mkdir -p ${TARGET_FOLDER}

# make the directory structure as (/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_02_XX_structured_as_version_2017_05_XX/)
cd /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_02_XX_structured_as_version_2017_05_XX/
find . -type d > ${TARGET_FOLDER}//directory_structure_as_version_2017_05_XX.txt
cd ${TARGET_FOLDER}
xargs mkdir -p < directory_structure_as_version_2017_05_XX.txt

set +x
