# -*- coding: utf-8 -*-
"""
GLOFRIS_utils.py contains several standard functions to be used in the GLOFRIS system

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

$Id: GLOFRIS_utils.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/GLOFRIS_utils.py $
$Keywords: $

# Modified/adopted by Edwin H. Sutanudjaja, starting on 24 November 2016

"""

import netCDF4 as nc4
import osgeo.gdal as gdal
from osgeo.gdalconst import *
from numpy import *
from scipy import *
import glob
import datetime as dt
import sys
import os, gzip, zipfile
#import matplotlib.pyplot as plt
import logging
import logging.handlers
#import pdb
import subprocess
#from mpl_toolkits.basemap import Basemap, cm, NetCDFFile

def recursive_glob(rootdir='.', suffix=''):
    """
    Prepares a list of files in location rootdir, with a suffix
    input:
        rootdir:    string, path-name
        suffix:     suffix of required files
    output:
        fileList:   list-strings, file paths and names
    """

    fileList = [os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(rootdir)
            for filename in filenames if filename.endswith(suffix)]
    return fileList
    
def purge_folder(rootdir, recursive=True):
    """
    Purges all files in a folder, including its subfolders
    """
    if recursive:
        fileList = recursive_glob(rootdir=rootdir)
    else:
        fileList = glob.glob(os.path.join(rootdir), '*')
    # now delete any files but keep folders
    for fileName in fileList:
        if os.path.isfile(fileName):
            os.unlink(fileName)

def lookup_climate_files(srcFolder, inputVars, startDate, endDate, timestep=dt.timedelta(days=1), srcFiles=[], lookup_table={}):
    """
    Generates or appends a dictionary of dates and references to files for each date and variable of interest
    The function checks for each date and each variable, which file in the srcFolder contains the variable
    of interest at the date of interest
    """
    if len(lookup_table) == 0:
        # lookup_table is still empty. Fill lookup_table with dates and empty strings
        # make list of all dates
        dateList = []
        curDate  = startDate
        while curDate <= endDate:
            dateList.append(curDate)
            curDate += timestep
        lookup_table['time'] = dateList
        # pre-fill the dictionary with lists of empty strings for each file
        for inputVar in inputVars:
            lookup_table[inputVar] = empty(len(dateList),'S1000')
        
    # make list of all available files
    if len(srcFiles) == 0:
        srcFiles = recursive_glob(rootdir=srcFolder, suffix='.nc')
        srcFiles.sort()
    
    for srcFile in srcFiles:
        print 'Scanning ' + srcFile
        nc_src  = nc4.Dataset(srcFile, 'r')
        time    = nc_src.variables['time']
        try:
            timeObjRaw = nc4.num2date(time[:], units=time.units, calendar=time.calendar)
        except:
            timeObjRaw = nc4.num2date(time[:], units=time.units, calendar='gregorian')
        # UUGGGHHH: this seems to be a bug. calendar other than gregorian give other objects than 
        # datetime.datetime objects. Here we convert to a year with a julian day string, then back to date objects
        timeObj = []
        for t in timeObjRaw:
            timeObj.append(dt.datetime.strptime(t.strftime('%Y%j'),'%Y%j'))
        #timeObj = nc4.num2date(nc4.date2num(timeObj, units=time.units, calendar='gregorian'), units=time.units, calendar='gregorian')
        # now loop over all time steps, check the date and write valid dates to a list, write time series to PCRaster maps
        for n in range(len(timeObj)):
            # remove any hours or minutes data from curTime
            timeObj[n] = timeObj[n].replace(hour=0)
            timeObj[n] = timeObj[n].replace(minute=0)
            
        # check for first and last date in timeObj
        firstDate = timeObj[0]
        lastDate  = timeObj[-1]
        # find locations of firstDate and lastDate in our target time periods
        idxStart  = where(array(lookup_table['time']) == firstDate)[0]
        idxEnd    = where(array(lookup_table['time']) == lastDate)[0]
        if len(idxStart) == 1 or len(idxEnd == 1):
            if len(idxStart) == 0:
                idxStart = array([0])
            if len(idxEnd) == 0:
                idxEnd   = len(dateList)-1
            allVars = nc_src.variables.keys()
            # check which variables are present in file, check file
            for inputVar in inputVars:
                if inputVar in allVars:
                    lookup_table[inputVar][idxStart:idxEnd+1] = srcFile
        nc_src.close()
    return lookup_table

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
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    x = linspace(originX+resX/2,originX+resX/2+resX*(cols-1),cols)
    y = linspace(originY+resY/2,originY+resY/2+resY*(rows-1),rows)
    # Retrieve raster
    RasterBand = ds.GetRasterBand(1) # there's only 1 band, starting from 1
    data = RasterBand.ReadAsArray(0,0,cols,rows)
    FillVal = RasterBand.GetNoDataValue()
    RasterBand = None
    ds = None
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
    
