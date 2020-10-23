#!/usr/bin/python3.6m

import sys
import os
import re
from glob import glob
import datetime
import logging as log

from spt_compute.imports.helper_functions import find_current_rapid_output
from spt_compute.imports.streamflow_assimilation import compute_initial_rapid_flows

log.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=log.INFO)


def get_date_timestep_from_forecast_folder(forecast_folder):
    """
    Gets the datetimestep from forecast
    """
    forecast_date_timestep = os.path.basename(forecast_folder)
    log.info(f'Forecast timestep - {forecast_date_timestep}')
    return datetime.datetime.strptime(forecast_date_timestep[:11],"%Y%m%d%H").strftime("%Y%m%d.%H")


def get_valid_watershed_list(input_directory):
    """
    Get a list of folders formatted correctly for watershed-subbasin
    """
    log.info(f'{input_directory}')
    valid_input_directories = []
    for directory in os.listdir(input_directory):
        log.info(os.listdir(input_directory))
        if os.path.isdir(os.path.join(input_directory, directory)) \
                and len(directory.split("-")) == 2:
            valid_input_directories.append(directory)
            log.info(f'Appending directory -  {directory}')
        else:
            print("{0} incorrectly formatted. Skipping ...".format(directory))
    return valid_input_directories


def get_ensemble_number_from_forecast(forecast_name):
    """
    Gets the datetimestep from forecast
    """
    forecast_split = os.path.basename(forecast_name).split(".")
    if forecast_name.endswith(".205.runoff.grib.runoff.netcdf"):
        ensemble_number = int(forecast_split[2])
    else:
        ensemble_number = int(forecast_split[0])
    return ensemble_number


def get_watershed_subbasin_from_folder(folder_name):
    """
    Get's the watershed & subbasin name from folder
    """
    input_folder_split = folder_name.split("-")
    watershed = input_folder_split[0].lower()
    subbasin = input_folder_split[1].lower()
    return watershed, subbasin


def ecmwf_rapid_process(rapid_io_files_location="",
                        ecmwf_forecast_location="",
                        region="",
                        date_string="",
                        ):
    
    # get list of correclty formatted rapid input directories in rapid directory
    rapid_input_directories = get_valid_watershed_list(
            os.path.join(rapid_io_files_location, "input"))
    log.info(f'Rapid_input_directories - {rapid_input_directories} {rapid_io_files_location}')
        
    # get list of folders to run
    ecmwf_folders = sorted(glob(ecmwf_forecast_location))
    
    master_job_list = []
    log.info(f'{ecmwf_folders}') 
    for ecmwf_folder in ecmwf_folders:
        # get list of forecast files
        ecmwf_forecasts = glob(os.path.join(ecmwf_folder,
                                            '*.runoff.%s*nc' % region))
        log.info(f'{ecmwf_forecasts} {ecmwf_folder}')
        
        # make the largest files first
        ecmwf_forecasts.sort(key=lambda x: int(os.path.basename(x).split('.')[0]), reverse=True)  # key=os.path.getsize
        forecast_date_timestep = get_date_timestep_from_forecast_folder(
                ecmwf_folder)
    
        # submit jobs to downsize ecmwf files to watershed
        rapid_watershed_jobs = {}
        for rapid_input_directory in rapid_input_directories:

            log.info(f'Adding rapid input folder {rapid_input_directory}')
            # keep list of jobs
            rapid_watershed_jobs[rapid_input_directory] = {
                'jobs': []
            }
            
            watershed, subbasin = get_watershed_subbasin_from_folder(
                    rapid_input_directory)
            
            master_watershed_input_directory = os.path.join(
                    rapid_io_files_location,
                    "input",
                    rapid_input_directory)
            
            master_watershed_outflow_directory = os.path.join(
                    rapid_io_files_location,
                    'output',
                    rapid_input_directory,
                    forecast_date_timestep)
            
            try:
                os.makedirs(master_watershed_outflow_directory)
            except OSError:
                pass
            
            initialize_flows = True
            
            # initialize flows for next run
            input_directory = os.path.join(rapid_io_files_location,
                                           'input',
                                           rapid_input_directory)

            forecast_directory = os.path.join(rapid_io_files_location,
                                              'output',
                                              rapid_input_directory,
                                              forecast_date_timestep)
            if os.path.exists(forecast_directory):
                watershed, subbasin = get_watershed_subbasin_from_folder(rapid_input_directory)
                log.info(f'find_rapid_output : {forecast_directory} {watershed} {subbasin}')
                basin_files = find_current_rapid_output(forecast_directory, watershed, subbasin)
                try:
                     
                    log.info(f'Compute_initial_rapid_flows : {basin_files} {input_directory} {forecast_date_timestep}')
                    compute_initial_rapid_flows(basin_files, input_directory, forecast_date_timestep)
                except Exception as ex:
                    print(ex)
                    pass


# ------------------------------------------------------------------------------
# main process
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    ecmwf_rapid_process(
        rapid_io_files_location=str(sys.argv[1]),
        ecmwf_forecast_location=str(sys.argv[1]),
        region="",
        date_string="*.00"
    )
