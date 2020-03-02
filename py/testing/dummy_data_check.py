# -*- coding: utf-8 -*-



"""
 Prints summary stats for EmotiBit triangle wave dummy data to assess for correctness
 
   Reports:
       Data range
       diff(data) range
       Signal period range (samples)
       Signal period range (EpochTimestamps)
       Signal freq range (EpochTimestamps)

 ToDo: Turn into a module

Created on Wed Feb 19 14:56:37 2020

@author: consu
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys 


type_tags = ['PR', 'PI', 'PG', 'EA', 'EL', 'ER', 'H0', 'AX', 'AY', 'AZ', 
             'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'TH', 'T0']
file_dir = r"C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share (1)\EmotiBit Test Data\Beta Test Data\Acute\DummyData\2020-03-02_05-47-42-936329"
file_base = "2020-03-02_05-47-42-936329"
nbins = 100
ylims = [0, 10]
fig_size = [1700.0, 900.0]
n_zfill = 9;
p_format = '{:.4f}'
stats_filename = "DummyDataStats.txt"

stats_file = open(file_dir +'/' + stats_filename, 'w+')
print(stats_file.closed)
print_locs = [sys.stdout, stats_file]

for print_loc in print_locs:
    print(file_base, file = print_loc)

stats_file = open(file_dir +'/' + stats_filename, 'a+')
print(stats_file.closed)

for type_tag in type_tags:
    
    data = pd.read_csv(file_dir +'/' + file_base + '_' + type_tag + '.csv');
    
    data_diff = np.diff(data[type_tag])
    trough_indices = data.index[data[type_tag] == min(data[type_tag])]
    sample_periods = np.diff(trough_indices)
    epoch_periods = np.diff(data.EpochTimestamp[trough_indices])
        
    for print_loc in print_locs:
        print(type_tag, file = print_loc)
        print((p_format.format(min(data[type_tag]))).rjust(n_zfill) + ", " + 
              (p_format.format(max(data[type_tag]))).rjust(n_zfill) + 
              " -- Data range", file = print_loc)
        print((p_format.format(min(data_diff))).rjust(n_zfill) + ", " + 
              (p_format.format(max(data_diff))).rjust(n_zfill) + 
              " -- Delta range", file = print_loc)
        print((p_format.format(min(sample_periods))).rjust(n_zfill) + ", " + 
              (p_format.format(max(sample_periods))).rjust(n_zfill) + 
              " -- Signal period range (samples)", file = print_loc)
        print((p_format.format(min(epoch_periods))).rjust(n_zfill) + ", " + 
              (p_format.format(max(epoch_periods))).rjust(n_zfill) + 
              " -- Signal period range (EpochTimestamps)", file = print_loc)
        print((p_format.format(min(1 / epoch_periods))).rjust(n_zfill) + ", " + 
              (p_format.format(max(1 / epoch_periods))).rjust(n_zfill) + 
              " -- Signal freq range (EpochTimestamps)", file = print_loc)
        
        # ToDo: print to a csv file?
        
    # ToDo: Add graphing to get at-a-glance assessment

   
#stats_file.close()
print(stats_file.closed)