def setlogger(logfilename, logReference):
    """
    Set-up the logging system. Exit if this fails
    """
    try:
        #create logger
        logger = logging.getLogger(logReference)
        logger.setLevel(logging.DEBUG)
        ch = logging.handlers.RotatingFileHandler(logfilename,maxBytes=10*1024*1024, backupCount=5)
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

def closeLogger(logger, ch):
    logger.removeHandler(ch)
    ch.flush()
    ch.close()
    return logger, ch

def readOUT(file,year):
    """
    Reads .OUT file from IMAGE 2.4 and retrieves the numbers for all world regions
    """
    nrLandCovs = 20
    yearstr = str(year) + '\n'
    fid = open(file,'r')
    data = fid.readlines()
    header = data[0].split(';')
    unit = header[1].split('= ')[1]
    label = header[2].split('= ')[1]
    table = data[2:]
    linenr = 0
    while table[linenr]!=yearstr:
        linenr = linenr + 1
    linenr = linenr + 1
    records = table[linenr:linenr+nrLandCovs]
    n = 0
    for record in records:
        recordSep = record.rsplit()
        if not('recTable' in locals()):
            recTable = zeros((len(records),len(recordSep)-1))
        recTable[n,:] = recordSep[0:-1]
        if float(recordSep[-1]) > 0:
            recTable[n,:] = recTable[n,:]/float(recordSep[-1]) # Last value is total surface.
        n = n + 1

    return recTable

def readUNF(fileName, worldncFile):
    """ Read UNF file into memory, until now only UNF0 is supported, can easily
    be extended to support:
    UNF0: F real(4)
    UNF1: F byte
    UNF2: F short
    UNF4: F integer 4
    Output given is LON, LAT and GRID, the last provides an array [t,lat,lon], where
    t is the amount of layers of the UNF0 file.
    """

    # Prepare final grid
    LAT = arange(-89.75,90,0.5)
    LON = arange(-179.75,180,0.5)

    # now read the actual data and write to correct coordinate positions
    dataFid = open(fileName, 'rb')
    # format of data is as follows:

    data    = fromfile(dataFid, dtype='f4')
    dataFid.close()

    # Open the coordinate file fo grid definition and read!
    coordFid = open(worldncFile, 'r')
    # skip the 15-line header of the worldnc file
    for n in arange(0,15):
        coordFid.readline()
    allLines = coordFid.readlines()
    nrOfPix  = len(allLines)
    # determine amount of grids in UNF file
    nrOfGrids = len(data)/nrOfPix
    print 'Reading number of grids in %s: %g' % (fileName, nrOfGrids)
    # all coordinates read, close file
    coordFid.close()
    # now set up the grid
    GRID = empty((nrOfGrids,len(LAT),len(LON)))
    GRID[:] = nan
    lon = zeros(len(allLines))
    lat = zeros(len(allLines))
    x   = zeros(lon.shape,dtype=int)
    y   = zeros(lon.shape,dtype=int)
    count = 0
    for linestr in allLines:
        line = linestr.split()
        lon[count] = 0.25 + float(line[0])
        lat[count] = 0.25 + float(line[1])
        y[count]   = round((lat[count]+89.75)/0.5)
        x[count]   = round((lon[count] - (-179.75))/0.5)
        for layer in arange(0,nrOfGrids):
            GRID[layer,y[count],x[count]] = data[nrOfGrids*count+layer]
        count = count + 1
    # coordinates are now known and data appointed to them!!
    return LON, LAT, GRID

def writeUNF(grid, fileName, worldncFile):
    """ Write UNF file from lon, lat, grid[t,lat,lon], until now only UNF0 is supported, can easily
    be extended to support:
    UNF0: F real(4)
    UNF1: F byte
    UNF2: F short
    UNF4: F integer 4
    No output is given
    """

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

