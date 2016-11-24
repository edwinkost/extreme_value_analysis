# changeGLCC.py
"""
changeGLCC.py changes the land cover fractions of a certain IMAGE region. based
on a table, that shows the changes in fractional land cover, averaged over the 
complete world region. The table is prepared from IMAGE outputs, which give the
land cover coverage in km2. From this table

  More detailed description goes here.

  Syntax: changeGLCC(GLCC_fracMap, GLCC_newMap, worldReg, lcFracChange, logfile)

  Input:
  GLCC_fracMap:    NetCDF file, containing the fractional GLCC map
  GLCC_newMap:     NetCDF file, containing future GLCC map (to be generated)
  worldReg:        World Region considered
  lcFracChange:    Fractional change per land cover for given world region
  logfile:         Name of logfile. Log messages will be added to this file
  at a later stage: also add changes in dominant land cover (spatially explicit)

  Output:
  None, output is directly written to NetCDF file

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

$Id: changeGLCC.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/changeGLCC.py $
$Keywords: $

"""
### Reads IMAGE outputs and external base maps to estimate population densities

# import relevant packages

from numpy import *
from scipy import *
# from struct import unpack
# import string
import sys, os, os.path, shutil, ConfigParser
import osgeo.gdal as gdal
from osgeo.gdalconst import *
from xml.dom.minidom import Document, parse
# Import GLOFRIS unique functions
from GLOFRIS_utils import *
from netcdftime import *
from netCDF4_utils import *
from netCDF4 import Dataset

import csv
# START FUNCTIE HIERONDER
def readLc(landCover):
    """
    This function reads an n-column csv file containing land covers [km2] per world region
    Format of files is as follows: 
        1st row: name of land cover (skipped while reading)
        1st column: name of region
        column 2:n-1 : land cover [km2]
        column n: total surface area of region (used to divide surfaces to reach a fraction
        
    Returns:
        region:       array of N strings, region names
        coverFrac:    array of [NxM] floats, N: number of regions, M: number of land cover types
    """
    
    f = open(landCover,'r')
    data = f.readlines()
    f.close()
    region = []
    dummy = data[1].split(',')
    coverFrac = zeros((len(data)-1,len(dummy)-2))
    count = 0
    for n in data[1:]:
        s = n.split(',')
        # print s
        region.extend([s[0]])
        # print region
        coverFrac[count,:] = array(s[1:-1],dtype='f')/float(s[-1])
        count = count + 1
        
#    print data[0]
#    for row in data:
#        print row
    # f.close()
    
    
    #return data
    return region, coverFrac

def changeGLCC(transXML, lcFracChange, logfile, logger):
    """
    read translation tables from xml file
    loop per worldregion:
        loop per IMAGE cover: 
            how much of the GLCC land cover should be changed (within world region and IMAGE cover)

    All changes are summed up to a total change of the GLCC cover within specific world regions
    """
    # fix number of glcc classes
    GLCC_count = 96
    worldReg_count = 25
    transTable = parse(transXML)
    regs = transTable.getElementsByTagName("worldRegion")
    fracChangeTotal = zeros((worldReg_count,GLCC_count))
    for worldReg, reg in map(None,arange(0,len(regs)),regs): # arange(0,len(lcFracChange)): # --> CHANGE TO LOOP OVER ALL WORLD REGIONS
    #reg = regs[worldReg]
        logger.info("Computing changes for world region: " + reg.getAttribute("name") + ". Messages are returned to screen.")
        print ":Treating Region " + reg.getAttribute("name")
        IMAGEcovs = reg.getElementsByTagName("landCoverIMAGE")
        # prepare change array (MxN) where M is number of IMAGE covers and N number of GLCC covers (19x96)
        change_IM_GLCC = zeros((lcFracChange.shape[0],GLCC_count))
        for IMcov, IMnum in map(None,IMAGEcovs,arange(0,len(IMAGEcovs))):
            # IMAGE land cover ID, converted to index in array
            IMId = int(IMcov.getAttribute("id")) - 1
            
            print "\t: Treating IMAGE land cover " + IMcov.getAttribute("name") + " with ID: %1.0f " % (IMId+1)
            GLCCCovs = IMcov.getElementsByTagName("landCoverGLCC")
            if len(GLCCCovs) == 0:
                print '\t\t: IMAGE Land cover "' + IMcov.getAttribute("name") + '" not present in ' +  reg.getAttribute("name")
                
            for Cov in GLCCCovs:
                fracElement = Cov.getElementsByTagName("fraction")
                CovId       = int(Cov.getAttribute("id"))-1
                frac = float(fracElement[0].lastChild.wholeText)
                fracChange = frac*lcFracChange[IMnum,worldReg]
                print "\t\t: Change in GLCC-cover: " + Cov.getAttribute("name") + " with ID: %1.0f \t: %1.3f %%" % (CovId+1,fracChange*100)
                # fill CHANGE array: change_IM_GLCC
                change_IM_GLCC[IMId,CovId] = fracChange
            # compute total change per GLCC cover (sum over IMAGE classes)
        fracChangeTotal[worldReg,:] = change_IM_GLCC.sum(axis=0)
    return fracChangeTotal

