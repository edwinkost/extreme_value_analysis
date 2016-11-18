
# - historical
cdo mergetime channelStorage_monthMax_output_*.nc    channelStorage_monthMax_output_1951-01-31_to_2005-12-31.nc &
cdo mergetime discharge_monthAvg_output_*.nc         discharge_monthAvg_output_1951-01-31_to_2005-12-31.nc &
cdo mergetime dynamicFracWat_monthMax_output_*.nc    dynamicFracWat_monthMax_output_1951-01-31_to_2005-12-31.nc &
cdo mergetime floodDepth_monthMax_output_*.nc        floodDepth_monthMax_output_1951-01-31_to_2005-12-31.nc &
cdo mergetime floodVolume_monthMax_output_*.nc       floodVolume_monthMax_output_1951-01-31_to_2005-12-31.nc &
cdo mergetime surfaceWaterLevel_monthMax_output_*.nc surfaceWaterLevel_monthMax_output_1951-01-31_to_2005-12-31.nc &
wait


# - climate/rcp
cdo mergetime channelStorage_monthMax_output_*.nc    channelStorage_monthMax_output_2000-01-31_to_2031-12-31.nc &
cdo mergetime discharge_monthAvg_output_*.nc         discharge_monthAvg_output_2000-01-31_to_2031-12-31.nc &
cdo mergetime dynamicFracWat_monthMax_output_*.nc    dynamicFracWat_monthMax_output_2000-01-31_to_2031-12-31.nc &
cdo mergetime floodDepth_monthMax_output_*.nc        floodDepth_monthMax_output_2000-01-31_to_2031-12-31.nc &
cdo mergetime floodVolume_monthMax_output_*.nc       floodVolume_monthMax_output_2000-01-31_to_2031-12-31.nc &
cdo mergetime surfaceWaterLevel_monthMax_output_*.nc surfaceWaterLevel_monthMax_output_2000-01-31_to_2031-12-31.nc &
wait

