#################################################################
# File: spt_extract_plain_table.py
# Author(s):
#   Riley Hales
#   Josh Ogden
#   Michael Souffront
#   Wade Roberts
#   Spencer McDonald
# Date: 03/07/2018
# Last Updated: 05/28/2020
# Purpose: Calculate basic statistics for GloFAS-RAPID files and
#          extract them to a summary table; interpolate forecast
#          values for time steps other than 3 hrs
# Requirements: NCO, netCDF4, pandas, numpy, scipy
#################################################################

import datetime
import logging
import multiprocessing as mp
import os
import subprocess as sp
import sys
import glob

import netCDF4 as nc
import pandas as pd
import numpy as np
from scipy.interpolate import pchip

def interpolate_time_series(arrays_obj):
    comid, maxes, means, dt_dates, interp_x, rp_array = arrays_obj  # (1, 2, 3) or [1, 2, 3]
    # interpolate maxes and means
    max_interpolator = pchip(dt_dates, maxes)
    mean_interpolator = pchip(dt_dates, means)
    max_flows = max_interpolator(interp_x)
    mean_flows = mean_interpolator(interp_x)

    # create dictionary from return period values
    rp_dict = {}
    for i, name in enumerate(['return_2', 'return_5', 'return_10', 'return_25', 'return_50', 'return_100']):
        rp_dict[name] = rp_array[i]

    # loop for creating color, thickness, and return period columns
    colors = []
    thicknesses = []
    ret_pers = []


    for mean_flow in mean_flows:
        # define reach color based on return periods
        if mean_flow > rp_dict['return_50']:
            color = 'purple'
        elif mean_flow > rp_dict['return_10']:
            color = 'red'
        elif mean_flow > rp_dict['return_2']:
            color = 'yellow'
        else:
            color = 'blue'

        colors.append(color)

        # define reach thickness based on flow magnitude
        if mean_flow < 20:
            thickness = '1'
        elif 20 <= mean_flow < 250:
            thickness = '2'
        elif 250 <= mean_flow < 1500:
            thickness = '3'
        elif 1500 <= mean_flow < 10000:
            thickness = '4'
        elif 10000 <= mean_flow < 30000:
            thickness = '5'
        else:
            thickness = '6'

        thicknesses.append(thickness)

        # define return period exceeded by the mean forecast
        if mean_flow > rp_dict['return_100']:
            ret_per = '100'
        elif mean_flow > rp_dict['return_50']:
            ret_per = '50'
        elif mean_flow > rp_dict['return_25']:
            ret_per = '25'
        elif mean_flow > rp_dict['return_10']:
            ret_per = '10'
        elif mean_flow > rp_dict['return_5']:
            ret_per = '5'
        elif mean_flow > rp_dict['return_2']:
            ret_per = '2'
        else:
            ret_per = '0'

        ret_pers.append(ret_per)

    columns = ['comid', 'timestamp', 'max', 'mean', 'color', 'thickness', 'ret_per']
    new_dates = list(interp_x)
    return pd.DataFrame({
        columns[0]: pd.Series([comid, ] * len(new_dates)),
        columns[1]: pd.Series(new_dates),
        columns[2]: pd.Series(max_flows).round(2),
        columns[3]: pd.Series(mean_flows).round(2),
        columns[4]: pd.Series(colors),
        columns[5]: pd.Series(thicknesses),
        columns[6]: pd.Series(ret_pers)
    })


