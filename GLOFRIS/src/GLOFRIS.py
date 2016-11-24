#!/usr/bin/env python
"""
Created on Wed May 04 12:00:57 2011

GLOFRIS.py

  More detailed description goes here.

 Copyright notice
  --------------------------------------------------------------------
  Copyright (C) 2011 Deltares
      W.(Willem van Verseveld)

      willem.vanverseveld@deltares.nl / hessel.winsemius@deltares.nl

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

$Id: GLOFRIS.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/GLOFRIS.py $
$Keywords: $

"""
#from numpy import *
#from scipy import *
import sys, os, os.path, shutil, ConfigParser
import time
import subprocess
import datetime as dt
import getopt
import traceback
import glob
import numpy as np
# import own functions
from GLOFRIS_utils import *
from changeGLCC import *
from GLCC2PCRGLOB import *
from GLOFRIS_risk import *
#from post_proc import *
from GLOFRIS_postprocess import *
import pdb

version  = '2.0'
runAll         = True # run all modules, True is default
runLandCover   = False
#runClimate     = False
runHydrology   = False
runPost        = False
runRisk        = False
# replace for command-line argument
# caseFolder = 'A1B'
logfile = 'GLOFRIS_diag.log'
config_file = 'GLOFRIS_config.ini'
# default values

""" The following land covers are expected not to change at all:
    GLACIER ICE (12)
    INLAND WATER (14)
    SEA WATER (15)
    GLACIER ROCK (70)
    LAND, WATER AND SHORE (74)
    LAND AND WATER, RIVERS (75)
    ROCKY CLIFFS AND SLOPES (86)
"""

fixedCovers            = array([12, 14, 15, 70, 74, 75, 86])-1
defaultTimePeriod      = '2050'
lon_ax                 = arange(-179.75, 180, 0.5)
lat_ax                 = arange(-89.75, 90, 0.5)
defaultRunId           = 'run_default'
pcrglobInputVars       = ['pr','tas','ep']
pcrglobInputFolders    = ['input/era40/precipitation','input/era40/temperature','input/era40/evaporation']
pcrglobInputPrefixs    = ['prec','temp','evap']
pcrglobInputSlopes     = [.001, 1., .001]
pcrglobInputOffsets    = [0., -273.15, 0.]
pcrglobOutputVars      = ['qloc','qw'] 
pcrglobOutputFolders   = ['output/qloc','output/qw']
pcrglobOutputPrefixs   = ['qloc','qw']
pcrglobOutputSlopes    = [1., 1.]
pcrglobOutputOffsets   = [0., 0.]
pcrglobOutputUnits     = ['m','m']
pcrglobOutputVarNames  = ['local_discharge_land','local_discharge_water']
pcrglobPurgeFolders    = ['input/era40','output/etot','output/fldf','output/gc','output/maps','output/q3','output/qc','output/qchannel','output/qloc',
                          'output/qw','output/results','output/snow','output/soilmoist','output/storage','output/timeseries','output/wh']
if sys.platform[0:3] == 'win':
    pcrglobCommand         = 'oldcalc -f pcrglobwb_new_snow.mod'
else:
    pcrglobCommand         = 'oldcalc -f pcrglobwb_new_snow.mod'

dynroutInputVars       = ['qloc','qw']
dynroutInputFolders    = ['world/inmaps','world/inmaps']
dynroutInputPrefixs    = ['qloc','qw']
dynroutInputSlopes     = [1., 1.]
dynroutInputOffsets    = [0., 0.]
dynroutOutputVars      = ['qc','fldf','fldd'] 
dynroutOutputFolders   = ['world/run_default/outmaps','world/run_default/outmaps','world/run_default/outmaps']
dynroutOutputPrefixs   = ['qc','fldf','fldd']
dynroutOutputSlopes    = [1., 1., 1.]
dynroutOutputOffsets   = [0., 0., 0.]
dynroutOutputUnits     = ['m3/s','-','m']
dynroutOutputVarNames  = ['river_discharge','flooded_fraction','flooded_depth']
dynroutPurgeFolders    = ['world/inmaps','world/run_default/outmaps']
if sys.platform[0:3] == 'win':
    dynroutCommand         = 'dynRout.bat'
else:
    dynroutCommand         = 'bin/dynRout_v2'

"""Treatment of command-line arguments"""
try:
    codeFile = os.path.abspath(sys.argv[0])
    codeDir  = os.path.split(codeFile)[0]
    rootDir  = os.path.split(codeDir)[0]
    print rootDir
    
    print sys.argv[1:]
    config_file = sys.argv[1]
    opts, args = getopt.getopt(sys.argv[2:], 'alchpr')