def Gzip(fileName, storePath=False, chunkSize=1024*1024):
        """
        Usage: Gzip(fileName, storePath=False, chunksize=1024*1024)
        Gzip the given file to the given storePath and then remove the file.
        A chunk size may be selected. Default is 1 megabyte
        Input:
            fileName:   file to be GZipped
            storePath:  destination folder. Default is False, meaning the file will be zipped to its own folder
            chunkSize:  size of chunks to write. If set too large, GZip will fail with memory problems
        """
        if not storePath:
            pathName = os.path.split(fileName)[0]
            fileName = os.path.split(fileName)[1]
            curdir   = os.path.curdir
            os.chdir(pathName)
        # open files for reading / writing
        r_file = open(fileName, 'rb')
        w_file = gzip.GzipFile(fileName + '.gz', 'wb', 9)
        dataChunk = r_file.read(chunkSize)
        while dataChunk:
            w_file.write(dataChunk)
            dataChunk = r_file.read(chunkSize)
        w_file.flush()
        w_file.close()
        r_file.close()
        os.unlink(fileName) #We don't need the file now
        if not storePath:
            os.chdir(curdir)

def zipFiles(fileList, fileTarget):
    """
    Usage: zipFiles(fileList, fileTarget)
    zip the given list of files to the given target file
    Input:
        fileList:   list of files to be zipped
        fileTarget: target zip-file
    """
    zout = zipfile.ZipFile(fileTarget, "w", compression=zipfile.ZIP_DEFLATED)
    for fname in fileList:
        zout.write(fname, arcname=os.path.split(fname)[1])
    zout.close()

def unzip_all(srcFile, trgFolder):
    """
    Usage: unzip_all(srcFile, trgFolder)
    Unzips the full content of srcFile to trgFolder
    Input:
        srcFile:    - string    - path to source zip-file
        trgFolder:  - string    - path to target
    """
    zip_ref = zipfile.ZipFile(srcFile, 'r')
    zip_ref.extractall(trgFolder)
    zip_ref.close()
            
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def prepare_nc(trgFile, year, x, y, metadata, logger, units='Days since 1900-01-01 00:00:00', calendar='gregorian'):
    """
    This function prepares a NetCDF file with given metadata, for a certain year, daily basis data
    The function assumes a gregorian calendar and a time unit 'Days since 1900-01-01 00:00:00'
    """
    logger.info('Setting up "' + trgFile + '"')
    startDayNr = nc4.date2num(dt.datetime(year, 1, 1, 0, 0), units=units, calendar=calendar)
    endDayNr   = nc4.date2num(dt.datetime(year + 1, 1, 1, 0, 0), units=units, calendar=calendar)
    time       = arange(startDayNr,endDayNr)
    nc_trg     = nc4.Dataset(trgFile,'w')
    logger.info('Setting up dimensions and attributes')
    nc_trg.createDimension('time', 0) #NrOfDays*8
    nc_trg.createDimension('lat', len(y))
    nc_trg.createDimension('lon', len(x))
    DateHour = nc_trg.createVariable('time','f8',('time',))
    DateHour.units = units
    DateHour.calendar = calendar
    DateHour.standard_name = 'time'
    DateHour.long_name = 'time'
    DateHour[:] = time
    y_var = nc_trg.createVariable('lat','f4',('lat',))
    y_var.standard_name = 'latitude'
    y_var.long_name = 'latitude'
    y_var.units = 'degrees_north'
    x_var = nc_trg.createVariable('lon','f4',('lon',))
    x_var.standard_name = 'longitude'
    x_var.long_name = 'longitude'
    x_var.units = 'degrees_east'
    y_var[:] = y
    x_var[:] = x
    projection= nc_trg.createVariable('projection','c')
    projection.long_name = 'wgs84'
    projection.EPSG_code = 'EPSG:4326'
    projection.proj4_params = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    projection.grid_mapping_name = 'latitude_longitude'

    # now add all attributes from user-defined metadata
    for attr in metadata:
        nc_trg.setncattr(attr, metadata[attr])
    nc_trg.sync()
    nc_trg.close()

