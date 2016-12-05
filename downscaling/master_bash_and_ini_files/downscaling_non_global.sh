
# prepare the clone maps at high and low resolution (manual)
cp /projects/0/dfguu/data/hydroworld/others/05ArcMinCloneMaps/new_masks_from_top/*M17* .
gdalinfo clone_M17.map
mapattr -p clone_M17.map
mapattr -s -R 3960 -C 5040 -B -P yb2t -x 57 -y 38 -l 0.008333333333333333333333333333333333333333333333333333 clone_M17_30sec.map

# check clone maps
mapattr -p clone*.map
aguila clone*.map

read -rsp $'Press enter to continue...\n'


# resampling high resolution dem map
gdalwarp -tr 0.008333333333333333333333333333333333333333333333333333 0.008333333333333333333333333333333333333333333333333333 -te 57 5 99 38 /projects/0/dfguu/users/edwin/data/data_for_glofris_downscaling/input_data/maps_30sec/SRTM_1km_merge_gtopo_masked.map resampled_30sec_dem.tif
pcrcalc resampled_30sec_dem.map = "scalar(resampled_30sec_dem.tif)"
mapattr -c clone_M17_30sec.map resampled_30sec_dem.map
aguila resampled_30sec_dem.map

# resampling high resolution ldd map
gdalwarp -tr 0.008333333333333333333333333333333333333333333333333333 0.008333333333333333333333333333333333333333333333333333 -te 57 5 99 38 /projects/0/dfguu/users/edwin/data/data_for_glofris_downscaling/input_data/maps_30sec/worldHydroSHEDS.used.ldd.tif resampled_30sec_ldd.tif
pcrcalc resampled_30sec_ldd.map = "lddrepair(lddrepair(ldd(resampled_30sec_ldd.tif)))" 
mapattr -c clone_M17_30sec.map resampled_30sec_ldd.map
aguila resampled_30sec_ldd.map

# calculating high resolution stream order map
pcrcalc resampled_30sec_stream_order.map = "streamorder(resampled_30sec_ldd.map)"
aguila resampled_30sec_stream_order.map


# resampling low resolution ldd map
gdalwarp -tr 0.08333333333333333333333333333333333333333333333333333 0.08333333333333333333333333333333333333333333333333333 -te 57 5 99 38 /projects/0/dfguu/users/edwin/data/data_for_glofris_downscaling/input_data/maps_05min/lddsound_05min.tif resampled_05min_ldd.tif
pcrcalc resampled_05min_ldd.map = "lddrepair(lddrepair(ldd(resampled_05min_ldd.tif)))" 
mapattr -c clone_M17.map resampled_05min_ldd.map
aguila resampled_05min_ldd.map

# resampling all low resolution maps
resample --clone clone_M17.map /projects/0/dfguu/users/edwin/data/data_for_glofris_downscaling/input_data/maps_05min/cellsize05min.correct.map           resampled_05min_cellsize.map       &
resample --clone clone_M17.map /projects/0/dfguu/users/edwin/data/data_for_glofris_downscaling/input_data/maps_05min/bankfull_width.map                  resampled_05min_bankfull_width.map &
resample --clone clone_M17.map /projects/0/dfguu/users/edwin/data/data_for_glofris_downscaling/input_data/maps_05min/celldiagonal05min.map               resampled_05min_celldiagonal.map   &

# resampling flood volume maps
resample --clone clone_M17.map /scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/2-year_of_flood_innundation_volume.map    2-year_of_flood_innundation_volume.map &
resample --clone clone_M17.map /scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/5-year_of_flood_innundation_volume.map    5-year_of_flood_innundation_volume.map &
resample --clone clone_M17.map /scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/10-year_of_flood_innundation_volume.map   10-year_of_flood_innundation_volume.map &
resample --clone clone_M17.map /scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/25-year_of_flood_innundation_volume.map   25-year_of_flood_innundation_volume.map &
resample --clone clone_M17.map /scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/50-year_of_flood_innundation_volume.map   50-year_of_flood_innundation_volume.map &
resample --clone clone_M17.map /scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/100-year_of_flood_innundation_volume.map  100-year_of_flood_innundation_volume.map &
resample --clone clone_M17.map /scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/250-year_of_flood_innundation_volume.map  250-year_of_flood_innundation_volume.map &
resample --clone clone_M17.map /scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/500-year_of_flood_innundation_volume.map  500-year_of_flood_innundation_volume.map &
resample --clone clone_M17.map /scratch-shared/edwinsut/flood_analyzer_analysis/extreme_values/watch_1960-1999/1000-year_of_flood_innundation_volume.map 1000-year_of_flood_innundation_volume.map &

# make output_folder and copy HAND maps to the output_folder (if they are ready)

# run the downscaling scripts
python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py -i downscaling.ini -f 5-year_of_flood_innundation_volume.map    -b 2-year_of_flood_innundation_volume.map -c 4 -d output_folder
python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py -i downscaling.ini -f 10-year_of_flood_innundation_volume.map   -b 2-year_of_flood_innundation_volume.map -c 4 -d output_folder
python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py -i downscaling.ini -f 25-year_of_flood_innundation_volume.map   -b 2-year_of_flood_innundation_volume.map -c 4 -d output_folder 
python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py -i downscaling.ini -f 50-year_of_flood_innundation_volume.map   -b 2-year_of_flood_innundation_volume.map -c 4 -d output_folder
python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py -i downscaling.ini -f 100-year_of_flood_innundation_volume.map  -b 2-year_of_flood_innundation_volume.map -c 4 -d output_folder
python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py -i downscaling.ini -f 250-year_of_flood_innundation_volume.map  -b 2-year_of_flood_innundation_volume.map -c 4 -d output_folder
python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py -i downscaling.ini -f 500-year_of_flood_innundation_volume.map  -b 2-year_of_flood_innundation_volume.map -c 4 -d output_folder
python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py -i downscaling.ini -f 1000-year_of_flood_innundation_volume.map -b 2-year_of_flood_innundation_volume.map -c 4 -d output_folder

