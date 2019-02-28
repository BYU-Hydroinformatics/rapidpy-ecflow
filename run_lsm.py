#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 09:08:13 2019

@author: michael
"""

import os
from datetime import datetime
from RAPIDpy.inflow import run_lsm_rapid_process


home = os.path.expanduser('~')
print(home)
rapid_exec = 'packages/rapid/run/rapid'
#era_data = 'host_share/era5_data/era5_runoff_2001to2015'
era_data = 'host_share/era_data'

run_lsm_rapid_process(
        rapid_executable_location=os.path.join(home, rapid_exec),
        rapid_io_files_location=os.path.join(home, 'host_share/rapid-io'),
        lsm_data_location=os.path.join(home, era_data),
        simulation_start_datetime=datetime(2010, 1, 1),
        simulation_end_datetime=datetime(2014, 12, 31),
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

