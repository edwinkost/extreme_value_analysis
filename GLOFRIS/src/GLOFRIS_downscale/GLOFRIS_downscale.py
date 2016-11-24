#!/usr/bin/env python
"""downscale_flood_volume.py

  more details here below


  Syntax: change the input folders / files if necessary and run the script
 Copyright notice
  --------------------------------------------------------------------
  Copyright (C) 2011 Hessel Winsemius (Deltares)

  ------------------------------
      H.(Hessel) C. Winsemius

      hessel.winsemius@deltares.nl
  ------------------------------
      Rotterdamseweg 185
      Delft
      The Netherlands

  This script is free software under the PBL-Deltares MoU: redistribute it and/or
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
based on IMAGE scenario outputs and a global hydrological model PCRGLOB-WB

 Version <http://svnbook.red-bean.com/en/1.5/svn.advanced.props.special.keywords.html>
Created: 10 Apr 2012
Created and tested with python 2.7.3 and 2.5.4 (some deprecated issues are still
included in try/catch loops)

$Id: GLOFRIS_downscale.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/GLOFRIS_downscale/GLOFRIS_downscale.py $
$Keywords: $
"""

import numpy as np
import os
import logging
import logging.handlers
import os.path
import sys
from netcdftime import *
from netCDF4_utils import *
from netCDF4 import Dataset
import getopt
import traceback
import osgeo.gdal as gdal
import xlrd
import pdb
try:
    from PCRaster import *
    from PCRaster.NumPy import *
    # from PCRaster.Framework import *
except:
    # this exception occurs under linux compilation of PCRaster
    from pcraster import *

def setlogger(logfilename, logReference):
    """
    Set-up the logging system. Exit if this fails
    """
    try:
        #create logger
        logger = logging.getLogger(logReference)
        logger.setLevel(logging.DEBUG)
        ch = logging.handlers.RotatingFileHandler(logfilename,maxBytes=200000, backupCount=5)
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
        #create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        #add formatter to ch
        ch.setFormatter(formatter)
        console.setFormatter(formatter)
        #add ch to logger
        logger.addHandler(ch)
        logger.addHandler(console)
        logger.debug("File logging to " + logfilename)
        return logger, ch
    except IOError:
        print "ERROR: Failed to initialize logger with logfile: " + logfilename
        sys.exit(2)
    stream_thres = int(sys.argv[4])
    relevant_T   = int(sys.argv[5])

def find_nearest(arrayInLon,arrayInLat,xax, yax):
    '''
    find_nearest finds the grid point in the map that is closest to the lon/lat
    location in de DIVA database.
    '''
    lonClose = []
    latClose = []
    for i in range(0,len(arrayInLon)):
        lonClose.append(np.abs(xax-arrayInLon[i]).argmin())
        latClose.append(np.abs(yax-arrayInLat[i]).argmin())

    return lonClose, latClose

def find_in_window(xmin,xmax,ymin,ymax,lon,lat):
    lon_idx = []
    idx = []
    for row in range(0,len(lon)):
        if lon[row]>=xmin and lon[row]<=xmax:
            lon_idx.append(row)
        else:
            lon_idx.append(np.nan)

    for i in range(0,len(lat)):
        if np.isfinite(lon_idx[i]):
            if lat[i]>=ymin and lat[i]<=ymax:
                idx.append(int(i))

    return idx

def prepare_nc(FileIn, FileRef, FileOut, x, y, stream_thres, relevant_T):
    """
    Prepares a target NetCDF, following the attributes of a source NetCDF file, but using the
    x-axis, y-axis of a certain projection. If the projection is lat-lon, then only a lat-lon axis
    is prepared. Otherwise an x, y axis is prepared, a projection variable is defined, and grids for
    latitude and longitude values are written to the NetCDF file.
    input:
        FileIn:         string      -- Path to NetCDF case file
        FileRef:        string      -- Path to NetCDF reference file
        FileOut:        string      -- Path to target result NetCDF file
        x:              array float -- Vector with x axis
        y:              array float -- Vector with y axis
        stream_thres:   int         -- Stream threshold, above which floods are taken into account
        relevant_T:     int         -- Return period, above which floods are taken into account
        y:              array float -- Vector with y axis
    output:
        No output from this function. The result is a prepared NetCDF file at FileOut

    """
    # if projStr.lower() == 'epsg:4326':
