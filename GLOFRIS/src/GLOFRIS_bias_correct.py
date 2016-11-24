"""

$Id: GLOFRIS.py 733 2013-07-03 06:32:48Z winsemi $
$Date: 2013-07-03 08:32:48 +0200 (Wed, 03 Jul 2013) $
$Author: winsemi $
$Revision: 733 $
$HeadURL: https://repos.deltares.nl/repos/Hydrology/trunk/GLOFRIS/src/GLOFRIS.py $
$Keywords: $
"""
import rp_bias_corr
from optparse import OptionParser
import os
import sys
from hydrotools import gis
import numpy as np
import shutil
import pdb

def main():
    # path of code
    def convert_to_list(option, opt, value, parser):
        setattr(parser.values, option.dest, list(np.array(value.replace(
            ' ', '').replace(
            '[', '').replace(
            ']', '').split(','), dtype='int')))

    code_path = os.path.abspath(os.path.split(sys.argv[0])[0])
    print(code_path)
    ### Read input arguments #####
    logfilename = 'GLOFRIS_bias_correct.log'
    parser = OptionParser()
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option('-q', '--quiet',
                      dest='verbose', default=True, action='store_false',
                      help='do not print status messages to stdout')
    parser.add_option('-r', '--reffile', dest='obs_hist_gumbel_file', nargs=1,
                      help='File (NetCDF) containing Gumbel parameters for reference')
    parser.add_option('-H', '--gcmhistfile', dest='gcm_hist_gumbel_file', nargs=1,
                      help='File (NetCDF) containing Gumbel parameters for GCM history')
    parser.add_option('-F', '--gcmfutfile', dest='gcm_fut_gumbel_file', nargs=1,
                      help='File (NetCDF) containing Gumbel parameters for GCM future')
    parser.add_option('-a', '--areafile', dest='cell_area_file', nargs=1,
                      help='PCRaster file, containing land area [m2] per cell', default=os.path.abspath(os.path.join(code_path, '..', 'baseMaps', 'cellarea30.map')))
    parser.add_option('-d', '--destination', dest='output_folder', nargs=1,
                      help='Destination folder for output files')
    parser.add_option('-P', '--returnperiods', dest='RPs', type='string', action='callback',
                      callback=convert_to_list, help='Comma separated list [] of return periods',
                      default=[2, 5, 10, 25, 50, 100, 250, 500, 1000])
    parser.add_option('-p', '--prefix', dest='prefix', nargs=1,
                      help='File prefix used for output files', default='flvol')
    parser.add_option('-s', '--suffix', dest='suffix', nargs=1,
                      help='File suffix used for output files (before .map)', default='')

    (options, args) = parser.parse_args()
    # load a map with amount of land surface per pixel. Any area > 0 is land area
    xax, yax, cell_area, fill_value = gis.gdal_readmap(options.cell_area_file, 'GTiff')
    cell_area = np.flipud(cell_area)
    yax = np.flipud(yax)
    if os.path.isdir(options.output_folder):
        shutil.rmtree(options.output_folder)
    os.makedirs(options.output_folder)
    rp_bias_corr.rp_bias_corr(options.obs_hist_gumbel_file,
                     options.gcm_hist_gumbel_file,
                     options.gcm_fut_gumbel_file,
                     cell_area, xax, yax,
                     options.RPs,
                     options.output_folder,
                     prefix=options.prefix,
                     suffix=options.suffix)

if __name__ == "__main__":
    main()


# # the files below contain the location, scale and p_zero values which describe the distribution function
# gcm_hist_gumbel_file = r'd:\projects\1220607-RiSa\GLOFRIS\ISIMIP\GFDL-ESM2M\historical\outstats\Gumbel_params.nc'
# gcm_fut_gumbel_file = r'd:\projects\1220607-RiSa\GLOFRIS\ISIMIP\GFDL-ESM2M\rcp6p0\outstats\Gumbel_params.nc'
# obs_hist_gumbel_file = r'd:\projects\1220607-RiSa\GLOFRIS\historical\EU-WATCH\run_default\outstats_1960-1999\Gumbel_params.nc'
