# -*- coding: utf-8 -*-
"""
Created on Wed Feb 09 12:54:16 2011

GLCC2PCRGLOB.py translates an Olson fractional land cover map (NetCDF format)
into all required PCRGLOB-WB parameter maps

***************************************************************************************************
* This script converts fractional GLCC maps (netCDF format) into PCRGLOB-WB parameter files       *
* fractional GLCC maps need to be prepared from script "conv_glcc.py"                             *
* Script has been adapted from ArcGIS scripting "goge_par_rerun.py" by R. van Beek, Utrecht Univ. *
***************************************************************************************************

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

$Id: GLCC2PCRGLOB.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/GLCC2PCRGLOB.py $
$Keywords: $

"""

from numpy import *
from scipy import *
from netcdftime import *
from netCDF4_utils import *
from netCDF4 import *
from csv import *
from GLOFRIS_utils import *
import glob
#from matplotlib.pyplot import *

def readNetCDF(file_path):
    rootgrp = Dataset(file_path, 'r')
    return rootgrp

def readOlson_par(file_path):
    olson_par=dict()
    csvReader = DictReader(open(file_path, "rb"))
    for line in csvReader:
        olson_par[line['Type']]=line
    return olson_par

def GLCC2PCRGLOB(caseFolder, runId, rootDir, logger):
    # file locations
    olson_parLoc  = os.path.join(rootDir,'landCoverGLCC')                        # location of Olson parameter file (.csv)
    GLCC_mapLoc   = os.path.join(caseFolder, runId, 'outlandcover')    # location of the new IMAGE-changed GLCC map
    relLAI_mapLoc = os.path.join(rootDir,'relLAI')  # location of fixed rel LAI maps
    metfactorloc  = os.path.join(rootDir,'metfactor')         # location of fixed metfactor map
    soilmaploc    = os.path.join(rootDir,'soilMap')           # location of fixed soil maps (z1 and z2)
    # file names
    GLCC_mapFile  = 'goge2_halfdeg_simple.nc'                 # GLCC map (will be converted to PCRGLOB-WB parameter files)
    olson_parFile = 'Olson_characteristics.csv'               # Olson parameter file (.csv)
    relLAI_mapFile= 'relLAI.nc'                               # rel LAI map file (.netCDF)
    metfactor_map = 'metfactor.map'                           # Meteo factor map (PCRaster)
    soilz1_map    = 'fao30_z1.map'                            # Soil depth layer z1 (PCRaster)
    soilz2_map    = 'fao30_z2.map'                            # Soil depth layer z2 (PCRaster)

    targetLoc     = os.path.join(caseFolder, runId, 'outlandcover','maps')           # Folder where new PCRGLOB-WB parameter files should be written
    if not os.path.isdir(targetLoc):                          # create folder if it does not already exist
        os.makedirs(targetLoc)

    logger.info('Writing PCRaster parameter maps to "' + targetLoc + '"')
    olson_pars    = readOlson_par(os.path.join(olson_parLoc,olson_parFile))
    glcc_root     = readNetCDF(os.path.join(GLCC_mapLoc, GLCC_mapFile))
    relLAI_root   = readNetCDF(os.path.join(relLAI_mapLoc, relLAI_mapFile))
    MonthExt      = ['001','032','060','091','121','152','182','213','244','274','305','335']

    # the ID number of land cover types which are excluded is given here! TRIAL WITH OPEN WATER INCLUDED
    # excluded_types = array([15,18,39,49,65,66,67,68,70,71,73,74,75,77,80,81,82,83,84,85,86,87,88,97,98,99])

    # The list of land types excluded below seems to be appropriate for Smax, cv and fraction short/tall.
    excluded_types = array([14,15,18,39,49,65,66,67,68,70,71,73,74,75,77,80,81,82,83,84,85,86,87,88,97,98,99])

    """ PROCESSING OF THE PARAMETER MAPS STARTS BELOW!!! """
    x, y, metfactorMap, FillVal = readMap(os.path.join(metfactorloc, metfactor_map), 'PCRaster'); metfactorMap[metfactorMap==FillVal] = nan
    x, y, soilMap_z1, FillVal   = readMap(os.path.join(soilmaploc, soilz1_map), 'PCRaster'); soilMap_z1[soilMap_z1==FillVal] = nan
    x, y, soilMap_z2, FillVal   = readMap(os.path.join(soilmaploc, soilz2_map), 'PCRaster'); soilMap_z2[soilMap_z2==FillVal] = nan

    mask = soilMap_z2 ==FillVal
    la,lo = where(isnan(soilMap_z2))
    relLAI      = relLAI_root.variables["relative_lai"][:].data; relLAI[where(relLAI==relLAI_root.variables["relative_lai"]._FillValue)]=0;relLAI[la,lo,:] = nan
    nrTypes     = len(glcc_root.dimensions["class"])
    nrLat       = len(glcc_root.variables["latitude"])
    nrLong      = len(glcc_root.variables["longitude"])
    nrMonthsLAI = len(relLAI_root.variables["month"])

    # initialize maps for PCRGLOB-WB parameters
    tall_fracMap  = zeros((nrLat, nrLong));                 tall_fracMap[la,lo]  = nan; tall_fracMapFile  = 'vegf_tall.map'      # tall vegetation fraction [-]
    short_fracMap = zeros((nrLat, nrLong));                 short_fracMap[la,lo] = nan; short_fracMapFile = 'vegf_short.map'     # short vegetation fraction [-]
    CV_short      = zeros((nrLat, nrLong, nrMonthsLAI));    CV_short[la,lo,:]    = nan; CV_shortFile = 'cv_s0000.'               # Fractional cover short [-] (monthly time series)
    CV_tall       = zeros((nrLat, nrLong, nrMonthsLAI));    CV_tall[la,lo,:]     = nan; CV_tallFile = 'cv_t0000.'                # Fractional cover tall [-] (monthly time series)
    Smax_short    = zeros((nrLat, nrLong, nrMonthsLAI));     Smax_short[la,lo,:] = nan; Smax_shortFile = 'smax_s00.'             # Interception capacity short [m] (monthly time series)
    Smax_tall     = zeros((nrLat, nrLong, nrMonthsLAI));     Smax_tall[la,lo,:]  = nan; Smax_tallFile = 'smax_t00.'              # Interception capacity tall [m] (monthly time series)
    Kc_rel_short  = zeros((nrLat, nrLong, nrMonthsLAI));     Kc_rel_short[la,lo,:]= nan   # Relative crop factor short (monthly time series)
    Kc_rel_tall   = zeros((nrLat, nrLong, nrMonthsLAI));     Kc_rel_tall[la,lo,:]= nan# Relative crop factor tall (monthly time series)
    Kc_short      = zeros((nrLat, nrLong, nrMonthsLAI));     Kc_short[la,lo,:]   = nan; Kc_shortFile = 'kc_s0000.'              # Crop factor short [-] (monthly time series)
    Kc_tall       = zeros((nrLat, nrLong, nrMonthsLAI));     Kc_tall[la,lo,:]    = nan; Kc_tallFile = 'kc_t0000.'               # Crop factor tall [-] (monthly time series)
    rootF_z1_short= zeros((nrLat, nrLong));                  rootF_z1_short[la,lo]  = nan; rootF_z1_shortFile = 'rfrac1_short.map'    # Root fraction layer 1 [-]
    rootF_z2_short= zeros((nrLat, nrLong));                  rootF_z2_short[la,lo]  = nan; rootF_z2_shortFile = 'rfrac2_short.map'    # # Root fraction layer 2 [-]
    rootF_z1_tall= zeros((nrLat, nrLong));                   rootF_z1_tall[la,lo]   = nan; rootF_z1_tallFile  = 'rfrac1_tall.map'    # Root fraction layer 1 [-]
    rootF_z2_tall= zeros((nrLat, nrLong));                   rootF_z2_tall[la,lo]   = nan; rootF_z2_tallFile  = 'rfrac2_tall.map'    # # Root fraction layer 2 [-]

    # initialize maps for calculation of PCRGLOB-WB parameters
    LAI           = zeros((nrLat, nrLong, nrMonthsLAI));     LAI[la,lo,:] = nan;               #
    CV            = zeros((nrLat, nrLong, nrMonthsLAI));     CV[la,lo,:] = nan;               #
    Smax          = zeros((nrLat, nrLong, nrMonthsLAI));     Smax[la,lo,:] = nan;               #
    Kc            = zeros((nrLat, nrLong, nrMonthsLAI));     Kc[la,lo,:] = nan;               #
    LAI_short     = zeros((nrLat, nrLong, nrMonthsLAI));     LAI_short[la,lo,:] = nan; # LAI (monthly time series)
    LAI_tall      = zeros((nrLat, nrLong, nrMonthsLAI));     LAI_tall[la,lo,:] = nan;  # LAI (monthly time series)
    Hveg_thresshort = zeros((nrLat, nrLong));                Hveg_thresshort[la,lo] = nan;       # Vegetation height
    Hveg_threstall  = zeros((nrLat, nrLong));                Hveg_threstall[la,lo]  = nan;       # Vegetation height
    # Find Caspian sea pixels (masked in metfactor map but available in parameter files)
    row_casp,col_casp = where((isfinite(rootF_z1_short))*(isnan(metfactorMap)))

    # Determine for each land cover type
    for i in range(nrTypes):
        # Load Olson fractions (remove values at positions where soil map has no values)
        if len(where(excluded_types == i+1)[0]) == 0: # if this occurs, the layer is NOT excluded and is treated!
        # if i!= 96 and i!=97 and i!=98 and i!=13 and i!=14: # These are open water bodies and no_data QUOTED: i != 13 and i != 14 and
            olsonLayer = glcc_root.variables["class_fractions"][:,:,i];olsonLayer[la,lo] = nan
            olsonLayer_rep = olsonLayer.repeat(12,axis=1).reshape((360,720,12))
            logger.info(str('Processing Olson layer %1.0f') % i)
            # Retrieve constants from Olson table
            Hveg       = min(max((float(olson_pars[str(i+1)]['z0 veg'])/0.123),0.1),10.) # Vegetation height [m]
            Hveg_thres = min(max((float(olson_pars[str(i+1)]['z0 veg'])/0.123),0.1),2.)  # Vegetation height limited to 2.0 m [m]
            LAId       = float(olson_pars[str(i+1)]['LAI d'])                            # dormancy LAI [-]
            LAIg       = float(olson_pars[str(i+1)]['LAI g'])                            # growing LAI [-]
            Smaxd      = float(olson_pars[str(i+1)]['Smax d'])                           # dormancy interception store [m]
            Smaxg      = float(olson_pars[str(i+1)]['Smax g'])                           # growing interception store [m]
            CVd        = float(olson_pars[str(i+1)]['cvd'])                              # dormancy fractional vegetation coverage [-]
            CVg        = float(olson_pars[str(i+1)]['cvg'])                              # growing fractional vegetation coverage [-]
            rootdepth  = float(olson_pars[str(i+1)]['Root depth'])                       # root depth [m]
            Kcb_h      = 1. + 0.1*Hveg_thres
            # Generate maps, fixed throughout year
            Kc_meteo   = metfactorMap*((Hveg/3.)**0.3)
            Kc_meteo[row_casp,col_casp] = 0 # add the Caspian sea pixels as zero
            Kc_max     = Kcb_h + Kc_meteo
            Kc_range   = Kc_max - 0.2

            # treatment of root fractions
            if rootdepth > 0:
                shapeFactor= log(0.0001)/rootdepth
                rootFrac_z1= 1-exp(shapeFactor*soilMap_z1)
                rootFrac_z2= (1-rootFrac_z1)-exp(shapeFactor*soilMap_z2)
            else:
                rootFrac_z1 = soilMap_z1*0
                rootFrac_z2 = soilMap_z2*0

            ### Compute monthly values for Olson fraction ###
            for t in range(nrMonthsLAI):
                LAI[:,:,t]   = LAId + relLAI[:,:,t]*(LAIg - LAId)
                CV[:,:,t]    = CVd + relLAI[:,:,t]*(CVg - CVd)
                Smax[:,:,t]  = Smaxd + relLAI[:,:,t]*(Smaxg - Smaxd)   # 0.0002*LAI[:,:,t]
                Kc_rel       = 1. - exp(-0.7*LAI[:,:,t])
                Kc[:,:,t]    = 0.2 + Kc_rel*Kc_range

            ### subdivide over short resp. tall fractions
            if(float(olson_pars[str(i+1)]['Tall']) == 0):
                short_fracMap = short_fracMap + olsonLayer
                CV_short     = CV_short + olsonLayer_rep*CV # Olsonlayer needs to be multiplied over 12 layers!!!
                Smax_short   = Smax_short + olsonLayer_rep*Smax
                Kc_short     = Kc_short + olsonLayer_rep*Kc
                rootF_z1_short = rootF_z1_short + olsonLayer*rootFrac_z1
                rootF_z2_short = rootF_z2_short + olsonLayer*rootFrac_z2
            else:
                tall_fracMap = tall_fracMap + olsonLayer
                CV_tall      = CV_tall  + olsonLayer_rep*CV
                Smax_tall    = Smax_tall + olsonLayer_rep*Smax
                Kc_tall      = Kc_tall + olsonLayer_rep*Kc
                rootF_z1_tall = rootF_z1_tall + olsonLayer*rootFrac_z1
                rootF_z2_tall = rootF_z2_tall + olsonLayer*rootFrac_z2
        else:
            logger.info(str('Skipping non-existent Olson layer %1.0f') % i)

    # prepare 12-layered short/tall fracmap
    tall_frac_rep = tall_fracMap.repeat(12,axis=1).reshape((360,720,12))
    short_frac_rep = short_fracMap.repeat(12,axis=1).reshape((360,720,12))

    ##
    ### Compute real average values for short/tall partitioned variables
    # short
    la_zero,lo_zero                  = where(short_fracMap!=0)
    CV_short[la_zero,lo_zero,:]      = CV_short[la_zero,lo_zero,:]/short_frac_rep[la_zero,lo_zero,:];CV_short[isnan(CV_short)]=FillVal
    Smax_short[la_zero,lo_zero,:]    = Smax_short[la_zero,lo_zero,:]/short_frac_rep[la_zero,lo_zero,:];Smax_short[isnan(Smax_short)]=FillVal
    Kc_short[la_zero,lo_zero,:]      = Kc_short[la_zero,lo_zero,:]/short_frac_rep[la_zero,lo_zero,:];Kc_short[isnan(Kc_short)]=FillVal
    rootF_z1_short[la_zero,lo_zero]  = rootF_z1_short[la_zero,lo_zero]/short_fracMap[la_zero,lo_zero];rootF_z1_short[isnan(rootF_z1_short)]=FillVal
    rootF_z2_short[la_zero,lo_zero]  = rootF_z2_short[la_zero,lo_zero]/short_fracMap[la_zero,lo_zero];rootF_z2_short[isnan(rootF_z2_short)]=FillVal

    # tall
    la_zero,lo_zero                  = where(tall_fracMap!=0)
    CV_tall[la_zero,lo_zero,:]       = CV_tall[la_zero,lo_zero,:]/tall_frac_rep[la_zero,lo_zero,:];CV_tall[isnan(CV_tall)]=FillVal
    Smax_tall[la_zero,lo_zero,:]     = Smax_tall[la_zero,lo_zero,:]/tall_frac_rep[la_zero,lo_zero,:];Smax_tall[isnan(Smax_tall)]=FillVal
    Kc_tall[la_zero,lo_zero,:]       = Kc_tall[la_zero,lo_zero,:]/tall_frac_rep[la_zero,lo_zero,:];Kc_tall[isnan(Kc_tall)]=FillVal
    rootF_z1_tall[la_zero,lo_zero]   = rootF_z1_tall[la_zero,lo_zero]/tall_fracMap[la_zero,lo_zero];rootF_z1_tall[isnan(rootF_z1_tall)]=FillVal
    rootF_z2_tall[la_zero,lo_zero]   = rootF_z2_tall[la_zero,lo_zero]/tall_fracMap[la_zero,lo_zero];rootF_z2_tall[isnan(rootF_z2_tall)]=FillVal


    for i in range(nrMonthsLAI):
    #    # Write maps to PCRaster files
        # writeMap(str(targetLoc + Smax_shortFile + MonthExt[i]), 'PCRaster', x, y, Smax_short[:,:,i], FillVal)
        writeMap(os.path.join(targetLoc, str(Smax_shortFile + MonthExt[i])), 'PCRaster', x, y, Smax_short[:,:,i], FillVal)
        writeMap(os.path.join(targetLoc, str(Smax_tallFile + MonthExt[i])), 'PCRaster', x, y, Smax_tall[:,:,i], FillVal)
        writeMap(os.path.join(targetLoc, str(CV_shortFile + MonthExt[i])), 'PCRaster', x, y, CV_short[:,:,i], FillVal)
        writeMap(os.path.join(targetLoc, str(CV_tallFile + MonthExt[i])), 'PCRaster', x, y, CV_tall[:,:,i], FillVal)
        # Kc is almost consistently much higher than the original Kc values, therefore excluded for the moment (HCW: 06-02-2012)
        # writeMap(os.path.join(targetLoc, str(Kc_shortFile + MonthExt[i])), 'PCRaster', x, y, Kc_short[:,:,i], FillVal)
        # writeMap(os.path.join(targetLoc, str(Kc_tallFile + MonthExt[i])), 'PCRaster', x, y, Kc_tall[:,:,i], FillVal)
    #
    # Write pars that are constant over the year:
    # : tallfrac and shortfrac maps (CHECKED AND OK!!!! QUOTED FOR NOW)
    sumFrac = tall_fracMap+short_fracMap
    i = where(sumFrac > 0)
    j = where(sumFrac == 0)
    #tall_fracMap[j] = nan # BUG RESOLVED on 06-02-2012 should not be nan but zero v.s. 1
    #short_fracMap[j] = nan
    tall_fracMap[j] = 0
    short_fracMap[j] = 1
    tall_fracMap[mask] = nan
    short_fracMap[mask] = nan
    # calculate sumFrac again, but now accounting for areas where there is no relevant fraction at all
    sumFrac = tall_fracMap+short_fracMap

    # NOTE!! THIS IS THE CORRECT PLACE TO FINALIZE THE TALL/SHORT FRAC!!
    tall_fracMap = tall_fracMap/sumFrac
    short_fracMap = short_fracMap/sumFrac
    tall_fracMap[isnan(tall_fracMap)] = FillVal
    short_fracMap[isnan(short_fracMap)] = FillVal
    #
    # Write tallfrac /shortfrac and root fractions to pcraster maps
    writeMap(os.path.join(targetLoc, str(tall_fracMapFile)), 'PCRaster', x, y, tall_fracMap, FillVal)
    writeMap(os.path.join(targetLoc, str(short_fracMapFile)), 'PCRaster', x, y, short_fracMap, FillVal)
    #writeMap(os.path.join(targetLoc, str(rootF_z1_shortFile)), 'PCRaster', x, y, rootF_z1_short, FillVal)
    #writeMap(os.path.join(targetLoc, str(rootF_z2_shortFile)), 'PCRaster', x, y, rootF_z2_short, FillVal)
    #writeMap(os.path.join(targetLoc, str(rootF_z1_tallFile)), 'PCRaster', x, y, rootF_z1_tall, FillVal)
    #writeMap(os.path.join(targetLoc, str(rootF_z2_tallFile)), 'PCRaster', x, y, rootF_z2_tall, FillVal)
    # remove xml files, generated by GDAL
    for xmlfile in glob.glob(os.path.join(targetLoc,'*.xml')):        # remove all xml files generated by GDAL
        os.unlink(xmlfile)
    glcc_root.close()                                            # close GLCC netCDF file
    """ PROCESSING OF PARAMETER FILES IS DONE!!! """