#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 11:43:42 2019

@author: michael
"""

#import unittest
from spt_compute.imports.ecmwf_rapid_multiprocess_worker import \
ecmwf_rapid_multiprocess_worker

ecmwf_rapid_multiprocess_worker(
        '/home/michael/execute',
        '/home/michael/host_share/rapid-io_init/input/dominican_republic-national',
        '/home/michael/host_share/ecmwf/Runoff.20190120.00.exp1.Fgrid.netcdf/2.runoff.nc',
        '20190120.00',
        'dominican_republic',
        'national',
        '/home/michael/rapid/run/rapid',
        True,
        )
#def test_ecmwf_rapid_multiprocess_worker():
    