except:
    noArgExitStr = str('****************      GLOFRIS 2.0       *****************\n' + \
    '$Id: GLOFRIS.py 733 2013-07-03 06:32:48Z winsemi $\n' + \
    '$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $\n' + \
    '$Author: winsemi $\n' + \
    '$Revision: 733 $\n' + \
    'Welcome to the "Global Flood Risks with IMAGE scenarios" toolbox.\n ' + \
    'GLOFRIS runs as follows: GLOFRIS <config-file.ini> -<option1> -<option2> ....\n' + \
    '<config-file.ini>:       a GLOFRIS configuration file, generated by you,\n' + \
    '                         the end-user.\n' + \
    '<option1>:               a run-time argument, used to select which \n' + \
    '                         GLOFRIS-componentshould be run.\n' + \
    '                         you can select multiple components at once, \n' + \
    '                         however, do make sure that all required\n' + \
    '                         pre-processing components (land cover and/or climate)\n' + \
    '                         for your scenario analysis are performed, before the \n' + \
    '                         hydrology component is run.\n' + \
    ' GLOFRIS can be run with the following run-time arguments:\n' + \
    '-l:                      run the land cover component.\n' + \
    '-h:                      run the hydrology component PCR-GLOBWB and DynRout\n' + \
    '-p:                      run the post-processor component (extracting extreme\n' + \
    '                         values from the PCR-GLOBWB-DynRout run)\n' + \
    '-r:                      run the risk component (establishing affected\n' + \
    '                         population/gdp from the extreme values)\n' + \
    '-a:                      run all components in sequence.\n' + \
    '****************         Have fun!        *****************')
    print noArgExitStr


    sys.exit(2)

