# -*- coding: utf-8 -*-
"""
Created on Wed Feb 09 12:54:16 2011

post_proc.py - post_processes 30-year fldd and fldf results into hazard maps

  More detailed description goes here.

 Copyright notice
  --------------------------------------------------------------------
  Copyright (C) 2011 Deltares
      H.C. (Hessel) Winsemius

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

$Id: post_proc.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/post_proc.py $
$Keywords: $

"""

from numpy import *
from scipy import *
from netCDF4 import *
from csv import *
from GLOFRIS_utils import *
import time
from datetime import datetime, timedelta

def extremeVals(sourceFiles, statisticFile, caseName, logger):
    # create netCDF statistic file
    logger.info('Creating new statistics netCDF file "' + statisticFile + '"')
    rootgrp = Dataset(statisticFile,'w',format='NETCDF3_CLASSIC')
    rootgrp.title       = 'Flooded fraction/flooded depth annual extremes, IMAGE scenario: ' + caseName
    rootgrp.comment     = 'File was created from PCRGLOB-WB run ' + caseName + ', generated with post_proc.py'
    rootgrp.institution = 'Deltares/PBL'
    rootgrp.source      = 'CRU/ERA40; IMAGE 2.4'
    rootgrp.history     = 'Last edited ' + time.ctime(time.time())
    rootgrp.createDimension("time", 0)
    rootgrp.createDimension("latitude", 360)
    rootgrp.createDimension("longitude", 720)
    # Create variables
    DateHour = rootgrp.createVariable('time','f8',('time',))
    DateHour.units = 'days since 1970-01-01 00:00:00.0'
    DateHour.calendar = 'gregorian'
    DateHour.standard_name = 'time'
    DateHour.long_name = 'DaysSince1970-01-01_000000.0'
    lat = rootgrp.createVariable('latitude','f4',('latitude',))
    lat.standard_name = 'latitude'
    lat.long_name = 'Latitude values'
    lat.units = 'degrees_N'
    lon = rootgrp.createVariable('longitude','f4',('longitude',))
    lon.standard_name = 'longitude'
    lon.long_name = 'Longitude values'
    lon.units = 'degrees_E'
    lats = arange(89.75,-90,-0.5)
    lons = arange(-179.75,180,0.5)
    lat[:] = lats
    lon[:] = lons
    fldf_all = rootgrp.createVariable('Flooded_Fraction_max','f4',('time','latitude','longitude',),fill_value=-9999)
    fldf_all.standard_name = 'Flooded_Fraction_max'
    fldf_all.units = '-'
    fldd_all = rootgrp.createVariable('Flooded_Depth_max','f4',('time','latitude','longitude',),fill_value=-9999)
    fldd_all.standard_name = 'Flooded_Depth_max'
    fldd_all.units = 'm'

    for source in sourceFiles:
        year = int(os.path.split(source)[1][0:4])
        print 'Year: ' + str(year)
        Pos  = year-1961
        print 'Pos: ' + str(Pos)
        DateHour[Pos] = date2num(datetime(year,1,1,0),units=DateHour.units,calendar=DateHour.calendar)
        sourcegrp = Dataset(source,'r')
        fldf          = sourcegrp.variables['Flooded_Fraction']
        fldd          = sourcegrp.variables['Flooded_Depth']
        logger.info('Computing annual maxima from "' + source + '"')
        fldf_max      = fldf[:].max(0)
        fldf_min      = fldf[:].min(0)
        fldd_max      = fldd[:].max(0)
        fldd_min      = fldd[:].min(0)
        fldf_diff     = fldf_max-fldf_min
        fldd_diff     = fldd_max-fldd_min
        # save the annual minimum minus annual maximum
        fldf_all[Pos,:,:] = fldf_diff.data
        fldd_all[Pos,:,:] = fldd_diff.data
    # close netCDF file
    rootgrp.sync()
    rootgrp.close()
#
## TIME!!!
#
#
## Retrieve location from .ini configuration (NOT IMPLEMENTED!)
#sourceLoc     = './A1B/run_default/outmaps/'
#sourceFile    =  '1975_dynRout_flf_wh.nc'
#source        = os.path.join(sourceLoc,sourceFile)
#popMapFile    = 'baseMaps/GPOPDENS.asc'
#landAreaFile  = 'baseMaps/cellarea30.map'
#lon,lat,popMap,FillValpopMap             = readMap(popMapFile, 'AAIGrid')
#popMap[popMap==FillValpopMap]            = NaN
#
#lon,lat,landArea,FillVallandArea         = readMap(landAreaFile, 'PCRaster')
#landArea[landArea==FillVallandArea]      = NaN
#
## Some parameters
#rootgrp       = Dataset(source,'r')
#fldf          = rootgrp.variables['Flooded_Fraction']
#fldd          = rootgrp.variables['Flooded_Depth']
#
#fldf_max      = fldf[:].max(0)
#fldf_min      = fldf[:].min(0)
#fldd_max      = fldd[:].max(0)
#fldd_min      = fldd[:].min(0)
#
## fldf_maxvals  = fldf_max[:].raw_data
#fldf_diff     = fldf_max-fldf_min
#fldd_diff     = fldd_max-fldd_min
#
#fldf_diffvals = fldf_diff.data
#fldd_diffvals = fldd_diff.data ;
#
#writeMap('fldf_1975.asc', 'AAIGrid', lon, lat, flipud(fldf_diffvals), fldf_diff.fill_value)
#writeMap('fldd_1975.asc', 'AAIGrid', lon, lat, flipud(fldd_diffvals), fldd_diff.fill_value)
#
#fldd_diffvals[fldd_diffvals==fldd_diff.fill_value] = nan
#fldf_diffvals[fldf_diffvals==fldf_diff.fill_value] = nan
#
#i,j = where(fldd_diffvals < h_thres)
#fldf_diffvals[i,j] = 0
#
#lon,lat = meshgrid(arange(-179.75,180.,0.5),arange(89.75,-90,-0.5))
#lon = arange(-179.75,180.,0.5)
#lat = arange(-89.75,90,0.5)
#thread = fldf_diffvals*(maximum(fldd_diffvals-h_thres,0))*flipud(popMap*landArea)/1e6
## plot data
#plotGrid(lon,lat,minimum(fldf_diffvals,0.5),[-60, 84], [-180, 180], 'Inundation hazard [-]', 'plt.cm.BuPu', 'Flooded_fraction_example.pdf')
#plotGrid_log(lon,lat,log10(maximum(thread,0.0001)),[-60, 84], [-180, 180], 'Population threaded [cap * m depth]', 2, 8, 'plt.cm.Reds', array([3,4,5,6,7,8]), 'Capita_thread.pdf')
#
## Retrieve maximum and minimum values
## rootgrp.close()