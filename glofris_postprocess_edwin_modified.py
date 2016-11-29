# -*- coding: utf-8 -*-
"""
GLOFRIS_postprocess.py contains post-processing functions for use in GLOFRIS runs

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

$Id: GLOFRIS_postprocess.py 1116 2015-07-30 18:36:30Z winsemi $
$Date: 2015-07-30 20:36:30 +0200 (Thu, 30 Jul 2015) $
$Author: winsemi $
$Revision: 1116 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/GLOFRIS_postprocess.py $
$Keywords: $

# Modified/adopted by Edwin H. Sutanudjaja, starting on 24 November 2016

"""
import glob, os
import numpy as np
import netCDF4 as nc
import logging as logger
import datetime
import scipy.stats as stats

import pdb
#from glofris_utils import *

import pcraster as pcr
import virtualOS as vos

def get_date_comp(dateObj, comp='day'):
    """
    Returns a list of components of a date (e.g. the day, month or year)
    input:
        dateObj:    a list of datetime objects
        comp:       string, referring to the time scale which should be returned
    output:
        date_comp:  a NumPy array, containing the required date component of each datetime object in dateObj
    """
    date_comp = np.zeros(len(dateObj))
    for date, count in zip(dateObj, np.arange(0,len(dateObj))):
        exec('date_comp[count] = date.' + comp)
    return date_comp

def prepare_nc_clim(nc_src, FileOut,datetimeObj, datetimeObj_upper, datetimeObj_lower, metadata, logger):
    """
    Prepares a target NetCDF containing climatologies, following the attributes of a source NetCDF file.
    input:
        nc_src:             NetCDF object of source file
        FileOut:            string, referring to target NetCDF file location
        datetimeObj:        list of datetime objects, to be written to the time variable of the target NetCDF
        datetimeObj_upper:  list of datetime objects, to be written as upper bound to the time variable of the target NetCDF
        datetimeObj_lower:  list of datetime objects, to be written as lower bound to the time variable of the target NetCDF
        metadata:           dictionary of metadata for global attributes
        logger:             logger object
    output:
        No output from this function. The resut is a prepared NetCDF file at FileOut

    """
    # retrieve axes
    x = nc_src.variables['lon'][:]
    y = nc_src.variables['lat'][:]
    # if projStr.lower() == 'epsg:4326':
    logger.info('Found lat-lon coordinate system, preparing lat, lon axis')
    x_dim      = 'lon';             y_dim     = 'lat'
    x_name     = 'longitude';       y_name = 'latitude'
    x_longname = 'Longitude values';y_longname = 'Latitude values'
    x_unit     = 'degrees_east';       y_unit     = 'degrees_north'
    gridmap    = 'latitude_longitude'

    logger.info('Preparing ' + FileOut)
    nc_trg = nc.Dataset(FileOut,'w') # format='NETCDF3_CLASSIC'
    # Create dimensions
    nc_trg.createDimension("time", 0) #NrOfDays*8
    nc_trg.createDimension(y_dim, len(y))
    nc_trg.createDimension(x_dim, len(x))
    nc_trg.createDimension("nv", 2) # dimension for climatological time ranges

    # create axis time
    DateHour = nc_trg.createVariable('time','f8',('time',))
    DateHour.units = 'Days since 1900-01-01 00:00:00'
    DateHour.calendar = 'gregorian'
    DateHour.standard_name = 'time'
    DateHour.long_name = 'time'
    DateHour.climatology = 'climatology_bounds'
    DateHour[:] = nc.date2num(datetimeObj,units=DateHour.units,calendar=DateHour.calendar)

    # create climatology bounds
    ClimDate = nc_trg.createVariable('climatology_bounds','f8',('time','nv',))
    ClimDate[:,0] = nc.date2num(datetimeObj_lower,units=DateHour.units,calendar=DateHour.calendar)
    ClimDate[:,1] = nc.date2num(datetimeObj_upper,units=DateHour.units,calendar=DateHour.calendar)
    
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
    projection= nc_trg.createVariable('projection','c')
    projection.long_name = 'wgs84'
    projection.EPSG_code = 'EPSG:4326'
    projection.proj4_params = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    projection.grid_mapping_name = 'latitude_longitude'

    # Set attributes
    # Change some of the attributes, add some
    for attr in metadata:
        nc_trg.setncattr(attr, metadata[attr])
    nc_trg.sync()
    nc_trg.close()


