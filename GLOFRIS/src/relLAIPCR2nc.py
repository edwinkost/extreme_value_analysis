### Converts relative LAI maps for twelve mionths cycle to netcdf
#
# import relevant packages
from numpy import *
from scipy import *
import sys,  gzip, os, os.path, gdal, glob
from gdalconst import *
from ftplib import FTP
import time
from datetime import datetime, timedelta
from netCDF4 import *
from GLOFRIS_utils import *

# define constants
s_nrRows           = 21600    # number of lines in global GLCC lat-long file
s_nrCols           = 43200    # number of columns in global GLCC lat-long file
t_nrRows           = 360      # number of lines in global GLCC lat-long file
t_nrCols           = 720      # number of columns in global GLCC lat-long file
aggScale_x = s_nrCols/t_nrCols  # aggregation scale x-direction
aggScale_y = s_nrRows/t_nrRows  # aggregation scale x-direction

def Gunzip(file):
        '''Gunzip the given file.'''
        r_file = gzip.GzipFile(file, 'rb')
        write_file = string.rstrip(file, '.gz')
        w_file = open(write_file, 'wb')
        w_file.write(r_file.read())
        w_file.close()
        r_file.close()
        os.unlink(file) # Yes this one too.

def read_relLAI(srcFolder, FillValnc):
    """ Convert PCRaster relLAI maps (with extention 001+012) to NetCDF
    Inputs:
        srcFolder       : The folder containing the twelve relLAI maps
    Outputs:
        relLAI          : 3-dim matrix containing the twelve maps
    """
    fileList = glob(srcFolder + '/*.0*')
    relLAI = zeros((360,720,12))
    # read PCRaster maps
    for file, month in map(None,fileList,(arange(0,12))):
        x, y, LAImap, FillVal = readMap(file,'PCRaster')
        LAImap[LAImap==FillVal] = FillValnc
        relLAI[:,:,month] = LAImap
            # Find position of maximum value
    return relLAI

def writeNC_simple(FileName, fracMaps, title, origFile, verbose):
    rootgrp = Dataset(FileName,'w', format='NETCDF3_CLASSIC')
    #  Determine total amount of needed time steps
    # Create dimensions
    if verbose:
        print 'Setting up nc-file: ' + FileName
    rootgrp.createDimension("latitude", shape(fracMaps)[0])
    rootgrp.createDimension("longitude", shape(fracMaps)[1])
    rootgrp.createDimension("month", shape(fracMaps)[2])
    # Create variables
    lat = rootgrp.createVariable('latitude','f4',('latitude',))
    lat.standard_name = 'latitude'
    lat.long_name = 'Latitude values'
    lon = rootgrp.createVariable('longitude','f4',('longitude',))
    lon.standard_name = 'longitude'
    lon.long_name = 'Longitude values'
    cov = rootgrp.createVariable('month', 'i2',('month',))
    cov.standard_name = 'Month_of_Year'
    cov.long_name = 'Month of Year'
    lat.units = 'degrees_N'
    lon.units = 'degrees_E'
    cov.units = '-'
	#Rain.units = '0.01mm/hr'
	#Rain._FillValue = -9999
	# Write data to NetCDF file
    lats = arange(89.75,-90,-0.5)
    lons = arange(-179.75,180,0.5)
    months = arange(0,shape(fracMaps)[2])+1
    lat[:] = lats
    lon[:] = lons
    cov[:] = months

    # Set attributes
    if verbose:
        print 'Writing attributes'
    rootgrp.title = title
    rootgrp.institution = 'Utrecht University'
    rootgrp.source = 'CRU climatology'
    rootgrp.references = origFile
    rootgrp.history = 'Created ' + time.ctime(time.time())
    rootgrp.source = 'Created by netCDF4-python, raw PCRaster files obtained from Rens van Beek'
    rootgrp.disclaimer = 'The timely delivery of these data and their quality is in no way guaranteed by Deltares'
    var = rootgrp.createVariable("relative_lai",'f4',('latitude','longitude','month',), fill_value=-9999)
    var.units = '-'
    var.standard_name = 'relative_lai'
    var.long_name = 'relative_lai'
    if verbose:
        print 'Writing relative LAI maps for each month:'
    for step in arange(0,shape(fracMaps)[2]):
        if verbose:
            print 'Writing LAI to ' + FileName + ' in layer ' + str(step)
        var[:,:,step] = fracMaps[:,:,step]
    rootgrp.sync()
    rootgrp.close()


print 'Done'
srcFolder = "F:/FEWS/GLOFRIS/python/relLAI"
destFile = "F:/FEWS/GLOFRIS/python/relLAI/relLAI.nc"
FillValnc = -9999.
relLAI = read_relLAI(srcFolder, FillValnc)
writeNC_simple(destFile, relLAI, 'Relative LAI for PCR-GLOBWB parameters', 'Utrecht University, dr. Rens van Beek (+31 30 253 2776)', 'True')