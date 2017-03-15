#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

#-modules

import os
import sys
import subprocess
import time as tm
import numpy as np
import datetime
import glob

from multiprocessing import Pool
from pcraster import setclone, Scalar, readmap, report, pcr2numpy, numpy2pcr

import pcraster as pcr

# utility module
import virtualOS as vos

# reporting module
import output_netcdf_cf_convention as outputNetCDF

# variable dictionaries
import aqueduct_flood_analyzer_variable_list as varDict

# logger
import logging
logger = logging.getLogger(__name__)


def getMax(x,a):
	if not isinstance(a,np.ndarray):
		a= np.array(a)		
	m= float(a.max())
	if x == None:
		return m
	else:
		return max(m,x)
	
def getMin(x,a):
	if not isinstance(a,np.ndarray):
		a= np.array(a)		
	m= float(a.min())
	if x == None:
		return m
	else:
		return min(m,x)

def getFileList(inputDir, filePattern):
	'''creates a dictionary of	files meeting the pattern specified'''
	#~ fileNameList = glob.glob(os.path.join(inputDir, filePattern))
	
	print inputDir
	print filePattern
	
	fileNameList = glob.glob(inputDir + filePattern)
	ll= {}
	for fileName in fileNameList:
		ll[os.path.split(fileName)[-1]]= fileName
	return ll

def getMapAttributesALL(cloneMap):
		co= ['mapattr -p %s ' %(cloneMap)]
		cOut,err= subprocess.Popen(co, stdout=subprocess.PIPE,stderr=open('/dev/null'),shell=True).communicate()
		if err !=None or cOut == []:
				print "Something wrong with mattattr in virtualOS, maybe clone Map does not exist ? "
				sys.exit()
		mapAttr = {'cellsize': float(cOut.split()[7]) ,\
							 'rows'		: float(cOut.split()[3]) ,\
							 'cols'		: float(cOut.split()[5]) ,\
							 'xUL'		 : float(cOut.split()[17]),\
							 'yUL'		 : float(cOut.split()[19])}
		return mapAttr

def checkResolution(c1,c2):
	'''Check resolution'''
	s1= str(c1)
	s2= str(c2)
	if len(s1) < len(s2):
		s= s1
	else:
		s= s2
	p= s.find('.')
	if p <> -1:
		nd= len(s)-(p+1)
	else:
		nd= 0
	c1= round(c1,nd)
	c2= round(c2,nd)
	if c1 <> c2: print 'resolutions %s, %s differ' % (s1,s2)
	return c1 == c2, nd
	
def getPosition(x,values,nd):
	'''Returns the position of value x in the array of values with the number of digits specified '''
	values= np.abs(values[:]-x)
	x= values.min()
	pos= np.where(values == x)
	if pos[0].size > 0 and x <= 1./nd:		
		return pos[0][0]
	else:
		return None

def checkRowPosition(r0,r1):
	'''' Returns the sorted row positions'''
	if r0 > r1:
		return r1, r0
	else:
		return r0, r1