def max_climatology(inputLoc, var, startYear, endYear, logger):
    """
    calculateClimatology computes the actual climatology for a given variable 
    over a given time period (startYear:endYear) from a list of files located at inputLoc
    Inputs:
        inputLoc:       string, path to location with resampled GCM or reference NetCDF files
        var:            one entry of dictionary, containing variable name, to be processed into climatology
        startYear:      int, start year
        endYear:        int, end year
        logger:         logger object
    Output:
        climatology:    NumPy array [12xMxN] containing the climatology
        parUnit:        String, containing the unit of the climatology variable
        dummy_ncfile:   Last file processed, to be used for copying attributes to climatology file
    """
    # retrieve files for specified dataset
    logger.info('Preparing climatology of variable "' + var + '"')
    fileList = glob.glob(os.path.join(inputLoc,'*.nc'))
    # sort in alphabetical and numerical order
    fileList.sort()
    #create empty arrays for sum of monthly averages and indexes of retrieved data
    nrYears             = float((endYear+1) - startYear)
    registerMonthYears  = np.zeros((12,nrYears))
    for fileName in fileList:
        logger.debug('Reading "' + fileName + '"')
        nc_src      = nc.Dataset(fileName,'r')
        # retrieve time object, retrieve the array with times and convert to a datetime object
        timeObj     = nc_src.variables['time']   # this is only a reference to the variable 'time' in the netCDF file
        timeArray   = timeObj[:]             # now retrieve an actual array of times
        timeUnit    = timeObj.units
        try:
            timeCalendar = timeObj.calendar
        except:
            timeCalendar ='gregorian'
        datetimeObj = nc.num2date(timeArray, timeUnit,timeCalendar)
        # retrieve month and year information
        years_list  = get_date_comp(datetimeObj, 'year') # retrieve years
        months_list = get_date_comp(datetimeObj, 'month') # retrieve months
        # check whether file contains data for the variable of interest
        try:
            parObj      = nc_src.variables[var]
            # read parameter units from file
            parUnit    = parObj.units
            # store source nc filename - to be used for nc global attributes
            dummy_ncfile    = fileName
            
            # check whether file contains missing data and replace those with nan
            try:
                FillVal     = parObj._FillValue
                # parObjData  = parObj[:];parObjData[parObjData==FillVal] = nan
            except:
                FillVal     = np.nan
                # parObjData  = parObj[:]    # GCM data is continuous fields also over oceans
            # check whether file contains data for one of the years of interest
            for year in range (startYear,endYear+1):
                ii = np.where(years_list == year)
                if len(ii[0] > 0):
                    logger.info('Year ' + str(year) + ' found in "' + fileName + '"')
                    for month in range(0,12):
                        # calculate monthly long-term averages and write to array
                        index                       = months_list == (month+1) # indices for specific month days
                        grid_stack                  = parObj[index,:,:]
                        # if a masked array is returned, then the raw data is retrieved
                        if hasattr(grid_stack, 'mask'):
                            grid_stack = grid_stack.data
                        if np.isfinite(FillVal):
                            grid_stack[grid_stack==FillVal] = np.nan
                        monthlyAverageStack         = np.max(grid_stack, axis=0)
                        try:
                            longTermAverage[month,:,:]  = longTermAverage[month,:,:] + monthlyAverageStack
                        except:
                            # first file is being processed so variables don't exist yet
                            longTermAverage     = np.zeros((12,monthlyAverageStack.shape[0],monthlyAverageStack.shape[1]))
                            climatology         = np.zeros((12,monthlyAverageStack.shape[0],monthlyAverageStack.shape[1]))
                            longTermAverage[month,:,:]  = longTermAverage[month,:,:] + monthlyAverageStack
                        registerMonthYears[month][year-startYear]  = 1
                        # grid_stack is done, requires lots of memory so delete!
                        del grid_stack
        except:
            logger.warning('Variable "' + var + '" is not found in file "' + fileName)
        nc_src.close()
    try:
        # count number of values for each month individually
        nrMonthValues   = np.zeros(12)
        for month in range(0,12):
            nrMonthValues[month] = sum(registerMonthYears[month,:])
            
        # calculate monthly long-term averages
        for month in range(0,12):
            climatology[month,:,:] = longTermAverage[month,:,:] / nrMonthValues[month]  
        climatology[np.isnan(climatology)] = FillVal
        logger.info('Climatology maximum for variable "' + var + '" prepared.')
    except:
        logger.warning('Variable "' + var + '" not present in files in "' + inputLoc)
        climatology = None;parUnit = None; dummy_ncfile = None;

    return climatology , parUnit, dummy_ncfile


