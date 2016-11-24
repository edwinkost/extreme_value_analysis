"""
IMAGE2GLCC.py
IMAGE2GLCC.py prepare lookup tables at IMAGE world region level between IMAGE
land cover classes and the GLCC Olson classification. This is determined by 
cross-referencing each pixel of the IMAGE dominant land cover map with the 
Olson dominant land cover map and determine the fraction of overlap between
classes of both maps per world region

  More detailed description goes here.

  Syntax: change the input folders / files if necessary and run the script

  Input:
  varargin  = not relevant, this is not a function

  Output:
  varargout = not relevant, this is not a function

 Copyright notice
  --------------------------------------------------------------------
  Copyright (C) 2011 Deltares
      H.(Hessel) C. Winsemius

      hessel.winsemius@deltares.nl

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

$Id: IMAGE2GLCC.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/IMAGE2GLCC.py $
$Keywords: $
"""

### Reads IMAGE outputs and external base maps to estimate population densities

# import relevant packages

from numpy import *
from scipy import *
# from struct import unpack
# import string
import sys,  gzip, os, os.path
import osgeo.gdal as gdal
from osgeo.gdalconst import *
from pdb import *
from mpl_toolkits.basemap import Basemap
from xml.dom.minidom import Document, parse
# Import GLOFRIS unique functions
from GLOFRIS_utils import *

# Script reads 2 files (using function "readMap"); 
# - GLCC project classification file, aggregated to 0.5 degrees dominant within-pixel land cover; and
# - HYDE basemap from IMAGE, aggregated to dominant land covers (0.5 x 0.5 deg.)
# The function "compareCover" generates an array of relations between the respective land covers

def compareCover(map1, map2, minVal,filter, worldRegions, region):
    """
    This function reads 2 classification maps and a worldRegions map and evaluates 
    for each combination of classes how many occurrences of both classes exist within
    the selected world region.
    Input:
        - map1         : map with first classification
        - map2         : map with second classification (same size as map1)
        - minVal       : contributions under this fraction are filtered out
        - filter       : classes in this filter in map2 are filtered out (e.g. sea water)
        - worldRegions : map containing all relevant wordl regions
        - region       : region considered to generate lookup table
    Output:
        - compArr   : comparison array having dimensions [<no. classes in map1> x <no. classes in map2>]
                      For each combination of classes, the number of occurrences in the whole map region is given
    """
    compArr = zeros((map1.max(),map2.max()))
    frac_class = zeros(map1.max())
    for m1 in arange(0,map1.max()):
        for m2 in arange(0,map2.max()):
            class1 = m1+1
            class2 = m2+1
            ii1 = map1==class1 # check where map1 contains land cover class 'class1'
            ii2 = map2==class2 # check where map2 contains land cover class 'class2'
            ii3 = worldRegions==region # check where worldRegion map is the selected region
            ii  = ii1*ii2*ii3
            jj  = ii1*ii3
            compArr[m1,m2] = len(nonzero(ii)[0])
            frac_class[m1] = float(len(nonzero(jj)[0]))/float(len(nonzero(ii3)[0]))
        # normalize the amount of counted pixels
        compArr[m1,:] = compArr[m1,:]/sum(compArr[m1,:])
        compArr[m1,compArr[m1,:] < minVal] = 0 
        compArr[m1,filter] = 0
        compArr[m1,:] = compArr[m1,:]/sum(compArr[m1,:])
    return frac_class, compArr

def parseResults(frac_class, compArr, map1Names, map2Names, TargetName):
    """
    This function is OBSOLETE and has been replaced by an XML-writer
    The function parses the comparison array 'compArr' to an ascii-formatted file 
    This file gives for each class in map1, the fractions of the classes, found in map2, resembling the pixel locations
    Input:

        - compArr       : array with comparison results in fractions
        - map1Names     : list of strings, belonging to the classes in map1
        - map2Names     : list of strings, belonging to the classes in map2
        - TargetName    : name (+path) of ascii file, where results are saved
    """
    
    fid = open(TargetName,'w')
    for m1 in arange(0,compArr.shape[0]):
        fid.write('IMAGE class : %g : %s : %2.2f of total surface \n\n' % (m1 + 1, map1Names[m1], frac_class[m1]))
        # find non-NaN entries in therow considered
        i = nonzero(isfinite(compArr[m1,:]))[0]
        for m2 in arange(0,len(i)):
            fid.write('%g : %s : %1.3f \n' % (i[m2]+1, map2Names[i[m2]], compArr[m1,i[m2]]))
        fid.write('\n')
    fid.close()
    return

