# -*- coding: utf-8 -*-
"""
GLOFRIS.py contains several standard functions to be used in the GLOFRIS system

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

$Id: netCDF2UNF0.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/netCDF2UNF0.py $
$Keywords: $

"""

from numpy import *
import sys
import os
#import matplotlib.pyplot as plt
import logging
import netCDF4 as nc4
#from mpl_toolkits.basemap import Basemap, cm, NetCDFFile

#try:
ncIn = sys.argv[1]
varIn = sys.argv[2]
fileName = sys.argv[3]
worldncFile = sys.argv[4]

# read variable from netCDF
nc_src = Dataset(ncIn)
grid = nc_src.variables[varIn][:]
fillval = nc.variables[varIn]._FillValue
grid[grid==fillval] = nan
# Prepare final grid
LAT = arange(-89.75,90,0.5)
LON = arange(-179.75,180,0.5)
# now read the actual data and write to correct coordinate positions
dataFid = open(fileName, 'wb')

# Open the coordinate file fo grid definition and read!
coordFid = open(worldncFile, 'r')
# skip the 15-line header of the worldnc file
for n in arange(0,15):
    coordFid.readline()
allLines = coordFid.readlines()
nrOfPix  = len(allLines)
# determine amount of grids in UNF file
nrOfGrids = grid.shape[0]
print 'Writing number of grids in %s: %g' % (fileName, nrOfGrids)
# all coordinates read, close file
coordFid.close()
# now set up the grid
lon = zeros(len(allLines))
lat = zeros(len(allLines))
x   = zeros(lon.shape,dtype=int)
y   = zeros(lon.shape,dtype=int)
for count, linestr in zip(range(0,len(allLines)), allLines):
    line = linestr.split()
    lon[count] = 0.25 + float(line[0])
    lat[count] = 0.25 + float(line[1])
    y[count]   = round((lat[count]+89.75)/0.5)
    x[count]   = round((lon[count] - (-179.75))/0.5)

#    idx = where(map(lambda xx: xx in LON, x ))
#    idy = where(map(lambda yy: yy in LAT, y ))
for gridcell in arange(0,len(y)):
    data  = array(grid[:,y[gridcell],x[gridcell]],dtype='f4')
    data.tofile(dataFid)
# coordinates are now known and data appointed to them!!
# return LON, LAT, GRID
dataFid.flush()
dataFid.close()
#except:
#    print 'Somethin went wrong!! Usage: netCDF2UNF0 <netCDF-in> <variable> <fileOut> <worldncfile>'