def impose_change(GLCC_fracMap, GLCC_newMap, worldRegGrid, fracChangeTotal, fixedCovers, logger):
    """
    Change per world Region, the land cover fractions according to the derived changes
    Write to new GLCC NetCDF file
    finally:
    Read NetCDF back into memory and normalize to a total of 1 per pixel
    Finally check whether the normailzed grid is more or less equivalent to the land cover changes from
    The IMAGE scenario
    Input:
        - GLCC_fracMap    : NetCDF file containing the GLCC fractional coverage map (0.5x0.5 deg)
        - GLCC_newMap     : New (future) GLCC NetCDF-file, to be made in this function
        - worldRegGrid    : world regions grid [0.5x0.5 deg.]
        - fracChangeTotal : fractional changes per world region per land cover
        - fixedCovers     : land covers indices that are not expected to change (such as sea and inland waters)
    """
    seterr(all='ignore')
    noOfClasses = fracChangeTotal.shape[1]
    xlen = worldRegGrid.shape[1]
    ylen = worldRegGrid.shape[0]
    # First generate a copy of the NetCDF file with the land covers
    try:
        logger.info("Creating new NetCDF GLCC map: " + os.path.abspath(GLCC_newMap) + " from original GLCC map: " + os.path.abspath(GLCC_fracMap))
        shutil.copy2(GLCC_fracMap, GLCC_newMap)
    except:
        logger.error('Original NetCDF GLCC map "' + os.path.abspath(GLCC_fracMap) + '" does not exist. Exiting')
        sys.exit(2)
    # Open both NetCDF files with Olson classes and compute per IMAGE land cover 
    rootnow = Dataset(GLCC_fracMap,'r')
    rootfut = Dataset(GLCC_newMap,'a')
    # link to variable 
    fracNow = rootnow.variables['class_fractions']
    print 'Old fractions loaded'
    fracFut = rootfut.variables['class_fractions']
    print 'New fractions loaded'

    # Now impose the changes on the new map
    logger.info('Imposing land cover changes...')
    for Cov in arange(0, fracChangeTotal.shape[1]):
        diff_map = ones((worldRegGrid.shape))
        # Loop over each world region to create a diff. map
        # for worldReg in arange(0,len(fracChangeTotal)):
        print "changing land cover: " + str(Cov)
        for worldReg in arange(0,len(fracChangeTotal)): # worldReg = 9
            # print "changing world region: " + str(worldReg)
            fracChange = fracChangeTotal[worldReg,:]
            diff_map[worldRegGrid==worldReg+1] = 1+fracChangeTotal[worldReg,Cov]
        fracFut[:,:,Cov] = fracNow[:,:,Cov]*diff_map
    # All covers are changed, now normalize so that their sum remains 1!!
    # In this action, the non-changing covers are excluded:
    # the multiplication factor for each changing land cover is computed as:
        #                  1-sum(fixed_covers)
        # multip = ----------------------------------
        #           sum(all_covers)-sum(fixed_covers)

    multip = (1-fracFut[:,:,fixedCovers].sum(axis=2))/(fracFut[:].sum(axis=2)-fracFut[:,:,fixedCovers].sum(axis=2))
    multip[isnan(multip)] = 1
    multip[multip < 0] = 1
    multip[multip > 2] = 1
    multip[~isfinite(multip)] = 1
    multip_rep = multip.repeat(noOfClasses,axis=1)
    multip_3d = multip_rep.reshape(ylen,xlen,noOfClasses)
    # now make the multiplication of fixed classes 1 (i.e. no change)
    multip_3d[:,:,fixedCovers] = 1
    fracFut[:,:,arange(0,multip_3d.shape[2])] = fracFut[:,:,arange(0,multip_3d.shape[2])]*multip_3d
    rootnow.sync()
    rootnow.close()
    rootfut.sync()
    rootfut.close()
    seterr()
    logger.info('Land cover changes imposed on "' + os.path.abspath(GLCC_newMap) + '"')