try:
    for o, a in opts:
        if o == '-l': runLandCover = True;runAll = False; print 'Running Land Cover Module'
        if o == '-h': runHydrology = True;runAll = False; print 'Running Hydrological Module'
        if o == '-p': runPost      = True;runAll = False; print 'Running Post Processing Module'
        if o == '-r': runRisk      = True;runAll = False; print 'Running Risk Module'
    if runAll: print 'Running all GLOFRIS Modules'


    # Set logging
    if os.path.isfile(logfile):
        os.unlink(logfile)

    logger, ch     = setlogger(logfile, 'GLOFRIS')
    # provide version info to log-file
    logger.info('Starting GLOFRIS v. 2.0')
    logger.info('$Id: GLOFRIS.py 733 2013-07-03 06:32:48Z winsemi $')
    logger.info('$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $')
    logger.info('$Author: winsemi $')
    logger.info('$Revision: 733 $')

    # initiate metadata entries
    metadata = {}
    metadata['title'] = 'GLObal Flood Risks with IMAGE Scenarios'
    metadata['institution'] = 'Deltares, PBL, Utrecht University'
    metadata['source'] = 'GLOFRIS v. 2.0; $Revision: 733 $; $Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $ '
    metadata['history'] = time.ctime()
    metadata['references'] = 'http://www.hydrol-earth-syst-sci-discuss.net/9/9611/2012/hessd-9-9611-2012.html'
    metadata['Conventions'] = 'CF-1.4'

    try:
        # Try and read config file and set default options
        config = ConfigParser.SafeConfigParser()
        config.optionxform = str
        # First read the file in master dir, next in Case dir
        con_handle = config.read(config_file)
        if len(con_handle)==0:
            logger.error('Configuration file: "' + os.path.abspath(config_file) + '" not found.')
        try: # land covers that should remain in cover area
            run_default = config.getboolean("default","run_default")
        except:
            # Fixed covers are better to remain explicit, so no log message returned
            run_default = False
        try: # land covers that should remain in cover area
            fixedCovers = array(config.get("exclude","coverId").split(','),dtype=int)-1
        except:
            # Fixed covers are better to remain explicit, so no log message returned
            fixedCovers = fixedCovers
        try:
            climateInFolder = config.get("input","climateInFolder")
        except:
            logger.error('Entry "climateInFolder" not given by config file. Exiting!')
            closeLogger(logger, ch)
            sys.exit(2)
        try:
            landcoverInFile = config.get("input","landcoverInFile")
            landcoverInFile = os.path.abspath(landcoverInFile)
        except:
            logger.error('Entry "landcoverInFile" not given by config file. Exiting!')
            closeLogger(logger, ch)
            sys.exit(2)
        try:
            scenarioFolder = config.get("output","scenarioFolder")
        except:
            logger.error('Entry "scenarioFolder" not given by config file. Exiting!')
            closeLogger(logger, ch)
            sys.exit(2)
        try:
            scenarioName   = config.get("scenario","scenarioName")
            caseFolder     = os.path.abspath(os.path.join(scenarioFolder,scenarioName))
            caseName       = scenarioName
            logger.info('Scenario "' + caseName + '" will be stored in "' + caseFolder + '"')
        except:
            logger.error('Entry "scenarioName" not given by config file. Exiting!')
            closeLogger(logger, ch)
            sys.exit(2)
        try: # name of runId (e.g. "onlyClimateChange")
            runId = config.get("scenario","runId")
        except:
            logger.info('Run Id not found, assuming "' + defaultRunId + '" as default')
            runId = defaultRunId
        try: # Selection of future year (e.g. "2050" or "2100")
            timePeriod = config.get("scenario","timePeriod")
            timePeriodInt = int(timePeriod)
        except:
            logger.info('Time period not found, assuming ' + defaultTimePeriod + ' as default')
            timePeriod = defaultTimePeriod
        try: # Selection of future year (e.g. "2050" or "2100")
            startYear = int(config.get("scenario","startYear"))
        except:
            logger.error('startYear not found but required! Exiting!')
            closeLogger(logger, ch)
            sys.exit(2)
        try: # Selection of future year (e.g. "2050" or "2100")
            endYear = int(config.get("scenario","endYear"))
        except:
            logger.error('endYear not found but required! Exiting!')
            closeLogger(logger, ch)
            sys.exit(2)
        try: # Selection of future year (e.g. "2050" or "2100")
            warmStatePeriod = int(config.get("scenario","warmStatePeriod"))
        except:
            logger.error('warmStatePeriod not found but required! Exiting!')
            closeLogger(logger, ch)
            sys.exit(2)
        if endYear < startYear:
            logger.error('startYear cannot be later then endYear! Exiting!')
            closeLogger(logger, ch)
            sys.exit(2)
        if warmStatePeriod > (endYear - startYear) + 1:
            logger.error('warmStatePeriod is longer than the startYear until endYear. Exiting!')
            closeLogger(logger, ch)
            sys.exit(2)
            
        
        metadata['scenario_name'] = scenarioName + '_' + runId + '_' + timePeriod
        try:
            metadata['scenario_long_name'] = config.get("scenario","scenarioLongName")
        except:
            metadata['scenario_long_name'] = metadata['scenario_name']
        logger.info("GLOFRIS Version: " + version + " [Case: " + caseName + "] time period: " + timePeriod)
        logger.info("Runid: " + runId)
        try: # land covers that should remain in cover area
            return_periods = array(config.get("postprocessor","return_periods").split(','),dtype=int)
        except:
            # Fixed covers are better to remain explicit, so no log message returned
            return_periods = []
        try:
            population_file= config.get("risk","population_file")
            population_file = os.path.join(caseFolder,'inexposure',population_file)
        except:
            population_file=None
        try:
            gdp_file= config.get("risk","gdp_file")
            gdp_file = os.path.join(caseFolder,'inexposure',gdp_file)
        except:
            gdp_file=None
        if population_file:
            try:
                population_factor=float(config.get("risk","population_factor"))
            except:
                logger.error('population_file was given, but population_factor is not found. Exiting!')
                closeLogger(logger, ch)
                sys.exit(2)
        if population_file:
            try:
                population_var=config.get("risk","population_var")
            except:
                logger.error('population_file was given, but population_var is not found. Exiting!')
                closeLogger(logger, ch)
                sys.exit(2)
        if gdp_file:
            try:
                gdp_factor=float(config.get("risk","gdp_factor"))
            except:
                logger.error('gdp_file was given, but gdp_factor is not found. Exiting!')
                closeLogger(logger, ch)
                sys.exit(2)
        if gdp_file:
            try:
                gdp_var=config.get("risk","gdp_var")
            except:
                logger.error('gdp_file was given, but gdp_var is not found. Exiting!')
                closeLogger(logger, ch)
                sys.exit(2)
    except:
        logger.error(sys.exc_info())
        logger.info("******************      Reading GLOFRIS_config.ini completed with ERRORS! Aborting   ******************")
        closeLogger(logger, ch)
        sys.exit(2)
    logger.info("Fixed covers: " + str(fixedCovers))
    logger.info("Case Name: " + caseName)
    logger.info("Run Id: " + runId)
    logger.info("Time period: " + timePeriod)


    """Hard paths are listed below"""
    # rootDir = os.path.abspath('../..');rootDir.replace('\\','/')
    # settings (paths are relative to fews bin dir)
    #java_bindir = '../jre/bin/java.exe'
    #java_bindir = os.path.join(rootDir, 'jre/bin/java.exe');java_bindir.replace('\\','/')
    #fews_bindir = os.path.join(rootDir, 'bin');fews_bindir.replace('\\','/')
    warmStateFolder = os.path.join(caseFolder, runId, 'outwarmstates')
    outMapsFolder = os.path.join(caseFolder, runId, 'outmaps')
    outStatsFolder = os.path.join(caseFolder, runId, 'outstats')
    outRiskFolder  = os.path.join(caseFolder, runId, 'outrisk')
    outLandcoverFolder = os.path.join(caseFolder, runId, 'outlandcover')
    GLCC_fracMap   = os.path.join(rootDir,'landCoverGLCC','goge2_halfdeg_simple.nc')
    modulesFolder  = os.path.join(caseFolder, runId, 'Modules')
    pcrglobZip     = os.path.join(rootDir,'Modules','pcrglob.zip')
    pcrglobFolder  = os.path.join(caseFolder, runId, 'Modules','pcrglob')
    pcrglobInStateFolder  = os.path.join(pcrglobFolder,'input','initstates')
    pcrglobEndStateFolder = os.path.join(pcrglobFolder,'output','endstates')
    pcrglobColdState      = os.path.join(rootDir,'coldStates','pcrglob_coldState.zip')
    dynroutZip     = os.path.join(rootDir,'Modules','dynRout.zip')
    dynroutFolder  = os.path.join(caseFolder, runId, 'Modules','dynRout')
    dynroutInStateFolder  = os.path.join(dynroutFolder,'world','instate')
    dynroutEndStateFolder = os.path.join(dynroutFolder,'world','instate')
    dynroutColdState      = os.path.join(rootDir,'coldStates','dynrout_coldState.zip')
    worldRegFile   = os.path.join(rootDir,'baseMaps','GREG.asc')
    cellAreaFile   = os.path.join(rootDir,'baseMaps','cellarea30.map')
    hydroYearsFile = os.path.join(rootDir,'baseMaps','hydroyear.map')
    lookupTableXML = os.path.join(rootDir,'lookupTables','goge2_lookup.xml')
