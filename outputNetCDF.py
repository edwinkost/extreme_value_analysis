#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import sys
import datetime
import time
import re
import glob
import subprocess
import netCDF4 as nc
import numpy as np
import virtualOS as vos

class OutputNetCDF():
    
    def __init__(self, global_map = True, netcdf_y_orientation_follow_cf_convention = True, netcdf_format = 'NETCDF4', zlib = True):
        		
        # corner cordinates (lat/lon system)
        self.global_map = global_map
        if self.global_map == True:
            self.x_min = -180.
            self.y_min =  -90.
            self.x_max =  180. 
            self.y_max =   90. 
        # TODO: Make the option for a non global map.     
        
        # let users decide what their preference regarding latitude order 
        self.netcdf_y_orientation_follow_cf_convention = netcdf_y_orientation_follow_cf_convention

        # netcdf format and zlib setup 
        self.netcdf_format = netcdf_format
        self.zlib          = zlib
        
    def set_netcdf_attributes(self, netcdf_setup_dictionary):

        for k, v in netcdf_setup_dictionary.items(): setattr(attributeDictionary, k, v)
        attributeDictionary["history"]      = 'created on ' + datetime.datetime.today().isoformat(' ')
        attributeDictionary["date_created"] = datetime.datetime.today().isoformat(' ')
        
        return attributeDictionary

    def createNetCDF(self, ncFileName, netcdf_setup_dictionary):

        # cell centres coordinates (lat/lon - arc degree)
        deltaLon = netcdf_setup_dictionary['resolution_arcmin'] / 60.
        deltaLat = deltaLon
        nrCols   = int((self.x_max - self.x_min) / deltaLon)
        nrRows   = int((self.y_max - self.y_min) / deltaLat)
        longitudes = np.linspace(self.x_min + 0.5*deltaLon, self.x_max + 0.5*deltaLon, nrCols)
        latitudes  = np.linspace(self.y_max - 0.5*deltaLat, self.y_min + 0.5*deltaLat, nrRows) 
        if self.netcdf_y_orientation_follow_cf_convention: latitudes = latitudes[::-1]

        rootgrp = nc.Dataset(ncFileName, 'w', format = self.format)

        # create dimensions - time is unlimited, others are fixed
        rootgrp.createDimension('time', None)
        rootgrp.createDimension('lat', len(self.latitudes) )
        rootgrp.createDimension('lon', len(self.longitudes))

        date_time = rootgrp.createVariable('time','f4',('time',))
        date_time.standard_name = 'time'
        date_time.long_name = 'Days since 1901-01-01'

        date_time.units = 'Days since 1901-01-01' 
        date_time.calendar = 'standard'

        lat = rootgrp.createVariable('lat','f4',('lat',))
        lat.long_name = 'latitude'
        lat.units = 'degrees_north'
        lat.standard_name = 'latitude'

        lon= rootgrp.createVariable('lon','f4',('lon',))
        lon.standard_name = 'longitude'
        lon.long_name = 'longitude'
        lon.units = 'degrees_east'

        lat[:]= self.latitudes
        lon[:]= self.longitudes

        shortVarName = varName
        longVarName  = varName
        if longName != None: longVarName = longName

        var = rootgrp.createVariable(shortVarName,'f4',('time','lat','lon',) ,fill_value=vos.MV,zlib=self.zlib)
        var.standard_name = varName
        var.long_name = longVarName
        var.units = varUnits

        attributeDictionary = self.attributeDictionary
        for k, v in attributeDictionary.items(): setattr(rootgrp,k,v)

        rootgrp.sync()
        rootgrp.close()

    def changeAtrribute(self, ncFileName, attributeDictionary):

        rootgrp = nc.Dataset(ncFileName,'a')

        for k, v in attributeDictionary.items(): setattr(rootgrp,k,v)

        rootgrp.sync()
        rootgrp.close()

    def addNewVariable(self, ncFileName, varName, varUnits, longName = None):

        rootgrp = nc.Dataset(ncFileName,'a')

        shortVarName = varName
        longVarName  = varName
        if longName != None: longVarName = longName

        var = rootgrp.createVariable(shortVarName,'f4',('time','lat','lon',) ,fill_value=vos.MV,zlib=self.zlib)
        var.standard_name = varName
        var.long_name = longVarName
        var.units = varUnits

        rootgrp.sync()
        rootgrp.close()

    def data2NetCDF(self, ncFileName, shortVarName, varField, timeStamp, posCnt = None):

        rootgrp = nc.Dataset(ncFileName,'a')

        date_time = rootgrp.variables['time']
        if posCnt == None: posCnt = len(date_time)
        date_time[posCnt] = nc.date2num(timeStamp,date_time.units,date_time.calendar)

        # flip variable if necessary (to follow cf_convention)
        if self.netcdf_y_orientation_follow_cf_convention: varField = np.flipud(varField)
        
        rootgrp.variables[shortVarName][posCnt,:,:] = varField

        rootgrp.sync()
        rootgrp.close()

    def dataList2NetCDF(self, ncFileName, shortVarNameList, varFieldList, timeStamp, posCnt = None):

        rootgrp = nc.Dataset(ncFileName,'a')

        date_time = rootgrp.variables['time']
        if posCnt == None: posCnt = len(date_time)

        for shortVarName in shortVarNameList:
            
            date_time[posCnt] = nc.date2num(timeStamp,date_time.units,date_time.calendar)
            varField = varFieldList[shortVarName]
            
            # flip variable if necessary (to follow cf_convention)
            if self.netcdf_y_orientation_follow_cf_convention: varField = np.flipud(varField)
            
            rootgrp.variables[shortVarName][posCnt,:,:] = varField

        rootgrp.sync()
        rootgrp.close()

    def close(self, ncFileName):

        rootgrp = nc.Dataset(ncFileName,'w')

        # closing the file 
        rootgrp.close()
