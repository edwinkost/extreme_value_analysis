
set -x

TARGET_FOLDER=/projects/0/aqueduct/users/edwinsut/aqueduct_flood_analyzer_results/version_2019_03_XX/river/surface_water_level_05min

cp -rf uploading_surface_water_level_rcp2p6_and_rcp8p5.sh ${TARGET_FOLDER}
cd ${TARGET_FOLDER}

SOURCE_FOLDER=/projects/0/dfguu/users/edwin/flood_analyzer_analysis_2019_03_XX/

echo "rcp2p6"
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00002.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00002.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00005.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00005.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00010.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00010.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00025.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00025.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00050.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00050.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00100.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00100.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00250.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00250.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00500.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp00500.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp01000.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2030_rp01000.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00002.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00002.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00005.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00005.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00010.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00010.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00025.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00025.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00050.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00050.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00100.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00100.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00250.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00250.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00500.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp00500.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp01000.nc            ${TARGET_FOLDER}/rcp2p6/2010-2049/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2030_rp01000.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00002.nc          ${TARGET_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00002.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00005.nc          ${TARGET_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00005.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00010.nc          ${TARGET_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00010.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00025.nc          ${TARGET_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00025.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00050.nc          ${TARGET_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00050.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00100.nc          ${TARGET_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00100.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00250.nc          ${TARGET_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00250.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00500.nc          ${TARGET_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp00500.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp01000.nc          ${TARGET_FOLDER}/rcp2p6/2010-2049/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2030_rp01000.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00002.nc        ${TARGET_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00002.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00005.nc        ${TARGET_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00005.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00010.nc        ${TARGET_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00010.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00025.nc        ${TARGET_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00025.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00050.nc        ${TARGET_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00050.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00100.nc        ${TARGET_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00100.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00250.nc        ${TARGET_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00250.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00500.nc        ${TARGET_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp00500.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp01000.nc        ${TARGET_FOLDER}/rcp2p6/2010-2049/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2030_rp01000.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00002.nc             ${TARGET_FOLDER}/rcp2p6/2010-2049/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00002.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00005.nc             ${TARGET_FOLDER}/rcp2p6/2010-2049/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00005.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00010.nc             ${TARGET_FOLDER}/rcp2p6/2010-2049/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00010.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00025.nc             ${TARGET_FOLDER}/rcp2p6/2010-2049/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00025.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00050.nc             ${TARGET_FOLDER}/rcp2p6/2010-2049/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00050.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00100.nc             ${TARGET_FOLDER}/rcp2p6/2010-2049/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00100.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00250.nc             ${TARGET_FOLDER}/rcp2p6/2010-2049/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00250.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00500.nc             ${TARGET_FOLDER}/rcp2p6/2010-2049/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2030_rp00500.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2010-2049/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2030_rp01000.nc             ${TARGET_FOLDER}/rcp2p6/2010-2049/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2030_rp01000.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00002.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00002.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00005.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00005.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00010.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00010.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00025.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00025.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00050.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00050.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00100.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00100.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00250.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00250.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00500.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp00500.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp01000.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2050_rp01000.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00002.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00002.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00005.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00005.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00010.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00010.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00025.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00025.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00050.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00050.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00100.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00100.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00250.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00250.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00500.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp00500.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp01000.nc            ${TARGET_FOLDER}/rcp2p6/2030-2069/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2050_rp01000.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00002.nc          ${TARGET_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00002.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00005.nc          ${TARGET_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00005.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00010.nc          ${TARGET_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00010.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00025.nc          ${TARGET_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00025.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00050.nc          ${TARGET_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00050.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00100.nc          ${TARGET_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00100.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00250.nc          ${TARGET_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00250.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00500.nc          ${TARGET_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp00500.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp01000.nc          ${TARGET_FOLDER}/rcp2p6/2030-2069/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2050_rp01000.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00002.nc        ${TARGET_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00002.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00005.nc        ${TARGET_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00005.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00010.nc        ${TARGET_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00010.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00025.nc        ${TARGET_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00025.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00050.nc        ${TARGET_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00050.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00100.nc        ${TARGET_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00100.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00250.nc        ${TARGET_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00250.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00500.nc        ${TARGET_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp00500.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp01000.nc        ${TARGET_FOLDER}/rcp2p6/2030-2069/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2050_rp01000.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00002.nc             ${TARGET_FOLDER}/rcp2p6/2030-2069/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00002.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00005.nc             ${TARGET_FOLDER}/rcp2p6/2030-2069/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00005.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00010.nc             ${TARGET_FOLDER}/rcp2p6/2030-2069/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00010.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00025.nc             ${TARGET_FOLDER}/rcp2p6/2030-2069/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00025.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00050.nc             ${TARGET_FOLDER}/rcp2p6/2030-2069/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00050.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00100.nc             ${TARGET_FOLDER}/rcp2p6/2030-2069/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00100.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00250.nc             ${TARGET_FOLDER}/rcp2p6/2030-2069/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00250.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00500.nc             ${TARGET_FOLDER}/rcp2p6/2030-2069/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2050_rp00500.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2030-2069/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2050_rp01000.nc             ${TARGET_FOLDER}/rcp2p6/2030-2069/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2050_rp01000.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00002.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00002.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00005.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00005.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00010.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00010.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00025.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00025.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00050.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00050.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00100.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00100.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00250.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00250.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00500.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp00500.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp01000.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/GFDL-ESM2M///surface_water_level_rcp2p6_0000GFDL-ESM2M_2080_rp01000.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00002.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00002.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00005.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00005.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00010.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00010.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00025.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00025.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00050.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00050.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00100.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00100.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00250.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00250.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00500.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp00500.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES/extreme_values/surface_water_level/surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp01000.nc            ${TARGET_FOLDER}/rcp2p6/2060-2099/HadGEM2-ES///surface_water_level_rcp2p6_0000HadGEM2-ES_2080_rp01000.nc           
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00002.nc          ${TARGET_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00002.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00005.nc          ${TARGET_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00005.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00010.nc          ${TARGET_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00010.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00025.nc          ${TARGET_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00025.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00050.nc          ${TARGET_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00050.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00100.nc          ${TARGET_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00100.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00250.nc          ${TARGET_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00250.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00500.nc          ${TARGET_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp00500.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR/extreme_values/surface_water_level/surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp01000.nc          ${TARGET_FOLDER}/rcp2p6/2060-2099/IPSL-CM5A-LR///surface_water_level_rcp2p6_00IPSL-CM5A-LR_2080_rp01000.nc         
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00002.nc        ${TARGET_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00002.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00005.nc        ${TARGET_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00005.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00010.nc        ${TARGET_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00010.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00025.nc        ${TARGET_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00025.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00050.nc        ${TARGET_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00050.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00100.nc        ${TARGET_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00100.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00250.nc        ${TARGET_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00250.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00500.nc        ${TARGET_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp00500.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM/extreme_values/surface_water_level/surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp01000.nc        ${TARGET_FOLDER}/rcp2p6/2060-2099/MIROC-ESM-CHEM///surface_water_level_rcp2p6_MIROC-ESM-CHEM_2080_rp01000.nc       
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00002.nc             ${TARGET_FOLDER}/rcp2p6/2060-2099/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00002.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00005.nc             ${TARGET_FOLDER}/rcp2p6/2060-2099/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00005.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00010.nc             ${TARGET_FOLDER}/rcp2p6/2060-2099/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00010.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00025.nc             ${TARGET_FOLDER}/rcp2p6/2060-2099/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00025.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00050.nc             ${TARGET_FOLDER}/rcp2p6/2060-2099/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00050.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00100.nc             ${TARGET_FOLDER}/rcp2p6/2060-2099/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00100.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00250.nc             ${TARGET_FOLDER}/rcp2p6/2060-2099/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00250.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00500.nc             ${TARGET_FOLDER}/rcp2p6/2060-2099/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2080_rp00500.nc            
cp -r ${SOURCE_FOLDER}/rcp2p6/2060-2099/NorESM1-M/extreme_values/surface_water_level/surface_water_level_rcp2p6_00000NorESM1-M_2080_rp01000.nc             ${TARGET_FOLDER}/rcp2p6/2060-2099/NorESM1-M///surface_water_level_rcp2p6_00000NorESM1-M_2080_rp01000.nc            

set +x
