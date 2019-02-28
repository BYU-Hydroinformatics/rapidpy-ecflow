#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 14:23:11 2019

@author: michael
"""
qout = '/home/michael/host_share/rapid-io/output' \
       '/south_america-col_negro_b' \
       '/Qout_erai_t511_24hr_19800101to19961231.nc'
connt = '/home/michael/host_share/rapid-io/input' \
        '/south_america-col_negro_b/rapid_connect.csv'
       
       
                        
from RAPIDpy.rapid import RAPID
rapid_manager = RAPID(
    Qout_file=qout,
    rapid_connect_file=connt
)

rapid_manager.generate_seasonal_intitialization(
    qinit_file='/home/michael/test_seasonal_qinit.csv'
)