def joinMaps(inputTuple):
	'''Merges maps starting from an input tuple that specifies the output map name, the number of rows\
 and the number rows, columns, ULL X and Y coordinates, cell length and the missing value identifer and a list of input maps'''
	outputFileName= inputTuple[0]
	nrRows= inputTuple[1]
	nrCols= inputTuple[2]
	xMin= inputTuple[3]
	yMax= inputTuple[4]
	cellLength= inputTuple[5]
	MV= inputTuple[6]
	fileNames= inputTuple[7]
	cloneFileName= inputTuple[8]
	#-echo to screen/logger
	msg = 'combining files for %s' % outputFileName,
	logger.info(msg)
	#-get extent
	xMax= xMin+nrCols*cellLength
	yMin= yMax-nrRows*cellLength
	xCoordinates= xMin+np.arange(nrCols+1)*cellLength
	yCoordinates= yMin+np.arange(nrRows+1)*cellLength
	yCoordinates= np.flipud(yCoordinates)
	msg = 'between %.2f, %.2f and %.2f, %.2f' % (xMin,yMin,xMax,yMax)
	logger.info(msg)

	#~ #-set output array
	#~ variableArray= np.ones((nrRows,nrCols))*MV
	#-set initial output aaray to zero
	variableArray= np.zeros((nrRows,nrCols))*MV

	#-iterate over maps
	for fileName in fileNames:
		
		print fileName
		attributeClone= getMapAttributesALL(fileName)
		cellLengthClone= attributeClone['cellsize']
		rowsClone= attributeClone['rows']
		colsClone= attributeClone['cols']
		xULClone= attributeClone['xUL']
		yULClone= attributeClone['yUL']
		# check whether both maps have the same attributes and process
		process, nd= checkResolution(cellLength,cellLengthClone)
		
		if process:
			#-get coordinates and locations
			sampleXMin= xULClone
			sampleXMax= xULClone+colsClone*cellLengthClone
			sampleYMin= yULClone-rowsClone*cellLengthClone
			sampleYMax= yULClone
			sampleXCoordinates= sampleXMin+np.arange(colsClone+1)*cellLengthClone
			sampleYCoordinates= sampleYMin+np.arange(rowsClone+1)*cellLengthClone
			sampleYCoordinates= np.flipud(sampleYCoordinates)
			sampleXMin= getMax(xMin,sampleXMin)
			sampleXMax= getMin(xMax,sampleXMax)
			sampleYMin= getMax(yMin,sampleYMin)
			sampleYMax= getMin(yMax,sampleYMax)
			sampleRow0= getPosition(sampleYMin,sampleYCoordinates,nd)
			sampleRow1= getPosition(sampleYMax,sampleYCoordinates,nd)			
			sampleCol0= getPosition(sampleXMin,sampleXCoordinates,nd)
			sampleCol1= getPosition(sampleXMax,sampleXCoordinates,nd)
			sampleRow0, sampleRow1= checkRowPosition(sampleRow0,sampleRow1)
			variableRow0= getPosition(sampleYMin,yCoordinates,nd)
			variableRow1= getPosition(sampleYMax,yCoordinates,nd)
			variableCol0= getPosition(sampleXMin,xCoordinates,nd)
			variableCol1= getPosition(sampleXMax,xCoordinates,nd)
			variableRow0,variableRow1= checkRowPosition(variableRow0,variableRow1)
			#-read sample array
			setclone(fileName)
			sampleArray= pcr2numpy(readmap(fileName),MV)
			
			print sampleArray
			
			sampleNrRows, sampleNrCols= sampleArray.shape

			# -create mask
			#~ mask= (variableArray[variableRow0:variableRow1,variableCol0:variableCol1] == MV) &\
				#~ (sampleArray[sampleRow0:sampleRow1,sampleCol0:sampleCol1] <> MV)
			mask= (variableArray[variableRow0:variableRow1,variableCol0:variableCol1] <> MV) &\
				(sampleArray[sampleRow0:sampleRow1,sampleCol0:sampleCol1] <> MV)

			#-add values
			msg = ' adding values in %d, %d rows, columns from (x, y) %.3f, %.3f and %.3f, %.3f to position (row, col) %d, %d and %d, %d' %\
				(sampleNrRows, sampleNrCols,sampleXMin,sampleYMin,sampleXMax,sampleYMax,variableRow0,variableCol0,variableRow1,variableCol1)
			logger.info(msg)	
	
			#~ variableArray[variableRow0:variableRow1,variableCol0:variableCol1][mask]= \
				#~ sampleArray[sampleRow0:sampleRow1,sampleCol0:sampleCol1][mask]
	
			variableArray[variableRow0:variableRow1,variableCol0:variableCol1][mask] += sampleArray[sampleRow0:sampleRow1,sampleCol0:sampleCol1][mask]

		else:

			msg = '%s does not match resolution and is not processed' % fileName
			logger.warning(msg)

	#-report output map
	setclone(cloneFileName)
	report(numpy2pcr(Scalar,variableArray,MV),outputFileName)


##################################
######## user input ##############
##################################

MV = 1e20

# map coordinates and resolution (at 30 arc-second resolution)
deltaLat = 0.5/60.0
deltaLon = 0.5/60.0
latMin =  -90.0
latMax =   90.0
lonMin = -180.0
lonMax =  180.0

inputDirRoot = str(sys.argv[1])

output_directory = str(sys.argv[2])

output_netcdf_file_name = "inunriver_historical_WATCH_1999.nc"
output_netcdf_file_name = str(sys.argv[3])

# time stamp for the first and last years
str_year = int(sys.argv[4])
end_year = int(sys.argv[5])

# - option for map types: *flood_inundation_volume.map or *channel_storage.map
map_type_name  = "channel_storage.map"
map_type_name  = str(sys.argv[6])

outputDir = output_directory + "/global/maps/"
try:
	os.makedirs(outputDir)
