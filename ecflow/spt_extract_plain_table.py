#################################################################
#
# File: spt_extract_plain_table.py
# Author(s): Michael Souffront, Wade Roberts, Spencer McDonald
# Date: 03/07/2018
# Last Updated: 05/28/2020
# Purpose: Calculate basic statistics for GloFAS-RAPID files and
#          extract them to a summary table; interpolate forecast
#          values for time steps other than 3 hrs
# Requirements: NCO, netCDF4, pandas
#
#################################################################

import os
from glob import glob
import sys
import multiprocessing as mp
import subprocess as sp
import netCDF4 as nc
import datetime as dt
import pandas as pd
import logging


def extract_summary_table(workspace):
    # calls NCO's nces function to calculate ensemble statistics for the max, mean, and min
    nces_exec = str(sys.argv[3])
    for stat in ['max', 'avg', 'min']:
        findstr = 'find {0} -name "Qout*.nc"'.format(workspace)
        filename = os.path.join(workspace, 'nces.{0}.nc'.format(stat))
        ncesstr = "{0} -O --op_typ={1} {2}".format(nces_exec, stat, filename)
        args = ' | '.join([findstr, ncesstr])
        sp.call(args, shell=True)

    # creates list with the stat netcdf files created in the previous step
    nclist = []
    for file in os.listdir(workspace):
        if file.startswith("nces"):
            nclist.append(os.path.join(workspace, file))

    # creates file name for the csv file
    date_string = os.path.split(workspace)[1].replace('.', '')
    full_name = os.path.split(os.path.split(workspace)[0])[1]
    file_name = 'summary_table_{0}_{1}.csv'.format(full_name, date_string)
    static_path = str(sys.argv[5])

    # creating pandas dataframe with return periods
    era_type = str(sys.argv[4])
    logging.info(f'Workspace {workspace}')
    rp_path = glob(os.path.join(static_path, era_type, os.path.basename(os.path.split(workspace)[0]), f'*return_periods_{era_type}*.nc*'))[0]
    logging.info(f'Return Period Path {rp_path}')
    rp_ncfile = nc.Dataset(rp_path, 'r')

    # extract values
    rp_comid = rp_ncfile.variables['rivid'][:]
    data = {
        'return_2': rp_ncfile.variables['return_period_2'][:],
        'return_10': rp_ncfile.variables['return_period_10'][:],
        'return_50': rp_ncfile.variables['return_period_50'][:]
    }

    #  creates dataframe
    rp_df = pd.DataFrame(data, index=rp_comid)

    # creates a csv file to store statistics
    try:
        with open(os.path.join(workspace, file_name), 'w') as f:
            # writes header
            # f.write('comid,timestamp,max,mean,color,thickness\n')

            # extracts forecast COMIDS and formatted dates into lists
            comids = nc.Dataset(nclist[0], 'r').variables['rivid'][:].tolist()
            rawdates = nc.Dataset(nclist[0], 'r').variables['time'][:].tolist()
            dates = []
            for date in rawdates:
                dates.append(dt.datetime.utcfromtimestamp(date).strftime("%m/%d/%y %H:%M"))

            # creates empty lists with forecast stats
            maxlist = []
            meanlist = []

            # loops through the stat netcdf files to populate lists created above
            for ncfile in sorted(nclist):
                res = nc.Dataset(ncfile, 'r')

                # loops through COMIDs with netcdf files
                for index, comid in enumerate(comids):
                    if 'max' in ncfile:
                        maxlist.append(res.variables['Qout'][index, 0:49].tolist())
                    elif 'avg' in ncfile:
                        meanlist.append(res.variables['Qout'][index, 0:49].tolist())

            # loops through COMIDs again to add rows to csv file
            for index, comid in enumerate(comids):
                for f_date, f_max, f_mean in zip(dates, maxlist[index], meanlist[index]):
                    # define reach color based on return periods
                    if f_mean > rp_df.loc[comid, 'return_50']:
                        color = 'purple'
                    elif f_mean > rp_df.loc[comid, 'return_10']:
                        color = 'red'
                    elif f_mean > rp_df.loc[comid, 'return_2']:
                        color = 'yellow'
                    else:
                        color = 'blue'

                    # define reach thickness based on flow magnitude
                    if f_mean < 20:
                        thickness = '1'
                    elif 20 <= f_mean < 250:
                        thickness = '2'
                    elif 250 <= f_mean < 1500:
                        thickness = '3'
                    elif 1500 <= f_mean < 10000:
                        thickness = '4'
                    elif 10000 <= f_mean < 30000:
                        thickness = '5'
                    else:
                        thickness = '6'

                    f.write(','.join([str(comid), f_date, str(f_max), str(f_mean), color, thickness + '\n']))

        return 'Stat Success'
    except Exception as e:
        logging.debug(e)


# runs function on file execution
if __name__ == "__main__":

    #logging.basicConfig(filename=str(sys.argv[2]), level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    # output directory
    workdir = str(sys.argv[1])

    # list of watersheds
    watersheds = [os.path.join(workdir, d) for d in os.listdir(workdir) if os.path.isdir(os.path.join(workdir, d))]
    logging.debug(watersheds)
    dates = []
    exclude_list = []
    for i in range(len(watersheds)):
        for d in os.listdir(watersheds[i]):
            if not any(excluded in watersheds[i] for excluded in exclude_list) and os.path.isdir(
                    os.path.join(watersheds[i], d)):
                dates.append(os.path.join(watersheds[i], d))
                logging.info(os.path.join(watersheds[i], d))
    logging.debug(dates)
    pool = mp.Pool()
    results = pool.map(extract_summary_table, dates)

    pool.close()
    pool.join()
    logging.debug('Finished')