# runs function on file execution
if __name__ == "__main__":
    """
    Arguments:

    1. Absolute path to the rapid-io/output directory
        This contains a directory for each region
        Each region directory contains a directory named for the forecast date 
    2. Path to the logging file

    3. NCO command to compute ensemble stats

    4. era_type: == 'era_5'

    5. static_path: absolute path to the root directory with all
        return period files. The next level after this directory
        should be the different era types.
    """
    logging.basicConfig(filename=str(sys.argv[2]), level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    # output directory
    workdir = str(sys.argv[1])

    # list of watersheds
    region_folders = [os.path.join(workdir, d) for d in os.listdir(workdir) if os.path.isdir(os.path.join(workdir, d))]

    # list of all forecast date folders in all the region folders
    date_folders = np.array([glob.glob(os.path.join(region_folder, '*')) for region_folder in region_folders]).flatten()
    date_folders = [d for d in date_folders if os.path.isdir(d)]

    # calls NCO's nces function to calculate ensemble statistics for the max, mean, and min
    nces_exec = str(sys.argv[3])
    for stat in ['max', 'avg', 'min']:
        findstr = 'find {0} -name "Qout*.nc"'.format(workspace)
        filename = os.path.join(workspace, 'nces.{0}.nc'.format(stat))
        ncesstr = "{0} -O --op_typ={1} {2}".format(nces_exec, stat, filename)
        args = ' | '.join([findstr, ncesstr])
        sp.call(args, shell=True)

    # creates file name for the csv file
    date_string = os.path.split(workspace)[1].replace('.', '')
    region_name = os.path.basename(os.path.split(workspace)[0])
    file_name = f'summary_table_{region_name}_{date_string}.csv'
    static_path = str(sys.argv[5])

    # creating pandas dataframe with return periods
    era_type = str(sys.argv[4])
    rp_path = glob.glob(os.path.join(static_path, era_type, region_name, f'*return_periods*.nc*'))[0]
    logging.info(f'Return Period Path {rp_path}')
    rp_ncfile = nc.Dataset(rp_path, 'r')
    rp_df = pd.DataFrame({
        'return_2': rp_ncfile.variables['return_period_2'][:],
        'return_5': rp_ncfile.variables['return_period_5'][:],
        'return_10': rp_ncfile.variables['return_period_10'][:],
        'return_25': rp_ncfile.variables['return_period_25'][:],
        'return_50': rp_ncfile.variables['return_period_50'][:],
        'return_100': rp_ncfile.variables['return_period_100'][:]
    }, index=rp_ncfile.variables['rivid'][:])
    rp_ncfile.close()

    # create the summary tables
    try:
        # create the summary table dataframe
        columns = ['comid', 'timestamp', 'max', 'mean', 'color', 'thickness', 'ret_per']
        summary_table_df = pd.DataFrame(columns=columns)

        # read the date and COMID lists from one of the netcdfs
        sample_nc = nc.Dataset(os.path.join(workspace, 'nces.avg.nc'), 'r')
        comids = sample_nc['rivid'][:].tolist()
        dates = sample_nc['time'][:].tolist()
        dates = [datetime.datetime.utcfromtimestamp(date).strftime("%m/%d/%y %H:%M") for date in dates]
        sample_nc.close()

        # create a time series at 3 hour intervals for interpolation
        interp_x = pd.date_range(
            start=dates[0],
            end=dates[-1],
            freq='3H'
        )
        interp_x_strings = interp_x.strftime("%m/%d/%y %H:%M")
        new_dates = list(interp_x_strings)
        dt_dates = pd.to_datetime(dates)

        # read the max and avg flows
        max_flow_nc = nc.Dataset(os.path.join(workspace, 'nces.max.nc'))
        max_flow_array = max_flow_nc.variables['Qout'][:].round(2).tolist()
        max_flow_nc.close()
        mean_flow_nc = nc.Dataset(os.path.join(workspace, 'nces.avg.nc'))
        mean_flow_array = mean_flow_nc.variables['Qout'][:].round(2).tolist()
        mean_flow_nc.close()

        # for each comid, interpolate to 3-hourly with pchip, compare to return periods to generate map styling info

        # create a 2d array with an iteration of the date values for each comid
        long_list_of_dt_dates = [dt_dates, ] * len(comids)
        long_list_of_interp_x = [interp_x, ] * len(comids)

        comid_pool = mp.Pool(4)
        df_rows = comid_pool.map(interpolate_time_series,
                                 zip(comids, max_flow_array, mean_flow_array, long_list_of_dt_dates,
                                     long_list_of_interp_x, rp_df.values))

        for df in df_rows:
            summary_table_df = pd.concat([summary_table_df, df], ignore_index=True)
        # write to csv
        # todo: this may need to be adjusted to have the correct file names
        summary_table_df.to_csv(os.path.join(workdir, file_name), index=False)
        comid_pool.close()
        comid_pool.join()
    except Exception as e:
        logging.debug(e)

    # map function to list of date folders
    pool = mp.Pool()
    results = pool.map(extract_summary_table, date_folders)

    pool.close()
    pool.join()
    logging.debug('Finished')
