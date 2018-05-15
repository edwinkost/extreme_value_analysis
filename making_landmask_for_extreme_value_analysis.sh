set -x

# making the landmask map for extreme value analysis

cd /scratch-shared/edwinsut/clone_for_extreme_value_analysis/

rm -r landmask_extreme_value_analysis
mkdir landmask_extreme_value_analysis
cd landmask_extreme_value_analysis

# identify cells with forcing
gdal_translate -of PCRaster ../forcing_extent/pr_gfdl_1_jan_2006.nc  pr_gfdl_1_jan_2006.map
gdal_translate -of PCRaster ../forcing_extent/pr_watch_1_jan_1958.nc pr_watch_1_jan_1958.map
pcrcalc landmask_forcing.map = "if(if(defined(pr_gfdl_1_jan_2006.map), defined(pr_watch_1_jan_1958.map)), boolean(1.0))"
mapattr -p *.map
aguila landmask_forcing.map 

# resample landmask of forcing to 5 arcmin resolution
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map .
resample --clone lddsound_05min.map landmask_forcing.map landmask_forcing_05min.map 
mapattr -c lddsound_05min.map landmask_forcing_05min.map
mapattr -p *.map
aguila landmask_forcing*

# identify all river basins
pcrcalc catchment_lddsound_05min.map = "catchment(lddsound_05min.map, pit(lddsound_05min.map))"
aguila catchment_lddsound_05min.map

# identify river basins with forcing - this will be the landmask for the extreme value analysis
pcrcalc areatotal_scalar_landmask_forcing_catchment_lddsound_05min.map = "areatotal(cover(scalar(landmask_forcing_05min.map), 0.0), catchment_lddsound_05min.map)"
aguila areatotal_scalar_landmask_forcing_catchment_lddsound_05min.map
pcrcalc landmask_extreme_value_analysis_05min.map = "if(areatotal_scalar_landmask_forcing_catchment_lddsound_05min.map gt 0, boolean(1.0))"
aguila landmask_extreme_value_analysis_05min.map