except:
	pass

# - prepare logger and its directory
log_file_location = output_directory + "/log/"
try:
    os.makedirs(log_file_location)
except:
    pass
vos.initialize_logging(log_file_location)

# number of cores that will be used
ncores = 5

# clone/mask maps
number_of_clone_maps = 53
areas = ['M%02d'%i for i in range(1,number_of_clone_maps+1,1)]



########################################################################
# MAIN SCRIPT
########################################################################


# get clone 
msg = "Make and set the clone map."
logger.info(msg)
# - number of rows and clones
nrRows = int((latMax-latMin)/deltaLat)
nrCols = int((lonMax-lonMin)/deltaLon)
# - make and set the clone map
tempCloneMap = outputDir+'/temp_clone.map'
command = 'mapattr -s -R %d -C %d -P "yb2t"	-B -x %f -y %f -l %f %s' %\
	(nrRows,nrCols,lonMin,latMax,deltaLat,tempCloneMap)
vos.cmd_line(command, using_subprocess = False)
# - set the clone map. 
setclone(tempCloneMap)

#~ print areas
#~ print areas[0]


# get a list of input files that will be merged
msg = "Get the list of input files that will be merged."
logger.info(msg)
inputDir = inputDirRoot + "/" + areas[0] + "/output_folder/"
files = getFileList(inputDir, '/*/*-year*.map')
msg = "The files that will be merged: " + str(files)
logger.info(msg)

# number of cores that will be used
ncores = min(len(files), ncores)
msg = 'Using %d cores to process' % ncores,
logger.info(msg)


for fileName in files.keys():
	#~ print fileName,
	files[fileName]= {}
	ll= []
	outputFileName= os.path.join(outputDir, fileName)
	for area in areas:
		#~ print area
		inputFileName = os.path.join(inputDirRoot, area, 'output_folder')
		try:
			inputFileName = glob.glob(inputFileName + "/*/" + fileName)[0]
			ll.append(inputFileName)
		except:
			pass
	files[fileName]= tuple((outputFileName,nrRows,nrCols,lonMin,latMax,deltaLat,MV,ll[:],tempCloneMap))


#~ # this is for testing
#~ joinMaps(files[fileName])


# MERGING PCRASTER MAPS
print
print
with_merging = True
if with_merging:
    msg = "Start merging."
    logger.info(msg)
    pool = Pool(processes=ncores)		# start "ncores" of worker processes
    pool.map(joinMaps,files.values())
else:
    msg = "It seems that merging has been done; we only have to convert the merged pcraster maps to a netcdf file."
    logger.info(msg)
print
print

#-remove temporary file
os.remove(tempCloneMap)
msg =' all done'
logger.info(msg)
print
print

# set the global clone maps
clone_map_file = "/projects/0/dfguu/users/edwinhs/data/HydroSHEDS/hydro_basin_without_lakes/integrating_ldd/version_9_december_2016/merged_ldd.map"
pcr.setclone(clone_map_file)

# boolean maps to mask out permanent water bodies (lakes and reservoirs):
reservoirs_30sec_file = "/scratch/shared/edwinsut/reservoirs_and_lakes_30sec/grand_reservoirs_v1_1.boolean.map"
msg = "Set the (high resolution) reservoirs based on the file: " + str(reservoirs_30sec_file)
logger.info(msg)
reservoirs_30sec = pcr.cover(pcr.readmap(reservoirs_30sec_file), pcr.boolean(0.0))
lakes_30sec_file      = "/scratch/shared/edwinsut/reservoirs_and_lakes_30sec/glwd1_lakes.boolean.map"
msg = "Set the (high resolution) lakes based on the file: " + str(lakes_30sec_file)
logger.info(msg)
lakes_30sec = pcr.cover(pcr.readmap(lakes_30sec_file), pcr.boolean(0.0))
# cells that do not belong lakes and reservoirs
non_permanent_water_bodies = pcr.ifthenelse(reservoirs_30sec, pcr.boolean(0.0), pcr.boolean(1.0))
non_permanent_water_bodies = pcr.ifthenelse(     lakes_30sec, pcr.boolean(0.0), non_permanent_water_bodies)

# Convert pcraster files to a netcdt file:
msg = "Convert pcraster maps to a netcdf file."
logger.info(msg)

