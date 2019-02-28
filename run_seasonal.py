#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 15:58:05 2019

@author: michael
"""

from RAPIDpy.postprocess.generate_seasonal_averages import \
generate_seasonal_averages as gsa


lsm_rapid_output_file = '/home/michael/rapid-io/output/' \
                        'dominican_republic-national/' \
                        'Qout_erai_t511_24hr_19800101to19961231.nc'
seasonal_averages_file = '/home/michael/rapid-io/output/' \
                         'dominican_republic-national/' \
                         'Qout_seasonal_test_80_96.nc'
num_cpus = 1

gsa(lsm_rapid_output_file, seasonal_averages_file, num_cpus)