#    if srs.IsProjected() == 0:
#        logger.info('Found lat-lon coordinate system, preparing lat, lon axis')
#        x_dim      = 'lon';             y_dim     = 'lat'
#        x_name     = 'longitude';       y_name = 'latitude'
#        x_longname = 'Longitude values';y_longname = 'Latitude values'
#        x_unit     = 'degrees_east';       y_unit     = 'degrees_north'
#        gridmap    = 'latitude_longitude'
#    else:
#        logger.info('Found a Cartesian projection coordinate system, preparing x, y axis')
#        x_dim = 'x';                                    y_dim = 'y'
#        x_name = 'projection_x_coordinate';             y_name = 'projection_x_coordinate'
#        x_longname = 'x-coordinate in Cartesian system';y_longname = 'y-coordinate in Cartesian system'
#        x_unit     = 'm';                               y_unit     = 'm'
#        gridmap    = ''
    y_dim = 'lat'
    x_dim = 'lon'
    y_unit = 'degrees_north'
    x_unit = 'degrees_east'
    y_name = 'latitude'
    x_name = 'longitude'
    y_longname = 'Latitude values'
    x_longname = 'Longitude values'
    gridmap = 'latitude_longitude'
    logger.info('Preparing ' + FileOut)
    nc_src = Dataset(FileIn,'r')
    nc_trg = Dataset(FileOut,'w') # format='NETCDF3_CLASSIC'
    # Create dimensions
    nc_trg.createDimension("time", 0) #NrOfDays*8
    nc_trg.createDimension(y_dim, len(y))
    nc_trg.createDimension(x_dim, len(x))
    # create axes

    DateHour = nc_trg.createVariable('time','f8',('time',))
    DateHour.units = 'Years since 0001-01-01 00:00:00'
    DateHour.calendar = 'gregorian'
    DateHour.standard_name = 'time'
    DateHour.long_name = 'time'
    DateHour_src = nc_src.variables['time'][:]
    DateHour[:] = np.arange(0,len(DateHour_src))
    # DateHour[:] = nc4.date2num(datetimeObj,units=nc_src.variables['time'].units,calendar=DateHour.calendar)
    y_var = nc_trg.createVariable(y_dim,'f4',(y_dim,))
    y_var.standard_name = y_name
    y_var.long_name = y_longname
    y_var.units = y_unit
    x_var = nc_trg.createVariable(x_dim,'f4',(x_dim,))
    x_var.standard_name = x_name
    x_var.long_name = x_longname
    x_var.units = x_unit
    y_var[:] = y
    x_var[:] = x

    # Set attributes
    # Change some of the attributes, add some
    all_attrs = nc_src.ncattrs()
    for attr in all_attrs:
        try:
            attr_val = eval('nc_src.' + attr)
            exec("nc_trg." + attr + " = '" + attr_val + "'")
        except:
            logger.warning('Could not write attribute')
    nc_trg.institution     = 'Deltares\nPBL\nUtrecht University'
    nc_trg.history         = "File generated from Deltares' GLOFRIS_downscale v1.0. Original file details given in global attributes"
    nc_trg.source_case     = FileIn
    nc_trg.reference_case  = FileRef
    nc_trg.stream_threshold= str(stream_thres)
    nc_trg.return_period_threshold = str(relevant_T)
    nc_trg.disclaimer      = 'The availability and quality of these data is in no way guaranteed by Deltares'
    # write projection info to file
    wgs84 = nc_trg.createVariable('wgs84','c')
    wgs84.long_name = 'wgs84'
    wgs84.EPSG_code = 'EPSG:4326'
    wgs84.proj4_params = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    wgs84.grid_mapping_name = 'latitude_longitude'

    # create water level variable
    variab               = nc_trg.createVariable('water_level','f4',('time',y_dim,x_dim,),chunksizes=(1,len(y),len(x)),fill_value=-9999)
    variab.units         = 'm'
    variab.standard_name = 'water_surface_height_above_reference_datum'
    variab.long_name     = 'Water level above surface elevation'

    nc_trg.sync()
    nc_trg.close()

def closeLogger(logger, ch):
    ch.flush()
    ch.close()
    logger.removeHandler(ch)
    # return logger, ch

def resampleMap(origMap,resMap,cloneMap):
    #resamples map to new extent
    command= 'resample --clone %s %s %s' % (cloneMap,origMap,resMap)
    os.system(command)

def distance_on_unit_sphere(lat1, long1, lat2, long2):
    setglobaloption("degrees")
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = pi/180.0
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    cos_angle = (np.sin(phi1)*np.sin(phi2)*np.cos(theta1 - theta2) + np.cos(phi1)*np.cos(phi2))
    arc = np.arccos( cos_angle )
    return arc