#x,y, cellarea, FillVal = readMap(cellareaFile,'PCRaster')

    # update the location of the inputs to pcr-globwb and dynrout
    for n in range(len(pcrglobInputFolders)):
        pcrglobInputFolders[n] = os.path.abspath(os.path.join(pcrglobFolder, pcrglobInputFolders[n]))
    for n in range(len(pcrglobOutputFolders)):
        pcrglobOutputFolders[n] = os.path.abspath(os.path.join(pcrglobFolder, pcrglobOutputFolders[n]))
    for n in range(len(pcrglobPurgeFolders)):
        pcrglobPurgeFolders[n] = os.path.abspath(os.path.join(pcrglobFolder, pcrglobPurgeFolders[n]))
    for n in range(len(dynroutInputFolders)):
        dynroutInputFolders[n] = os.path.abspath(os.path.join(dynroutFolder, dynroutInputFolders[n]))
    for n in range(len(dynroutOutputFolders)):
        dynroutOutputFolders[n] = os.path.abspath(os.path.join(dynroutFolder, dynroutOutputFolders[n]))
    for n in range(len(dynroutPurgeFolders)):
        dynroutPurgeFolders[n] = os.path.abspath(os.path.join(dynroutFolder, dynroutPurgeFolders[n]))
    
    ### PREPARE CASE FOLDERS AND LAND COVER ###
    try:
        # prepare case folders
        if not os.path.isdir(caseFolder +"/" + runId):
            os.makedirs(outMapsFolder)
            os.makedirs(outStatsFolder)
            os.makedirs(outRiskFolder)
            os.makedirs(outLandcoverFolder)
            os.makedirs(warmStateFolder)
            os.makedirs(modulesFolder)
        # RUN LAND COVER MODULE IF ASKED FOR BY USER
        if any([runAll,runLandCover]):
            logger.info("******************      Initializing Land Cover Change module    ******************")
            GLCC_newMap    = os.path.join(outLandcoverFolder,'goge2_halfdeg_simple.nc')

            # worldReg       = 9 # Id of worldRegion
            # Read region mapfile
            try:
                x, y, worldRegGrid, FillVal = readMap(worldRegFile, 'AAIGrid')
            except:
                logger.error('World region Grid file (Arc/ASCII) "' + os.path.abspath(worldRegFile) + ' not found...')
                sys.exit(2)
            # Formulate land cover change (Method: Report Winsemius, 2010)
            # landcoverInFile = os.path.join(caseFolder, 'inlandcover','LANDCOVER.OUT')
            Now = 2000;
            Fut = int(timePeriod)

            # Read land cover files in current climate and future climate
            try:
                coverFracNow = readOUT(landcoverInFile, Now)
                # region, coverFracNow = readLc(landCoverNow)
            except:
                logger.error('Current land cover .OUT file "' + os.path.abspath(landcoverInFile) + '" not found or wrongfully formatted')
                sys.exit(2)
            try:
                coverFracFut = readOUT(landcoverInFile, Fut)
            except:
                logger.error('Future land cover .OUT file "' + os.path.abspath(landcoverInFile) + '" not found or wrongfully formatted')
                sys.exit(2)
            landCoverDiff = coverFracFut-coverFracNow
            select_types = arange(0,len(landCoverDiff)); select_types = select_types[select_types!=4]     # Remove the 5th land cover (biofuel, not included in the translation routine)
            landCoverDiff = landCoverDiff[select_types,:]

            # Compute change per world region per GLCC class
            try:
                fracChangeTotal = changeGLCC(lookupTableXML, landCoverDiff, logfile, logger)
            except:
                logger.error('Land Cover Change lookup table failed, aborting')
                sys.exit(2)
            # Impose change on NetCDF file
            try:
                impose_change(GLCC_fracMap, GLCC_newMap, worldRegGrid, fracChangeTotal, fixedCovers, logger)
            except:
                logger.error('Imposing land cover on GLCC map "' + os.path.abspath(GLCC_fracMap) + ' failed. Aborting')
                sys.exit(2)
            logger.info("GLCC land cover change imposed!")
            logger.info("New NetCDF GLCC land cover file at " + os.path.abspath(GLCC_newMap))

            # Impose change in land cover on PCRGLOB-WB parameters
            try:
                GLCC2PCRGLOB(caseFolder, runId, rootDir, logger)
                logger.info("PCR-GLOBWB parameter files successfully generated at " + os.path.abspath(os.path.join(caseName,runId,'outlandcover','maps')))
                logger.info("******************      Land Cover change module completed successfully    ******************")

            except:
                logger.error(sys.exc_info())
                logger.info("******************       PCR-GLOBWB parameter maps change completed with ERRORS!   ******************")
                closeLogger(logger, ch)
                sys.exit(2)
        """LAND COVER CHANGE MODULE IS DONE!"""
        """
        HYDROLOGICAL MODULE STARTS BELOW
        """
        if any([runAll,runHydrology]):
            logger.info('******************       Initializing Hydrology Module      ******************')
            # startYear   = 1961
            # endYear     = 1990 # 1962
