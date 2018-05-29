set -x 
pwd

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_05_29_structured_as_version_2017_05_XX/
mkdir ${TARGET_FOLDER}

# make the directory structure as (/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_02_XX_structured_as_version_2017_05_XX/)
cd /projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2018_02_XX_structured_as_version_2017_05_XX/
find . -type d > ${TARGET_FOLDER}//directory_structure_as_version_2017_05_XX.txt
cd ${TARGET_FOLDER}
xargs mkdir -p < dirs.txt

# uploading/making links for the rcp2p6
cd /home/edwinsut/github/edwinkost/extreme_value_analysis/0_bash_scripts_version_2018_05_XX/0_uploading_results/
bash uploading_with_structure_as_version_2017_05_XX_rcp2p6_inundation.sh
