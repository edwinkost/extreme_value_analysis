#!/usr/bin/python
# -*- coding: utf-8 -*-

# dictionary for netcdf file names, variable names and units: 
netcdf_short_name         = {}
netcdf_unit               = {}
netcdf_monthly_total_unit = {} 
netcdf_yearly_total_unit  = {}
netcdf_long_name          = {}
description               = {}
comment                   = {}
latex_symbol              = {}
pcr_short_name            = {}     

# channelStorage 
pcrglobwb_variable_name = 'channelStorage'
netcdf_short_name[pcrglobwb_variable_name] = 'channel_storage'
netcdf_unit[pcrglobwb_variable_name]       = 'm3'
netcdf_monthly_total_unit[pcrglobwb_variable_name] = None 
netcdf_yearly_total_unit[pcrglobwb_variable_name]  = None
netcdf_long_name[pcrglobwb_variable_name]  = 'channel_storage'
description[pcrglobwb_variable_name]       = None
comment[pcrglobwb_variable_name]           = None
latex_symbol[pcrglobwb_variable_name]      = None

# floodVolume
pcrglobwb_variable_name = 'floodVolume'
netcdf_short_name[pcrglobwb_variable_name] = 'flood_inundation_volume'
netcdf_unit[pcrglobwb_variable_name]       = 'm3'
netcdf_monthly_total_unit[pcrglobwb_variable_name] = None 
netcdf_yearly_total_unit[pcrglobwb_variable_name]  = None
netcdf_long_name[pcrglobwb_variable_name]  = 'flood_inundation_volume'
description[pcrglobwb_variable_name]       = None
comment[pcrglobwb_variable_name]           = 'Flood inundation volume above the channel storage capacity. Not including flood overtopping reservoirs and lakes.'
latex_symbol[pcrglobwb_variable_name]      = None

# fraction_of_surface_water
pcrglobwb_variable_name = 'dynamicFracWat'
netcdf_short_name[pcrglobwb_variable_name] = 'fraction_of_surface_water'
netcdf_unit[pcrglobwb_variable_name]       = '1'
netcdf_monthly_total_unit[pcrglobwb_variable_name] = None 
netcdf_yearly_total_unit[pcrglobwb_variable_name]  = None
netcdf_long_name[pcrglobwb_variable_name]  = 'fraction_of_surface_water'
description[pcrglobwb_variable_name]       = None
comment[pcrglobwb_variable_name]           = 'Fraction of surface water over the cell area.'
latex_symbol[pcrglobwb_variable_name]      = None

# surfaceWaterLevel
pcrglobwb_variable_name = 'surfaceWaterLevel'
netcdf_short_name[pcrglobwb_variable_name] = 'surface_water_level'
netcdf_unit[pcrglobwb_variable_name]       = 'm'
netcdf_monthly_total_unit[pcrglobwb_variable_name] = None 
netcdf_yearly_total_unit[pcrglobwb_variable_name]  = None
netcdf_long_name[pcrglobwb_variable_name]  = 'surface_water_level'
description[pcrglobwb_variable_name]       = None
comment[pcrglobwb_variable_name]           = 'Estimate of surface/river water levels within surface water bodies (above channel bottom elevations).'
latex_symbol[pcrglobwb_variable_name]      = None

# floodDepth
pcrglobwb_variable_name = 'floodDepth'
netcdf_short_name[pcrglobwb_variable_name] = 'flood_inundation_depth'
netcdf_unit[pcrglobwb_variable_name]       = 'm'
netcdf_monthly_total_unit[pcrglobwb_variable_name] = None 
netcdf_yearly_total_unit[pcrglobwb_variable_name]  = None
netcdf_long_name[pcrglobwb_variable_name]  = None
description[pcrglobwb_variable_name]       = None
comment[pcrglobwb_variable_name]           = 'Flood inundation depth above the channel flood plain. Not including flood overtopping reservoirs and lakes.'
latex_symbol[pcrglobwb_variable_name]      = None