def define_hydroyears(outmaps, climFile, startYear, endYear, metadata, logger):
    """
    Based on matlab scripts by Philip Ward (philip.ward@ivm.vu.nl)
    Date: 26 March 2012
    Produces a map showing for each WATCH basin34 whether to use normal
    hydro years (Oct-Sep) or alternative hydro years (Jul-Jun)
    
    The user must ensure that the correct command and arguments (e.g. time period, or other runtime info)
    is given.
    
    Inputs:
        outmaps:        string      -- path to outputs of hydrodynamics
        climFile:       string      -- path to target netCDF file with maximum climatology
        startYear:      string      -- start year to look for climatology
        endYear:        string      -- end year to look for climatology
        metadata:           dictionary of metadata for global attributes
        logger:             logger object
        
    """
    #   initialize general settings
    # prepare climatology netCDF files
    climatology_datetimeObj = []
    climatology_datetimeObj_upper = []
    climatology_datetimeObj_lower = []
    
    for n in np.arange(0,12):
        climatology_datetimeObj_lower.append(datetime.datetime(startYear,n+1,1,0,0))
        if n == 11:
            climatology_datetimeObj_upper.append(datetime.datetime(endYear+1,1,1,0,0))
        else:
            climatology_datetimeObj_upper.append(datetime.datetime(endYear,n+2,1,0,0))
            
        climatology_datetimeObj.append(datetime.datetime((endYear-startYear)/2+startYear,n+1,16,0,0))

    # first derive a climatology
    climatology, parUnit , dummy_ncfile = max_climatology(outmaps, 'qc', startYear, endYear, logger) # , logger
    # write climatology ref to file
    logger.info('writing climatology to "' + climFile + '"')
    nc_src = nc.Dataset(dummy_ncfile, 'r')
    try:
        nc_trg = nc.Dataset(climFile, 'a')
    except:
        prepare_nc_clim(nc_src, climFile, climatology_datetimeObj, climatology_datetimeObj_upper, climatology_datetimeObj_lower, metadata, logger)
        nc_trg = nc.Dataset(climFile, 'a')
        nc_trg.createVariable('qc','f4',('time','lat','lon',),zlib=True, fill_value=-9999.)

    nc_trg.variables['qc'][:] = climatology

    # close files
    nc_src.close()
    nc_trg.sync()
    nc_trg.close()


