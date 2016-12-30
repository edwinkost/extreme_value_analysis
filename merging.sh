
# change the permission
chmod -R a-w *

# make the "merged" folder target
mkdir merged_2006-2099

# merging 
cdo mergetime begin_from_2006/global/netcdf/channelStorage_monthMax_output*.nc continue_from_*/global/netcdf/channelStorage_monthMax_output*.nc merged_2006-2099/channelStorage_monthMax_output_2006-01-31_to_2099-12-31.nc &
cdo mergetime begin_from_2006/global/netcdf/discharge_monthAvg_output*.nc continue_from_*/global/netcdf/discharge_monthAvg_output*.nc merged_2006-2099/discharge_monthAvg_output_2006-01-31_to_2099-12-31.nc &
cdo mergetime begin_from_2006/global/netcdf/dynamicFracWat_monthMax_output*.nc continue_from_*/global/netcdf/dynamicFracWat_monthMax*.nc merged_2006-2099/dynamicFracWat_monthMax_output_2006-01-31_to_2099-12-31.nc &
cdo mergetime begin_from_2006/global/netcdf/floodDepth_monthMax_output*.nc continue_from_*/global/netcdf/floodDepth_monthMax_output*.nc merged_2006-2099/floodDepth_monthMax_output_2006-01-31_to_2099-12-31.nc &
cdo mergetime begin_from_2006/global/netcdf/floodVolume_monthMax_output*.nc continue_from_*/global/netcdf/floodVolume_monthMax_output*.nc merged_2006-2099/floodVolume_monthMax_output_2006-01-31_to_2099-12-31.nc &
cdo mergetime begin_from_2006/global/netcdf/surfaceWaterLevel_monthMax_output*.nc continue_from_*/global/netcdf/surfaceWaterLevel_monthMax_output*.nc merged_2006-2099/surfaceWaterLevel_monthMax_output_2006-01-31_to_2099-12-31.nc &
wait

# test using ncview (there must be 1128 timesteps)
ncview merged_2006-2099/*.nc