def write_pcr_timeseries(lookup_table, srcVar, trgFolder, trgPrefix, logger, slope=1., offset=0., year=False, remove_missings=True):
    # if necessary, make trgPrefix maximum of 8 characters
    if len(trgPrefix) > 8:
        trgPrefix = trgPrefix[0:8]
    # prepare a counter for the number of files with non-missing values
    count = 0
    timeList = []
    # establish the points in the lookup_table where the dates of interest are located
    startDate = dt.datetime(year,  1,  1, 0, 0)
    endDate   = dt.datetime(year, 12, 31, 0, 0)
    allDates  = lookup_table['time']
    idxs      = where(logical_and(array(allDates) >= startDate, array(allDates) <= endDate))[0]
    
    # start with an empty string to compare with
    srcFile = ''
    for idx in idxs:
        if logical_and(lookup_table[srcVar][idx] != srcFile, lookup_table[srcVar][idx] != ''):
            # read a new source netCDF file
            if srcFile != '':
                # if we are not reading the first time, then close the previous file
                nc_src.close()
            # set the new source file and open it and read x and y-axis and time and the variable of interest
            srcFile = lookup_table[srcVar][idx]
            nc_src = nc4.Dataset(srcFile, 'r')
            # read axis, try 'lat' otherwise try 'latitude'
            try:
                y = nc_src.variables['lat'][:]
            except:
                y = nc_src.variables['latitude'][:]
        
            try:
                x = nc_src.variables['lon'][:]
            except:
                x = nc_src.variables['longitude'][:]
            # read time axis and convert to time objects
            time = nc_src.variables['time']
            timeObjRaw = nc4.num2date(time[:], units=time.units, calendar=time.calendar)
            # UUGGGHHH: this seems to be a bug. calendar other than gregorian give other objects than 
            # datetime.datetime objects. Here we convert to gregorian numbers, then back to date objects
            timeObj = []
            for t in timeObjRaw:
                timeObj.append(dt.datetime.strptime(t.strftime('%Y%j'),'%Y%j'))
#            timeObj = nc4.num2date(nc4.date2num(timeObj, units=time.units, calendar='gregorian'), units=time.units, calendar='gregorian')
            # now loop over all time steps, check the date and write valid dates to a list, write time series to PCRaster maps
            for n in range(len(timeObj)):
                # remove any hours or minutes data from curTime
                timeObj[n] = timeObj[n].replace(hour=0)
                timeObj[n] = timeObj[n].replace(minute=0)
            # Read the variable of interest
            nc_var = nc_src.variables[srcVar]

        #### Correct file is read, now read in position ####
        # look up the position in the current file, where the current time step is located
        curTime = allDates[idx]
        location = where(array(timeObj)==curTime)[0]
        if len(location) == 1:
            # in case of a difference in the used calendar, there may be one or more missing days in a year. 
            # These are accounted for by ignoring dates that are not found inside the input data files
            curGrid = nc_var[location[0],:,:]
            if remove_missings:
                if hasattr(curGrid, 'mask'):
                    curMask = curGrid.mask
                    curGrid = curGrid.data
                    curGrid[curMask] = nan
                # check if grid contains valid values
                pixloc = where(isfinite(curGrid))  # != nc_var._FillValue)[0]
                if len(pixloc) > 0:
                    # there are valid values, so write to a PCRaster map and add time to list
                    timeList.append(curTime)
                    count += 1
                    below_thousand = count % 1000
                    above_thousand = count / 1000
                    pcraster_file  = str(trgPrefix + '%0' + str(8-len(trgPrefix)) + '.f.%03.f') % (above_thousand, below_thousand)
                    pcraster_path = os.path.join(trgFolder, pcraster_file)
                    logger.debug('Writing "' + srcVar + '" on date ' + curTime.strftime('%Y-%m-%d') + ' to ' + pcraster_path)
                    # prepare grid for writing to file
                    trgGrid = curGrid*slope+offset;trgGrid[isnan(trgGrid)] = nc_var._FillValue
                    # write grid to PCRaster file
                    if y[1]-y[0] > 0.:
                        # the y-axis is ascending, flip the y axis and the target grid!
                        writeMap(pcraster_path, 'PCRaster', x, flipud(y), flipud(trgGrid), float(nc_var._FillValue))
                    else:
                        writeMap(pcraster_path, 'PCRaster', x, y, trgGrid, float(nc_var._FillValue))
        else:
            logger.debug('"' + srcVar + '" not available on date ' + curTime.strftime('%Y-%m-%d'))
    nc_src.close()
    return timeList
                        
