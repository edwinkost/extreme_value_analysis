"""
Created on Wed May 04 12:00:57 2011

conv_glcc.py
***************************************************************************************************
* This script converts a selected GLCC map (retrieved from http://edc2.usgs.gov/glcc/glcc.php)    *
* into fractional coverage maps at 0.5x0.5 degree resolution                                      *
* Script has been adapted from ArcGIS scripting "goge_par_rerun.py" by R. van Beek, Utrecht Univ. *
***************************************************************************************************

 Copyright notice
  --------------------------------------------------------------------
  Copyright (C) 2011 Deltares
      H.(Hessel Winsemius)

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

$Id: conv_glcc.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/tools/conv_glcc.py $
$Keywords: $
"""

from numpy import *
from scipy import *
#from struct import unpack
#import string
import sys,  os, os.path
#from gdalconst import *
#from ftplib import FTP
import time
#from datetime import datetime, timedelta
from netcdftime import *
from netCDF4_utils import *
from netCDF4 import *

# define constants
s_nrRows           = 21600    # number of lines in global GLCC lat-long file
s_nrCols           = 43200    # number of columns in global GLCC lat-long file
t_nrRows           = 360      # number of lines in global GLCC lat-long file
t_nrCols           = 720      # number of columns in global GLCC lat-long file
aggScale_x = s_nrCols/t_nrCols  # aggregation scale x-direction
aggScale_y = s_nrRows/t_nrRows  # aggregation scale x-direction

#def Gunzip(file):
#        '''Gunzip the given file.'''
#        r_file = gzip.GzipFile(file, 'rb')
#        write_file = string.rstrip(file, '.gz')
#        w_file = open(write_file, 'wb')
#        w_file.write(r_file.read())
#        w_file.close()
#        r_file.close()
#        os.unlink(file) # Yes this one too.

def conv_GLCC(FileName, varName, verbose):
    """ Convert GLCC global grid (0.008333 deg. resolution) to fractional land cover maps of 0.5 degrees
    Inputs:
        FileName        : The .img file that contains the unformatted global gridded 8-bit land cover class-map
        varName         : A list of variable names that represent the classes in the map in FileName
        verbose         : Boolean, either give output to screen or don't
    Outputs:
        fracMaps        : a float64 array (map-stack) of dimensions [lat,lon,number of classes+1]. 
                            Each map layer contains the fraction of the land cover type, 
                            belonging to land cover type 1 for layer 1, cover type 2 for layer 2, etc.
        maxFracMap      : an 8-bit integer array (map) of dimensions [lat,lon] containing for each pixel, the 
                            dominant land cover (i.e. with the highest fractional coverage)
    """
    # Create fraction arrays, the size of the number of classes available in the grid
    nrClasses = len(varName)
    fracMaps = zeros((t_nrRows,t_nrCols,nrClasses))
    maxFracMaps = zeros((t_nrRows,t_nrCols),dtype=uint8)
    # Open file for binary-reading
    file  = open(FileName,'rb')
    if verbose:
        print 'Reading from ' + FileName
    for row in arange(0, t_nrRows):
        print str((float(row)/t_nrRows)*100.) + '% done...'
        data = fromfile(file, dtype='>u1', count=aggScale_y*s_nrCols) # >u means single-byte unsigned integer, big-endian
        mat  = reshape(data, (aggScale_y,-1))
        for col in arange(0,t_nrCols):
            matSelect = mat[:,col*aggScale_x:(col+1)*aggScale_x]
            for Class in arange(0,nrClasses):
                
                fracMaps[row,col,Class] = float(shape(nonzero(matSelect==Class+1))[1])/float((aggScale_x*aggScale_y))
            # Find position of maximum value
            maxFracMaps[row,col] = nonzero(fracMaps[row,col,:]==fracMaps[row,col,:].max())[0][0]+1
    file.close()
    return fracMaps, maxFracMaps

def writeNC(FileName, fracMaps, maxFracMaps, varName, longName, title, origFile, verbose):
    rootgrp = Dataset(FileName,'w', format='NETCDF3_CLASSIC')
    #  Determine total amount of needed time steps
    # Create dimensions
    if verbose:
        print 'Setting up nc-file: ' + FileName
    rootgrp.createDimension("latitude", shape(fracMaps)[0])
    rootgrp.createDimension("longitude", shape(fracMaps)[1])
    # Create variables
    lat = rootgrp.createVariable('latitude','f4',('latitude',))
    lat.standard_name = 'latitude'
    lat.long_name = 'Latitude values'
    lon = rootgrp.createVariable('longitude','f4',('longitude',))
    lon.standard_name = 'longitude'
    lon.long_name = 'Longitude values'
    lat.units = 'degrees_N'
    lon.units = 'degrees_E'
	#Rain.units = '0.01mm/hr'
	#Rain._FillValue = -9999
	# Write data to NetCDF file
    lats = arange(89.75,-90,-0.5)
    lons = arange(-179.75,180,0.5)
    lat[:] = lats
    lon[:] = lons
