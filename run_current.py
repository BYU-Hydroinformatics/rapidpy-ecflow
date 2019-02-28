#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 11:38:05 2019

@author: michael
"""

import os
from spt_compute import run_ecmwf_forecast_process

home = os.path.expanduser('~')
rapid_exec = 'rapid/run/rapid'

#------------------------------------------------------------------------------
#main process
#------------------------------------------------------------------------------
if __name__ == "__main__":
    run_ecmwf_forecast_process(
        rapid_executable_location=os.path.join(home, rapid_exec),
        rapid_io_files_location=os.path.join(home, 'host_share/rapid-io_init'),
        ecmwf_forecast_location=os.path.join(home, 'host_share/ecmwf'),
        era_interim_data_location=os.path.join(home, "rapid-io/output"),
        subprocess_log_directory=os.path.join(home, 'subprocess_logs'),
        main_log_directory=os.path.join(home, 'host_share/spt_compute_logs'),
        sync_rapid_input_with_ckan=False,
        download_ecmwf=False,
#        ftp_host="ftp.ecmwf.int",
#        ftp_login="",
#        ftp_passwd="",
#        ftp_directory="",
#        region="",
        date_string="*.00",
        upload_output_to_ckan=False,
        initialize_flows=True,
        create_warning_points=True,
        warning_flow_threshold=30,
        delete_output_when_done=False,
        mp_mode='multiprocess',
        mp_execute_directory='/home/michael/execute',
    )