def append_XML(frac_class, compArr, worldRegName, worldRegId, map1Names, map2Names, TargetName):
    """
    This function does the same as parseResults, but appends to an easy to read XML file
    The XML file should be generated first, using the function open_XML
    """
    xmlObj = parse(TargetName)
    worldRegs = xmlObj.firstChild
    worldReg  = xmlObj.createElement("worldRegion")
    worldReg.setAttribute("name",worldRegName)
    worldReg.setAttribute("id",worldRegId)
    worldRegs.appendChild(worldReg)
    for m1n, count1 in map(None,map1Names,arange(0,len(map1Names))):
        landCov1 = xmlObj.createElement("landCoverIMAGE")
        landCov1.setAttribute("name",m1n)
        landCov1.setAttribute("id",str(count1+1))
        worldReg.appendChild(landCov1)
        i = nonzero(isfinite(compArr[count1,:]))[0]
        for count2 in arange(0,len(i)):
            landCov2 = xmlObj.createElement("landCoverGLCC")
            landCov2.setAttribute("name",map2Names[i[count2]])
            landCov2.setAttribute("id",str(i[count2]+1))
            landCov1.appendChild(landCov2)
            fraction=xmlObj.createElement("fraction")
            landCov2.appendChild(fraction)
            fracText = xmlObj.createTextNode(str('%1.3f') % compArr[count1,i[count2]])
            fraction.appendChild(fracText)
    f = open(TargetName,'w')
    xmlObj.writexml(f)    
    #f.write(xmlObj.toprettyxml(indent="\t"))
    f.close()
    
    return xmlObj

def open_XML(TargetName):
    """
    Open a worldRegions XML-file for writing. The parent 'worldRegions' is added automatically
    """
    xmlObj = Document()
    worldRegs = xmlObj.createElement("worldRegions")
    xmlObj.appendChild(worldRegs)
    f = open(TargetName,'w')
    f.write(xmlObj.toprettyxml(indent="\t"))
    f.close()
    return xmlObj

def close_XML(TargetName):
    """
    Function generates a nicely formatted XML file from a one-line-only XML file
    """
    xmlObj = parse(TargetName)
    f = open(TargetName,'w')
    f.write(xmlObj.toprettyxml(indent="\t"))
    f.close()
    
############# END OF FUNCTIONS #########################
IMAGELoc = './landCoverIMAGE/'
GLCCLoc  = './landCoverGLCC/'
worldRegionFile = './baseMaps/GREG.asc'
TargetFolder = './lookupTables/'
TargetNameExt = '.txt'
xmlExt= '.xml'
classType = "goge"
IMAGE_class  = ["Agricultural land", \
    "Extensive grasslands", \
    "C plantations (not used)", \
    "Regrowth forest (Abandoning)", \
    "Regrowth forest (Timber)", \
    "Ice", \
    "Tundra", \
    "Wooded tundra", \
    "Boreal forest", \
    "Cool conifer", \
    "Temp. mixed forest", \
    "Temp. decid. forest", \
    "Warm mixed forest", \
    "Grassland/ steppe", \
    "Hot desert", \
    "Scrubland", \
    "Savannah", \
    "Tropical woodland", \
    "Tropical forest"]
    