###	Rain = rootgrp.createVariable('Rain','i2',('time','latitude','longitude',))
    # Set attributes
    if verbose:
        print 'Writing attributes'
    rootgrp.title = title
    rootgrp.institution = 'USGS'
    rootgrp.source = 'AVHRR NDVI data, collected in 1993-1994'
    rootgrp.references = origFile
    rootgrp.history = 'Created ' + time.ctime(time.time())
    rootgrp.source = 'Created by netCDF4-python, raw file obtained from http://edc2.usgs.gov/glcc/glcc.php'
    rootgrp.disclaimer = 'The timely delivery of these data and their quality is in no way guaranteed by Deltares'
    if verbose:
        print 'Writing fraction maps of each class:'
    for Class in arange(0,shape(fracMaps)[2]):
        if verbose:
            print 'Writing ' + longName[Class] + ' to ' + FileName
        var = rootgrp.createVariable(varName[Class],'f4',('latitude','longitude',))
        var.units = '-'
        var._FillValue = -9999
       	var.standard_name = varName[Class]
        var.long_name = longName[Class]
        var[:,:] = fracMaps[:,:,Class]
    # Finally write the map with maximum classes
    if verbose:
        print 'Writing maximum occurring land cover (variable maxCover) to ' + FileName
    var = rootgrp.createVariable('MAX_COVER','i2',('latitude','longitude',))
    var.units = '-'
    var._FillValue = -9999
    var.standard_name = 'MAX_COVER'
    var.long_name     = 'Maximum land cover occurring in pixel'
    var[:,:] = maxFracMaps
    rootgrp.sync()
    rootgrp.close()

def writeNC_simple(FileName, fracMaps, title, origFile, verbose):
    rootgrp = Dataset(FileName,'w', format='NETCDF3_CLASSIC')
    #  Determine total amount of needed time steps
    # Create dimensions
    if verbose:
        print 'Setting up nc-file: ' + FileName
    rootgrp.createDimension("latitude", shape(fracMaps)[0])
    rootgrp.createDimension("longitude", shape(fracMaps)[1])
    rootgrp.createDimension("class", shape(fracMaps)[2])
    # Create variables
    lat = rootgrp.createVariable('latitude','f4',('latitude',))
    lat.standard_name = 'latitude'
    lat.long_name = 'Latitude values'
    lon = rootgrp.createVariable('longitude','f4',('longitude',))
    lon.standard_name = 'longitude'
    lon.long_name = 'Longitude values'
    cov = rootgrp.createVariable('class', 'i2',('class',))
    cov.standard_name = 'Land_cover'
    cov.long_name = 'Land cover classes'
    lat.units = 'degrees_N'
    lon.units = 'degrees_E'
    cov.units = '-'
	#Rain.units = '0.01mm/hr'
	#Rain._FillValue = -9999
	# Write data to NetCDF file
    lats = arange(89.75,-90,-0.5)
    lons = arange(-179.75,180,0.5)
    classes = arange(0,shape(fracMaps)[2])+1
    lat[:] = lats
    lon[:] = lons
    cov[:] = classes
    
    # Set attributes
    if verbose:
        print 'Writing attributes'
    rootgrp.title = title
    rootgrp.institution = 'USGS'
    rootgrp.source = 'AVHRR NDVI data, collected in 1993-1994'
    rootgrp.references = origFile
    rootgrp.history = 'Created ' + time.ctime(time.time())
    rootgrp.source = 'Created by netCDF4-python, raw file obtained from http://edc2.usgs.gov/glcc/glcc.php'
    rootgrp.disclaimer = 'The timely delivery of these data and their quality is in no way guaranteed by Deltares'
    var = rootgrp.createVariable("class_fractions",'f4',('latitude','longitude','class',), fill_value=-9999)
    var.units = '-'
    # var._FillValue = -9999
    var.standard_name = 'class_fractions'
    var.long_name = 'class_fractions'
    if verbose:
        print 'Writing fraction maps of each class:'
    for Class in arange(0,shape(fracMaps)[2]):
        if verbose:
            print 'Writing ' + longName[Class] + ' to ' + FileName + ' in layer ' + str(Class)
        var[:,:,Class] = fracMaps[:,:,Class]
    # Finally write the map with maximum classes
    rootgrp.sync()
    rootgrp.close()