def readMap(fileName, fileFormat):
    """ Read geographical file into memory
    """
    # Open file for binary-reading
    mapFormat = gdal.GetDriverByName(fileFormat)
    mapFormat.Register()
    ds = gdal.Open(fileName)
    if ds is None:
        print 'Could not open ' + fileName + '. Something went wrong!! Shutting down'
        sys.exit(1)
        # Retrieve geoTransform info
    geotrans = ds.GetGeoTransform()
    originX = geotrans[0]
    originY = geotrans[3]
    resX    = geotrans[1]
    resY    = geotrans[5]
    cols    = ds.RasterXSize
    rows    = ds.RasterYSize
    x       = np.linspace(originX+resX/2,originX+resX/2+resX*(cols-1),cols)
    y       = np.linspace(originY+resY/2,originY+resY/2+resY*(rows-1),rows)
    # Retrieve raster
    RasterBand = ds.GetRasterBand(1) # there's only 1 band, starting from 1
    data       = RasterBand.ReadAsArray(0,0,cols,rows)
    FillVal    = RasterBand.GetNoDataValue()
    RasterBand = None
    ds         = None

    return x, y, data, FillVal

def writeMap(fileName, fileFormat, x, y, data, FillVal):
    """ Write geographical data into file"""

    verbose = False
    gdal.AllRegister()
    driver1 = gdal.GetDriverByName('GTiff')
    driver2 = gdal.GetDriverByName(fileFormat)

		# Processing
    if verbose:
        print 'Writing to temporary file ' + fileName + '.tif'
	# Create Output filename from (FEWS) product name and date and open for writing
    TempDataset = driver1.Create(fileName + '.tif',data.shape[1],data.shape[0],1,gdal.GDT_Float32)
	# Give georeferences
    xul = x[0]-(x[1]-x[0])/2
    yul = y[0]+(y[0]-y[1])/2
    TempDataset.SetGeoTransform( [ xul, x[1]-x[0], 0, yul, 0, y[1]-y[0] ] )
	# get rasterband entry
    TempBand = TempDataset.GetRasterBand(1)
	# fill rasterband with array
    TempBand.WriteArray(data,0,0)
    TempBand.FlushCache()
    TempBand.SetNoDataValue(FillVal)
	# Create data to write to correct format (supported by 'CreateCopy')
    if verbose:
        print 'Writing to ' + fileName + '.map'
    outDataset = driver2.CreateCopy(fileName, TempDataset, 0)
    TempDataset = None
    outDataset = None
    if verbose:
        print 'Removing temporary file ' + fileName + '.tif'
    os.remove(fileName + '.tif');

    if verbose:
        print 'Writing to ' + fileName + ' is done!'

