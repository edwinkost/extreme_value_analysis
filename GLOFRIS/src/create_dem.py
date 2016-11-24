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
from glob import glob


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
  
def checkerboard(mapin,fcc):
  """
  checkerboard create a checkerboard map with unique id's in a 
  fcc*fcc cells large area. The resulting map can be used
  to derive statistics for (later) upscaling of maps (using the fcc factor)
  
  CAUTION: use with unitcell to get most reliable results!
  
  Input: map (used to determine coordinates), fcc (size of the areas in cells)
  Output: checkerboard type map
  """
  ymin = mapminimum(ycoordinate(boolean(mapin)))
  yc = (ycoordinate(boolean(mapin))-ymin)/celllength()
  yc = rounddown(yc/fcc)
  xmin = mapminimum(xcoordinate(boolean(mapin)))
  xc = (xcoordinate(boolean(mapin)) - xmin)/celllength()
  xc = rounddown(xc/fcc)
   
  yc = yc * (mapmaximum(xc) + 1.0)
  
  xy = ordinal(xc + yc)
  
  return xy

#def resample_map(xmin,xmax,ymin,ymax,xres,yres,srcdem,resampledem):
def resample_map(srcdem,resampledem, scale):
  """
  resample_map is used to resample the high resolution dem's to low resolution
  dem's. 
  xmin,xmax,ymin,ymax creates the window of the dem
  xres,yres is the cellLength in x and y direction 
  srcdem is the high resolution dem
  destdem is the low resolution dem
  """
  command = 'gdal_translate -outsize %g%% %g%% %s %s' % (scale, srcdem, resampledem)
#  command = 'gdalwarp -te %f %f %f %f -tr %s %s -srcnodata -32768 -dstnodata -32768 %s temp.tif' % (xmin,ymin,xmax,ymax,str(xres),str(yres),srcdem)
#  os.system(command)
#  command = 'gdal_translate -ot Float32 -of PCRaster -a_nodata -32768 temp.tif temp.map'
#  os.system(command) 
#  command = 'resample %s --clone temp.map %s' % (srcdem,resampledem)
#  os.system(command)
#  if os.path.isfile('temp.tif'):
#    os.remove('temp.tif')
#  elif os.path.isfile('temp.map'):
#    os.remove('temp.map')
  
def createDEM(xmin,xmax,ymin,ymax,upscalefactor):
  """
  createDEM creates a minimum/maximum/mean dem from srtm data. 
  Input is:
    xmin = left boundary of srtm map
    xmax = right boundary of srtm map
    ymin = lower boundary of srtm map
    ymax = upper boundary of srtm map
    upscalefactor = scale factor for upscaling the srtm 90*90 dem to another resolution
  """
  files = []
  os.chdir(r'd:/test//Demmin')
  url_prefix  = 'http://droppr.org/srtm/v4.1/6_5x5_TIFs/'
  file_prefix = 'srtm_'
  url_suffix  = '.zip'
  
  
  tileMinX = floor(( floor(xmin) + 180 ) / 5 + 1)
  tileMaxX = ceil(( ceil(xmax) + 180 ) / 5 + 1)
  tileMinY = floor(( 60 - floor(ymax) ) / 5 + 1)
  tileMaxY = ceil(( 60 - ceil(ymin) ) / 5 + 1)
  
  for tileLon in range(tileMinX,tileMaxX,1):
    for tileLat in range(tileMinY,tileMaxY,1):
      fileName = file_prefix + str('%02d' % tileLon) + '_' + str('%02d' % tileLat) + url_suffix 
      url= url_prefix + fileName
      if os.path.isfile('d://test//Demmin//SRTM_files//' + file_prefix + str('%02d' % tileLon) + '_' + str('%02d' % tileLat) + '_min'  + '.map'):
        print 'File allready created before'
      else:
        try:
          if os.path.isfile('d://test//Demmin//SRTM_files//' + file_prefix + str('%02d' % tileLon) + '_' + str('%02d' % tileLat) + '.zip'):
            print 'File allready created before'
          else:
            print 'Retrieving url'
            print url
            urllib.urlretrieve(url,'d://test//Demmin//SRTM_files//%s' %(fileName))
      
          print 'Unzipping %s' %(fileName)
          zf = zipfile.ZipFile('d://test//Demmin//SRTM_files//' +fileName , 'r') 
          nameList = zf.namelist()
          for n in nameList:
            print n
            outFile = open("%s\\%s" % (r"d://test//Demmin//SRTM_files//" , n), 'wb') 
            outFile.write(zf.read(n))
            outFile.close()
      
          print 'Translating Tif to Map'
          tiff_dem = 'd://test//Demmin//SRTM_files//' + file_prefix + str('%02d' % tileLon) + '_' + str('%02d' % tileLat) +'.tif' 
          map_dem  = 'd://test//Demmin//SRTM_files//' + file_prefix + str('%02d' % tileLon) + '_' + str('%02d' % tileLat) +'.map' 
          translateMap(tiff_dem,map_dem)
          
          setclone(map_dem)
          print 'Reading DEM to memory'
          dem = readmap(map_dem)
          print 'Use checkerbox'      
          ck = checkerboard(dem,upscalefactor)
          print 'Create minimum DEM'
          demmin = areaminimum(dem,ck)
#          demmean= areaaverage(dem,ck)
#          demmax = areamaximum(dem,ck)
          report(demmin, 'd://test//Demmin//SRTM_files//' + file_prefix + str('%02d' % tileLon) + '_' + str('%02d' % tileLat) + '_min'  + '.map') 
#          report(demmean,'d://test//Demmin//SRTM_files//' + file_prefix + str(tileLon) + '_' + str(tileLat) + '_mean' + '.map')
#          report(demmax, 'd://test//Demmin//SRTM_files//' + file_prefix + str(tileLon) + '_' + str(tileLat) + '_max'  + '.map')
          print 'Translate back to tiff'
          translateBack('d://test//Demmin//SRTM_files//' + file_prefix + str('%02d' % tileLon) + '_' + str('%02d' % tileLat) + '_min'  + '.map', 
              'd://test//Demmin//SRTM_files//' + file_prefix + str('%02d' % tileLon) + '_' + str('%02d' % tileLat) + '_min'  + '.tif')  
          
        except:
          print 'File does not exist for this extend'
          
      files.append('d://test//Demmin//SRTM_files//' + file_prefix + str('%02d' % tileLon) + '_' + str('%02d' % tileLat) + '_min'  + '.tif')
    
  return files
      
def run_createDEM(xmin,xmax,ymin,ymax,scale,cellLen):
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
  for f in glob('d://test//Demmin//*.tif'):
    os.unlink(f)  
      
  files = createDEM(xmin,xmax,ymin,ymax,scale)
  
  if len(files)>1:
      outputFile = r'd://test//Demmin//out.tif'
      command = ['-o',outputFile]  
  
      for i in range(0,len(files)):
          command.append(files[i])
      print command    
      print 'Merging tiles'
      gdal_merge.main(command)
      print 'Translate to .map'
      translateMap('d://test//Demmin//out.tif','d://test//Demmin//merge_test.map')
      print 'Resample to low resolution'
      resample_map(xmin,xmax,ymin,ymax,cellLen,cellLen,'merge_test.map','resample_dem.map')
      translateBack('resample_dem.map','resample_map.tif')

# Example for Myanmar  
run_createDEM(93,97,15,19,10,1/120.0)