#            startdate   = [startYear,12,31]
            logger.info(str('Running hydrology from %4.f until %4.f') % (startYear, endYear))
            # make a lookup table in a dictionary containing:
            # - time: all the dates that we will run
            # - var1: for each date, the file that contains var1
            # - var2: for each date, the file that contains var2, 
            # etc....
            startDate                  = dt.datetime(startYear, 1,  1, 0, 0)
            endDate                    = dt.datetime(endYear,  12, 31, 0, 0)
            lookup_pcrglobInputs       = lookup_climate_files(climateInFolder, pcrglobInputVars, startDate, endDate)
            for f, year in enumerate(range(startYear, endYear + 1)):
                # outputLoc = os.path.join(caseFolder,runId,'outmaps')
                lastDateOfPrevYear     = dt.datetime(year-1, 12, 31, 0, 0)
                lastDateOfYear         = dt.datetime(year, 12, 31, 0, 0)
                lastDateOfPrevYearStr  = lastDateOfPrevYear.strftime('%Y%m%d')
                lastDateOfYearStr      = lastDateOfYear.strftime('%Y%m%d')
                pcrglobInStateFile     = os.path.join(warmStateFolder, lastDateOfPrevYearStr + '_pcrglob.zip')  # this is the expected initial state file in current year
                dynroutInStateFile     = os.path.join(warmStateFolder, lastDateOfPrevYearStr + '_dynrout.zip')  # this is the expected initial state file in current year
                pcrglobEndStateFile    = os.path.join(warmStateFolder, lastDateOfYearStr + '_pcrglob.zip')  # this is the expected initial state file in current year
                dynroutEndStateFile    = os.path.join(warmStateFolder, lastDateOfYearStr + '_dynrout.zip')  # this is the expected initial state file in current year
                pcrglobOutMapsFile     = os.path.join(outMapsFolder, lastDateOfYearStr + '_pcrglob.nc')  # this is the expected output file in the current year
                dynroutOutMapsFile     = os.path.join(outMapsFolder, lastDateOfYearStr + '_dynrout.nc')  # this is the expected output file in the current year
                # outputFile = os.path.join(outputLoc,str(year) + '1231_dynRout_flf_wh.nc')  # this is the expected output file in the current year
                if logical_and(os.path.isfile(pcrglobOutMapsFile)==True, os.path.isfile(dynroutOutMapsFile)==True):
                    logger.info('Files "' + pcrglobOutMapsFile + '" and "' + dynroutOutMapsFile + '" already exists')     # check if outputfile already exists, if so, skip this year
                else:
                    """
                    All code below is only executed in the first year! This includes:
                        - deleting old localDataStore
                        - choosing PCRaster parameter maps (original or updated?)
                        - preparing warm initial states for PCRGLOB-WB and dynRout
                    """
                    if f==0:
                        # first check if the models PCR-GLOBWB and dynRout are already present in the case folder
                        if not os.path.isdir(pcrglobFolder):
                            logger.info('Unzipping a clean PCR-GLOBWB model to "' + modulesFolder + '"')
                            unzip_all(pcrglobZip, modulesFolder)
                            # check whether default or land cover changed parameters should be used.                        
                        else:
                            logger.info('PCR-GLOBWB model already present in "' + modulesFolder)
                        
                        # Copying new parameter files from IMAGE
                        if run_default==True:
                            useNewParameters = 'yes'
                        else:
                            useNewParameters = query_yes_no('Do you want to run with newly derived PCR-GLOBWB land cover parameter set (made with the "-l" option)?')
                        if useNewParameters == 'yes':
                            mapLoc = os.path.join(caseFolder, runId, 'outlandcover', 'maps')
                            pcrglob_mapLoc = os.path.join(pcrglobFolder, 'input','maps')
                            try:
                                logger.info('Copy land cover paramater files from "' + mapLoc + '" to "' + os.path.abspath(pcrglob_mapLoc) + '"')
                                for filename in glob.glob(os.path.join(mapLoc, '*.*')):
                                    shutil.copy(filename, pcrglob_mapLoc)
                            except:
                                logger.error(sys.exc_info())
                                logger.info('Please check existence of folders: ' + os.path.abspath(mapLoc) + ' and ' + os.path.abspath(pcrglob_mapLoc))
                                closeLogger(logger, ch)
                                sys.exit(2)
                        else:
                            logger.info('Keeping default parameter set')
                            
                        # unzipping clean DynRout model instance
                        if not os.path.isdir(dynroutFolder):
                            logger.info('Unzipping a clean DynRout model to "' + modulesFolder + '"')
                            unzip_all(dynroutZip, modulesFolder)
                        else:
                            logger.info('DynRout model already present in "' + modulesFolder)
                        
                        # now check if a state is present on the 31st of December of the previous year
                        if logical_and(os.path.isfile(pcrglobInStateFile)==True, os.path.isfile(dynroutInStateFile)==True):
                            logger.info('File "' + pcrglobInStateFile + '" and "' + dynroutInStateFile + '" already exists')     # check if statefiles already exist, then skip
                            # prepare an initial state by running hydrology over some years
                        else:
                            pcrglobInColdStateFile     = os.path.join(warmStateFolder, 'state_update_pcrglob.zip')  # this is the expected initial state file in current year
                            dynroutInColdStateFile     = os.path.join(warmStateFolder, 'state_update_dynrout.zip')  # this is the expected initial state file in current year
                            pcrglobEndColdStateFile    = os.path.join(warmStateFolder, 'state_update_pcrglob.zip')  # this is the expected initial state file in current year
                            dynroutEndColdStateFile    = os.path.join(warmStateFolder, 'state_update_dynrout.zip')  # this is the expected initial state file in current year
                            pcrglobColdOutMapsFile     = os.path.join(outMapsFolder,   'state_update_pcrglob.nc')   # this is a temporary output file, only for the state updating
                            dynroutColdOutMapsFile     = os.path.join(outMapsFolder,   'state_update_dynrout.nc')   # this is a temporary output file, only for the state updating
                            shutil.copy(pcrglobColdState, pcrglobInColdStateFile)
                            shutil.copy(dynroutColdState, dynroutInColdStateFile)
                            logger.info(str('Preparing warm states by running year %4.f until year %4.f from a cold start') % (startYear, startYear + warmStatePeriod - 1))
                            ############ RUNNING THE MODELS ##############
                            for stateUpdateYear in range(startYear, startYear + warmStatePeriod):
                                pcrglobArguments = '%g .' # the %g argument is always replaced by the number of time steps
                                timeList = run_model_year(pcrglobPurgeFolders, 
                                    pcrglobInColdStateFile, 
                                    pcrglobInStateFolder,
                                    pcrglobEndColdStateFile,
                                    pcrglobEndStateFolder,
                                    lookup_pcrglobInputs,
                                    pcrglobInputVars, 
                                    pcrglobInputFolders,
                                    pcrglobInputPrefixs,
                                    pcrglobInputSlopes,
                                    pcrglobInputOffsets,
                                    stateUpdateYear,
                                    pcrglobFolder,
                                    pcrglobCommand,
                                    logger,
                                    arguments=pcrglobArguments,
                                    logFileModel='pcrglob.log')

                                # now save the results to the correct files
                                prepare_nc(pcrglobColdOutMapsFile, stateUpdateYear, lon_ax, lat_ax, metadata, logger)
                                #timeList = [dt.datetime(stateUpdateYear, 1, 1, 0, 0), dt.datetime(stateUpdateYear, 1, 2, 0, 0)]
                                for pcrglobOutputFolder, pcrglobOutputPrefix, pcrglobOutputVar, pcrglobOutputUnit, pcrglobOutputVarName in zip(pcrglobOutputFolders, pcrglobOutputPrefixs, pcrglobOutputVars, pcrglobOutputUnits, pcrglobOutputVarNames):
                                    write_netcdf_timeseries(pcrglobOutputFolder, pcrglobOutputPrefix, pcrglobColdOutMapsFile, pcrglobOutputVar, pcrglobOutputUnit, pcrglobOutputVarName, timeList)
                                # prepare dictionary of input locations for DynRout
                                lookup_dynroutInputs       = lookup_climate_files('', dynroutInputVars, startDate, endDate, srcFiles=[pcrglobColdOutMapsFile], lookup_table={})
                                # now run dynRout, with the outputs of pcr-globwb as inputs
                                dynroutArguments = '-C world -T %g' # the %g argument is always replaced by the number of time steps
                                timeList = run_model_year(dynroutPurgeFolders, 
                                    dynroutInColdStateFile, 
                                    dynroutInStateFolder,
                                    dynroutEndColdStateFile,
                                    dynroutEndStateFolder,
                                    lookup_dynroutInputs,
                                    dynroutInputVars, 
                                    dynroutInputFolders,
                                    dynroutInputPrefixs,
                                    dynroutInputSlopes,
                                    dynroutInputOffsets,
                                    stateUpdateYear,
                                    dynroutFolder,
                                    dynroutCommand,
                                    logger,
                                    arguments=dynroutArguments,
                                    logFileModel='dynrout.log')
                                # delete the temporary output file
                                os.unlink(pcrglobColdOutMapsFile)
                            # States are prepared !now write the state files to the first warm state
                            logger.info('Copy PCR-GLOBWB warm states to the first initial state "' + pcrglobInStateFile + '"')
                            logger.info('Copy DynRout warm states to the first initial state "' + dynroutInStateFile + '"')
                            shutil.copy(pcrglobInColdStateFile, pcrglobInStateFile)                            
                            shutil.copy(dynroutInColdStateFile, dynroutInStateFile)                            
                    """
                    All code above is only executed in the first year!
                    """