def readCase(caseFile):
    # read maxima at global scale from scenario and resample to local
    try:
        nc = Dataset(caseFile,'r')
        max_fldf = nc.variables['Flooded_Fraction_max'][:]
        # in case python 2.5 is used, max_fldf will be a normal numpy array. In case 2.7 is used, a masked array will be returned. This needs to be converted to a normal array.
        try:
        	max_fldf.mask
        	max_fldf = max_fldf.data
        except:
        	pass
        max_fldd = nc.variables['Flooded_Depth_max'][:]
        try:
        	max_fldd.mask
        	max_fldd = max_fldd.data
        except:
        	pass
        max_vol  = max_fldf*max_fldd
        max_vol[max_vol==max_vol.max()] = np.nan
        nc.close()
    except:
        logger.error('Case "' + caseFile + '" is missing. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)
    max_vol.sort(axis=0)

    return max_vol

def downscale(n, ldd, stream_thres, conv_factor, logger, ch):
    """
    This function computes the inundation pattern from a certain designated strahler threshold
    n:  integer, defines the number of flood map (starting from 0)
    """
    logger.info(str("Processing volume_t." + "%03.f" % (n+1)))
    volMapFile      = os.path.join(downscaleLoc,str("volume_t." + "%03.f") % (n+1))
    volume_target   = readmap(volMapFile)
    stream          = streamorder(ldd)      # make a stream order map
    # make a river-map, rivers are streams with strahler order < the largest order - a threshold
    # rivers = ifthenelse(scalar(stream) < mapmaximum(scalar(stream)) - stream_thres,boolean(0), boolean(stream))
    rivers          = ifthenelse(scalar(stream) < stream_thres,boolean(0), boolean(stream))
    report(rivers,os.path.join(downscaleLoc,'rivers.map'))
    # initialize loop
    floodedLand     = volume_target*0
    count           = 0
    floodHeightInactiveCells = volume_target*0
    # now iterate in a loop, 15 meters is assumed to be the largest inundation level possible. Increase by steps of 0.3
    # check volume of cells taken into consideration
    volInRiver      = ifthenelse(rivers==1,volume_target,scalar(0))
    volInLargeCells = areamaximum(volInRiver,ordinal(uniqueid_target))
    for level in np.arange(0.0,30,0.1):
        logger.debug('Processing with inundation depth = ' + str(level))

        """
        Below, a short explanation of the maps, generated in this PCRaster routine is given. The principle idea is to impose a certain water level on river cells
        an check where the backwater of this imposed height may go to upstream through use of the local drain directions and elevation map
        The routine also checks where the imposed water in each cell comes from (i.e. from which 0.5 degree cell).
        In the end, the total volume of backwater from each 0.5 deg. cell is computed and compared to PCRGLOB volumes.
        If the imposed volume exceeds the PCRGLOB volume, the 0.5 deg. cell is assumed to be 'depleted' and the river cells are excluded from
        the river network in further processing steps. In the next step, a slightly higher level is imposed and the volume check is repeated.
        Hence, more downstream cells may impose backwater on the target cells under consideration in later steps.
        In the end of the routine, all volumes of each pcrglob cell should be accounted for in the downscaled map.

        floodInRiver:           flood level, with resp. to MSL imposed on the river network map
        floodInRiverUpstream:   the flood level of floodInRiver, imposed on the upstream area of each river pixel
        idInRiver:              id of te 0.5 deg. cell, imposed on the river network map
        idInRiverUpstream:      id imposed on the upstream area of each river cell.
        volInRiver:             the volume of flood water in each 0.5 deg. pixel, imposed on the river network
        volInRiverUpstream:     flood water volume, imposed on the upstream area of each river pixel
        areaInRiver:            cell size, imposed on river network map
        areaInRiverUpstream:    total surface area of areas with the same idInRiverUpstream value
        floodedLandTemp:        The water level in areas, which would occur if the current 'level' was imposed on the river network
        floodedLandAv:          The flooded water level, averaged over the idInRiverUpstream areas
        floodedLandTotal:       The total volume of flood water in each contiguous area of idInRiverUpstream
        floodedLand:            A volume comparison is made between floodedLandTotal and volInRiverUpstream.
                                If floodedLandTotal is smaller, then the amount of imposed water will be smaller then the
                                volume, computed by PCRGLOB in the 0.5 degree area. The inundation height in the cell will be updated in floodedLand.
                                If the volume is exceeded, the cell will not be updated and the river cells in this area will be removed.
                                Hence, backwater from more downstream cells can still impact on the cell under consideration.

        TO-DO: als een cel inactief wordt, dan gaat een benedenstroomse cel ineens heel veel water dumpen op deze plaatsen met als gevolg, mogelijk ernstige overschrijding van het volume uit die cel.
        """
        floodInRiver         = ordinal((ifthenelse(rivers==1,scalar(level)+dem,scalar(0)))*100)
        idInRiver            = ordinal(ifthenelse(rivers==1,uniqueid_target,scalar(0)))
        volInRiver           = ifthenelse(rivers==1,volume_target,scalar(0))
        areaInRiver          = ifthenelse(rivers==1,surf,scalar(0))
        floodInRiverUpstream = subcatchment(ldd,floodInRiver)
        idInRiverUpstream    = subcatchment(ldd,idInRiver)
        if level > 0:
            changedSourceCells = ifthenelse(idInRiverOld != idInRiverUpstream, boolean(1),boolean(0)) # if a different 0.5 deg. area is the source of floods
            floodHeightInactiveCells       = ifthenelse(changedSourceCells,floodedLand,floodHeightInactiveCells)
        volInRiverUpstream   = areamaximum(volInRiver,idInRiverUpstream)
        areaInRiverUpstream  = areatotal(areamaximum(areaInRiver,idInRiverUpstream),idInRiverUpstream) # compute total catchment area of Id cell
        floodedLandTemp      = min(max(scalar(floodInRiverUpstream)/100-dem,0),level)
        floodedLandTempAv    = areaaverage(max(floodedLandTemp - floodHeightInactiveCells, 0),idInRiverUpstream)
        floodedLandTotal     = floodedLandTempAv*areaInRiverUpstream
        # check which cells have a changed source area of .5 degrees and subtract the volume there
        # ERROR IN LINE BELOW: statement max(scalar(floodedLandTemp),scalar(floodedLand)), will result in wrong values in areas that were classified as 'inactive'
        floodedLand          = ifthenelse(floodedLandTotal < volInRiverUpstream, max(scalar(floodedLandTemp),scalar(floodedLand)), scalar(floodedLand))# hieronder uitrekenen of volume al meer is dan eerder of niet.
        # update relevant river streams (exclude the ones that are already saturated)
        rivers               = ifthenelse(floodedLandTotal < volume_target, rivers, boolean(0))
        idInRiverOld         = idInRiverUpstream

    vol_pcrglob = pcr2numpy(volInLargeCells,0)/conv_factor
    vol_pcr = vol_pcrglob.sum()
    volmodelled = pcr2numpy(floodedLand*surf,0)
    vol_mod = volmodelled.sum()
    #
    logger.info(str('volume_t.' + '%03.f' + ': Volume PCRGLOB: ' + '%03.3f' + 'km3, Volume downscaling: ' + '%03.3f' + 'km3' + ', perc. diff: ' + '%2.2f' + '%%')  % (n+1,vol_pcr/1e9, vol_mod/1e9, (vol_mod-vol_pcr)/vol_pcr*100))
    return logger, ch, floodedLand
    # end of function part

def translate_DIVA(xax, yax, T, DIVAXls, dem):
    xmin    = np.nanmin(xax)
    xmax    = np.nanmax(xax)
    ymin    = np.nanmin(yax)
    ymax    = np.nanmax(yax)

    wb = xlrd.open_workbook(DIVAXls)
    sh = wb.sheet_by_index(0)

    lon = np.array(sh.col_values(7)[1:],dtype='f')
    lat = np.array(sh.col_values(8)[1:],dtype='f')

    s1    = np.array(sh.col_values(1)[1:],dtype='f')
    s10   = np.array(sh.col_values(2)[1:],dtype='f')
    s100  = np.array(sh.col_values(3)[1:],dtype='f')
    s1000 = np.array(sh.col_values(4)[1:],dtype='f')

    selected = find_in_window(xmin,xmax,ymin,ymax,lon,lat)
    s1Selection    = s1[selected]
    s10Selection   = s10[selected]
    s100Selection  = s100[selected]
    s1000Selection = s1000[selected]

    sAllSelection = np.array([s1Selection,s10Selection,s100Selection,s1000Selection])
    tAllSelection = [1.0,10.0,100.0,1000.0]
    tInt = np.linspace(1,1000,1000)
    intVals = []
    for i in range(0,len(sAllSelection[1,:])):
        intVals.append(np.interp(tInt,tAllSelection,sAllSelection[:,i]))
#        plt.plot(tInt,intVals[i],'-+')

    intVals = np.array(intVals)

#    plt.figure(figsize=(30,24))
#    plt.plot(lon,lat,'b.')
#    plt.plot(lon[selected],lat[selected],'ro')
#    plt.plot([xmin,xmax],[ymin,ymin],'r')
#    plt.plot([xmin,xmax],[ymax,ymax],'r')
#    plt.plot([xmin,xmin],[ymin,ymax],'r')
#    plt.plot([xmax,xmax],[ymin,ymax],'r')
#    plt.grid('on')

    #nrCols = np.round((xmax-xmin)/cellLen)
    #nrRows = np.round((ymax-ymin)/cellLen)

    lonClose, latClose = find_nearest(lon[selected],lat[selected],xax,yax)
    # latClose = find_nearest(lon[selected],lat[selected],xax,yax)[1]

    point_levels = np.zeros((len(yax),len(xax)))
    point_levels[point_levels==0.0]=-999
    point_levels[latClose,lonClose] = intVals[:,T-1]

    #cut_dem(xmin,xmax,ymin,ymax,'resample_map.tif','cut_dem.map')
    #setclone('cut_dem.map')
    point_levels_map = numpy2pcr(Scalar,point_levels,-999)
    #report(rasterTmap,'rasterT.map')

    interp_levels = inversedistance(boolean(dem),point_levels_map, 2,0,0)
    # report(result,'result.map')
    return interp_levels

def coastal_hazard(demThres, demRaise, DIVAXls, dem, ldd, T):
#    demFolder    = os.path.split(caseDem)[0]
#    demFile      = os.path.split(caseDem)[1]
#    region       = demFile.split('.map')[0]
#    caseLdd      = os.path.join(demFolder, region + '_ldd.map')
#    caseName     = os.path.dirname(__file__)
#    demRaiseFile = os.path.join(demFolder, region + '_raised.map')
#    setclone(caseDem)
#    dem          = readmap(caseDem)                          # read elevation from PCRaster DEM map
    # determine extents of DEM
    xc      = pcr2numpy(xcoordinate(boolean(cover(dem,1))), np.nan)
    yc      = pcr2numpy(ycoordinate(boolean(cover(dem,1))), np.nan)
    xax     = xc[0,:]
    yax     = yc[:,0]
    cellLen = xc[0,1]-xc[0,0]

    # read relevant DIVA points
    levelAtCoast = translate_DIVA(xax, yax, T, DIVAXls, dem)

#    if os.path.isfile(caseLdd):
#        print 'Ldd already exists'
#        ldd = readmap(caseLdd)
#    else:
#        print 'Ldd being created'
#        ldd = lddcreate(dem,1e31,1e31,1e31,1e31)        # make a local drain direction map
#        report(ldd,'ldd.map')

    # determine pit cells at downstream ends
    coastal_locs = ifthenelse(pit(ldd)!=0,ifthenelse(dem < demThres,boolean(1),boolean(0)),boolean(0))
    # Distance to coast
    dist2coast   = ldddist(ldd,coastal_locs,120)               # there's about 120 factor to km scale from degree scale of cells
    # report(dist2coast,'dist2coast.map')
    # Adjust DEM
    dem_manip    = dem + dist2coast*demRaise                  # raise the elevation using a damping factor
    # report(dem_manip, demRaiseFile)

    # levelDem = 'result.map'     # caseName +

    # level = readmap(levelDem)
    floodedLandCoastal   = max(levelAtCoast - dem_manip,0)
    return floodedLandCoastal
    # report(floodedLandCoastal,'flood_%s_T_%03.f.map' % (region, T))


##### END OF FUNCTIONS #######
# Set default values (overwritten from input from command line arguments)
logfile = 'GLOFRIS_downscale.log'
#stream_thres = 2
nrExtremes = 30
earth_radius = 6378137.
h_min_impact = 0 # water level where there's no impact of a flood
h_max_impact = 3 # water level with maximum impact, anything above is just as bad
do_coastal = True
dem_thres    = 10
damping      = 0.3 # Amount of meters per km damping

"""Treatment of command-line arguments"""
try:
    # print sys.argv[1:]
    #config_file = os.path.abspath(sys.argv[1])
    workFolder   = os.path.split(sys.argv[0])[0]        # location of downscale executable
    caseFile     = os.path.abspath(sys.argv[1])         # case file
    caseFile_ref = os.path.abspath(sys.argv[2])         # file of reference conditions
    caseDem      = os.path.abspath(sys.argv[3])         # case DEM elevation model
    stream_thres = int(sys.argv[4])                     # Stream threshold
    relevant_T   = int(sys.argv[5])                     # bank-full return period
    demFolder    = os.path.split(caseDem)[0]            # DEM folder
    demFile      = os.path.split(caseDem)[1]            # DEM file
    region       = demFile.split('.map')[0]             # Name of region (stripped from DEM folder)
    caseLdd      = os.path.join(demFolder, region + '_ldd.map')     # Name of local drain direction map
    caseDemMin   = os.path.join(demFolder, region + '_min.map')
    # demRaiseFile = os.path.join(demFolder, region + '_raised.map')  # Name of raised DEM
    downscaleLoc = os.path.join(demFolder,region)         # location where downscaled results are stored
    if not os.path.isdir(downscaleLoc):
        os.makedirs(downscaleLoc)
    logfile      = os.path.join(downscaleLoc, 'GLOFRIS_downscale_' + region  + '.log')
    FileOut      = os.path.join(downscaleLoc, region + '.nc')
    DIVAXls      = os.path.abspath(os.path.join(workFolder,'diva','DIVA_data.xls'))
except:
    noArgExitStr = str('****************      GLOFRIS downscale tool v. 1.0       *****************\n' + \
    '$Id: GLOFRIS_downscale.py 733 2013-07-03 06:32:48Z winsemi $\n' + \
    '$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $\n' + \
    '$Author: winsemi $\n' + \
    '$Revision: 733 $\n' + \
    'GLOFRIS_downscale downscales a GLOFRIS scenario into 1x1 km2 maps. This version assumes that a 30-year run is used. \n ' + \
    'GLOFRIS_downscale runs as follows: \n' + \
    '======================================================================================================================== \n' + \
    'GLOFRIS_downscale <path to case> <path to reference> <path to PCRaster dem> <stream threshold> <return period threshold> \n' + \
    '======================================================================================================================== \n' + \
    '<path to case>:            path to NetCDF file, output from your GLOFRIS run\n' + \
    '<path to reference>:       path to NetCDF file, output from the reference run,\n' + \
    '                           used to determine current bank-full flood volume\n' + \
    '<path to PCRaster dem>:    path to PCRaster DEM (0.008333 degrees resolution preferred), \n' + \
    '                           with regional elevation.\n' + \
    '                           The downscaling will be done to this grid extent\n' + \
    '                           elevation should be in meters, ocean should be missing values,\n' + \
    '                           projection should be lat-lon WGS84.\n' + \
    '<stream threshold>:        Strahler stream threshold at which a river is considered to be \n' + \
    '                           large enough to cause fluvial flooding (6 or 7 gives good results). \n' + \
    '<return period threshold>: return period (years) at which no fluvial flooding is assumed to occur. \n' + \
    '                           This value should be much smaller than the return periods, included in \n' + \
    '                           the run. E.g. a 30-year run should have a return period << 30, e.g. 2 years. \n')
    print noArgExitStr
    sys.exit(2)

    # Set logging (delete old file if it exists)
if os.path.isfile(logfile):
    os.unlink(logfile)
logger, ch     = setlogger(logfile, 'GLOFRIS_downscale')
logger.info('Starting GLOFRIS_downscale v. 1.0')
logger.info('GLOFRIS_downscale capabilities: downscales river flood maxima from GLOFRIS to 1x1 km2 scale, based on a PCRaster DEM file.')
logger.info('$Id: GLOFRIS_downscale.py 733 2013-07-03 06:32:48Z winsemi $')
logger.info('$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $')
logger.info('$Author: winsemi $')
logger.info('$Revision: 733 $')
logger.info('GLOFRIS_downscale is run with the following arguments:')
logger.info('Case File :                ' + caseFile)
logger.info('Reference File :           ' + caseFile_ref)
logger.info('Case DEM :                 ' + caseDem)
logger.info('Stream threshold :         ' + str(stream_thres))
logger.info('Return period threshold :  ' + str(relevant_T))

workDir = os.path.dirname(sys.argv[0])

if workDir[-4:] == 'dist':
    workDir = workDir[0:-5]
cellareaFolder = os.path.join(workDir, 'baseMaps')

try:
    cellarea_file = os.path.join(cellareaFolder,'cellarea30.map')   # already in system, replace this
    # clone is cellarea
    setclone(cellarea_file)
    ## now make a uniqueId map of land cells of the full globe
    cellarea = readmap(cellarea_file)
    landyesno = ifthenelse(cellarea > 0, boolean(1), boolean(0))
    uniqueid_map  = uniqueid(landyesno)
    report(uniqueid_map,os.path.join(downscaleLoc,'uniqueid.map'))

    # read case, reference case and prepare volume arrays
    logger.info('Reading case from ' + caseFile)
    max_vol     = readCase(caseFile)
    logger.info('Reading reference from ' + caseFile_ref)
    max_vol_ref = readCase(caseFile_ref)
    ### DOWNSCALING PROCEDURE STARTS BELOW.  REPEAT FOR EACH REGION OF INTEREST ######
    # region counter
    # determine CDF Weibull positions and return periods
    p =(nrExtremes-(np.arange(0.,nrExtremes)+0.5))/nrExtremes
    T = 1/p
    ii_p_relevant = T > relevant_T
    p_relevant = p*ii_p_relevant
    weight = 1./nrExtremes

    # determine relevant volumes
    vol_irrelevant = max_vol_ref.copy()
    vol_relevant   = max_vol_ref.copy()
    for n in np.arange(0,nrExtremes):
        # keep all irrelevant probability values and set remainder to zero in vol_irrelevant
        if p_relevant[n] > 0:
            vol_irrelevant[n,:,:] = 0
    # determine maximum irrelevant water level
    vol_irrelevant = vol_irrelevant.max(axis=0)

    # now remove irrelevant volume (from reference run) from the scenario run volumes
    for n in np.arange(0,nrExtremes):
        vol_relevant[n,:,:] = np.maximum(max_vol[n,:,:]-vol_irrelevant,0)

    setclone(cellarea_file)
    # check if DEM exists, if not return error message
    if not os.path.isfile(caseDem):
        logger.error('Elevation map "' + os.path.abspath(caseDem) + '" is missing. Required for downscaling. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)
    try:
        dem_test = readmap(caseDem) # test if map is readable. If so, immediately delete objedct from memory
        del dem_test
    except:
        logger.error('Elevation map "' + os.path.abspath(caseDem) + '" is not a PCRaster map. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)

    if not os.path.isfile(caseDemMin):
        logger.warning('Minimum elevation map "' + os.path.abspath(caseDemMin) + '" is missing. Will use "' + os.path.abspath(caseDemMin) + '" instead for coastal downscaling')
        caseDemMin = caseDem
        #closeLogger(logger, ch)
        #sys.exit(2)
    try:
        dem_test = readmap(caseDemMin) # test if map is readable. If so, immediately delete objedct from memory
        del dem_test
    except:
        logger.error('Elevation map "' + os.path.abspath(caseDemMin) + '" is not a PCRaster map. Will use "' + os.path.abspath(caseDemMin) + '" instead for coastal downscaling!')
        caseDemMin = caseDem
        closeLogger(logger, ch)
        sys.exit(2)

    # downscaleLoc = os.path.join(caseFolder,runId,region)         # location where downscaled results are stored

    # write to temporary maps
    resampleMap(os.path.join(downscaleLoc,"uniqueid.map"),os.path.join(downscaleLoc,"uniqueid_target.map"),caseDem) # ????? nearest neighbour
    resampleMap(cellarea_file, os.path.join(downscaleLoc,"cellarea_target.map"),caseDem)
    cellarea_target = readmap(os.path.join(downscaleLoc,"cellarea_target.map"))

    # derive maximum anual flood volumes and save to PCRaster maps
    for n in np.arange(0, nrExtremes):
        max_heightav_diff = np.flipud(vol_relevant[n,:,:])
        # max_heightav_diff[isnan(max_heightav_diff)] = -9999
        max_vol_pcr = max_heightav_diff*pcr2numpy(cellarea, np.nan)
        ## make a PCR-object
        #max_heightav_pcr = numpy2pcr(Scalar,max_heightav_diff,-9999)
        #
        # max_vol_pcr = max_heightav_pcr*cellarea
        vol_mapFile = os.path.join(downscaleLoc,str("volume00."+"%03.f") % (n+1))
        vol_maptargetFile = os.path.join(downscaleLoc,str("volume_t."+"%03.f") % (n+1))
        # report(max_vol_pcr,vol_mapFile)
        max_vol_pcr[np.isnan(max_vol_pcr)] = -9999
        writeMap(vol_mapFile, 'PCRaster', np.arange(-179.75,180,0.5), np.arange(89.75,-90,-0.5), max_vol_pcr, -9999)
        # resample map of volume per cell to target
        resampleMap(vol_mapFile,vol_maptargetFile,caseDem) # ????? nearest neighbour
        #os.unlink(vol_mapFile)


    #### PERFORM OPERATIONS WITH DEM FOR RIVER AND COASTAL #####
    ## set target area as clone
    setclone(caseDem)
    dem = readmap(caseDem)
    dem_min = readmap(caseDemMin)
    try:
        ldd = readmap(caseLdd)
        logger.info('LDD has been read from ' + os.path.abspath(caseLdd))
    except:
        logger.info('Creating LDD in ' + os.path.abspath(caseLdd))
        ldd = lddcreate(dem,1e31,1e31,1e31,1e31)      # make a local drain direction map
        report(ldd, caseLdd)
    # area_target     = readmap(os.path.join(downscaleLoc,"cellarea_target.map"))

    uniqueid_target = readmap(os.path.join(downscaleLoc,"uniqueid_target.map"))
    exposure        = dem*0
    # compute surface area of each pixel with geographical functions
    # yc = float64(pcr2numpy(ycoordinate(defined(area_target)),-9999))
    # xc = float64(pcr2numpy(xcoordinate(defined(area_target)),-9999))
    yc = pcr2numpy(ycoordinate(defined(cellarea_target)),-9999)
    xc = pcr2numpy(xcoordinate(defined(cellarea_target)),-9999)
    xax = xc[0,:]
    yax = np.flipud(yc[:,0])
    xres = xc[0,1]-xc[0,0]
    yres = yc[0,0]-yc[1,0]
    conv_factor = (0.5/yres)*(0.5/xres)
    surf = cellarea_target/conv_factor
    del yc, xc
    # prepare the target NetCDF file
    prepare_nc(caseFile, caseFile_ref, FileOut, xax, yax, stream_thres, relevant_T)

    # now process per return period
    for n in np.arange(0, nrExtremes):
        if p_relevant[n] > 0:
            # compute downscaled flood map
            logger, ch, floodedLand = downscale(n, ldd, stream_thres, conv_factor, logger, ch)
        else:
            logger.info("Volume below bank-full, no downscaling performed for volume_t." + "%03.f" % (n+1))
            floodedLand = dem*0
        if do_coastal:
            # also compute coastal flood hazard and add to hazard map

            floodedLandCoastal = cover(coastal_hazard(10, 0.3, DIVAXls, dem_min, ldd, 100), 0)
            floodedLand = max(floodedLand, floodedLandCoastal)
        flood_scaled = max(min((floodedLand-h_min_impact)/(h_max_impact-h_min_impact),1),0)
        exposure     = exposure + flood_scaled*weight
        # write to netCDF file
        nc_trg = Dataset(FileOut,'a')
        var_trg = nc_trg.variables['water_level']
        var_trg[n,:,:] = np.flipud(pcr2numpy(floodedLand, -9999))
        nc_trg.sync()
        nc_trg.close()
        # DEPRECATED, reporting to PCRaster files should be abandoned
        report(floodedLand,os.path.join(downscaleLoc,str('flood000.' + '%03.f') % (n + 1)))
        os.unlink(os.path.join(downscaleLoc,str("volume_t."+"%03.f") % (n+1)))

    # DEPRECATED: finally report the effective exposure map (REMOVE THIS IN TERM)
    report(exposure,os.path.join(downscaleLoc,'relative_damage.map'))
    # remove unnecessary files
    # os.unlink(os.path.join(downscaleLoc,"cellarea_target.map"))
    os.unlink(os.path.join(downscaleLoc,"uniqueid_target.map"))
    # now combine with GDP map
    # now combine with population map

    os.unlink(os.path.join(downscaleLoc,'uniqueid.map'))
    logger.info('GLOFRIS_downscale is done!')
    closeLogger(logger, ch)
except:
    logger.error('Unknown error occurred, exiting...')
    logger.error(traceback.print_exc())
    closeLogger(logger, ch)
    sys.exit(2)

