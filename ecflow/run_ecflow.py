#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 11:43:42 2019

@author: Michael Souffront
"""

import sys
import os
from shutil import move, rmtree

from spt_compute.imports.ecmwf_rapid_multiprocess_worker import ecmwf_rapid_multiprocess_worker


class CaptureStdOutToLog(object):
    def __init__(self, log_file_path, error_file_path=None):
        self.log_file_path = log_file_path
        self.error_file_path = error_file_path
        if error_file_path is None:
            self.error_file_path = "{0}.err".format(os.path.splitext(log_file_path)[0])

    def __enter__(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        try:
            os.makedirs(os.path.dirname(self.log_file_path))
        except OSError:
            pass
        sys.stdout = open(self.log_file_path, 'w')
        sys.stderr = open(self.error_file_path, 'w')
        return self

    def __exit__(self, *args):
        sys.stdout.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr
        
        
with open(os.path.join(str(sys.argv[1]), 'rapid_run.txt'), 'r') as f:
    lines = f.readlines()
    for line in lines:
        params = line.split(',')
        if int(params[8].replace('\n', '')) == int(sys.argv[2]):
            ecmwf_forecast = params[0]
            forecast_date_timestep = params[1]
            watershed = params[2]
            subbasin = params[3]
            rapid_executable_location = str(sys.argv[3])
            initialize_flows = params[4]
            job_name = params[5]
            master_rapid_outflow_file = params[6]
            rapid_input_directory = params[7]
            mp_execute_directory = str(sys.argv[4])
            subprocess_forecast_log_dir = str(sys.argv[5])
            watershed_job_index = int(params[8].replace('\n', ''))

            with CaptureStdOutToLog(os.path.join(subprocess_forecast_log_dir, "{0}.log".format(job_name))):
                execute_directory = os.path.join(mp_execute_directory, job_name)
                try:
                    os.mkdir(execute_directory)
                except OSError:
                    pass
        
                try:
                    os.makedirs(os.path.dirname(master_rapid_outflow_file))
                except OSError:
                    pass
        
                ecmwf_rapid_multiprocess_worker(
                    execute_directory,
                    rapid_input_directory,
                    ecmwf_forecast,
                    forecast_date_timestep,
                    watershed,
                    subbasin,
                    rapid_executable_location,
                    initialize_flows,
                )
        
                node_rapid_outflow_file = os.path.join(
                    execute_directory,
                    os.path.basename(master_rapid_outflow_file)
                )
        
                move(node_rapid_outflow_file, master_rapid_outflow_file)
                rmtree(execute_directory)