# USER INPUT STARTS BELOW
try:  
    TargetFolder = sys.argv[1]
except:
    noArgExitStr = str('****************      conv_glcc.exe       *****************\n' + \
    '$Id: conv_glcc.py 733 2013-07-03 06:32:48Z winsemi $\n' + \
    '$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $\n' + \
    '$Author: winsemi $\n' + \
    '$Revision: 733 $\n' + \
    'conv_glcc.exe converts a .BIL formatted 0.0083333x0.0083333 deg. GLCC map\n ' + \
    'into a half degree fractional map. The source GLCC map must be in .BIL format\n' + \
    'with the same specifications as the original GLCC map. This map can be found on\n' + \
    'http://edcftp.cr.usgs.gov/pub/data/glcc/globe/latlon/goge2_0ll.img.gz\n' + \
    '********************************************************\n' + \
    'Usage:\n' + \
    '******\n' + \
    '\n' + \
    '> conv_glcc <input_folder>\n' + \
    '\n' + \
    'The input folder should use file separators with slash (/), not back-slash'
    '****************         Have fun!        *****************')
    print noArgExitStr
    sys.exit(2)   

# TargetFolder = "D:/1202803-PBL/WP1/GLCC/GLCC_orig"
classType = "goge" # can be: "igbp" or "goge"
print 'Processing ' + classType
# USER INPUT DONE!

if classType == "igbp":
    origFile = "http://edcftp.cr.usgs.gov/pub/data/glcc/globe/latlon/gigbp2_0ll.img.gz"
    TargetName = TargetFolder + "/gigbp2_halfdeg.nc"
    TargetName_simple = TargetFolder + "/gigbp2_halfdeg_simple.nc"
    title = "International Geosphere Biosphere Programme Global Land Cover"
    FileName = TargetFolder + "/gigbp2_0ll.img"
    varName   = ["EVERGREEN_NEEDLE", \
        "EVERGREEN_BROADLEAF", \
        "DECIDUOUS_NEEDLELEAF", \
        "DECIDUOUS_BROADLEAF", \
        "MIXED_FORESTS", \
        "CLOSED_SHRUB", \
        "OPEN_SHRUB", \
        "WOODY_SAVANNAS", \
        "SAVANNAS", \
        "GRASSLANDS", \
        "PERMANENT_WET", \
        "CROPLANDS", \
        "URBAN_BUILT", \
        "CROPLAND_NATURAL", \
        "SNOW_ICE", \
        "BARREN_SPARSE", \
        "WATER_BODIES"]
    longName   = ["EVERGREEN NEEDLELEAF FOREST", \
        "EVERGREEN BROADLEAF FOREST", \
        "DECIDUOUS NEEDLELEAF FOREST", \
        "DECIDUOUS BROADLEAF FOREST", \
        "MIXED FORESTS", \
        "CLOSED SHRUBLANDS", \
        "OPEN SHRUBLANDS", \
        "WOODY SAVANNAS", \
        "SAVANNAS", \
        "GRASSLANDS", \
        "PERMANENT WETLANDS", \
        "CROPLANDS", \
        "URBAN AND BUILT-UP", \
        "CROPLAND/NATURAL VEGETATION MOSAIC", \
        "SNOW AND ICE", \
        "BARREN OR SPARSELY VEGETATED", \
        "WATER BODIES"]
    