#                    try:
#                        srcFile = os.path.abspath(glob.glob(os.path.join(climateInFolder,'*' + str(year) +'*.nc*'))[0])
#                    except:
#                        logger.error('File or path location/wildcard "' + os.path.join(climateInFolder,'*' + str(year) +'*.nc*') + '" was not found! Exiting!')
#                        closeLogger(logger, ch)
#                        sys.exit(2)
                    # pcrglobArguments = '%g ' + pcrglobFolder # the %g argument is always replaced by the number of time steps
                    if os.path.isfile(pcrglobOutMapsFile)==True:
                        logger.info('File "' + pcrglobOutMapsFile + '" already exists')     # check if outputfile already exists, if so, skip this year
                    else:
                        pcrglobArguments = '%g .' # the %g argument is always replaced by the number of time steps
                        timeList = run_model_year(pcrglobPurgeFolders, 
                            pcrglobInStateFile, 
                            pcrglobInStateFolder,
                            pcrglobEndStateFile,
                            pcrglobEndStateFolder,
                            lookup_pcrglobInputs,
                            pcrglobInputVars, 
                            pcrglobInputFolders,
                            pcrglobInputPrefixs,
                            pcrglobInputSlopes,
                            pcrglobInputOffsets,
                            year,
                            pcrglobFolder,
                            pcrglobCommand,
                            logger,
                            arguments=pcrglobArguments)
    
                        # now save the results to the correct files
                        prepare_nc(pcrglobOutMapsFile, year, lon_ax, lat_ax, metadata, logger)
                        #timeList = [dt.datetime(year, 1, 1, 0, 0), dt.datetime(year, 1, 2, 0, 0)]
                        for pcrglobOutputFolder, pcrglobOutputPrefix, pcrglobOutputVar, pcrglobOutputUnit, pcrglobOutputVarName in zip(pcrglobOutputFolders, pcrglobOutputPrefixs, pcrglobOutputVars, pcrglobOutputUnits, pcrglobOutputVarNames):
                            write_netcdf_timeseries(pcrglobOutputFolder, pcrglobOutputPrefix, pcrglobOutMapsFile, pcrglobOutputVar, pcrglobOutputUnit, pcrglobOutputVarName, timeList)
                    # prepare dictionary of input locations for DynRout
                    lookup_dynroutInputs       = lookup_climate_files('', dynroutInputVars, startDate, endDate, srcFiles=[pcrglobOutMapsFile], lookup_table={})
                    # now run dynRout, with the outputs of pcr-globwb as inputs
                    dynroutArguments = '-C world -T %g' # the %g argument is always replaced by the number of time steps
                    timeList = run_model_year(dynroutPurgeFolders, 
                        dynroutInStateFile, 
                        dynroutInStateFolder,
                        dynroutEndStateFile,
                        dynroutEndStateFolder,
                        lookup_dynroutInputs,
                        dynroutInputVars, 
                        dynroutInputFolders,
                        dynroutInputPrefixs,
                        dynroutInputSlopes,
                        dynroutInputOffsets,
                        year,
                        dynroutFolder,
                        dynroutCommand,
                        logger,
                        arguments=dynroutArguments)
                    prepare_nc(dynroutOutMapsFile, year, lon_ax, lat_ax, metadata, logger)
                    #timeList = [dt.datetime(year, 1, 1, 0, 0), dt.datetime(year, 1, 2, 0, 0)]
                    for dynroutOutputFolder, dynroutOutputPrefix, dynroutOutputVar, dynroutOutputUnit, dynroutOutputVarName in zip(dynroutOutputFolders, dynroutOutputPrefixs, dynroutOutputVars, dynroutOutputUnits, dynroutOutputVarNames):
                        write_netcdf_timeseries(dynroutOutputFolder, dynroutOutputPrefix, dynroutOutMapsFile, dynroutOutputVar, dynroutOutputUnit, dynroutOutputVarName, timeList)

        """HYDROLOGICAL MODULE IS DONE!"""
        """
        POST-PROCESSING MODULE STARTS BELOW
        """
        if any([runAll,runPost]):
            logger.info('******************       Initializing Post-processing Module      ******************')
            outStatsFile = os.path.join(outStatsFolder, 'Statistics.nc')
            gumbelFile   = os.path.join(outStatsFolder, 'Gumbel_params.nc')
            prefix       = 'flvol_dynRout_' + caseName + '_' + runId
            try:
                x, y, cellArea, FillVal = readMap(cellAreaFile, 'PCRaster')
                cellArea = np.flipud(cellArea)
            except:
                logger.error('Cell Area file "' + os.path.abspath(cellAreaFile) + ' not found...')
                sys.exit(2)
            try:
                x, y, hydroYears, FillVal = readMap(hydroYearsFile, 'PCRaster')
                hydroYears = np.flipud(hydroYears)
            except:
                logger.error('Hydro years file "' + os.path.abspath(hydroYearsFile) + ' not found...')
                sys.exit(2)

            #logger.warning('Post-processing is not yet implemented in GLOFRIS 2.0')
            #logger.warning('New post-processing will use extreme value analysis as presented in ERL, Ward et al. (submitted)')
            if not(os.path.isfile(outStatsFile)):
                try:
                    logger.info('Deriving annual extreme flood volumes in "' + outStatsFile + '"')
                    derive_maxima(outMapsFolder, startYear, endYear, cellArea, hydroYears, outStatsFile, metadata, logger)
                except:
                    logger.error('Please check if all files for all years are present in "' + outMapsFolder + '"')
                    sys.exit(2)
            else:
                logger.info('Annual extreme flood volumes already present in "' + outStatsFile + '"')
            if not(os.path.isfile(gumbelFile)):
                try:
                    logger.info('Deriving Gumbel distribution')
                    derive_Gumbel(outStatsFile, startYear, endYear, gumbelFile, metadata, logger)
                except:
                    logger.error('Please check if file "' + statsFile + '" is present and complete')
                    sys.exit(2)
            else:
                logger.info('Gumbel statistics already present in "' + gumbelFile + '"')
            if len(return_periods) > 0:
                apply_Gumbel(gumbelFile, outStatsFolder, prefix, return_periods, cellArea, logger)
            else:
                logger.warning('No return periods found in section "postprocessor" in .ini file. Please specify these and run again')
                
            logger.info('Please continue with the GLOFRIS inundation using the .map files in "' + outStatsFolder + '"')
        """POST-PROCESSING MODULE IS DONE"""
        """
        RISK MODULE STARTS BELOW
        """
            # prepare risk statistics if configured by user
        if any([runAll,runRisk]):
            logger.warning('The risk module is not yet transferred to GLOFRIS 2.0.')
            logger.warning('Risks will be transferred to the 30" GLOFRIS inundation downscaling and will be abandoned in the main GLOFRIS')
