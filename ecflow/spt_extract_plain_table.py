#################################################################
#
# File: spt_extract_plain_table.py
# Author(s): Michael Souffront, Wade Roberts, Spencer McDonald
# Date: 03/07/2018
# Purpose: Calculate basic statistics for GloFAS-RAPID files and
#          extract them to a summary table; interpolate forecast
#          values for time steps other than 3 hrs
# Requirements: NCO, netCDF4, pandas
#
#################################################################

import os
import sys
import multiprocessing as mp
import subprocess as sp
import netCDF4 as nc
import datetime as dt
import numpy as np
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

    # creating pandas dataframe with return periods
    d = {}
    return_periods_path = os.path.join(os.path.split(workspace)[0], '{0}-return_periods.csv'.format(full_name))
    with open(return_periods_path, 'r') as f:
        lines = f.readlines()
        lines.pop(0)
        for line in lines:
            d[line.split(',')[0]] = line.split(',')[1:4]

    # creates a csv file to store statistics
    try:
        with open(os.path.join(workspace, file_name), 'w') as f:
            # writes header
            # f.write('comid,timestamp,max,min,style,flow_class\n')

            # extracts forecast COMIDS and formatted dates into lists
            comids = nc.Dataset(nclist[0], 'r').variables['rivid'][:].tolist()
            rawdates = nc.Dataset(nclist[0], 'r').variables['time'][:].tolist()
            dates = []
            for date in rawdates:
                dates.append(dt.datetime.utcfromtimestamp(date).strftime("%m/%d/%y %H:%M"))

            # creates empty lists with forecast stats
            maxlist = []
            meanlist = []
            minlist = []

            # loops through the stat netcdf files to populate lists created above
            for ncfile in sorted(nclist):
                res = nc.Dataset(ncfile, 'r')

                # loops through COMIDs with netcdf files
                for index, comid in enumerate(comids):
                    if 'max' in ncfile:
                        maxlist.append(res.variables['Qout'][index, 0:49].tolist())
                    elif 'avg' in ncfile:
                        meanlist.append(res.variables['Qout'][index, 0:49].tolist())
                    elif 'min' in ncfile:
                        minlist.append(res.variables['Qout'][index, 0:49].tolist())

            # creates step order list
            step_order = range(1, 50)
            #           step_order = range(1, 200)

            # creates watershed and subbasin names
            watershed_name = full_name.split('-')[0]
            subbasin_name = full_name.split('-')[1]

            # creates unique id
            count = 1

            # loops through COMIDs again to add rows to csv file
            for index, comid in enumerate(comids):
                for step, date, max, mean, min in zip(step_order, dates, maxlist[index], meanlist[index],
                                                      minlist[index]):
                    # define style
                    if mean > float(d[str(comid)][2]):
                        style = 'purple'
                    elif mean > float(d[str(comid)][1]):
                        style = 'red'
                    elif mean > float(d[str(comid)][0]):
                        style = 'yellow'
                    else:
                        style = 'blue'

                    # define flow_class
                    if mean < 20:
                        flow_class = '1'
                    elif 20 <= mean < 250:
                        flow_class = '2'
                    elif 250 <= mean < 1500:
                        flow_class = '3'
                    elif 1500 <= mean < 10000:
                        flow_class = '4'
                    elif 10000 <= mean < 30000:
                        flow_class = '5'
                    else:
                        flow_class = '6'

                    f.write(','.join([str(comid), date, str(max), str(mean), style, flow_class + '\n']))
                    count += 1

        return 'Stat Success'
    except Exception as e:
        logging.debug(e)