def derive_maxima(srcFolder, startYear, endYear, cellarea, hydroyears, statsFile, metadata, logger):
    """
    This function derives annual maxima over a number of files of a GLOFRIS run. It searches for each day for the extreme value and writes to a map.
    This function uses two different hydrological years and keeps track of the extremes per hydrological year.
    The hydrological years are defined as follows:
        Hydroyear 1: October - September
        Hydroyear 2: July - June
    
    """
    
    def read_single_grid(varObj, idx):
        # in case of a difference in the used calendar, there may be one or more missing days in a year. 
        # These are accounted for by ignoring dates that are not found inside the input data files
        curGrid = varObj[location[0],:,:]
        if hasattr(curGrid, 'mask'):
            curMask = curGrid.mask
            curGrid = curGrid.data
            curGrid[curMask] = nan
        return curGrid
    startMonth_1 = 7 # July
    startMonth_2 = 10 # October
    hydroyear_1_idx = np.where(hydroyears==2)
    hydroyear_2_idx = np.where(hydroyears==1)
        
    logger.info('Preparing annual maximum flood volumes')
    inputVars = ['fldf','fldd']
    fileList = glob.glob(os.path.join(srcFolder,'*.nc'))
    # sort in alphabetical and numerical order
    fileList.sort()
    #create empty arrays for sum of monthly averages and indexes of retrieved data
    nrYears             = float((endYear+1) - startYear)
    registerMonthYears  = np.zeros((12,nrYears))
    startDate = datetime.datetime(startYear, startMonth_1, 1, 0, 0)
    endDate   = datetime.datetime(endYear, startMonth_2-1, 30, 0, 0)
    #   initialize general settings
    # prepare climatology netCDF files
    stats_datetimeObj = []
    stats_datetimeObj_upper = []
    stats_datetimeObj_lower = []
    
    for n in np.arange(0,endYear-startYear):
        startPeriod   = datetime.datetime(startYear+n,startMonth_1,1,0,0)
        endPeriod     = datetime.datetime(startYear+n+1,startMonth_2-1,30,0,0)
        averagePeriod = startPeriod + (endPeriod-startPeriod)/2
        stats_datetimeObj_lower.append(startPeriod)
        stats_datetimeObj_upper.append(endPeriod)
        stats_datetimeObj.append(averagePeriod)
    # open a dummy netCDF file
    dummy_nc = nc4.Dataset(fileList[0],'r')
    prepare_nc_clim(dummy_nc, statsFile, stats_datetimeObj, stats_datetimeObj_upper, stats_datetimeObj_lower, metadata, logger)
    dummy_nc.close()
    # now add a variable for the extreme values to the grid
    nc_trg = nc4.Dataset(statsFile, 'a')
    # add the hydrological year grid to the file
    hydyear = nc_trg.createVariable('hydroyear','i2', ('lat','lon',), fill_value=0, zlib=True)
    hydyear.setncattr('standard_name','hydrological_year')
    hydyear.setncattr('long_name','Definition of hydrological year per cell')
    hydyear.setncattr('units','-')
    hydyear.setncattr('comment','1: October-September; 2: July-June')
    hydyear[:] = hydroyears
    flvolObj = nc_trg.createVariable('flvol','f4', ('time','lat','lon',), fill_value=-9999, zlib=True)
    flvolObj.setncattr('standard_name','water_volume')
    flvolObj.setncattr('long_name','inundated volume from river flooding')
    flvolObj.setncattr('units','m3')
    flvolObj.setncattr('cell_methods','time: maximum within years time')
    
    # prepare a lookup table for reading files
    lookup_table = lookup_climate_files(srcFolder, inputVars, startDate, endDate)
    # now prepare two maps for two different hydrological year orders.
    maximum_1 = np.zeros(cellarea.shape);maximum_1[:] = np.nan
    maximum_2 = np.zeros(cellarea.shape);maximum_2[:] = np.nan
    # initially, there is no map to write, this value becomes true as soon as 
    # the first complete cycle for both hydrological years has been run through
    map_to_write = False
    # prepare the final map that will be written to the NetCDF file with extreme values
    map_final    = np.zeros(cellarea.shape);map_final[:] = np.nan
    
    # define some lists
    nc_src = [[],[]]
    timeObjs=[[],[]]
    nc_vars=[[],[]]
    yearNr = 0
    allDates  = lookup_table['time']
    idxs      = where(logical_and(array(allDates) >= startDate, array(allDates) <= endDate))[0]
    
    # start with an empty string to compare with
    srcFiles = ['','']
    for idx in idxs:
        for nvar, var in enumerate(inputVars):
            if logical_and(lookup_table[var][idx] != srcFiles[nvar], lookup_table[var][idx] != ''):
                #pdb.set_trace()
                # read a new source netCDF file
                if srcFiles[nvar] != '':
                    # if we are not reading the first time, then close the previous file
                    nc_src[nvar].close()
                # set the new source file and open it and read x and y-axis and time and the variable of interest
                srcFiles[nvar] = lookup_table[var][idx]
                logger.debug('Switching to source file ' + srcFiles[nvar] + ' for variable ' + var + ' at date ' + allDates[idx].strftime('%Y-%m-%d'))
                nc_src[nvar] = nc4.Dataset(srcFiles[nvar], 'r')
                # read axis, try 'lat' otherwise try 'latitude'
                try:
                    y = nc_src[nvar].variables['lat'][:]
                except:
                    y = nc_src[nvar].variables['latitude'][:]
            
                try:
                    x = nc_src[nvar].variables['lon'][:]
                except:
                    x = nc_src[nvar].variables['longitude'][:]
                # read time axis and convert to time objects
                time = nc_src[nvar].variables['time']
                timeObjRaw = nc4.num2date(time[:], units=time.units, calendar=time.calendar)
                # UUGGGHHH: this seems to be a bug. calendar other than gregorian give other objects than 
                # datetime.datetime objects. Here we convert to gregorian numbers, then back to date objects
                timeObj = []
                for t in timeObjRaw:
                    timeObj.append(datetime.datetime.strptime(t.strftime('%Y%j'),'%Y%j'))
    #            timeObj = nc4.num2date(nc4.date2num(timeObj, units=time.units, calendar='gregorian'), units=time.units, calendar='gregorian')
                # now loop over all time steps, check the date and write valid dates to a list, write time series to PCRaster maps
                for n in range(len(timeObj)):
                    # remove any hours or minutes data from curTime
                    timeObj[n] = timeObj[n].replace(hour=0)
                    timeObj[n] = timeObj[n].replace(minute=0)
                # Read the variable of interest
                timeObjs[nvar] = timeObj
                nc_vars[nvar] = nc_src[nvar].variables[var]

        #### Correct files are read for each variables, now read in position ####
        # look up the position in the current file, where the current time step is located
        curTime = allDates[idx]
        logger.debug('Establish flood volume on date ' + curTime.strftime('%Y-%m-%d'))
        location = where(array(timeObjs[0])==curTime)[0]
        if len(location) == 1:
            fldf = read_single_grid(nc_vars[0], location)
        location = where(array(timeObjs[1])==curTime)[0]
        if len(location) == 1:
            fldd = read_single_grid(nc_vars[1], location)
        flvol = fldf*fldd*cellarea
        # fill both hydroyear maps with the maximum of the map and the new flood volume
        maximum_1 = np.nanmax(np.array([maximum_1, flvol]), axis=0)
        maximum_2 = np.nanmax(np.array([maximum_2, flvol]), axis=0)
        # if the month is the end of the first hydroyear period, then copy the values to the map_final
        if np.logical_and(curTime.month==startMonth_1-1, curTime.day==30):
            map_final[hydroyear_1_idx] = maximum_1[hydroyear_1_idx]
            maximum_1 = np.zeros(cellarea.shape);maximum_1[:] = np.nan
        # if the month is the end Month of the second hydroyear period, then write to NetCDF file
        if np.logical_and(curTime.month==startMonth_2-1, curTime.day==30):
            if map_to_write:
                map_final[hydroyear_2_idx] = maximum_2[hydroyear_2_idx]
                # write the maximum map to the target NetCDF file
                logger.info('Writing map maximum to NetCDF at date ' + curTime.strftime('%Y-%m-%d'))# BLAHLBALHLBALHB
                print curTime.strftime('%Y-%m-%d')
                map_final[np.isnan(map_final)] = -9999
                flvolObj[yearNr,:,:] = map_final
                yearNr += 1
            else:
                map_to_write = True
            maximum_2 = np.zeros(cellarea.shape);maximum_2[:] = np.nan
            #pdb.set_trace()
            map_final = np.zeros(cellarea.shape);map_final[:] = np.nan
    nc_trg.sync()
    nc_trg.close()    