# netcdf general setup:
netcdf_setup = {}
netcdf_setup['format']          = "NETCDF4"
netcdf_setup['zlib']            = True
netcdf_setup['institution']     = "Department of Physical Geography, Utrecht University"
netcdf_setup['title'      ]     = "PCR-GLOBWB 2 output (post-processed for the Aqueduct Flood Analyzer): Flood Inundation Depth (above surface level)."
netcdf_setup['created by' ]     = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['description']     = "The extreme values of flood inundation depth (above surface level)."
netcdf_setup['source'     ]     = "Utrecht University, Department of Physical Geography - contact: Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['references' ]     = "Sutanudjaja et al., in prep."

# netcdf output folderls -lah 
netcdf_output_folder = output_directory + "/global/netcdf/"
try:
	os.makedirs(netcdf_output_folder)
except:
	pass
print outputDir	


# object for reporting/making netcdf files
netcdf_report = outputNetCDF.OutputNetCDF()

msg = "Preparing the netcdf output file."
logger.info(msg)
#
# - PCR-GLOBWB variable name
var_name = 'floodDepth' 
#
# - return periods
return_periods = ["5-year", "10-year", "25-year", "50-year", "100-year", "250-year", "500-year", "1000-year"]

# - the dictionary for attribute information in a netcdf file
netcdf_file = {}
netcdf_file[var_name] = {}
#
# - all return periods in one file: file name (format from Philip: inunriver_rcp4p5_0000GFDL-ESM2M_2030_rp00000.nc)
netcdf_file[var_name]['file_name']  = netcdf_output_folder + "/" + output_netcdf_file_name
#
# - general attribute information:
netcdf_file[var_name]['description'] = netcdf_setup['description']
netcdf_file[var_name]['institution'] = netcdf_setup['institution']
netcdf_file[var_name]['title'      ] = netcdf_setup['title'      ]
netcdf_file[var_name]['created by' ] = netcdf_setup['created by' ]
netcdf_file[var_name]['source'     ] = netcdf_setup['source'     ]
netcdf_file[var_name]['references' ] = netcdf_setup['references' ]
#
# - resolution (unit: arc-minutes)
netcdf_file[var_name]['resolution_arcmin'] = 0.5 
#
# - preparing netcdf file:
msg = "Preparing the netcdf file: " + netcdf_file[var_name]['file_name']
logger.info(msg)
netcdf_report.create_netcdf_file(netcdf_file[var_name]) 
#
#
# time bounds in a netcdf file
lowerTimeBound = datetime.datetime(str_year,  1,  1, 0)
upperTimeBound = datetime.datetime(end_year, 12, 31, 0)
timeBounds = [lowerTimeBound, upperTimeBound]
#
#
msg = "Writing extreme values to a netcdf file: " + str(netcdf_file[var_name]['file_name'])
logger.info(msg)
#
#
# preparing the variables in the netcdf file:
for return_period in return_periods:
    # variable names and unit 
    variable_name = str(return_period) + "_of_" + varDict.netcdf_short_name[var_name]
    variable_unit = varDict.netcdf_unit[var_name]
    var_long_name = str(return_period) + "_of_" + varDict.netcdf_long_name[var_name]
    # 
    netcdf_report.create_variable(\
                                  ncFileName = netcdf_file[var_name]['file_name'], \
                                  varName    = variable_name, \
                                  varUnit    = variable_unit, \
                                  longName   = var_long_name, \
                                  comment    = varDict.comment[var_name]
                                  )

# store the pcraster map to netcdf files:
for return_period in return_periods:
    
    # variable name
    variable_name = str(return_period) + "_of_" + varDict.netcdf_short_name[var_name]

    msg = "Writing " + str(variable_name)
    logger.info(msg)
    
    # read from pcraster files
    inundation_file_name = output_directory + "/global/maps/" + "inun_" + str(return_period) + "_of_flood_inundation_volume_catch_04.tif.map"
    if map_type_name == "channel_storage.map": inundation_file_name = output_directory + "/global/maps/" + "inun_" + str(return_period) + "_of_channel_storage_catch_04.tif.map"
    inundation_map = pcr.readmap(inundation_file_name)
    inundation_map = pcr.cover(inundation_map, 0.0)
    # masking out permanent water bodies
    inundation_map = pcr.ifthen(non_permanent_water_bodies, inundation_map)
    inundation_map = pcr.cover(inundation_map, 0.0)
    
    # put it in a data dictionary
    netcdf_report.data_to_netcdf(netcdf_file[var_name]['file_name'], variable_name, pcr.pcr2numpy(inundation_map, vos.MV), timeBounds, timeStamp = None, posCnt = 0)


