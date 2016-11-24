# -*- coding: utf-8 -*-
"""
Test script for GLOFRIS return-period based bias correction 
Created on Fri Jul 10 20:26:18 2015

@author: winsemi
"""

import numpy as np
import netCDF4 as nc
from hydrotools import gis
import matplotlib.pyplot as plt
import os
import pdb

def plot_gumbel(ax, gumbel_dists, y, x, yax, xax, labels, title='Gumbel distributions', filename='foo.png'):
    p = np.arange(0.00001, 1.-0.00001, 0.00001)
    # lookup what the row and column is belonging to y and x resp.
    row = lookup_nearest(y, yax)
    column = lookup_nearest(x, xax)
    #RPs = 1/(1-p)
    RP_ticks = np.array([2, 5, 10, 50, 100, 1000, 10000, 100000, 1000000])
    x_ticks = -np.log(-np.log(1-1./RP_ticks))
    for gumbel_dist, label in zip(gumbel_dists, labels):
        p_zero = gumbel_dist['p_zero'][row, column]
        loc = gumbel_dist['loc'][row, column]
        scale = gumbel_dist['scale'][row, column]
        p_residual = np.minimum(np.maximum((p-p_zero)/(1-p_zero), 0), 1)  # reduce p-distribution to p-distr of non-zero values only
        #  any places where p is zero, the flvol becomes -inf. Make any areas < 0 equal to zero
        reduced_variate = -np.log(-np.log(np.float64(p_residual)))
        reduced_variate_plot = -np.log(-np.log(np.float64(p)))
        #pdb.set_trace()
        
        ev_with_inf = reduced_variate*scale + loc
        ev_with_inf[np.isinf(ev_with_inf)] = 0.
        ev = np.maximum(ev_with_inf, 0)
        #pdb.set_trace()
        ax.plot(reduced_variate_plot, ev, label=label)
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(RP_ticks)
    plt.legend(loc=2)
    plt.xlabel('Return period [yr]')
    plt.ylabel('Volume [m3]')
    plt.title(title)
    plt.savefig('{:s}'.format(filename))

def lookup_nearest(t, x):
    """
    Gives the index of nearest position
    Inputs:
        t:      value to look up
        x:      array of values in which to look for t
    """
    return np.abs(t-x).argmin()

def read_gumbel_pars(in_file):
    f = nc.Dataset(in_file, 'r')
    gumbel_pars = {
    'p_zero': f.variables['flvol_zero_prob'][0, :, :],
    'loc': f.variables['flvol_location'][0, :, :],
    'scale': f.variables['flvol_scale'][0, :, :]}
    f.close()
    
    return gumbel_pars
def inv_gumbel(p_zero, loc, scale, return_period):
    """
    This function computes values for a given return period using the zero probability, location and shape
    parameters given. 
    """
    
    np.seterr(divide='ignore')
    np.seterr(invalid='ignore')
    p = 1-1./np.float64(return_period)
    # p_residual is the probability density function of the population consisting of any values above zero
    p_residual = np.minimum(np.maximum((p-p_zero)/(1-p_zero), 0), np.float64(1-1./1e9))  # I think this is the correct equation"""
    #  any places where p is zero, the flvol becomes -inf. Make any areas < 0 equal to zero
    reduced_variate = -np.log(-np.log(np.float64(p_residual)))
    flvol = reduced_variate*scale+loc
    # negative infinite numbers can occur. reduce these to zero!
    flvol = np.atleast_1d(flvol)
    flvol[np.isinf(flvol)] = 0.  # if flood volume becomes infinitely high due to a p-value of 1
    np.seterr(divide='warn')
    np.seterr(invalid='warn')
    return flvol

def rp_gumbel(p_zero, loc, scale, flvol, max_return_period=1e9):
    """
    Transforms a unique, or array of flood volumes into the belonging return
    periods, according to gumbel parameters (belonging to non-zero part of the
    distribution) and a zero probability
    Inputs:
        p_zero:        probability that flood volume is zero
        loc:           Gumbel location parameter (of non-zero part of distribution)
        scale:         Gumbel scale parameter (of non-zero part of distribution)
        flvol:         Flood volume that will be transformed to return period
        max_return_period: maximum return period considered. This maximum is needed to prevent that floating point
                        precision becomes a problem (default: 1e9)
    """
    np.seterr(divide='ignore')
    np.seterr(invalid='ignore')
    max_p = 1-1./max_return_period
    max_p_residual = np.minimum(np.maximum((max_p-np.float64(p_zero))/(1-np.float64(p_zero)), 0), 1)
    max_reduced_variate = -np.log(-np.log(np.float64(max_p_residual)))
    # compute the gumbel reduced variate belonging to the Gumbel distribution (excluding any zero-values)
    # make sure that the reduced variate does not exceed the one, resembling the 1,000,000 year return period
    reduced_variate = np.minimum((flvol-loc)/scale, max_reduced_variate)
    # reduced_variate = (flvol-loc)/scale
    # transform the reduced variate into a probability (residual after removing the zero volume probability)
    p_residual = np.minimum(np.maximum(np.exp(-np.exp(-np.float64(reduced_variate))), 0), 1)
    # tranform from non-zero only distribution to zero-included distribution
    p = np.minimum(np.maximum(p_residual*(1-p_zero) + p_zero, p_zero), max_p)  # Never larger than max_p
    # transform into a return period    
    return_period = 1./(1-p)
    test_p = p == 1    
    return return_period, test_p
    


