#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import datetime

from multiprocessing import Pool

import netCDF4 as nc
import numpy as np
import pcraster as pcr

# utility module:
import virtualOS as vos
import glofris_postprocess_edwin_modified as glofris

# netcdf reporting module:
import output_netcdf_cf_convention as outputNetCDF

# variable dictionaries:
import aqueduct_flood_analyzer_variable_list as varDict

import logging
logger = logging.getLogger(__name__)


#############################################################################################
# The script to apply gumbel fits WITH BIAS CORRECTION to the Annual Flood Maxima time series
#############################################################################################


# input files
input_files            = {}
#
# The gumbel fit parameters based on the annual flood maxima based on the FUTURE/CLIMATE/GCM run:
input_files["future"]  = {}
# - input folder based on the system argument
input_files["future"]['folder']    = os.path.abspath(sys.argv[1]) + "/"
#~ # - gfdl-esm2m future/climate (example)
#~ input_files["future"]['folder'] = "/scratch-shared/edwinhs/bias_correction_test/input/rcp4p5/gumbel_fits/gfdl-esm2m_2010-2049/"
#
input_files["future"]['file_name'] = {}
input_files["future"]['file_name']['channelStorage']    = input_files["future"]['folder'] + "/" + "gumbel_analysis_output_for_channel_storage.nc" 
input_files["future"]['file_name']['surfaceWaterLevel'] = input_files["future"]['folder'] + "/" + "gumbel_analysis_output_for_surface_water_level.nc" 
#
# The gumbel fit parameters based on the annual flood maxima based on the HISTORICAL run:
input_files["historical"]  = {}
# - input folder based on the system argument
input_files["historical"]['folder']    = os.path.abspath(sys.argv[2]) + "/"
#~ # - gfdl-esm2m historical (example)
#~ input_files["historical"]['folder'] = "/scratch-shared/edwinhs/bias_correction_test/input/historical/gumbel_fits/gfdl-esm2m_1960-1999/"
#
input_files["historical"]['file_name'] = {}
input_files["historical"]['file_name']['channelStorage']    = input_files["historical"]['folder'] + "/" + "gumbel_analysis_output_for_channel_storage.nc" 
input_files["historical"]['file_name']['surfaceWaterLevel'] = input_files["historical"]['folder'] + "/" + "gumbel_analysis_output_for_surface_water_level.nc" 
#
#
# general input files
# - clone map
input_files['clone_map_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
pcr.setclone(input_files['clone_map_05min'])
# - cell area, ldd maps
input_files['cell_area_05min'] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_files['ldd_map_05min'  ] = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
# - landmask
landmask = pcr.defined(input_files['ldd_map_05min'  ])
#
# The gumbel fit parameters based on the annual flood maxima based on the BASELINE run: WATCH 1960-1999
input_files["baseline"]  = {}
input_files["baseline"]['folder']    = os.path.abspath(sys.argv[3]) + "/"
input_files["baseline"]['file_name'] = {}
input_files["baseline"]['file_name']['channelStorage']    = input_files["baseline"]['folder'] + "/" + "gumbel_analysis_output_for_channel_storage.nc" 
input_files["baseline"]['file_name']['surfaceWaterLevel'] = input_files["baseline"]['folder'] + "/" + "gumbel_analysis_output_for_surface_water_level.nc" 


# output files
output_files                    = {}
#
# - output folder
# output folder based on the system argument
output_folder_for_this_analysis = sys.argv[4]
output_files['folder']          = output_folder_for_this_analysis + "/" 
#~ # - gfdl-esm2m
#~ output_files['folder']       = "/scratch-shared/edwinhs/bias_correction_test/output/extreme_values_bias_corrected/gfdl-esm2m_2010-2049/"
#
#
try:
    os.makedirs(output_files['folder'])
except:
    os.system('rm -r ' + output_files['folder']  + "/*")
    pass
# - temporary output folder (e.g. needed for resampling/gdalwarp)
output_files['tmp_folder']       = output_files['folder'] + "/tmp/"
try:
    os.makedirs(output_files['tmp_folder'])
except:
    os.system('rm -r ' + output_files['tmp_folder'] + "/*")
    pass
# - prepare logger and its directory
log_file_location = output_files['folder'] + "/log/"
try:
    os.makedirs(log_file_location)
except:
    pass
vos.initialize_logging(log_file_location)


# start and end years for this analysis:
#~ # - for the year 2030
#~ str_year = 2010
#~ end_year = 2049
#~ # - for the year 2050
#~ str_year = 2030
#~ end_year = 2069
#~ # - for the year 2080
#~ str_year = 2060
#~ end_year = 2099
str_year = np.int(sys.argv[5])
end_year = np.int(sys.argv[6])


# output netcdf file name (without extension) for the variable 'surfaceWaterLevel'
output_netcdf_file_name_for_surface_water_level = "surface_water_level_historical_000000000WATCH_1999"
output_netcdf_file_name_for_surface_water_level = str(sys.argv[7])


# option to limit only certain variables being processed
option_to_limit_variables = "None"
try:
    option_to_limit_variables = sys.argv[8]
except:
    pass
variable_name_list = ['channelStorage', 'surfaceWaterLevel']
if option_to_limit_variables != "None": variable_name_list = [option_to_limit_variables]


# netcdf general setup:
netcdf_setup = {}
netcdf_setup['format']      = "NETCDF4"
netcdf_setup['zlib']        = True
netcdf_setup['institution'] = "Utrecht University, Department of Physical Geography ; Deltares ; World Resources Institute"
netcdf_setup['title'      ] = "PCR-GLOBWB 2 output (post-processed for the Aqueduct Flood Analyzer): Gumbel Fit to Annual Flood Maxima"
netcdf_setup['created by' ] = "Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['description'] = "The extreme values based on the gumbel fits of the annual flood maxima."
netcdf_setup['source'     ] = "Utrecht University, Department of Physical Geography - contact: Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl)"
netcdf_setup['references' ] = "Sutanudjaja et al., in prep."


# change to the output folder (use it as the working folder) 
os.chdir(output_files['folder'])

# object for reporting/making netcdf files
netcdf_report = outputNetCDF.OutputNetCDF()
# - dictionary for netcdf output files 
netcdf_file = {}

msg = "Preparing netcdf output files."
logger.info(msg)
for bias_type in ['including_bias', 'bias_corrected_deltares', 'bias_corrected_additive', 'bias_corrected_multiplicative', \
                  'including_bias_above_2_year', 'bias_corrected_deltares_above_2_year', 'bias_corrected_additive_above_2_year', 'bias_corrected_multiplicative_above_2_year', \
                  'bias_corrected']:
    netcdf_file[bias_type] = {}
    for var_name in variable_name_list: 
        #
        netcdf_file[bias_type][var_name] = {}
        #
        # all gumbel fit parameters in a netcdf file:
        # - file name
        netcdf_file[bias_type][var_name]['file_name']   = output_files['folder'] + "/" + str(bias_type) + "_" + "extreme_values_based_on_gumbel_fit_for_" + varDict.netcdf_short_name[var_name] + ".nc"
        #
        # - general attribute information:
        netcdf_file[bias_type][var_name]['description'] = netcdf_setup['description']
        netcdf_file[bias_type][var_name]['institution'] = netcdf_setup['institution']
        netcdf_file[bias_type][var_name]['title'      ] = netcdf_setup['title'      ]
        netcdf_file[bias_type][var_name]['created by' ] = netcdf_setup['created by' ]
        netcdf_file[bias_type][var_name]['source'     ] = netcdf_setup['source'     ]
        netcdf_file[bias_type][var_name]['references' ] = netcdf_setup['references' ]
        #
        if "bias_corrected_deltares" in bias_type:
            netcdf_file[bias_type][var_name]['description'] += " BIAS-CORRECTED based on the historical and baseline output, using the quantile matching method (Deltares bias correction procedure)"
        if "bias_corrected_additive" in bias_type:
            netcdf_file[bias_type][var_name]['description'] += " BIAS-CORRECTED based on the historical and baseline output, using the additive correction method"
        if "bias_corrected_multiplicative" in bias_type:
            netcdf_file[bias_type][var_name]['description'] += " BIAS-CORRECTED based on the historical and baseline output, using the multiplicative correction method"
        #
        if "above_2_year" in bias_type:
            netcdf_file[bias_type][var_name]['description'] += " Values shown are above 2 year return period values of the baseline output."
        #
        # - resolution (unit: arc-minutes)
        netcdf_file[bias_type][var_name]['resolution_arcmin'] = 5. 
        #
        # - preparing netcdf file:
        msg = "Preparing the netcdf file: " + netcdf_file[bias_type][var_name]['file_name']
        logger.info(msg)
        netcdf_report.create_netcdf_file(netcdf_file[bias_type][var_name]) 


# applying gumbel parameters with bias correction to get extreme values for every return period:
msg = "Applying gumbel parameters with bias correction."
logger.info(msg)
#
# - a dictionary for input gumbel parameters:
p_zero = {}
location = {}
scale = {}
#
# - a dictionary for return periods
return_periods = ["2-year", "5-year", "10-year", "25-year", "50-year", "100-year", "250-year", "500-year", "1000-year"]
#
# - dictionaries for extreme value:
extreme_values = {}
#
# - without bias correction
extreme_values["including_bias"] = {}
extreme_values["including_bias_above_2_year"] = {}
#
# - bias corrected using the quantile matching approach. 
extreme_values["bias_corrected_deltares"] = {}
extreme_values["bias_corrected_deltares_above_2_year"] = {}
extreme_values['return_period_historical_deltares'] = {}
# 
# - bias_corrected_additive
extreme_values["bias_corrected_additive"] = {}
extreme_values["bias_corrected_additive_above_2_year"] = {}
#
# - bias_corrected_multiplicative
extreme_values["bias_corrected_multiplicative"] = {}
extreme_values["bias_corrected_multiplicative_above_2_year"] = {}
extreme_values["problematic_mult_with_zero_historical_gcm"] = {}
#
# - the chosen/suggested bias corrected method
extreme_values["bias_corrected"] = {}

#
for var_name in variable_name_list: 
    
    msg  = "Applying gumbel parameters from the climate run: " + str(input_files["future"]['file_name'][var_name])
    msg += "    that are bias corrected to the baseline run: " + str(input_files["baseline"]['file_name'][var_name])
    msg += "                         and the historical run: " + str(input_files["historical"]['file_name'][var_name])
    logger.info(msg)

    # read gumbel parameters from : ['p_zero', 'location_parameter', 'scale_parameter']
    for run_type in ["future", "historical", "baseline"]:

        netcdf_input_file = input_files[run_type]['file_name'][var_name]
        #
        variable_name = str('p_zero') + "_of_" + varDict.netcdf_short_name[var_name]
        p_zero[run_type]   = vos.netcdf2PCRobjClone(netcdf_input_file,\
                                          variable_name,\
                                          1,\
                                          "Yes",\
                                          input_files['clone_map_05min'])
        #
        variable_name = str('location_parameter') + "_of_" + varDict.netcdf_short_name[var_name]
        location[run_type] = vos.netcdf2PCRobjClone(netcdf_input_file,\
                                          variable_name,\
                                          1,\
                                          "Yes",\
                                          input_files['clone_map_05min'])
        #
        variable_name = str('scale_parameter') + "_of_" + varDict.netcdf_short_name[var_name]
        scale[run_type]    = vos.netcdf2PCRobjClone(netcdf_input_file,\
                                          variable_name,\
                                          1,\
                                          "Yes",\
                                          input_files['clone_map_05min'])
    
    
    # calculate/obtain extremes value for the 2-year return period of the baseline run (EUWATCH)
    reference_2_year_map = glofris.inverse_gumbel(p_zero["baseline"], location["baseline"], scale["baseline"], 2.0)  
    
    
    # compute future extreme values (including bias correction - based on the quantile matching approach):
    for i_return_period in range(0, len(return_periods)):
        
        return_period = return_periods[i_return_period]
        
        msg  = "\n"
        msg += "\n"
        msg += "\n"
        msg += "Compute bias corrected exteme values for the return period: " + str(return_period)
        msg += "\n"
        msg += "\n"
        logger.info(msg)
        return_period_in_year = float(return_period.split("-")[0]) 

        # compute future extreme values (with bias): applying gumbel parameters
        msg = "Compute future/climate/gcm extreme values (biases are still included here)."
        logger.info(msg)
        extreme_values["including_bias"][return_period] = glofris.inverse_gumbel(p_zero["future"], location["future"], scale["future"], return_period_in_year)
    
        # lookup the return period in present days (historical run) belonging to future extreme values
        msg = "For the given future extreme values, obtain the return period based on the historical gumbel fit/parameters."
        logger.info(msg)
        #
        # - set the maximum return period that can be assigned in order to avoid 
        max_return_period_that_can_be_assigned = np.longdouble(1e9) 
        #
        return_period_historical = glofris.get_return_period_gumbel(p_zero["historical"], location["historical"], scale["historical"], \
                                                                    extreme_values["including_bias"][return_period], \
                                                                    max_return_period_that_can_be_assigned, \
                                                                    max_return_period_that_can_be_assigned)
        extreme_values['return_period_historical'][return_period] = return_period_historical
        
        #~ pcr.report(return_period_historical, "return_period_historical.map")
        #~ cmd = "aguila " + "return_period_historical.map"
        #~ os.system(cmd)
        

        # bias corrected extreme values - Deltares approach (quantile matching)
        extreme_value_map = None
        msg = "Calculate the bias corrected extreme values, based on the DELTARES (quantile matching) method: Using the return period based on the historical gumbel fit/parameters and the gumbel fit/parameters of the baseline run."
        logger.info(msg)
        # 
        extreme_value_map = glofris.inverse_gumbel(p_zero["baseline"], location["baseline"], scale["baseline"], return_period_historical)
        #
        # - make sure that we have positive extreme values
        extreme_value_map = pcr.max(extreme_value_map, 0.0)
        #
        # - saving extreme values in the dictionary  
        extreme_values["bias_corrected_deltares"][return_period] = extreme_value_map
        #
        # - make sure that extreme value maps increasing over return period - this is not necessary, but to make sure
        if i_return_period >  0: extreme_values["bias_corrected_deltares"][return_period] = pcr.max(extreme_values["bias_corrected_deltares"][return_period], \
                                                                                                    extreme_values["bias_corrected_deltares"][i_return_period - 1]) 
        #
        # - calculate values above 2 year
        extreme_values["bias_corrected_deltares_above_2_year"][return_period] = pcr.max(0.0, extreme_values["bias_corrected_deltares"][return_period] - reference_2_year_map)


        # additive correction approach
        extreme_value_map = None
        msg = "Calculate the bias corrected extreme values, based on the ADDITIVE correction method"
        logger.info(msg)
        # 
        # - obtain baseline, historical and future values for the current return period analyzed
        baseline_value = glofris.inverse_gumbel(p_zero["baseline"]  , location["baseline"],   scale["baseline"],   return_period_in_year)
        historical_gcm = glofris.inverse_gumbel(p_zero["historical"], location["historical"], scale["historical"], return_period_in_year)
        future_gcm     = glofris.inverse_gumbel(p_zero["future"]    , location["future"],     scale["future"],     return_period_in_year)
        # 
        # - the bias corrected value - additive approach
        extreme_value_map = pcr.max(0.0, baseline_value + (future_gcm - historical_gcm))
        #
        # - make sure that we have positive extreme values
        extreme_value_map = pcr.max(extreme_value_map, 0.0)
        #
        # - saving extreme values in the dictionary  
        extreme_values["bias_corrected_additive"][return_period] = extreme_value_map
        #
        # - make sure that extreme value maps increasing over return period - this is not necessary, but to make sure
        if i_return_period >  0: extreme_values["bias_corrected_additive"][return_period] = pcr.max(extreme_values["bias_corrected_additive"][return_period], \
                                                                                                    extreme_values["bias_corrected_additive"][i_return_period - 1]) 
        #
        # - calculate values above 2 year
        extreme_values["bias_corrected_additive_above_2_year"][return_period] = pcr.max(0.0, extreme_values["bias_corrected_additive"][return_period] - reference_2_year_map)


        # multiplicative correction approach
        extreme_value_map = None
        msg = "Calculate the bias corrected extreme values, based on the MULTIPLICATIVE correction method"
        logger.info(msg)
        # 
        # - the bias corrected value - multiplicative approach
        extreme_value_map = baseline_value * (future_gcm / historical_gcm)
        #
        # - set it to zero if either baseline_value or future gcm is zero
        extreme_value_map = pcr.ifthenelse(baseline_value = 0., 0., extreme_value_map)
        extreme_value_map = pcr.ifthenelse(future_gcm = 0., 0., extreme_value_map)
        #
        # - make sure that we have positive extreme values
        extreme_value_map = pcr.max(extreme_value_map, 0.0)
        #
        # - saving extreme values in the dictionary  
        extreme_values["bias_corrected_multiplicative"][return_period] = extreme_value_map
        #
        # - make sure that extreme value maps increasing over return period - this is not necessary, but to make sure
        if i_return_period >  0: extreme_values["bias_corrected_multiplicative"][return_period] = pcr.max(extreme_values["bias_corrected_multiplicative"][return_period], \
                                                                                                          extreme_values["bias_corrected_multiplicative"][i_return_period - 1]) 
        #
        # - calculate values above 2 year
        extreme_values["bias_corrected_multiplicative_above_2_year"][return_period] = pcr.max(0.0, extreme_values["bias_corrected_multiplicative"][return_period] - reference_2_year_map)
        #
        # - problematic areas
        extreme_values["problematic_mult_with_zero_historical_gcm"] = pcr.ifthenelse(historical_gcm == 0., pcr.ifthenelse(extreme_value_map > 0.0, pcr.boolean(1.0), pcr.boolean(0.0)), \
                                                                                                           pcr.boolean(0.0))

 
        # THE CHOSEN bias corrected method  
        extreme_values["bias_corrected"][return_period] = extreme_values["bias_corrected_additive"]



    # time bounds in a netcdf file
    lowerTimeBound = datetime.datetime(str_year,  1,  1, 0)
    upperTimeBound = datetime.datetime(end_year, 12, 31, 0)
    timeBounds = [lowerTimeBound, upperTimeBound]
    
    # reporting/saving extreme values in netcdf and pcraster files
    #~ for bias_type in ['including_bias', 'bias_corrected']:
    for bias_type in ['including_bias', 'bias_corrected_deltares', 'bias_corrected_additive', 'bias_corrected_multiplicative', \
                      'including_bias_above_2_year', 'bias_corrected_deltares_above_2_year', 'bias_corrected_additive_above_2_year', 'bias_corrected_multiplicative_above_2_year']:
    
        msg = "Writing extreme values to a netcdf file: " + str(netcdf_file[bias_type][var_name]['file_name'])
        logger.info(msg)
        
        # preparing the variables in the netcdf file:
        for return_period in return_periods:
            # variable names and unit 
            variable_name = str(return_period) + "_of_" + varDict.netcdf_short_name[var_name]
            variable_unit = varDict.netcdf_unit[var_name]
            var_long_name = str(return_period) + "_of_" + varDict.netcdf_long_name[var_name]
            # 
            netcdf_report.create_variable(\
                                          ncFileName = netcdf_file[bias_type][var_name]['file_name'], \
                                          varName    = variable_name, \
                                          varUnit    = variable_unit, \
                                          longName   = var_long_name, \
                                          comment    = varDict.comment[var_name]
                                          )
        
        # store the variables to pcraster map and netcdf files:
        data_dictionary = {}
        for return_period in return_periods:
            
            # variable name
            variable_name = str(return_period) + "_of_" + varDict.netcdf_short_name[var_name]
            
            # report to a pcraster map
            pcr.report(pcr.ifthen(landmask, extreme_values[bias_type][return_period]), bias_type + "_" + variable_name + ".map")
        
            # put it into a dictionary
            data_dictionary[variable_name] = pcr.pcr2numpy(extreme_values[bias_type][return_period], vos.MV)
        
        # save the variables to a netcdf file
        netcdf_report.dictionary_of_data_to_netcdf(netcdf_file[bias_type][var_name]['file_name'], \
                                                   data_dictionary, \
                                                   timeBounds)

    # saving "return_period_historical" and "problematic_mult_with_zero_historical_gcm"
    # - to pcraster files only
    for return_period in return_periods:

        # report to pcraster maps
        pcr.report(pcr.ifthen(landmask, extreme_values['return_period_historical'][return_period]), 'return_period_historical_corresponding_to' + "_" + str(return_period) + ".map")
        pcr.report(pcr.ifthen(landmask, extreme_values['problematic_mult_with_zero_historical_gcm'][return_period]), 'problematic_mult_with_zero_historical_gcm_corresponding_to' + "_" + str(return_period) + ".map")
    


###################################################################################


if 'surfaceWaterLevel' not in variable_name_list: sys.exit()

# masking out permanent water bodies
msg = "Preparing final netcdf files, one for every return period, as requested by Philip."
logger.info(msg)

landmask           = pcr.defined(pcr.readmap(input_files['ldd_map_05min'  ]))

#~ # permanent water bodies files (at 5 arc-minute resolution) 
#~ fracwat_file            = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/reservoirs/waterBodiesFinal_version15Sept2013/maps/fracwat_2010.map"
#~ water_body_id_file      = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/reservoirs/waterBodiesFinal_version15Sept2013/maps/waterbodyid_2010.map"
#~ 
#~ # read the properties of permanent water bodies
#~ fracwat            = pcr.cover(pcr.readmap(fracwat_file), 0.0)
#~ water_body_id      = pcr.readmap(water_body_id_file)
#~ water_body_id      = pcr.ifthen(pcr.scalar(water_body_id) > 0.00, water_body_id)
#~ water_body_area    = pcr.areatotal(input_files['cell_area_05min'] * fracwat, water_body_id)
#~ water_body_area    = pcr.cover(water_body_area, 0.0)
#~ water_body_id      = pcr.cover(water_body_id, pcr.nominal(0.0))
#~ water_body_id      = pcr.ifthen( landmask, water_body_id)                                         
#~ non_permanent_water_bodies = pcr.boolean(1.0)
#~ non_permanent_water_bodies = pcr.ifthenelse(water_body_area > 50. * 1000. * 1000., pcr.boolean(0.0), non_permanent_water_bodies)
#~ non_permanent_water_bodies = pcr.ifthen(landmask, non_permanent_water_bodies)
#~ pcr.aguila(non_permanent_water_bodies)

# - time bounds for netcdf files
lowerTimeBound = datetime.datetime(str_year,  1,  1, 0)
upperTimeBound = datetime.datetime(end_year, 12, 31, 0)
timeBounds = [lowerTimeBound, upperTimeBound]

# - variable name according to the PCR-GLOBWB variable dictionary
var_name = 'surfaceWaterLevel' 

# - return periods
return_periods      = [ "2-year",  "5-year", "10-year", "25-year", "50-year", "100-year", "250-year", "500-year", "1000-year"]
return_period_codes = ["rp00002", "rp00005", "rp00010", "rp00025", "rp00050",  "rp00100",  "rp00250",  "rp00500",   "rp01000"]

# preparing netcdf files and their variables:
var_name = "surfaceWaterLevel"
for bias_type in ['including_bias', 'bias_corrected']:
    for i_return_period in range(0, len(return_periods)):
        # 
        return_period      = return_periods[i_return_period]
        return_period_code = return_period_codes[i_return_period]
        # 
        # - preparing netcdf file:
        file_name = output_files['folder'] + "/" + output_netcdf_file_name_for_surface_water_level + "_" + return_period_code + ".nc"
        if bias_type == "including_bias": file_name = file_name + ".including_bias.nc"
        msg = "Preparing the netcdf file: " + file_name
        logger.info(msg)
        netcdf_file[bias_type][var_name]['file_name'] = file_name
        netcdf_report.create_netcdf_file(netcdf_file[bias_type][var_name]) 
        #
        # - variable name and unit 
        variable_name = str(return_period) + "_of_" + varDict.netcdf_short_name[var_name]
        var_long_name = str(return_period) + "_of_" + varDict.netcdf_long_name[var_name]
        variable_unit = varDict.netcdf_unit[var_name]
        # 
        # - creating variable 
        netcdf_report.create_variable(\
                                      ncFileName = file_name, \
                                      varName    = variable_name, \
                                      varUnit    = variable_unit, \
                                      longName   = var_long_name, \
                                      comment    = varDict.comment[var_name]
                                      )
    
        # read from pcraster files
        surface_water_level_file_name = output_files['folder'] + "/" + bias_type + "_" + str(return_period) + "_of_surface_water_level" + ".map"
        surface_water_level = pcr.readmap(surface_water_level_file_name)
        surface_water_level = pcr.cover(surface_water_level, 0.0)
        
        # masking out ocean
        surface_water_level = pcr.ifthen(landmask, surface_water_level)
    
        #~ # masking out permanent water bodies
        #~ surface_water_level = pcr.ifthen(non_permanent_water_bodies, surface_water_level)
    
        # report in pcraster maps
        pcr.report(surface_water_level, surface_water_level_file_name + ".masked_out.map")
        
        # write to netcdf files
        netcdf_report.data_to_netcdf(file_name, variable_name, pcr.pcr2numpy(surface_water_level, vos.MV), timeBounds, timeStamp = None, posCnt = 0)
