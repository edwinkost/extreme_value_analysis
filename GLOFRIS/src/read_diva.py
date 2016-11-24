# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 16:50:47 2012

READ DIVA DATABASE

@author: Mark Hegnauer
"""

import time
from datetime import date
from datetime import timedelta
import numpy as np
import pdb
import scipy
import matplotlib.pyplot as plt
import os
import xlrd
from PCRaster import *
from PCRaster.Framework import *
from PCRaster.NumPy import *
import getopt, sys, os


def find_nearest(arrayInLon,arrayInLat,xax, yax):
    '''
    find_nearest finds the grid point in the map that is closest to the lon/lat
    location in de DIVA database.
    '''
#    lonMap = []
#    latMap = []
    lonClose = []
    latClose = []
#    for i in range(0,int(nrCols)):
#        lonMap.append(xmin+(i*cellLen))
#    for i in range(0,int(nrRows)):
#        latMap.append(ymin+(i*cellLen))
    for i in range(0,len(arrayInLon)):
        lonClose.append(np.abs(xax-arrayInLon[i]).argmin())
        latClose.append(np.abs(yax-arrayInLat[i]).argmin())

    return lonClose, latClose


def cut_dem(xmin,xmax,ymin,ymax,srcdem,destdem):
    command = 'gdalwarp -te %f %f %f %f -srcnodata -32768 -dstnodata -32768 %s temp.tif' % (xmin,ymin,xmax,ymax,srcdem)
    os.system(command)
    command = 'gdal_translate -ot Float32 -of PCRaster -a_nodata -32768 temp.tif temp.map'
    os.system(command)
    command = 'pcrcalc %s = if(temp.map ne -999,temp.map)' % destdem
    os.system(command)
    if os.path.isfile('temp.tif'):
        os.remove('temp.tif')
    if os.path.isfile('temp.map'):
        os.remove('temp.map')

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

'''
###############################################################################
# Read data from DIVA database (.XLS)
###############################################################################
'''

def translate_DIVA(xax, yax, T, DIVAXls, dem):

#    try:
#        opts, args = getopt.getopt(sys.argv[1:], 'x:X:y:Y:C:T:')
#    except:
#        print 'error'
#    try:
#        for o, a in opts:
#            if o == '-x':
#                xmin = float(a)
#            if o == '-X':
#                xmax = float(a)
#            if o == '-y':
#                ymin = float(a)
#            if o == '-Y':
#                ymax = float(a)
#            if o == '-C':
#                cellLen = float(a)
#            if o == '-T':
#                cellLen = float(a)
#    except:
#        print 'test'
#
#    tileMinX = np.floor(( np.floor(xmin) + 180 ) / 5 + 1)
#    tileMaxX = np.ceil(( np.ceil(xmax) + 180 ) / 5 + 1)
#    tileMinY = np.floor(( 60 - np.floor(ymax) ) / 5 + 1)
#    tileMaxY = np.ceil(( 60 - np.ceil(ymin) ) / 5 + 1)
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
        plt.plot(tInt,intVals[i],'-+')

    intVals = np.array(intVals)

    plt.figure(figsize=(30,24))
    plt.plot(lon,lat,'b.')
    plt.plot(lon[selected],lat[selected],'ro')
    plt.plot([xmin,xmax],[ymin,ymin],'r')
    plt.plot([xmin,xmax],[ymax,ymax],'r')
    plt.plot([xmin,xmin],[ymin,ymax],'r')
    plt.plot([xmax,xmax],[ymin,ymax],'r')
    plt.grid('on')

    #nrCols = np.round((xmax-xmin)/cellLen)
    #nrRows = np.round((ymax-ymin)/cellLen)

    lonClose, latClose = find_nearest(lon[selected],lat[selected],xax,yax)
    # latClose = find_nearest(lon[selected],lat[selected],xax,yax)[1]

    rasterT = np.zeros((len(yax),len(xax)))
    rasterT[rasterT==0.0]=-999
    rasterT[latClose,lonClose] = intVals[:,T-1]

    #cut_dem(xmin,xmax,ymin,ymax,'resample_map.tif','cut_dem.map')
    #setclone('cut_dem.map')
    rasterTmap = numpy2pcr(Scalar,rasterT,-999)
    report(rasterTmap,'rasterT.map')

    result = inversedistance(boolean(dem+100),rasterTmap, 2,0,0)
    report(result,'result.map')

'''
###############################################################################
# Actual calculation of flood extent
###############################################################################
'''
def calc_floodExtend(demThres, demRaise, DIVAXls, caseDem, T):
    plt.close('all')
    demFolder    = os.path.split(caseDem)[0]
    demFile      = os.path.split(caseDem)[1]
    region       = demFile.split('.map')[0]
    caseLdd      = os.path.join(demFolder, region + '_ldd.map')
    caseName     = os.path.dirname(__file__)
    demRaiseFile = os.path.join(demFolder, region + '_raised.map')
    setclone(caseDem)
    dem          = readmap(caseDem)                          # read elevation from PCRaster DEM map
    # determine extents of DEM
    xc      = pcr2numpy(xcoordinate(boolean(cover(dem,1))), np.nan)
    yc      = pcr2numpy(ycoordinate(boolean(cover(dem,1))), np.nan)
    xax     = xc[0,:]
    yax     = yc[:,0]
    cellLen = xc[0,1]-xc[0,0]

    # read relevant DIVA points
    translate_DIVA(xax, yax, T, DIVAXls, dem)


    if os.path.isfile(caseLdd):
        print 'Ldd already exists'
        ldd = readmap(caseLdd)
    else:
        print 'Ldd being created'
        ldd = lddcreate(dem,1e31,1e31,1e31,1e31)        # make a local drain direction map
        report(ldd,'ldd.map')

    # determine pit cells at downstream ends
    coastal_locs = ifthenelse(pit(ldd)!=0,ifthenelse(dem < demThres,boolean(1),boolean(0)),boolean(0))
    # Distance to coast
    dist2coast   = ldddist(ldd,coastal_locs,120)               # there's about 120 factor to km scale from degree scale of cells
    report(dist2coast,'dist2coast.map')
    # Adjust DEM
    dem_manip    = dem + dist2coast*demRaise                  # raise the elevation using a damping factor
    report(dem_manip, demRaiseFile)

    levelDem = 'result.map'     # caseName +

    level = readmap(levelDem)
    floodedLandCoastal   = max(level - dem_manip,0)

    report(floodedLandCoastal,'flood_%s_T_%03.f_raise_%03.3f.map' % (region, T, demRaise))

# Example for Myanmar
workDir = os.path.split(sys.argv[0])[0] # os.path.dirname(__file__)
DIVAXls = os.path.abspath(os.path.join(workDir, 'GLOFRIS_downscale', 'diva', 'DIVA_data.xls'))
print 'Reading DIVA from ' + DIVAXls

calc_floodExtend(10, 0.0, DIVAXls, r'd:\1202803-PBL\Myanmar\myanmar_pcr_min.map',1000)
calc_floodExtend(10, 0.01, DIVAXls, r'd:\1202803-PBL\Myanmar\myanmar_pcr_min.map',1000)
calc_floodExtend(10, 0.03, DIVAXls, r'd:\1202803-PBL\Myanmar\myanmar_pcr_min.map',1000)
calc_floodExtend(10, 0.05, DIVAXls, r'd:\1202803-PBL\Myanmar\myanmar_pcr_min.map',1000)
calc_floodExtend(10, 0.1, DIVAXls, r'd:\1202803-PBL\Myanmar\myanmar_pcr_min.map',1000)
calc_floodExtend(10, 0.4, DIVAXls, r'd:\1202803-PBL\Myanmar\myanmar_pcr_min.map',1000)
#calc_floodExtend(10, 10, DIVAXls, r'd:\1202803-PBL\Bangladesh\downscale_maps\ref\dem.map',10)
#calc_floodExtend(10, 10, DIVAXls, r'd:\1202803-PBL\Bangladesh\downscale_maps\ref\dem.map',100)
#calc_floodExtend(10, 10, DIVAXls, r'd:\1202803-PBL\Bangladesh\downscale_maps\ref\dem.map',500)
#calc_floodExtend(10, 10, DIVAXls, r'd:\1202803-PBL\Bangladesh\downscale_maps\ref\dem.map',1000)