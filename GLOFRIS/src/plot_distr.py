import rp_bias_corr
import numpy as np
import matplotlib.pyplot as plt
import os

RPs = [5., 10., 25., 50., 100., 250., 500., 1000]  # 5-year
output_folder = r'd:\projects\1220607-RiSa\maps'  # write all maps and figures here!
#
# use a nice plot style, so that we can use figures for the report :-)
plt.style.use('ggplot')


# the files below contain the location, scale and p_zero values which describe the distribution function
gcm_hist_gumbel_file = r'd:\projects\1220607-RiSa\GLOFRIS\ISIMIP\GFDL-ESM2M\historical\outstats\Gumbel_params.nc'
gcm_fut_gumbel_file = r'd:\projects\1220607-RiSa\GLOFRIS\ISIMIP\GFDL-ESM2M\rcp6p0\outstats\Gumbel_params.nc'
obs_hist_gumbel_file = r'd:\projects\1220607-RiSa\GLOFRIS\historical\EU-WATCH\run_default\outstats_1960-1999\Gumbel_params.nc'

gcm_hist_gumbel = rp_bias_corr.read_gumbel_pars(gcm_hist_gumbel_file)
gcm_fut_gumbel = rp_bias_corr.read_gumbel_pars(gcm_fut_gumbel_file)
obs_hist_gumbel = rp_bias_corr.read_gumbel_pars(obs_hist_gumbel_file)

yax = np.flipud(np.arange(-89.75, 90, 0.5))
xax = np.arange(-179.75, 180, 0.5)
# TEST [y, x] = [148, 609]  # Australia
# TEST [y, x] = [242, 579]  # China (cells become zero! Drying??)
# TEST [y, x] = [140, 620]  # Australia (collapse at RP 50 year!)

ys = [44.2644, -19.75, 31.25, -15.75, 47.254]  # y-coordinates for gumbel plots
xs = [116.237, 130.25, 109.75, 124.75, 134.723] # x-coordinates for gumbel plots
png_names = ['China_2.png', 'Australia_gumbel.png', 'China.png', 'Australia_2.png', 'North_Russia']
for y, x, png_name in zip(ys, xs, png_names):
    plt.figure()
    png_name = os.path.join(output_folder, png_name)
    ax = plt.subplot(111)
    title = 'Gumbel distributions lat: {:g} lon: {:g}'.format(y, x)
    rp_bias_corr.plot_gumbel(ax, [gcm_fut_gumbel, gcm_hist_gumbel, obs_hist_gumbel],
                y, x, np.flipud(yax), xax, ['GCM fut.', 'GCM hist.', 'obs hist'], title=title, filename=png_name)
    plt.close('all')
