
# prepare the clone maps at high and low resolution (manual)

# check gdalinfo of both clone maps at high and low resolution (manuals)

# check clone maps
aguila clone*.map

read -rsp $'Press enter to continue...\n'


# resampling high resolution dem map
gdalwarp -tr 0.008333333333333333333333333333333333333333333333333333 0.008333333333333333333333333333333333333333333333333333 -te 57 5 99 38 ../input_data/maps_30sec/SRTM_1km_merge_gtopo_masked.map resampled_30sec_dem.tif
pcrcalc resampled_30sec_dem.map = "scalar(resampled_30sec_dem.tif)"
mapattr -c clone_M17_30sec.map resampled_30sec_dem.map
aguila resampled_30sec_dem.map

# resampling high resolution stream order map
gdalwarp -tr 0.008333333333333333333333333333333333333333333333333333 0.008333333333333333333333333333333333333333333333333333 -te 57 5 99 38 ../input_data/maps_30sec/stream_order_worldHydroSHEDS.used.map resampled_30sec_stream_order.tif
pcrcalc resampled_30sec_stream_order.map = "nominal(resampled_30sec_stream_order.tif)"
mapattr -c clone_M17_30sec.map resampled_30sec_stream_order.map
aguila resampled_30sec_stream_order.map

# resampling high resolution ldd map
gdalwarp -tr 0.008333333333333333333333333333333333333333333333333333 0.008333333333333333333333333333333333333333333333333333 -te 57 5 99 38 ../input_data/maps_30sec/worldHydroSHEDS.used.ldd.tif resampled_30sec_ldd.tif
pcrcalc resampled_30sec_ldd.map = "lddrepair(lddrepair(ldd(resampled_30sec_ldd.tif)))" 
aguila resampled_30sec_ldd.map

# calculating high resolution stream order map
pcrcalc resampled_30sec_stream_order.map = "streamorder(resampled_30sec_ldd.map)"
aguila resampled_30sec_stream_order.map


# resampling low resolution ldd map
gdalwarp -tr 0.08333333333333333333333333333333333333333333333333333 0.08333333333333333333333333333333333333333333333333333 -te 57 5 99 38 ../input_data/maps_05min/lddsound_05min.tif resampled_05min_ldd.tif
pcrcalc resampled_05min_ldd.map = "lddrepair(lddrepair(ldd(resampled_05min_ldd.tif)))" 
mapattr -c clone_M17.map resampled_05min_ldd.map
aguila resampled_05min_ldd.map

# resampling all low resolution maps
resample --clone clone_M17.map ../input_data/maps_05min/cellsize05min.correct.map                   resampled_05min_cellsize.map       &
resample --clone clone_M17.map ../input_data/maps_05min/bankfull_width.map                          resampled_05min_bankfull_width.map &
resample --clone clone_M17.map ../input_data/maps_05min/celldiagonal05min.map                       resampled_05min_celldiagonal.map   &

# resampling flood volume maps
resample --clone clone_M17.map ../pcrglobwb_output/timpctl_33.3_floodVolume_dailyTot_output_maximum_05min_1958_to_2010.map timpctl_33.3_floodVolume.map &
resample --clone clone_M17.map ../pcrglobwb_output/timpctl_50.0_floodVolume_dailyTot_output_maximum_05min_1958_to_2010.map timpctl_50.0_floodVolume.map &
resample --clone clone_M17.map ../pcrglobwb_output/timpctl_80.0_floodVolume_dailyTot_output_maximum_05min_1958_to_2010.map timpctl_80.0_floodVolume.map &
resample --clone clone_M17.map ../pcrglobwb_output/timpctl_90.0_floodVolume_dailyTot_output_maximum_05min_1958_to_2010.map timpctl_90.0_floodVolume.map &
resample --clone clone_M17.map ../pcrglobwb_output/timpctl_96.0_floodVolume_dailyTot_output_maximum_05min_1958_to_2010.map timpctl_96.0_floodVolume.map &
resample --clone clone_M17.map ../pcrglobwb_output/timpctl_98.0_floodVolume_dailyTot_output_maximum_05min_1958_to_2010.map timpctl_98.0_floodVolume.map &
resample --clone clone_M17.map ../pcrglobwb_output/timpctl_99.0_floodVolume_dailyTot_output_maximum_05min_1958_to_2010.map timpctl_99.0_floodVolume.map &
resample --clone clone_M17.map ../pcrglobwb_output/timpctl_99.6_floodVolume_dailyTot_output_maximum_05min_1958_to_2010.map timpctl_99.6_floodVolume.map &
resample --clone clone_M17.map ../pcrglobwb_output/timpctl_99.8_floodVolume_dailyTot_output_maximum_05min_1958_to_2010.map timpctl_99.8_floodVolume.map &
resample --clone clone_M17.map ../pcrglobwb_output/timpctl_99.9_floodVolume_dailyTot_output_maximum_05min_1958_to_2010.map timpctl_99.9_floodVolume.map


# run the downscaling script
python /home/edwin/github/edwinkost/wflow/wflow-py/Scripts/wflow_flood.py -i downsclaing.ini -f timpctl_99.9_floodVolume.map -b timpctl_33.3_floodVolume.map -c 4 -d timpctl_99.9_flood

