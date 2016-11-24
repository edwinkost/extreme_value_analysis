# -*- coding: utf-8 -*-
"""
Created on Fri May 25 09:29:27 2012

@author: Mark Hegnauer

Create Minimum Dem

This script is developed in order to produce low resolution DEM's with either the minimum value, maximum value or mean value per grid cell.
The script contains three functions: translateMap, checkerboard and createDEM.
The script can download and process the srtm data into minimum, maximum
"""

import numpy as np
import urllib
import zipfile
import os, sys
from PCRaster import *
from PCRaster.Framework import *
from PCRaster.NumPy import *
from osgeo import gdal
from subprocess import *
import gdal_merge
import glob


def translateMap(origMap,transMap):
  """
  translateMap translates the tif formatted files from the srtm to PCRaster .map files
  origMap = your_map.tif
  transMap= your_map.map
  """
  command= 'gdal_translate -of PCRaster -ot Float32 -a_nodata -32768  %s %s' % (origMap,transMap)
  os.system(command)

def translateBack(origMap,transMap):
  """
  translateMap translates the tif formatted files from the srtm to PCRaster .map files
  origMap = your_map.map
  transMap= your_map.tif
  """
  command= 'gdal_translate -of GTiff -ot Int16 -a_nodata -32768 %s %s' % (origMap,transMap)
  os.system(command)

def cutMap(xmin, ymin, xmax, ymax, origMap,transMap):
    """
    cutMap prepares a cut from a large GeoTIFF map
    xmin, xmax, ymin, ymax :    the selection window
    origMap:                    the original GeoTIFF
    transMap:                   The cut geotiff
    """
    command = 'gdal_translate -a_nodata -32768 -ot Float32 -projwin %f %f %f %f %s %s' % (xmin, ymax, xmax, ymin, origMap, transMap)
    os.system(command)

def checkerboard(mapin,fcc):
    """
    checkerboard create a checkerboard map with unique id's in a
    fcc*fcc cells large area. The resulting map can be used
    to derive statistics for (later) upscaling of maps (using the fcc factor)

    CAUTION: use with unitcell to get most reliable results!

    Input: map (used to determine coordinates), fcc (size of the areas in cells)
    Output: checkerboard type map
    """
    trueFalse = boolean(mapin*0+1)
    ymin = mapminimum(ycoordinate(trueFalse))
    yc = (ycoordinate(trueFalse)-ymin)/celllength()
    yc = rounddown(yc/fcc)
    xmin = mapminimum(xcoordinate(trueFalse))
    xc = (xcoordinate(trueFalse) - xmin)/celllength()
    xc = rounddown(xc/fcc)
    yc = yc * (mapmaximum(xc) + 1.0)
    xy = ordinal(xc + yc)

    return xy

def resample_map(scale, srcdem,resampledem):
  """
  resample_map is used to resample the high resolution dem's to low resolution
  dem's.
  xmin,xmax,ymin,ymax creates the window of the dem
  xres,yres is the cellLength in x and y direction
  srcdem is the high resolution dem
  destdem is the low resolution dem
  """
  command = 'gdal_translate -outsize %g%% %g%% %s %s' % (scale, scale, srcdem, resampledem)
  os.system(command)

def removeFiles(wildCard):
    filelist = glob.glob(wildCard)
    for filename in filelist:
        os.unlink(filename)

