set -x

# making the landmask map for inundation downscaling

cd /scratch-shared/edwinsut/clone_for_extreme_value_analysis/

rm -r landmask_downscaling
mkdir landmask_downscaling
cd landmask_downscaling

# resample landmask of extreme value analysis to 5 arcmin resolution
cp /projects/0/dfguu/users/edwinhs/data/HydroSHEDS/hydro_basin_without_lakes/integrating_ldd/version_9_december_2016/merged_ldd.map merged_ldd_30sec.map
gdalwarp -tr 0.00833333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333 0.00833333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333 ../landmask_extreme_value_analysis/landmask_extreme_value_analysis_05min.tif landmask_extreme_value_analysis_05min_30sec.tif landmask_extreme_value_analysis_05min_30sec.map
gdal_translate -of PCRaster landmask_extreme_value_analysis_05min_30sec.tif landmask_extreme_value_analysis_05min_30sec.map
mapattr -c merged_ldd_30sec.map landmask_extreme_value_analysis_05min_30sec.map
mapattr -p *.map
aguila landmask_extreme_value_analysis_05min_30sec.map

# identify all river basins
pcrcalc catchment_merged_ldd_30sec.map = "catchment(merged_ldd_30sec.map, pit(merged_ldd_30sec.map))"
aguila catchment_merged_ldd_30sec.map

# identify river basins with extreme value analysis - this will be the landmask for the downscaling process
pcrcalc areatotal_scalar_landmask_extreme_value_analysis_catchment_merged_ldd_30sec.map = "areatotal(cover(scalar(landmask_extreme_value_analysis_05min_30sec.map), 0.0), catchment_merged_ldd_30sec.map)"
aguila areatotal_scalar_landmask_extreme_value_analysis_catchment_merged_ldd_30sec.map
pcrcalc landmask_downscaling_30sec.map = "if(areatotal_scalar_landmask_extreme_value_analysis_catchment_merged_ldd_30sec.map gt 0, boolean(1.0))"
aguila landmask_downscaling_30sec.map
