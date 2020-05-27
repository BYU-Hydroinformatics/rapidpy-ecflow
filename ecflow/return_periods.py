################################################################
#
# File: return_periods_to_csv.py
# Author(s): Michael Souffront and Spencer McDonald
# Date: 01/25/2018
# Purpose: Extracts return periods from ECMWF-RAPID era_interim
#          results into a csv file
# Requirements: netCDF4, pandas
#
################################################################


import netCDF4 as nc
import os
import pandas as pd


# creates csv file with return periods
def get_return_periods_as_csv(input_dir, output_dir, watershed_name):
    # opens netcdf file with return periods
    ncfile = nc.Dataset(os.path.join(input_dir, 'return_periods_erai_t511_24hr_19800101to20141231.nc'),'r')

    # extract values
    comid = ncfile.variables['rivid'][:]
    max_flow = ncfile.variables['max_flow'][:]
    return20 = ncfile.variables['return_period_20'][:]
    return10 = ncfile.variables['return_period_10'][:]
    return2 = ncfile.variables['return_period_2'][:]

    # creates panda series from values
    max_table = pd.Series(max_flow, index=comid)
    return2_table = pd.Series(return2, index=comid)
    return10_table = pd.Series(return10, index=comid)
    return20_table = pd.Series(return20, index=comid)

    #  creates dataframe
    df = pd.DataFrame([return2_table, return10_table, return20_table, max_table])
    df = df.transpose()

    # creates filename and header
    filename = '-'.join([watershed_name, 'return_periods.csv'])
    header = ['return_2', 'return_10', 'return_20', 'return_max']

    # exports dataframe as csv
    df.to_csv(os.path.join(output_dir, filename), index=True, index_label='comid', header=header)

    return 'Success'


# runs function on file execution
if __name__ == "__main__":
    get_return_periods_as_csv(
        input_dir='/home/michael/host_share/era_data',
        output_dir='/home/michael/host_share/rapid-io_init/output/dominican_republic-national',
        watershed_name='dominican_republic-national'
    )