elif classType == "goge":
    origFile = "http://edcftp.cr.usgs.gov/pub/data/glcc/globe/latlon/goge2_0ll.img.gz"
    TargetName = TargetFolder + "/goge2_halfdeg.nc"
    TargetName_simple = TargetFolder + "/goge2_halfdeg_simple.nc"
    title = "Olson Global Ecosystem"
    FileName = TargetFolder + "/goge2_0ll.img"

    longName = ["URBAN", \
        "LOW SPARSE GRASSLAND", \
        "CONIFEROUS FOREST", \
        "DECIDUOUS CONIFER FOREST", \
        "DECIDUOUS BROADLEAF FOREST", \
        "EVERGREEN BROADLEAF FORESTS", \
        "TALL GRASSES AND SHRUBS", \
        "BARE DESERT", \
        "UPLAND TUNDRA", \
        "IRRIGATED GRASSLAND", \
        "SEMI DESERT", \
        "GLACIER ICE", \
        "WOODED WET SWAMP", \
        "INLAND WATER", \
        "SEA WATER", \
        "SHRUB EVERGREEN", \
        "SHRUB DECIDUOUS", \
        "MIXED FOREST AND FIELD", \
        "EVERGREEN FOREST AND FIELDS", \
        "COOL RAIN FOREST", \
        "CONIFER BOREAL FOREST", \
        "COOL CONIFER FOREST", \
        "COOL MIXED FOREST", \
        "MIXED FOREST", \
        "COOL BROADLEAF FOREST", \
        "DECIDUOUS BROADLEAF FOREST 2", \
        "CONIFER FOREST", \
        "MONTANE TROPICAL FORESTS", \
        "SEASONAL TROPICAL FOREST", \
        "COOL CROPS AND TOWNS", \
        "CROPS AND TOWN", \
        "DRY TROPICAL WOODS", \
        "TROPICAL RAINFOREST", \
        "TROPICAL DEGRADED FOREST", \
        "CORN AND BEANS CROPLAND", \
        "RICE PADDY AND FIELD", \
        "HOT IRRIGATED CROPLAND", \
        "COOL IRRIGATED CROPLAND", \
        "COLD IRRIGATED CROPLAND", \
        "COOL GRASSES AND SHRUBS", \
        "HOT AND MILD GRASSES AND SHRUBS", \
        "COLD GRASSLAND", \
        "SAVANNA (WOODS)", \
        "MIRE, BOG, FEN", \
        "MARSH WETLAND", \
        "MEDITERRANEAN SCRUB", \
        "DRY WOODY SCRUB", \
        "DRY EVERGREEN WOODS", \
        "VOLCANIC ROCK", \
        "SAND DESERT", \
        "SEMI DESERT SHRUBS", \
        "SEMI DESERT SAGE", \
        "BARREN TUNDRA", \
        "COOL SOUTHERN HEMISPHERE MIXED FORESTS", \
        "COOL FIELDS AND WOODS", \
        "FOREST AND FIELD", \
        "COOL FOREST AND FIELD", \
        "FIELDS AND WOODY SAVANNA", \
        "SUCCULENT AND THORN SCRUB", \
        "SMALL LEAF MIXED WOODS", \
        "DECIDUOUS AND MIXED BOREAL FOREST", \
        "NARROW CONIFERS", \
        "WOODED TUNDRA", \
        "HEATH SCRUB", \
        "COASTAL WETLAND - NW", \
        "COASTAL WETLAND - NE", \
        "COASTAL WETLAND - SE", \
        "COASTAL WETLAND - SW", \
        "POLAR AND ALPINE DESERT", \
        "GLACIER ROCK", \
        "SALT PLAYAS", \
        "MANGROVE", \
        "WATER AND ISLAND FRINGE", \
        "LAND, WATER, AND SHORE", \
        "LAND AND WATER, RIVERS", \
        "CROP AND WATER MIXTURES", \
        "SOUTHERN HEMISPHERE CONIFERS", \
        "SOUTHERN HEMISPHERE MIXED FOREST", \
        "WET SCLEROPHYLIC FOREST", \
        "COASTLINE FRINGE", \
        "BEACHES AND DUNES", \
        "SPARSE DUNES AND RIDGES", \
        "BARE COASTAL DUNES", \
        "RESIDUAL DUNES AND BEACHES", \
        "COMPOUND COASTLINES", \
        "ROCKY CLIFFS AND SLOPES", \
        "SANDY GRASSLAND AND SHRUBS", \
        "BAMBOO", \
        "MOIST EUCALYPTUS", \
        "RAIN GREEN TROPICAL FOREST", \
        "WOODY SAVANNA", \
        "BROADLEAF CROPS", \
        "GRASS CROPS", \
        "CROPS, GRASS, SHRUBS", \
        "EVERGREEN TREE CROP", \
        "DECIDUOUS TREE CROP"]
    varName = ["URBAN", \
        "LOW_SPARSE_GRASSLAND", \
        "CONIFEROUS_FOREST", \
        "DECIDUOUS_CONIFER_FOREST", \
        "DECIDUOUS_BROADLEAF_FOREST", \
        "EVERGREEN_BROADLEAF_FORESTS", \
        "TALL_GRASSES_AND_SHRUBS", \
        "BARE_DESERT", \
        "UPLAND_TUNDRA", \
        "IRRIGATED_GRASSLAND", \
        "SEMI_DESERT", \
        "GLACIER_ICE", \
        "WOODED_WET_SWAMP", \
        "INLAND_WATER", \
        "SEA_WATER", \
        "SHRUB_EVERGREEN", \
        "SHRUB_DECIDUOUS", \
        "MIXED_FOREST_AND_FIELD", \
        "EVERGREEN_FOREST_AND_FIELDS", \
        "COOL_RAIN_FOREST", \
        "CONIFER_BOREAL_FOREST", \
        "COOL_CONIFER_FOREST", \
        "COOL_MIXED_FOREST", \
        "MIXED_FOREST", \
        "COOL_BROADLEAF_FOREST", \
        "DECIDUOUS_BROADLEAF_FOREST_2", \
        "CONIFER_FOREST", \
        "MONTANE_TROPICAL_FORESTS", \
        "SEASONAL_TROPICAL_FOREST", \
        "COOL_CROPS_AND_TOWNS", \
        "CROPS_AND_TOWN", \
        "DRY_TROPICAL_WOODS", \
        "TROPICAL_RAINFOREST", \
        "TROPICAL_DEGRADED_FOREST", \
        "CORN_AND_BEANS_CROPLAND", \
        "RICE_PADDY_AND_FIELD", \
        "HOT_IRRIGATED_CROPLAND", \
        "COOL_IRRIGATED_CROPLAND", \
        "COLD_IRRIGATED_CROPLAND", \
        "COOL_GRASSES_AND_SHRUBS", \
        "HOT_AND_MILD_GRASSES_AND_SHRUBS", \
        "COLD_GRASSLAND", \
        "SAVANNA_(WOODS)", \
        "MIRE,_BOG,_FEN", \
        "MARSH_WETLAND", \
        "MEDITERRANEAN_SCRUB", \
        "DRY_WOODY_SCRUB", \
        "DRY_EVERGREEN_WOODS", \
        "VOLCANIC_ROCK", \
        "SAND_DESERT", \
        "SEMI_DESERT_SHRUBS", \
        "SEMI_DESERT_SAGE", \
        "BARREN_TUNDRA", \
        "COOL_SOUTHERN_HEMISPHERE_MIXED_FORESTS", \
        "COOL_FIELDS_AND_WOODS", \
        "FOREST_AND_FIELD", \
        "COOL_FOREST_AND_FIELD", \
        "FIELDS_AND_WOODY_SAVANNA", \
        "SUCCULENT_AND_THORN_SCRUB", \
        "SMALL_LEAF_MIXED_WOODS", \
        "DECIDUOUS_AND_MIXED_BOREAL_FOREST", \
        "NARROW_CONIFERS", \
        "WOODED_TUNDRA", \
        "HEATH_SCRUB", \
        "COASTAL_WETLAND_-_NW", \
        "COASTAL_WETLAND_-_NE", \
        "COASTAL_WETLAND_-_SE", \
        "COASTAL_WETLAND_-_SW", \
        "POLAR_AND_ALPINE_DESERT", \
        "GLACIER_ROCK", \
        "SALT_PLAYAS", \
        "MANGROVE", \
        "WATER_AND_ISLAND_FRINGE", \
        "LAND,_WATER,_AND_SHORE", \
        "LAND_AND_WATER,_RIVERS", \
        "CROP_AND_WATER_MIXTURES", \
        "SOUTHERN_HEMISPHERE_CONIFERS", \
        "SOUTHERN_HEMISPHERE_MIXED_FOREST", \
        "WET_SCLEROPHYLIC_FOREST", \
        "COASTLINE_FRINGE", \
        "BEACHES_AND_DUNES", \
        "SPARSE_DUNES_AND_RIDGES", \
        "BARE_COASTAL_DUNES", \
        "RESIDUAL_DUNES_AND_BEACHES", \
        "COMPOUND_COASTLINES", \
        "ROCKY_CLIFFS_AND_SLOPES", \
        "SANDY_GRASSLAND_AND_SHRUBS", \
        "BAMBOO", \
        "MOIST_EUCALYPTUS", \
        "RAIN_GREEN_TROPICAL_FOREST", \
        "WOODY_SAVANNA", \
        "BROADLEAF_CROPS", \
        "GRASS_CROPS", \
        "CROPS,_GRASS,_SHRUBS", \
        "EVERGREEN_TREE_CROP", \
        "DECIDUOUS_TREE_CROP"]

try:
    fracMaps, maxFracMaps = conv_GLCC(FileName, varName, "True")
    #writeNC(TargetName, fracMaps, maxFracMaps, varName, longName, title, origFile, "True")
    writeNC_simple(TargetName_simple, fracMaps, title, origFile, "True")
    print 'Done'
except:
    print 'ERROR: File "' + FileName + '" not present, not a valid GLCC map or something else went wrong.'