if classType == "igbp":
    TargetNamePrefix = TargetFolder + "/gigbp2_lookup"
    maxCoverGLCCFile = GLCCLoc + "MAX_COVER_IGBP.asc"
    longName   = ["EVERGREEN NEEDLELEAF FOREST", \
        "EVERGREEN BROADLEAF FOREST", \
        "DECIDUOUS NEEDLELEAF FOREST", \
        "DECIDUOUS BROADLEAF FOREST", \
        "MIXED FORESTS", \
        "CLOSED SHRUBLANDS", \
        "OPEN SHRUBLANDS", \
        "WOODY SAVANNAS", \
        "SAVANNAS", \
        "GRASSLANDS", \
        "PERMANENT WETLANDS", \
        "CROPLANDS", \
        "URBAN AND BUILT-UP", \
        "CROPLAND/NATURAL VEGETATION MOSAIC", \
        "SNOW AND ICE", \
        "BARREN OR SPARSELY VEGETATED", \
        "WATER BODIES"]
    
elif classType == "goge":
    TargetNamePrefix = TargetFolder + "/goge2_lookup"
    maxCoverGLCCFile = GLCCLoc + "MAX_COVER_GOGE.asc"

    longName = ["URBAN", \
        "LOW SPARSE GRASSLAND", \
        "CONIFEROUS FOREST", \
        "DECIDUOUS CONIFER FOREST", \
        "DECIDUOUS BROADLEAF FOREST", \
        "EVERGREEN BROADLEAF FORESTS", \
        "TALL GRASSES AND SHRUBS", \
        "BARE DESERT", \
        "UPLAND TUNDRA", \
        "IRRIGATED GRASSLAND", \
        "SEMI DESERT", \
        "GLACIER ICE", \
        "WOODED WET SWAMP", \
        "INLAND WATER", \
        "SEA WATER", \
        "SHRUB EVERGREEN", \
        "SHRUB DECIDUOUS", \
        "MIXED FOREST AND FIELD", \
        "EVERGREEN FOREST AND FIELDS", \
        "COOL RAIN FOREST", \
        "CONIFER BOREAL FOREST", \
        "COOL CONIFER FOREST", \
        "COOL MIXED FOREST", \
        "MIXED FOREST", \
        "COOL BROADLEAF FOREST", \
        "DECIDUOUS BROADLEAF FOREST 2", \
        "CONIFER FOREST", \
        "MONTANE TROPICAL FORESTS", \
        "SEASONAL TROPICAL FOREST", \
        "COOL CROPS AND TOWNS", \
        "CROPS AND TOWN", \
        "DRY TROPICAL WOODS", \
        "TROPICAL RAINFOREST", \
        "TROPICAL DEGRADED FOREST", \
        "CORN AND BEANS CROPLAND", \
        "RICE PADDY AND FIELD", \
        "HOT IRRIGATED CROPLAND", \
        "COOL IRRIGATED CROPLAND", \
        "COLD IRRIGATED CROPLAND", \
        "COOL GRASSES AND SHRUBS", \
        "HOT AND MILD GRASSES AND SHRUBS", \
        "COLD GRASSLAND", \
        "SAVANNA (WOODS)", \
        "MIRE, BOG, FEN", \
        "MARSH WETLAND", \
        "MEDITERRANEAN SCRUB", \
        "DRY WOODY SCRUB", \
        "DRY EVERGREEN WOODS", \
        "VOLCANIC ROCK", \
        "SAND DESERT", \
        "SEMI DESERT SHRUBS", \
        "SEMI DESERT SAGE", \
        "BARREN TUNDRA", \
        "COOL SOUTHERN HEMISPHERE MIXED FORESTS", \
        "COOL FIELDS AND WOODS", \
        "FOREST AND FIELD", \
        "COOL FOREST AND FIELD", \
        "FIELDS AND WOODY SAVANNA", \
        "SUCCULENT AND THORN SCRUB", \
        "SMALL LEAF MIXED WOODS", \
        "DECIDUOUS AND MIXED BOREAL FOREST", \
        "NARROW CONIFERS", \
        "WOODED TUNDRA", \
        "HEATH SCRUB", \
        "COASTAL WETLAND - NW", \
        "COASTAL WETLAND - NE", \
        "COASTAL WETLAND - SE", \
        "COASTAL WETLAND - SW", \
        "POLAR AND ALPINE DESERT", \
        "GLACIER ROCK", \
        "SALT PLAYAS", \
        "MANGROVE", \
        "WATER AND ISLAND FRINGE", \
        "LAND, WATER, AND SHORE", \
        "LAND AND WATER, RIVERS", \
        "CROP AND WATER MIXTURES", \
        "SOUTHERN HEMISPHERE CONIFERS", \
        "SOUTHERN HEMISPHERE MIXED FOREST", \
        "WET SCLEROPHYLIC FOREST", \
        "COASTLINE FRINGE", \
        "BEACHES AND DUNES", \
        "SPARSE DUNES AND RIDGES", \
        "BARE COASTAL DUNES", \
        "RESIDUAL DUNES AND BEACHES", \
        "COMPOUND COASTLINES", \
        "ROCKY CLIFFS AND SLOPES", \
        "SANDY GRASSLAND AND SHRUBS", \
        "BAMBOO", \
        "MOIST EUCALYPTUS", \
        "RAIN GREEN TROPICAL FOREST", \
        "WOODY SAVANNA", \
        "BROADLEAF CROPS", \
        "GRASS CROPS", \
        "CROPS, GRASS, SHRUBS", \
        "EVERGREEN TREE CROP", \
        "DECIDUOUS TREE CROP"]

