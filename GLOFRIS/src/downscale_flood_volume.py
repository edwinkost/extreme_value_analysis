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
Created: 04 Nov 2010
Created and tested with python 2.6.5

$Id: downscale_flood_volume.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/downscale_flood_volume.py $
$Keywords: $
"""

from numpy import *
# import osgeo.gdal as gdal
from osgeo.gdalconst import *
import numpy as np
import os, datetime, calendar
import logging
import logging.handlers
import ConfigParser
import time
import os.path
import sys
from PCRaster import *
from PCRaster.Framework import *
from PCRaster.NumPy import *
from netcdftime import *
from netCDF4_utils import *
from netCDF4 import Dataset
import getopt

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

def readCase(caseFile, caseFile_ref):
    logger.info('Reading case from ' + caseFile)
    # read maxima at global scale from scenario and resample to local
    try:
        nc = Dataset(caseFile,'r')
        max_fldf = nc.variables['Flooded_Fraction_max'][:]
        max_fldd = nc.variables['Flooded_Depth_max'][:]
        max_vol  = max_fldf*max_fldd
        max_vol[max_vol==max_vol.max()] = nan
        nc.close()
    except:
        logger.error('Case "' + caseFile + '" is missing. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)


    logger.info('Reading reference from ' + caseFile_ref)
    # read maxima at global scale from reference
    try:
        nc = Dataset(caseFile_ref,'r')
        max_fldf_ref = nc.variables['Flooded_Fraction_max'][:]
        max_fldd_ref = nc.variables['Flooded_Depth_max'][:]
        max_vol_ref  = max_fldf_ref*max_fldd_ref
        max_vol_ref[max_vol_ref==max_vol_ref.max()] = nan
        nc.close()
    except:
        logger.error('Reference "' + os.path.abspath(caseFile) + '" is missing. Required to estimate difference between scenario and reference. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)

    # sort the extreme values from low to high
    max_vol.sort(axis=0)
    max_vol_ref.sort(axis=0)

    return max_vol, max_vol_ref

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
    for level in arange(0.0,30,0.1):
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


##### END OF FUNCTIONS #######
# Set default values (overwritten from input from ini file or command line arguments)
logfile = 'GLOFRIS_downscale.log'
stream_thres = 2
nrExtremes = 30
relevant_T = 2
earth_radius = 6378137.
h_min_impact = 0 # water level where there's no impact of a flood
h_max_impact = 3 # water level with maximum impact, anything above is just as bad
defaultRunId = 'run_default'
demFolder    = os.path.join('.','regions')
#caseFolder = './Scenarios/HadGEM'

"""Treatment of command-line arguments"""
try:
    print sys.argv[1:]
    config_file = sys.argv[1]
    # caseFolder = sys.argv[1];caseName = caseFolder
    # print 'Case: ' + caseFolder # suggest: world
    # opts, args = getopt.getopt(sys.argv[2:], 'alchp')
except getopt.error, msg:
    usage(msg)

#try:
#    for o, a in opts:
#        if o == '-l': runLandCover = True;runAll = False; print 'Running Land Cover Module'
#        if o == '-c': runClimate   = True;runAll = False; print 'Running Climate Change Module'
#        if o == '-h': runHydrology = True;runAll = False; print 'Running Hydrological Module'
#        if o == '-p': runPost      = True;runAll = False; print 'Running Post Processing Module'
#    if runAll: print 'Running all GLOFRIS Modules'


    # Set logging (delete old file if it exists)
if os.path.isfile(logfile):
    os.unlink(logfile)
logger, ch     = setlogger(logfile, 'postprocessor')

try:
    # Try and read config file and set default options
    config = ConfigParser.SafeConfigParser()
    config.optionxform = str
    # First read the file in master dir, next in Case dir
    con_handle = config.read(config_file)
    if len(con_handle)==0:
        logger.info('Configuration file: "' + os.path.abspath(config_file) + '" not found, using default values')
    try: # regions, included in post-processing
        regions = config.get("postprocessor","regions").split(',')
    except:
        # Fixed covers are better to remain explicit, so no log message returned
        logger.error('Entry "regions" not given by config file. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)
    try: # return period with no flood
        relevant_T_all = array(config.get("postprocessor","returnPeriodThreshold").split(','),dtype=float)
    except:
        # Fixed covers are better to remain explicit, so no log message returned
        logger.error('Entry "returnPeriodThreshold" not given by config file. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)
    try: # stream thresholds
        stream_thres_all = array(config.get("postprocessor","streamThreshold").split(','),dtype=float).round()
    except:
        # Fixed covers are better to remain explicit, so no log message returned
        logger.error('Entry "streamThreshold" not given by config file. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)
    try:
        scenarioFolder = config.get("misc","scenarioFolder")
    except:
        logger.error('Entry "scenarioFolder" not given by config file. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)
    try:
        scenarioName = config.get("misc","scenarioName")
        caseFolder   = os.path.join(scenarioFolder,scenarioName)
        caseName     = scenarioName
        logger.info('Scenario "' + caseName + '" will be stored in "' + caseFolder + '"')
    except:
        logger.error('Entry "scenarioName" not given by config file. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)
    try: # name of runId (e.g. "onlyClimateChange")
        runId = config.get("misc","runId")
    except:
        logger.info('Run Id not found, assuming "' + defaultRunId + '" as default')
        runId = defaultRunId

    # check if length of stream_thres_all and relevant_T_all is equal to number of regions.
    if len(relevant_T_all) != len(regions):
        logger.error('number of entries in "returnPeriodThreshold" is not equal to number regions. Each region needs a return period threshold. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)

    if len(stream_thres_all) != len(regions):
        logger.error('number of entries in "streamThreshold" is not equal to number regions. Each region needs a stream threshold to define which pixels are significant rivers. Exiting!')
        closeLogger(logger, ch)
        sys.exit(2)

    caseFile = os.path.join(caseFolder,runId,'outstats','Statistics.nc')
    caseFile_ref = os.path.join(caseFolder,'..','ref',runId,'outstats','Statistics.nc') # review the folder with reference case
    cellarea_file = os.path.join('.','baseMaps','cellarea30.map')   # already in system, replace this

    # clone is cellarea
    setclone(cellarea_file)
    ## now make a uniqueId map of land cells of the full globe
    cellarea = readmap(cellarea_file)
    landyesno = ifthenelse(cellarea > 0, boolean(1), boolean(0))
    uniqueid_map  = uniqueid(landyesno)
    report(uniqueid_map,os.path.join(demFolder,'uniqueid.map'))

    # read case and prepare volume arrays
    max_vol, max_vol_ref = readCase(os.path.abspath(caseFile),os.path.abspath(caseFile_ref))
    ### DOWNSCALING PROCEDURE STARTS BELOW.  REPEAT FOR EACH REGION OF INTEREST ######
    # region counter
    for region, stream_thres, relevant_T in map(None, regions, stream_thres_all, relevant_T_all):
        # determine CDF Weibull positions and return periods
        p =(nrExtremes-(arange(0.,nrExtremes)+0.5))/nrExtremes
        T = 1/p
        ii_p_relevant = T > relevant_T
        p_relevant = p*ii_p_relevant
        weight = 1./nrExtremes

        # determine relevant volumes
        vol_irrelevant = max_vol_ref.copy()
        vol_relevant   = max_vol_ref.copy()
        for n in arange(0,nrExtremes):
            # keep all irrelevant probability values and set remainder to zero in vol_irrelevant
            if p_relevant[n] > 0:
                vol_irrelevant[n,:,:] = 0
        # determine maximum irrelevant water level
        vol_irrelevant = vol_irrelevant.max(axis=0)

        # now remove irrelevant volume (from reference run) from the scenario run volumes
        for n in arange(0,nrExtremes):
            vol_relevant[n,:,:] = maximum(max_vol[n,:,:]-vol_irrelevant,0)

        setclone(cellarea_file)
        caseDem  = os.path.join(demFolder,str(region + '.map'))# location where dem should be stored
        caseLdd  = os.path.join(demFolder,str(region + '_ldd.map'))# location where dem should be stored
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

        downscaleLoc = os.path.join(caseFolder,runId,region)         # location where downscaled results are stored
        if not os.path.isdir(downscaleLoc):
            os.makedirs(downscaleLoc)

        # write to temporary maps
        resampleMap(os.path.join(demFolder,"uniqueid.map"),os.path.join(downscaleLoc,"uniqueid_target.map"),caseDem) # ????? nearest neighbour
        resampleMap(cellarea_file, os.path.join(downscaleLoc,"cellarea_target.map"),caseDem)
        cellarea_target = readmap(os.path.join(downscaleLoc,"cellarea_target.map"))

        # derive maximum anual flood volumes and save to PCRaster maps
        for n in arange(0, nrExtremes):
            max_heightav_diff = flipud(vol_relevant[n,:,:])
            max_heightav_diff[isnan(max_heightav_diff)] = -9999

            # make a PCR-object
            max_heightav_pcr = numpy2pcr(Scalar,max_heightav_diff,-9999)
            #
            max_vol_pcr = max_heightav_pcr*cellarea
            vol_mapFile = os.path.join(downscaleLoc,str("volume00."+"%03.f") % (n+1))
            vol_maptargetFile = os.path.join(downscaleLoc,str("volume_t."+"%03.f") % (n+1))
            report(max_vol_pcr,vol_mapFile)
            # resample map of volume per cell to target
            resampleMap(vol_mapFile,vol_maptargetFile,caseDem) # ????? nearest neighbour
            os.unlink(vol_mapFile)

        ## set target area as clone
        setclone(caseDem)
        dem = readmap(caseDem)
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
        xres = xc[0,1]-xc[0,0]
        yres = yc[0,0]-yc[1,0]
        conv_factor = (0.5/yres)*(0.5/xres)
        # xc1 = xc-xres/2;xc2 = xc+xres/2;yc1=yc-yres/2;yc2=yc+yres/2
        # xdist = distance_on_unit_sphere(yc,xc1,yc,xc2)*earth_radius # this function takes too much memory on 32-bit machines so has been discarded
        # ydist = distance_on_unit_sphere(yc1,xc,yc2,xc)*earth_radius # this function takes too much memory on 32-bit machines so has been discarded
        # surf = numpy2pcr(Scalar,xdist*ydist,-9999)                  # this function takes too much memory on 32-bit machines so has been discarded
        surf = cellarea_target/conv_factor
        del yc, xc
        # now process per return period
        for n in arange(0, nrExtremes):
            if p_relevant[n] > 0:
                # compute downscaled flood map
                logger, ch, floodedLand = downscale(n, ldd, stream_thres, conv_factor, logger, ch)
            else:
                print "non-relevant probability, writing zeros to volume_t." + "%03.f" % (n+1)
                floodedLand = dem*0
            flood_scaled = max(min((floodedLand-h_min_impact)/(h_max_impact-h_min_impact),1),0)
            exposure     = exposure + flood_scaled*weight
            report(floodedLand,os.path.join(downscaleLoc,str('flood000.' + '%03.f') % (n + 1)))
            os.unlink(os.path.join(downscaleLoc,str("volume_t."+"%03.f") % (n+1)))

        # finally report the effective exposure map
        report(exposure,os.path.join(downscaleLoc,'exposure.map'))
        # remove unnecessary files
        # os.unlink(os.path.join(downscaleLoc,"cellarea_target.map"))
        os.unlink(os.path.join(downscaleLoc,"uniqueid_target.map"))
        # now combine with GDP map
        # now combine with population map

    os.unlink(os.path.join(demFolder,'uniqueid.map'))
    logger.info('Post-processing GLOFRIS is done!')
    closeLogger(logger, ch)
except:
    logger.error('Unknown error occurred, exiting...')
    closeLogger(logger, ch)
    sys.exit(2)

