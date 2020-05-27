#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:08:13 2019

@author: Michael Souffront
"""

import os
import sys
from datetime import datetime
from re import split
from RAPIDpy.inflow import run_lsm_rapid_process


# home = os.path.expanduser('~')
# print(home)
# rapid_exec = 'rapid/run/rapid'
# era_data = 'host_share/era5_data/era5_runoff_2001to2015'
# era_data = 'host_share/era_data'
start_date = list(map(int, split("/|-", str(sys.argv[4]))))
end_date = list(map(int, split("/|-", str(sys.argv[5]))))

run_lsm_rapid_process(
        rapid_executable_location=str(sys.argv[1]),
        rapid_io_files_location=str(sys.argv[2]),
        lsm_data_location=str(sys.argv[3]),
        simulation_start_datetime=datetime(*start_date),  # datetime(2010, 1, 1),
        simulation_end_datetime=datetime(*end_date),  # datetime(2014, 12, 31),
        generate_rapid_namelist_file=True,
        run_rapid_simulation=True,
        generate_return_periods_file=True,
        return_period_method='weibull',
        generate_seasonal_averages_file=True,
        generate_seasonal_initialization_file=True,
        generate_initialization_file=False,
        use_all_processors=False,
        num_processors=1,
)