def retrieve_SRTM(url_prefix, file_prefix, url_suffix, demLoc, case, xmin, ymin, xmax, ymax):
    """
    This function retrieves an SRTM DEM from the designated location, merges it together into a dem for a wanted target area
    Inputs:
        url_prefix:     the website where the SRTM tiles are located
        file_prefix:    file prefix of SRTM tile files
        url_suffix:     file suffix of SRTM tile files
        demLoc:         Folder where SRTM data should go to
        case:           Name of the DEM file to be used
        xmin:           minimum longitude
        xmax:           maximum longitude
        ymin:           minimum latitude
        ymax:           maximum latitude
    Outputs:
        A DEM over wanted area in original resolution at designated location and filename. Provided in GeoTIFF and PCRaster
    """
    # url_prefix=http://droppr.org/srtm/v4.1/6_5x5_TIFs/
    # url_prefix=ftp://srtm.csi.cgiar.org/SRTM_v41/SRTM_Data_GeoTIFF/
    tileMinX=np.int((np.round(xmin) + 180 ) / 5 + 1)
    tileMaxX=np.int((np.round(xmax) + 180 ) / 5 + 1)
    tileMinY=np.int((60 - np.round(ymax) ) / 5 + 1)
    tileMaxY=np.int((60 - np.round(ymin) ) / 5 + 1)
    print str('Retrieving DEM tiles minX: %3.2f maxX: %3.2f, minY: %3.2f, maxY: %3.2f') % (tileMinX, tileMaxX, tileMinY, tileMaxY)
    # compute UTM zone
    tileLat=tileMinY-1
    tileLon=tileMinX-1
    for tileLon in range(tileMinX, tileMaxX+1):
        for tileLat in range(tileMinY, tileMaxY+1):
            try:
                fileName = str(file_prefix + '%02.f_%02.f' + url_suffix) % (tileLon, tileLat)
                url = url_prefix + fileName
                fileTarget = os.path.join(demLoc, fileName)
                print 'Retrieving ' + url
                urllib.urlretrieve(url,fileTarget)
                print 'Unzipping %s' %(fileTarget)
                zf = zipfile.ZipFile(fileTarget , 'r')
                nameList = zf.namelist()
                for n in nameList:
                    outFile = open(os.path.join(demLoc, n), 'wb')
                    outFile.write(zf.read(n))
                    outFile.close()
                zf.close()
                os.unlink(fileTarget)
            except:
                print 'No suitable tile found, going to next tile...'
            # call gdal_merge to stitch everythin together
    temporary_dem = os.path.join(demLoc, 'temp.tif')
    cut_dem       = os.path.join(demLoc, case + '_rawSRTM.tif')
    pcr_dem       = os.path.join(demLoc, case + '_rawSRTM.map')
    source_dems   = os.path.join(demLoc, 'srtm*.tif')
    gdal_merge.main(argv=['dummy','-o', temporary_dem, source_dems])
    cutMap(xmin, ymin, xmax, ymax, temporary_dem, cut_dem) # this is the final lat lon map
    translateMap(cut_dem,pcr_dem)
    removeFiles(os.path.join(demLoc, 'srtm*.tif'))
    removeFiles(os.path.join(demLoc, 'srtm*.hdr'))
    removeFiles(os.path.join(demLoc, 'srtm*.tfw'))
    os.unlink(os.path.join(demLoc, 'readme.txt'))
    os.unlink(os.path.join(demLoc, 'temp.tif'))

    return pcr_dem

def mean_min_max_dem(demLoc, case, scale):
    """
    This function resamples a map from high to lower resolution according to a scale factor.
    It returns a mean value and a minimum value map.
    Input:
        demLoc:     Folder location of source elevation model
        case:       Name of the case
        scale:      Reduction scale (e.g. 10 means the resolution becomes 10 times lower in both directions)
    """
    pcr_dem = os.path.join(demLoc, case + '_rawSRTM.map')
    demmin_file = os.path.join(demLoc, case + '_rawSRTM_min.map')
    demmean_file = os.path.join(demLoc, case + '_rawSRTM_mean.map')
    setclone(pcr_dem)
    print 'Reading DEM to memory'
    dem = readmap(pcr_dem)
    print 'Use checkerbox'
    ck = checkerboard(dem,scale)
    print 'Create minimum DEM'
    demmin = areaminimum(dem,ck)
    demmean= areaaverage(dem,ck)
    # demmax = areamaximum(dem,ck)
    report(demmin, demmin_file)
    report(demmean,demmean_file)