def gumbel_fit(vals, sigma_mu_tolerance=0.002, sample_limit=5.):
    """
    This function performs a gumbel fit. There are a number of tolerance limits that need to be set before any fit is considered:
        vals:                   array with samples from the (assumed Gumbel) distribution
        sigma_mu_tolerance:     the minimum value for the relation standard dev. over mean of the samples, for it to be considered. 
                                If the variation is too small, then a good Gumbel fit cannot be established and nans are returned
        sample_limits:          If less than this amount of valid (i.e. non-zero) samples is found, then the values are assumed to be zero always
        
                                
        
        
    """
    # check the sigma/mu tolerance. If sigma/mu is very very small, then no reliable gumbel can be estimated. In this case return a NaN for all
    sigma_mu = np.std(vals)/np.mean(vals)
    if sigma_mu > sigma_mu_tolerance:
        # the tolerance criterium is met, now estimate the distribution function
        # first estimate probability of zero
        idx_zero = np.where(vals==0)[0]
        idx_non_zero = np.where(vals!=0)[0]
        p_zero   = float(len(idx_zero))/len(vals)
        if len(idx_non_zero) >= sample_limit:
            # there are enough samples, let's fit gumbel!
            vals_nonzero = vals[idx_non_zero]
            loc, scale = stats.gumbel_r.fit(vals_nonzero)
        else:
            loc = 0.
            scale = 0.
            p_zero = 1.
    else:
        
        print 'sigma/mu tolerance not met!'
        p_zero = 1.
        loc = 0.
        scale = 0.
    return p_zero, loc, scale