worldRegionNames = ["Canada", \
    "USA", \
    "Mexico", \
    "Rest Central America", \
    "Brazil", \
    "Rest South America", \
    "Northern Africa", \
    "Western Africa", \
    "Eastern Africa", \
    "Southern Africa", \
    "Western Europe", \
    "Central Europe", \
    "Turkey", \
    "Ukraine +", \
    "Asia-Stan", \
    "Russia +", \
    "Middle East", \
    "India +", \
    "Korea", \
    "China +", \
    "Southeastern Asia", \
    "Indonesia +", \
    "Japan", \
    "Oceania", \
    "Greenland", \
    "Antarctica"]

maxCoverIMFile   = IMAGELoc + 'GLCT_2000.asc'

# Load maps
fileFormat   = 'AAIGrid'

lon,lat,GLCC,FillValGLCC   = readMap(maxCoverGLCCFile, fileFormat)
lon,lat,IMAGE,FillValIMAGE = readMap(maxCoverIMFile, fileFormat)
lon,lat,worldRegions,FillValworldRegions = readMap(worldRegionFile, fileFormat)
GLCC[IMAGE==FillValIMAGE]    = 0
IMAGE[IMAGE==FillValIMAGE] = 0
worldRegions[worldRegions==FillValworldRegions] = 0

#latplot = flipud(lat)
#lonplot = lon

# LOOP OVER EACH WORLD REGION STARTS BELOW
# Initiate the XML file
TargetTotalName = TargetNamePrefix + xmlExt
xmlObjTotal     = open_XML(TargetTotalName)
for n in arange(0, worldRegions.max()):
    worldRegName = worldRegionNames[n]
    worldRegId   = str(n+1)
    print 'Please wait...: ' + str(float(n)/worldRegions.max()*100) + ' % Done'
    frac_class, compArr = compareCover(IMAGE, GLCC, 0.05, 14, worldRegions, n+1) # 14 is sea water and is filtered out
    compArr[compArr == 0] = NaN
    TargetName = str(TargetNamePrefix + '_region' + '%02.0f' + TargetNameExt) % (n+1)
    # Create loose XML file for each region as well
    TargetName = str(TargetNamePrefix + '_region' + '%02.0f' + xmlExt) % (n+1)
    xmlObj = open_XML(TargetName)
    xmlObj = append_XML(frac_class, compArr, worldRegName, worldRegId, IMAGE_class, longName, TargetName)
    xmlObjTotal = append_XML(frac_class, compArr, worldRegName, worldRegId, IMAGE_class, longName, TargetTotalName)
# Write XML file to pretty formatted XML-file
xmlObj = close_XML(TargetTotalName)

# POTENTIAL PLOT COMMANDS FOR REPORTING ARE GIVEN BELOW!!
#plt.close()
#plt.imshow(compArr,interpolation='nearest')
#plt.colorbar(orientation='h')
#plotGrid(lonplot,latplot,flipud(GLCC),[-60, 84], [-180, 180], 'GLCC.eps')
#plotGrid(lonplot,latplot,flipud(IMAGE),[-60, 84], [-180, 180], 'IMAGE.eps')