# function to take a given csv and interpolate all time series in it
def interpolate_table(path):
    # importing the table
    print('working on interpolation')
    df = pd.read_csv(path, index_col=8)
    interpolated_df = pd.DataFrame([])
    if len(df.index) % 85 == 0:
        n = 85
        for i in range(int(len(df.index) / 85)):
            # making a temporay df to interpolate in
            df_temp = df.iloc[n - 85: n]

            # resetting the index to datetime type
            df_temp.index = pd.to_datetime(df_temp.index, infer_datetime_format=True)

            # making a temporary dataframe for the 6 hour gap time series
            df_temp_6_hr = df_temp.iloc[48:, :]

            # making a new index with 3 hour time intervals rather than 6 hour
            new_index = pd.date_range(df_temp_6_hr.index[0], df_temp_6_hr.index[len(df_temp_6_hr.index) - 1], freq='3H')

            # reindexing the 6 hour df to a 3 hr df
            df_temp_3_hr = df_temp_6_hr.reindex(new_index)

            # filling the constant values with a forward fill
            for col in ["watershed", "subbasin", "comid", "return2", "return10", "return20"]:
                df_temp_3_hr[col].ffill(inplace=True)

            # making a new index column
            df_temp_3_hr['index'] = np.linspace(49, 121, len(df_temp_3_hr.index))

            # using a pchip spline to interpolate the values in the new time interval
            for col in ['max', 'mean', 'min']:
                df_temp_3_hr[col] = df_temp_3_hr[col].interpolate('pchip')

            # creating a variable to combine the new interpolated values to the dataframe
            frames = [df_temp.iloc[:48], df_temp_3_hr]
            # concatenating the variable
            df_temp = pd.concat(frames)

            # rearranging the dataframe to match how it was before
            df_temp['timestamp'] = df_temp.index
            df_temp.index = df_temp['id']
            df_temp = df_temp.drop(['id'], axis=1)
            cols = ['watershed', 'subbasin', 'comid', 'return2', 'return10', 'return20', 'index', 'timestamp', 'max',
                    'mean', 'min', 'style', 'flow_class']
            df_temp = df_temp[cols]

            # appending this section of the table back to the entire table
            interpolated_df = interpolated_df.append(df_temp)

            n += 85

        # resetting the id column
        interpolated_df.index = np.linspace(1, len(interpolated_df.index), len(interpolated_df.index), dtype=np.int16)

        # changing the data types to match what was originally in the table
        interpolated_df.index = interpolated_df.index.astype(np.int16)
        interpolated_df['timestamp'] = interpolated_df['timestamp'].dt.strftime("%m/%d/%y %H:%M")
        interpolated_df['index'] = interpolated_df['index'].astype(np.int16)
        interpolated_df['comid'] = interpolated_df['comid'].astype(np.int64)

        # logical indexing the styles column to fill the interpolated values with corresponding colors
        interpolated_df.ix[(interpolated_df['mean'] > interpolated_df['return2']), ['style']] = 'yellow'
        interpolated_df.ix[(interpolated_df['mean'] > interpolated_df['return10']), ['style']] = 'red'
        interpolated_df.ix[(interpolated_df['mean'] > interpolated_df['return20']), ['style']] = 'purple'
        interpolated_df.ix[(interpolated_df['mean'] <= interpolated_df['return2']), ['style']] = 'blue'

        # logical indexing the flow class column to fill the interpolated values with corresponding values
        interpolated_df.ix[(interpolated_df['mean'] < 20), ['flow_class']] = '1'
        interpolated_df.ix[(interpolated_df['mean'] >= 20) & (interpolated_df['mean'] < 250), ['flow_class']] = '2'
        interpolated_df.ix[(interpolated_df['mean'] >= 250) & (interpolated_df['mean'] < 1500), ['flow_class']] = '3'
        interpolated_df.ix[(interpolated_df['mean'] >= 1500) & (interpolated_df['mean'] < 10000), ['flow_class']] = '4'
        interpolated_df.ix[(interpolated_df['mean'] >= 10000) & (interpolated_df['mean'] < 30000), ['flow_class']] = '5'
        interpolated_df.ix[(interpolated_df['mean'] > 30000), ['flow_class']] = '6'

        # overwrite csv table with interpolated values, leaving header out
        interpolated_df.to_csv(path, index_label='id', header=False)
        return ('Interpolation Success')


# runs function on file execution
if __name__ == "__main__":
    # output directory
    workdir = str(sys.argv[1])

    # list of watersheds
    watersheds = [os.path.join(workdir, d) for d in os.listdir(workdir) if os.path.isdir(os.path.join(workdir, d))]

    dates = []
    exclude_list = []
    for i in range(len(watersheds)):
        for d in os.listdir(watersheds[i]):
            if not any(excluded in watersheds[i] for excluded in exclude_list) and os.path.isdir(
                    os.path.join(watersheds[i], d)):
                dates.append(os.path.join(watersheds[i], d))

    logging.basicConfig(filename=str(sys.argv[2]), level=logging.DEBUG)

    pool = mp.Pool()
    results = pool.map(extract_summary_table, dates)

    pool.close()
    pool.join()
    logging.debug('Finished')

#            # populate interpolation list
#            date_list = os.listdir(date)
#            for file in date_list:
#                if file.startswith("summary_table"):
#                    interpolation_list.append(os.path.join(date, file))
#
#    # run interpolation
#    for csv_path in interpolation_list:
#        interpolate_table(
#            path=csv_path
#        )