def run_createDEM(xmin,ymin,xmax,ymax,demLoc, case):
    """
    run_createDEM is used to run the createDEM function and to resample and
    translate the created DEM to a usable format for the coastal module.
    xmin,xmax,ymin,ymax creates the window of the dem
    scale is the factor over which to use the checkerboard function
    cellLen is the length of the cells

    e.g.: scale and cellLen need to be adjusted accordingly
    It has been used as: scale = 10, cellLen = 1/120.0, which creates a DEM with
    10 times less cells along an axis.
    """
    url_prefix='ftp://xftp.jrc.it/pub/srtmV4/tiff/'
    file_prefix='srtm_'
    url_suffix='.zip'
    scale = 10
    pcr_dem = retrieve_SRTM(url_prefix, file_prefix, url_suffix, demLoc, case, xmin, ymin, xmax, ymax)
    mean_min_max_dem(demLoc, case, scale)
    demmin_file = os.path.join(demLoc, case + '_rawSRTM_min.map')
    demmean_file = os.path.join(demLoc, case + '_rawSRTM_mean.map')
    demmin_reduced_file = os.path.join(demLoc, case + '_min.map')
    demmean_reduced_file = os.path.join(demLoc, case + '.map')
    resample_map(scale,demmin_file,demmin_reduced_file)
    resample_map(scale,demmean_file,demmean_reduced_file)
    os.unlink(demmin_file);os.unlink(demmean_file)

try:
    # print sys.argv[1:]
    #config_file = os.path.abspath(sys.argv[1])
    workFolder   = os.path.split(sys.argv[0])[0]        # location of downscale executable
    xmin = np.float(sys.argv[1])
    ymin = np.float(sys.argv[2])
    xmax = np.float(sys.argv[3])
    ymax = np.float(sys.argv[4])
    demFolder    = os.path.abspath(sys.argv[5])            # DEM folder
    region       = sys.argv[6]                             # Name of region
    # demRaiseFile = os.path.join(demFolder, region + '_raised.map')  # Name of raised DEM
    if not os.path.isdir(demFolder):
        os.makedirs(demFolder)
except:
    noArgExitStr = str('****************      GLOFRIS SRTM downloader       *****************\n' + \
    '$Id: GLOFRIS_SRTM.py 733 2013-07-03 06:32:48Z winsemi $\n' + \
    '$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $\n' + \
    '$Author: winsemi $\n' + \
    '$Revision: 733 $\n' + \
    'GLOFRIS SRTM downloader downloads an SRTM elevation model and prepares it for GLOFRIS downscaling. \n ' + \
    'During this preparation, all required SRTM tiles are downloaded, aggregated to the user-defined extent. \n ' + \
    'Finally, the mean and minimum over a 10x10 pixel-area (approx. 1x1 km2) is calculated. These two maps can be \n' + \
    'directly and automatically used in the GLOFRIS downscaling.  \n ' + \
    '- The mean dem is used to downscale river flooding to appropriate resolutions. \n ' + \
    '- The minimum dem is used to downscale coastal flooding from DIVA. \n\n ' + \
    '- The full 90x90 meter resolution dem is also maintained in both GeoTIFF and PCRaster format.\n\n ' + \
    'GLOFRIS_SRTM runs as follows: \n' + \
    '======================================================================================================================== \n' + \
    'GLOFRIS_SRTM <xmin> <ymin> <xmax> <ymax> <DEM output location> <Name of region> \n' + \
    '======================================================================================================================== \n' + \
    '<xmin>:                    minimum longitude coordinate \n' + \
    '<ymin>:                    minimum latitude coordinate \n' + \
    '<xmax>:                    maximum longitude coordinate \n' + \
    '<ymax>:                    maximum latitude coordinate \n' + \
    '<DEM output location>:     path where elevation models should be stored\n' + \
    '<Name of region>:          User-defined name of the region that is downloaded\n\n' + \
    'NOTE: sometimes the download site for SRTM DEMs stalls. In that case break the process with Ctrl+C and try again!\n' + \
    'NOTE: very large areas may cause memory problems, If you want a very large area, \n' + \
    'please do this in smaller parts and merge afterwards.')
    print noArgExitStr
    sys.exit(2)


# Example for Myanmar
run_createDEM(xmin,ymin,xmax,ymax, demFolder, region)