#!/usr/bin/python3.6m

import sys
import os
import re
from glob import glob
import datetime
import logging as log

log.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=log.INFO)



def get_date_timestep_from_forecast_folder(forecast_folder):
    """
    Gets the datetimestep from forecast
    """
    forecast_date_timestep = os.path.basename(forecast_folder)
    log.info(f'Forecast timestep {forecast_date_timestep}')
    return datetime.datetime.strptime(forecast_date_timestep[:11],"%Y%m%d%H").strftime("%Y%m%d.%H")


def get_valid_watershed_list(input_directory):
    """
    Get a list of folders formatted correctly for watershed-subbasin
    """
    valid_input_directories = []
    for directory in os.listdir(input_directory):
        if os.path.isdir(os.path.join(input_directory, directory)) \
                and len(directory.split("-")) == 2:
            valid_input_directories.append(directory)
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
        
    # get list of folders to run
    ecmwf_folders = sorted(glob(ecmwf_forecast_location))
    
    master_job_list = []
    
    for ecmwf_folder in ecmwf_folders:
        # get list of forecast files
        ecmwf_forecasts = glob(os.path.join(ecmwf_folder,
                                            '*.runoff.%s*nc' % region))
        
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
            
            # create jobs
            for watershed_job_index, forecast in enumerate(ecmwf_forecasts):
                ensemble_number = get_ensemble_number_from_forecast(forecast)

                # get basin names
                outflow_file_name = 'Qout_%s_%s_%s.nc' % (watershed.lower(), 
                                                          subbasin.lower(), 
                                                          ensemble_number)

                master_rapid_outflow_file = os.path.join(
                        master_watershed_outflow_directory, outflow_file_name)

                job_name = 'job_%s_%s_%s_%s' % (forecast_date_timestep, 
                                                watershed, subbasin, 
                                                ensemble_number)
                
                rapid_watershed_jobs[rapid_input_directory]['jobs'].append((
                        forecast,
                        forecast_date_timestep,
                        watershed.lower(),
                        subbasin.lower(),
                        initialize_flows,
                        job_name,
                        master_rapid_outflow_file,
                        master_watershed_input_directory,
                        watershed_job_index
                ))
                                
            master_job_list += rapid_watershed_jobs[rapid_input_directory]['jobs']
    
#    print(master_job_list)
    with open(os.path.join(str(sys.argv[3]), 'rapid_run.txt'), 'w') as f:
        for line in master_job_list:
            formatted_line = ','.join(map(str, line))
            f.write(f"{formatted_line}\n")
    return master_job_list


# ------------------------------------------------------------------------------
# main process
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    ecmwf_rapid_process(
        rapid_io_files_location=str(sys.argv[1]),
        ecmwf_forecast_location=str(sys.argv[2]),
        region="",
        date_string="*.00"
    )