def inverse_gumbel(p_zero, loc, scale, return_period):
    """
    This function computes values for a given return period using the zero probability, location and shape
    parameters given. 
    """

    p = pcr.scalar(1. - 1./return_period)
    
    # p_residual is the probability density function of the population consisting of any values above zero
    p_residual = pcr.min(pcr.max((p - p_zero) / (1.0 - p_zero), 0.0), 1.0) 

    reduced_variate = -pcr.ln(-pcr.ln(p_residual))

    flvol = reduced_variate * scale + loc

    # infinite numbers can occur. reduce these to zero!
    # if any values become negative due to the statistical extrapolation, fix them to zero (may occur if the sample size for fitting was small and a small return period is requested)
    flvol = pcr.max(0.0, pcr.cover(flvol, 0.0))

    return flvol

def inv_gumbel_original(p_zero, loc, scale, return_period):
    """
    This function computes values for a given return period using the zero probability, location and shape
    parameters given. 
    """
    np.seterr(divide='ignore')
    np.seterr(invalid='ignore')
    p = 1-1./return_period
    
    # p_residual is the probability density function of the population consisting of any values above zero
    # p_residual = p + (1-p)*p_zero # """ this equation is (I think) not correct! You should fit through the population bigger than zero, leaving the zero probability out of the equation"""
    p_residual = np.minimum(np.maximum((p-p_zero)/(1-p_zero), 0), 1)  # I think this is the correct equation""" 
    #  any places where p is zero, the flvol becomes -inf. Make any areas < 0 equal to zero
    # pdb.set_trace()
    reduced_variate = -log(-log(p_residual))
    flvol = reduced_variate*scale+loc
    # negative infinite numbers can occur. reduce these to zero!
    flvol[isinf(flvol)] = 0.
    # flvol = np.maximum(stats.gumbel_r.ppf(p_residual,loc=loc, scale=scale), 0) # WARNING I wonder if this is correct!!!!
    np.seterr(divide='warn')
    np.seterr(invalid='warn')
    return flvol

