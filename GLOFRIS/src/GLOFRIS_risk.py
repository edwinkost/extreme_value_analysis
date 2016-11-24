# -*- coding: utf-8 -*-
"""
GLOFRIS_postprocess.py contains a function to estimate 0.5x0.5 degree risk
of e.g. affected population or affected GDP.

  More detailed description goes here.

 Copyright notice
  --------------------------------------------------------------------
  Copyright (C) 2011 Deltares
      H.(Hessel) C. Winsemius

      hessel.winsemius@deltares.nl

      Rotterdamseweg 185
      Delft
      The Netherlands

  This function is free software under the PBL-Deltares MoU: redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation, either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library. If not, see <http://www.gnu.org/licenses/>.
  --------------------------------------------------------------------

This tools is part of <a href="http://GlobalFloods.Deltares.nl">Global floods Deltares</a>.
Global Floods is a PBL-Deltares project, that estimates flood risk indicators,
based on IMAGE scenario outputs and a global hydrological model PCR-GLOBWB

 Version <http://svnbook.red-bean.com/en/1.5/svn.advanced.props.special.keywords.html>
Created: 04 Nov 2010
Created and tested with python 2.6.5.4

$Id: GLOFRIS_risk.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/GLOFRIS_risk.py $
$Keywords: $

"""

from numpy import *
import logging
import netCDF4 as nc4
import logging.handlers
import datetime
import sys

def read_NetCDF_exposure(fileIn, varName, timePeriod):
    a = nc4.Dataset(fileIn, 'r')
    # read axis
    try:
        y = a.variables['lat']
    except:
        y = a.variables['latitude']
    # test for reverse axis
    if y[0] - y[1] > 0:
        axis_reverse = True
    else:
        axis_reverse = False
    var = a.variables[varName]
    timeDim = var.dimensions[0]
    time = a.variables[timeDim]
    dates = nc4.num2date(time[:],time.units,time.calendar)
    years = zeros(len(dates))
    for date, count in zip(dates, arange(0,len(dates))):
        years[count] = date.year
    idx = where(years==timePeriod)[0]
    grid = squeeze(var[idx,:,:])
    if hasattr(grid, 'mask'):
        grid = grid.data
    if isfinite(var._FillValue):
        grid[grid==var._FillValue] = nan
    if axis_reverse:
        grid = flipud(grid)

    # retrieve metadata
    attrs = a.ncattrs()
    glob_attr = {}
    for attr in attrs:
        glob_attr[attr] = a.getncattr(attr)
    attrs = var.ncattrs()
    var_attr  = {}
    for attr in attrs:
        var_attr[attr] = var.getncattr(attr)
    return grid, glob_attr, var_attr
    
    # retrieve grid from variables

def GLOFRIS_risk(fileIn, exposure, factor, startYear, endYear, logger):
    """
    GLOFRIS_postprocess converts hazard data from GLOFRIS NetCDF output statistics
    into a risk estimate
    """
    try:
        a = nc4.Dataset(fileIn,'r')
    except:
        logger.error('Statistics file "' + fileIn + '" not found. Please run the hydrology component first.')
        sys.exit(2)
    fldf_obj = a.variables['Flooded_Fraction_max']
    fldd_obj = a.variables['Flooded_Depth_max']
    t_num = a.variables['time']
    # find years
    years = []
    t_objs = nc4.num2date(t_num[:], units=t_num.units, calendar=t_num.calendar)
    for t_obj in t_objs:
        years.append(t_obj.year)
    years = array(years)
    # find the years of relevance for the end-user
    idx_all = where(logical_and(years >=startYear, years <= endYear))[0]
    # prepare risk array
    risk = zeros((fldf_obj.shape[1], fldf_obj.shape[2]))
    # process years
    for idx in idx_all:
        logger.info(str('Estimating risk in %4.f') % years[idx])
        fldd = fldd_obj[idx,:,:].data;fldd[fldd==fldd_obj._FillValue] = nan
        fldf = fldf_obj[idx,:,:].data;fldf[fldf==fldf_obj._FillValue] = nan
        risk += minimum(fldd*factor, 1)*fldf*exposure
    risk = risk/len(idx_all)
    
    missings = where(logical_and(isnan(fldf),isfinite(exposure)));
    risk[missings] = 0
    a.close()
    return risk

def write_risk_file(fileOut, varOut, grid, glob_attr, var_attr, timePeriod, FillVal, logger):
    y = arange(-89.75, 90, 0.5)
    x = arange(-179.75, 180, 0.5)
    nc = nc4.Dataset(fileOut,'w', format='NETCDF3_CLASSIC') # ,format='NETCDF3_CLASSIC'
    nc.createDimension('time', 0) #NrOfDays*8
    nc.createDimension('lat', len(y))
    nc.createDimension('lon', len(x))
    DateHour = nc.createVariable('time','f8',('time',))
    DateHour.units = 'days since 1970-01-01 00:00:00'
    DateHour.calendar = 'gregorian'
    DateHour.standard_name = 'time'
    DateHour.long_name = 'time'
    DateHour[0] = nc4.date2num(datetime.datetime(timePeriod, 1, 1, 0, 0), DateHour.units, DateHour.calendar)
    y_var = nc.createVariable('lat','f4',('lat',))
    y_var.standard_name = 'latitude'
    y_var.long_name = 'latitude'
    y_var.units = 'degrees_north'
    x_var = nc.createVariable('lon','f4',('lon',))
    x_var.standard_name = 'longitude'
    x_var.long_name = 'longitude'
    x_var.units = 'degrees_east'
    y_var[:] = y
    x_var[:] = x
    projection= nc.createVariable('projection','c')
    projection.long_name = 'wgs84'
    projection.EPSG_code = 'EPSG:4326'
    projection.proj4_params = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    projection.grid_mapping_name = 'latitude_longitude'

    # first add any metadata entry from the original file exported from FEWS
    for attr in glob_attr:
        nc.setncattr(attr,glob_attr[attr])
    # now prepare the variable of interest
    var = nc.createVariable(varOut,'f4',('time','lat','lon',),fill_value=FillVal)
    # now add all attributes from user-defined metadata
    for attr in var_attr:
        var.setncattr(attr,var_attr[attr])
    var[0,:,:] = grid
    nc.sync()
    nc.close()