def rp_bias_corr(obs_hist_gumbel_file,
                 gcm_hist_gumbel_file,
                 gcm_fut_gumbel_file,
                 cell_area, xax, yax,
                 RPs,
                 output_folder,
                 prefix='flvol',
                 suffix=''):
    # below, the gumbel parameters are read from the NetCDF files using a small function
    gcm_hist_gumbel = read_gumbel_pars(gcm_hist_gumbel_file)
    gcm_fut_gumbel = read_gumbel_pars(gcm_fut_gumbel_file)
    obs_hist_gumbel = read_gumbel_pars(obs_hist_gumbel_file)

    # here we start the comparison grid used to test if increasing RP values lead to increasing volumes
    flvol_bias_corr_old = np.zeros((360, 720))

    # loop over all return periods in RPs
    for n, RP in enumerate(RPs):
        # compute future flvol (WITH bias)
        flvol_fut = inv_gumbel(gcm_fut_gumbel['p_zero'],
                               gcm_fut_gumbel['loc'],
                               gcm_fut_gumbel['scale'],
                               RP)
        # any area with cell > 0, fill in a zero. This may occur because:
            # a) dynRout produces missing values (occuring in some pixels in the Sahara)
            # b) the forcing data is not exactly overlapping the cell area mask (e.g. EU-WATCH land cells are slightly different from PCR-GLOBWB mask)
            # c) the probability of zero flooding is 100%. This causes a division by zero in the inv_gumbel function
        test = np.logical_and(flvol_fut.mask, cell_area > 0)
        flvol_fut[test] = 0.
        test = np.logical_and(np.isnan(flvol_fut), cell_area > 0)
        flvol_fut[test] = 0.
        # if any values become negative due to the statistical extrapolation, fix them to zero (may occur if the sample size for fitting was small and a small return period is requested)
        flvol_fut = np.maximum(flvol_fut, 0.)

        # lookup the return period in present day belonging to flvol_fut
        rp_present, test_p = rp_gumbel(gcm_hist_gumbel['p_zero'],
                               gcm_hist_gumbel['loc'],
                               gcm_hist_gumbel['scale'],
                               flvol_fut)
        # pdb.set_trace()
        # now we know the RPs per 0.5 degree cell. Apply these in the present-day obs gumbel
        flvol_bias_corr = inv_gumbel(obs_hist_gumbel['p_zero'],
                               obs_hist_gumbel['loc'],
                               obs_hist_gumbel['scale'],
                               rp_present)

        test = np.logical_and(flvol_bias_corr.mask, cell_area > 0)
        flvol_bias_corr[test] = 0.
        test = np.logical_and(np.isnan(flvol_bias_corr), cell_area > 0)
        flvol_bias_corr[test] = 0.
        # if any values become negative due to the statistical extrapolation, fix them to zero (may occur if the sample size for fitting was small and a small return period is requested)
        flvol_bias_corr = np.maximum(flvol_bias_corr, 0.)
        # write to maps (TODO: add writing the present-day flood volumes for RP from observations, can be used to test difference of flood volumes)
        map_file = os.path.join(output_folder, '{:s}_corr_RP{:05d}{:s}.map'.format(prefix, RP, suffix))  # 'flvol_b0.{:03d}'.format(n+1))
        gis.gdal_writemap(map_file, 'PCRaster', xax, np.flipud(yax), np.flipud(flvol_bias_corr.data), np.float(flvol_bias_corr.fill_value))
        map_file = os.path.join(output_folder, '{:s}_biased_RP{:05d}{:s}.map'.format(prefix, RP, suffix))
        gis.gdal_writemap(map_file, 'PCRaster', xax, np.flipud(yax), np.flipud(flvol_fut.data), np.float(flvol_fut.fill_value))
        map_file = os.path.join(output_folder, '{:s}_rptrans_RP{:05d}{:s}.map'.format(prefix, RP, suffix)) #  'rp_trans.{:03d}'.format(n+1))
        gis.gdal_writemap(map_file, 'PCRaster', xax, np.flipud(yax), np.flipud(rp_present.data), np.float(rp_present.fill_value))

        # test if rp_values are larger than former rp values
        test_larger = flvol_bias_corr >= flvol_bias_corr_old
        map_file = os.path.join(output_folder, '{:s}_testlt_RP{:05d}{:s}.map'.format(prefix, RP, suffix))  # test larger than previous return period
        gis.gdal_writemap(map_file, 'PCRaster', xax, np.flipud(yax), np.flipud(test_larger.data), np.float(test_larger.fill_value))
    #    plt.figure()
    #    plt.imshow(np.flipud(test_larger));plt.colorbar()
    #    plt.title('RP {:f}'.format(RP))
        flvol_bias_corr_old = flvol_bias_corr
    return obs_hist_gumbel, gcm_hist_gumbel, gcm_fut_gumbel

# # TEST [y, x] = [148, 609]  # Australia
# # TEST [y, x] = [242, 579]  # China (cells become zero! Drying??)
# # TEST [y, x] = [140, 620]  # Australia (collapse at RP 50 year!)
#
# ys = [44.2644, -19.75, 31.25, -15.75]  # y-coordinates for gumbel plots
# xs = [116.237, 130.25, 109.75, 124.75] # x-coordinates for gumbel plots
# png_names = ['China_2.png', 'Australia_gumbel.png', 'China.png', 'Australia_2.png']
# for y, x, png_name in zip(ys, xs, png_names):
#     plt.figure()
#     png_name = os.path.join(output_folder, png_name)
#     ax = plt.subplot(111)
#     title = 'Gumbel distributions lat: {:g} lon: {:g}'.format(y, x)
#     plot_gumbel(ax, [gcm_fut_gumbel, gcm_hist_gumbel, obs_hist_gumbel],
#                 y, x, np.flipud(yax), xax, ['GCM fut.', 'GCM hist.', 'obs hist'], title=title, filename=png_name)
#     plt.close('all')