def get_gumbel_parameters(input_data_dictionary):
        
            
        # exclude pixels where the value is always the same by approximation
        # estimate the location and scale parameters on non-zero values
        # return zero probability, location and scale parameters
        
    # the input_data_dictionary contains the following
    starting_row = input_data_dictionary['1strow']
    input_data   = input_data_dictionary['values']
    
    # input data    
    #~ flvol = input_data 
    flvol = input_data[:,:,:].copy()
    
    mask = flvol == vos.MV 
    flvol = np.ma.array(flvol, mask = mask)
    flvol = np.ma.filled(flvol, vos.MV)
    
    #~ test_map = pcr.numpy2pcr(pcr.Scalar, \
                             #~ flvol[0,:,:], vos.MV)
    #~ pcr.aguila(test_map)                         
    
    # prepary the arrays:
    row = flvol.shape[1]
    col = flvol.shape[2]
    
    zero_prob = np.zeros([1, row, col]) + vos.MV  
    gumbel_loc = np.zeros([1, row, col]) + vos.MV  
    gumbel_scale = np.zeros([1, row, col]) + vos.MV

    for row in range(flvol.shape[1]):
        print 'row: ' + str(row + starting_row) 
        
        for col in range(flvol.shape[2]):
            rawdata = flvol[:,row,col]
            data = rawdata[rawdata != vos.MV]
            print 'row: ' + str(row + starting_row) + ' col: ' + str(col)
            #~ print data
            if len(data) > 0:
                p_zero, loc, scale = gumbel_fit(data)
                print 'row: ' + str(row + starting_row) + ' col: ' + str(col)
                #~ print data 
                msg = 'p_zero: ' + str(p_zero) + ' ; loc: ' + str(loc) + ' ; scale: ' + str(scale)
                logger.debug(msg)
            else:
                p_zero = vos.MV; loc = vos.MV; scale = vos.MV
            
            zero_prob[0, row, col]    = p_zero
            gumbel_loc[0, row, col]   = loc
            gumbel_scale[0, row, col] = scale

    # put the results into a nice dictionary
    gumbel_parameters = {}
    gumbel_parameters["starting_row"] = starting_row
    gumbel_parameters["p_zero"] = zero_prob[0, :, :].copy()
    gumbel_parameters["gumbel_loc"] = gumbel_loc[0, :, :].copy()
    gumbel_parameters["gumbel_scale"] = gumbel_scale[0, :, :].copy()
    
    return gumbel_parameters