def write_netcdf_timeseries(srcFolder, srcPrefix, trgFile, trgVar, trgUnits, trgName, timeList):
    # if necessary, make trgPrefix maximum of 8 characters
    if len(srcPrefix) > 8:
        srcPrefix = srcPrefix[0:8]
    # Open target netCDF file
    nc_trg = nc4.Dataset(trgFile, 'a')
    # read time axis and convert to time objects
    time = nc_trg.variables['time']
    timeObj = nc4.num2date(time[:], units=time.units, calendar=time.calendar)
    try:
        nc_var = nc_trg.variables[trgVar]
    except:
        # prepare the variable
        nc_var = nc_trg.createVariable(trgVar, 'f4', ('time', 'lat', 'lon',), fill_value=-9999., zlib=True)
        nc_var.units = trgUnits
        nc_var.standard_name = trgName
    # now loop over all time steps, check the date and write valid dates to a list, write time series to PCRaster maps
    for nn, curTime in enumerate(timeList):
        idx = where(timeObj==curTime)[0]
        count = nn + 1
        below_thousand = count % 1000
        above_thousand = count / 1000
        
        # read the file of interest
        pcraster_file  = str(srcPrefix + '%0' + str(8-len(srcPrefix)) + '.f.%03.f') % (above_thousand, below_thousand)
        pcraster_path = os.path.join(srcFolder, pcraster_file)
        # write grid to PCRaster file
        x, y, data, FillVal = readMap(pcraster_path, 'PCRaster')
        data[data==FillVal] = nc_var._FillValue
        nc_var[idx,:,:] = flipud(data)
    nc_trg.sync()
    nc_trg.close()
    #return timeList

def run_model_year(purgeFolders, instateZip, instateFolder, endstateZip, endstateFolder, lookup_table, inputVars, inputFolders, inputPrefixs, inputSlopes, inputOffsets, year, modelPath, command, logger, arguments='', logFileModel=os.devnull):
    """
    Run a model at a given location with a certain command. 
    Before the model is run, an initial state is unzipped to a designated folder
    After the model run, the last state is again zipped to a designated file.
    
    The user must ensure that the correct command and arguments (e.g. time period, or other runtime info)
    is given.
    
    Inputs:
        modelPath:      string      -- path to the model
        instateZip:     string      -- path to initial state of the model
        instateFolder:  string      -- path where to unzip the initial state file
        endstateZip:    string      -- path to the end state zip file of the model
        endstateFolder: string      -- path where end states are written by the model
        lookup_table:   dictionary  -- Contains the relevant dates for the complete run period along with the file path for each relevant variable per time step
        inputVars:      list        -- contains strings referring to variables in the source files in lookup_table
        inputFolders:   list        -- contains paths (one per input variables) where inputs should be written to
        inputPrefixs:   list        -- contains strings, prefix of file names (no longer than 8 characters) of PCRaster input time series
        command:        string      -- command used to start the model
        arguments:      string      -- (set of) input argument(s) for model runtime
        
    """
    # TO-DO PURGE ACTIVITIES IN INPUT/OUTPUT/STATE FOLDERS
    for folder_to_purge in purgeFolders:
        purge_folder(folder_to_purge)
    # first unpack the states
    unzip_all(instateZip, instateFolder)
    # prepare all PCRaster time series
        # prepare the PCRaster time series
    timeLists = []
    try:
        for inputVar, inputFolder, inputPrefix, inputSlope, inputOffset in zip(inputVars, inputFolders, inputPrefixs, inputSlopes, inputOffsets):
            timeList = write_pcr_timeseries(lookup_table, inputVar, inputFolder, inputPrefix, logger, slope=inputSlope, offset=inputOffset, year=year, remove_missings=True)
            timeLists.append(timeList)
    except:
        logger.error(sys.exc_info())
        logger.info('Please check if all input files are valid NetCDF file and contain the correct variables.')
        closeLogger(logger, ch)
        sys.exit(2)
    # check if the number of time steps of each input is the same
    nrOfTimeSteps = len(timeLists[0])
    for timeList in timeLists[1:]:
        if len(timeList) != nrOfTimeSteps:
            logger.error('Number of time steps from the different model inputs are not the same')
            closeLogger(logger, ch)
            sys.exit(2)
    # all checks are done. Now run the model
    logger.info('Running for year: ' + str(year))
#    nrOfTimeSteps = 3 # TEST DEBUG!!!!
    curDir = os.getcwd()
    os.chdir(modelPath)
    system_command = str(command + ' ' + arguments) % nrOfTimeSteps
    system_command_list = system_command.split(' ')
    # change permission of executable so that it can be run by anyone and any process
    try:
        os.chmod(system_command_list[0],0o777)
    except:
        pass
    logger.info('Running with command: "' + system_command + '"')
    with open(logFileModel, 'w') as modelLog:
        result = subprocess.call(system_command_list, stdout=modelLog, stderr=modelLog)
    #os.system(system_command)
    # now zip all the end state files to the associated end state zip file
    endstateFiles = glob.glob(os.path.join(endstateFolder, '*.*'))
    zipFiles(endstateFiles, endstateZip)
    # go back to the original folder
    os.chdir(curDir)
    return timeList