#            outputLoc = os.path.join(caseFolder,runId,'outstats')
#            statisticFileOutput = os.path.join(outputLoc, scenarioName + '_' + timePeriod + '_' + runId + '.nc')
#            if population_file:
#                FillVal = -9999.
#                try:
#                    population, glob_attr, var_attr = read_NetCDF_exposure(population_file, population_var, int(timePeriod))
#                    # x, y, population, FillVal = readMap(population_file, 'AAIGrid');population[population==FillVal] = nan;population=flipud(population)
#                except:
#                    logger.warning('Could not read or find "' + population_file + '". Skipping affected population !')
#                    logger.error(traceback.print_exc())
#                    population = None
#                # overwrite some of the metadata entries
#                glob_attr['title'] = 'GLObal Flood Risks with IMAGE Scenarios'
#                glob_attr['institution'] = 'Deltares, PBL, Utrecht University'
#                glob_attr['source'] = 'GLOFRIS v. 2.0; $Revision: 733 $; $Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $ '
#                glob_attr['history'] = time.ctime()
#                glob_attr['references'] = 'http://www.hydrol-earth-syst-sci-discuss.net/9/9611/2012/hessd-9-9611-2012.html'
#                glob_attr['Conventions'] = 'CF-1.4'
#                glob_attr['scenario_name'] = metadata['scenario_name']
#                glob_attr['scenario_long_name'] = metadata['scenario_long_name']
#                var_attr['standard_name'] = 'pop_risk'
#                var_attr['long_name'] = 'Yearly average population affected'
#                if type(population) is ndarray:
#                    logger.info('Establishing yearly averaged affected population risk')
#                    population_risk_file =  os.path.join(caseFolder, runId, 'outrisk', 'population_risk.nc')
#                    population_risk = GLOFRIS_risk(statisticFileOutput, population, population_factor, startYear, endYear, logger)
#                    population_risk[isnan(population_risk)] = FillVal
#                    write_risk_file(population_risk_file, 'population_risk', population_risk, glob_attr, var_attr, int(timePeriod), FillVal, logger)
#                    
#            if gdp_file:
#                FillVal = -9999.
#                try:
#                    gdp, glob_attr, var_attr = read_NetCDF_exposure(gdp_file, gdp_var, int(timePeriod))
#                    # x, y, gdp, FillVal = readMap(gdp_file, 'AAIGrid');gdp[gdp==FillVal] = nan;gdp=flipud(gdp)
#                except:
#                    logger.warning('Could not read or find "' + gdp_file + '". Skipping affected GDP !')
#                    logger.error(traceback.print_exc())
#                    gdp = None
#                glob_attr['title'] = 'GLObal Flood Risks with IMAGE Scenarios'
#                glob_attr['institution'] = 'Deltares, PBL, Utrecht University'
#                glob_attr['source'] = 'GLOFRIS v. 2.0; $Revision: 733 $; $Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $ '
#                glob_attr['history'] = time.ctime()
#                glob_attr['references'] = 'http://www.hydrol-earth-syst-sci-discuss.net/9/9611/2012/hessd-9-9611-2012.html'
#                glob_attr['Conventions'] = 'CF-1.4'
#                glob_attr['scenario_name'] = metadata['scenario_name']
#                glob_attr['scenario_long_name'] = metadata['scenario_long_name']
#                var_attr['standard_name'] = 'gdp_risk'
#                var_attr['long_name'] = 'Yearly average GDP affected'
#                if type(gdp) is ndarray:
#                    logger.info('Establishing yearly average affected gdp risk')
#                    gdp_risk_file =  os.path.join(caseFolder, runId, 'outrisk', 'gdp_risk.nc')
#                    gdp_risk = GLOFRIS_risk(statisticFileOutput, gdp, gdp_factor, startYear, endYear, logger)
#                    gdp_risk[isnan(gdp_risk)] = FillVal
#                    write_risk_file(gdp_risk_file, 'gdp_risk', gdp_risk, glob_attr, var_attr, int(timePeriod), FillVal, logger)
            
            # now compute two risk numbers, one for GDP and one for 
    except:
        logger.info('One of the GLOFRIS modules failed. Aborting')
        logger.error(traceback.print_exc())
        closeLogger(logger, ch)
        # Copy log-file to scenario Folder
#        shutil.copy2(logfile,os.path.join(caseFolder +"/" + runId))
        sys.exit(2)

except:
    sys.exit(2)
#    shutil.copy2(logfile,os.path.join(caseFolder +"/" + runId))
    logger.error(traceback.print_exc())
finally:
    logger.info('GLOFRIS Done!')
    closeLogger(logger, ch)
#    shutil.copy2(logfile,os.path.join(caseFolder +"/" + runId))