def derive_Gumbel(statsFile, startYear, endYear, gumbelFile, metadata, logger):
        
            
        # exclude pixels where the value is always the same by approximation
        # estimate the location and scale parameters on non-zero values
        # return zero probability, location and scale parameters
        
        
    startPeriod   = datetime.datetime(startYear,1,1,0,0)
    endPeriod     = datetime.datetime(endYear,12,31,0,0)
    averagePeriod = startPeriod + (endPeriod-startPeriod)/2
    gumbel_datetimeObj_lower = [startPeriod]
    gumbel_datetimeObj_upper = [endPeriod]
    gumbel_datetimeObj       = [averagePeriod]
    # open a dummy netCDF file
    dummy_nc = nc4.Dataset(statsFile,'r')
    prepare_nc_clim(dummy_nc, gumbelFile, gumbel_datetimeObj, gumbel_datetimeObj_upper, gumbel_datetimeObj_lower, metadata, logger)
    dummy_nc.close()

    nc_trg = nc4.Dataset(gumbelFile, 'a')
    # add the hydrological year grid to the file
    zero_prob = nc_trg.createVariable('flvol_zero_prob','f4', ('time','lat','lon',), fill_value=-9999., zlib=True)
    zero_prob.setncattr('standard_name','flvol_zero_prob')
    zero_prob.setncattr('long_name','Probability of zero flood volume')
    zero_prob.setncattr('units','-')
    gumbel_loc = nc_trg.createVariable('flvol_location','f4', ('time','lat','lon',), fill_value=-9999., zlib=True)
    gumbel_loc.setncattr('standard_name','flvol_gumbel_location')
    gumbel_loc.setncattr('long_name','Gumbel distribution location parameter of flood volume')
    gumbel_loc.setncattr('units','m3')
    gumbel_scale = nc_trg.createVariable('flvol_scale','f4', ('time','lat','lon',), fill_value=-9999., zlib=True)
    gumbel_scale.setncattr('standard_name','flvol_gumbel_scale')
    gumbel_scale.setncattr('long_name','Gumbel distribution scale parameter of flood volume')
    gumbel_scale.setncattr('units','m3')
    nc_src = nc4.Dataset(statsFile, 'r')
    flvol  = nc_src.variables['flvol']
    for row in range(flvol.shape[1]):
        print 'row: ' + str(row)
        
        for col in range(flvol.shape[2]):
            # print 'col: ' + str(col)
            rawdata = flvol[:,row,col]
            if hasattr(rawdata, 'mask'):
                if not(rawdata.mask.all()):
                # cell apparently has sometimes missing values. Extract the non-missings
                    data = rawdata.data[rawdata.mask]
                else:
                    data = []
            else:
                # all values are non-masked, use all data values
                data = rawdata
            if len(data) > 0:
                p_zero, loc, scale = gumbel_fit(data)
            else:
                p_zero = -9999;loc   = -9999; scale = -9999
            zero_prob[0, row, col]    = p_zero
            gumbel_loc[0, row, col]   = loc
            gumbel_scale[0, row, col] = scale
    nc_trg.sync()
    nc_trg.close()
            
def apply_Gumbel_original(gumbelFile, trgFolder, prefix, return_periods, cellArea, logger):
    # read gumbel file
    nc_src = nc4.Dataset(gumbelFile, 'r')
    # read axes and revert the y-axis
    x = nc_src.variables['lon'][:]
    y = np.flipud(nc_src.variables['lat'][:])
    
    # read different variables
    loc   = nc_src.variables['flvol_location'][0,:,:]#; loc    = gumbel_loc.data;  loc[loc==gumbel_loc._FillValue]       = np.nan
    scale = nc_src.variables['flvol_scale'][0,:,:]#;    scale  = gumbel_scale.data;scale[scale==gumbel_scale._FillValue] = np.nan
    p_zero    = nc_src.variables['flvol_zero_prob'][0,:,:]#;p_zero = zero_prob.data;   p_zero[p_zero==zero_prob._FillValue]  = np.nan
    # loop over all return periods
    for return_period in return_periods:
        logger.info('Preparing return period %05.f' % return_period)
        flvol = inv_gumbel(p_zero, loc, scale, return_period)
        # any area with cell > 0, fill in a zero. This may occur because:
            # a) dynRout produces missing values (occuring in some pixels in the Sahara)
            # b) the forcing data is not exactly overlapping the cell area mask (e.g. EU-WATCH land cells are slightly different from PCR-GLOBWB mask)
            # c) the probability of zero flooding is 100%. This causes a division by zero in the inv_gumbel function
        test = logical_and(flvol.mask, cellArea > 0)
        flvol[test] = 0.
        test = logical_and(np.isnan(flvol), cellArea > 0)
        flvol[test] = 0.
        # if any values become negative due to the statistical extrapolation, fix them to zero (may occur if the sample size for fitting was small and a small return period is requested)
        flvol = np.maximum(flvol, 0.)
        # write to a PCRaster file
        flvol_data = flvol.data
        # finally mask the real not-a-number cells
        flvol_data[flvol.mask] = -9999.
        fileName = os.path.join(trgFolder, '%s_RP_%05.f.map') % (prefix, return_period)
        writeMap(fileName, 'PCRaster', x, y, np.flipud(flvol_data), -9999.)
    nc_src.close()
    
