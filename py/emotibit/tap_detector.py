# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math as math
from scipy.signal import find_peaks

print ("Number of arguments:", len(sys.argv), "arguments")
print ("Argument List:", str(sys.argv))

print('arguments', sys.argv)

file_dir = r"C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share\EmotiBit Test Data\Appelbaum Jam 2022-06-07\Liam"


file_base_names = ["2022-06-07_15-23-33-810389"]
time_window = [0, 2000] # seconds
height = 0.25

type_tags = ['AX', 'AY', 'AZ']
time_mask = []


fig_name = "taps"
fig = plt.figure(fig_name)
fig.clf()
fig, axs = plt.subplots(nrows=len(type_tags) + 1, ncols=1, num=fig_name)

print("type_tags: ", type_tags)
print("time_window: ", time_window)
print("height: ", height)
print("Directory: ", file_dir)


for f in range(len(file_base_names)):
    file_base = file_base_names[f]
    print("File: ", file_base)
    
    data = []
    data_vec = []
    for t in range(len(type_tags)):
        type_tag = type_tags[t]
                
        file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + type_tag + '.csv'
        print(file_path)
        data.append(pd.read_csv(file_path))
        
        # Create time segment
        # NOTE: this only works for signals with the same sampling rate
        timestamps = data[t]['LocalTimestamp'].to_numpy()
        timestamps_rel = timestamps - timestamps[0]
        time_mask = np.where((timestamps_rel > time_window[0]) & (timestamps_rel < time_window[1]))
        
        # Plot data
        plt.sca(plt.subplot(len(type_tags) + 1, 1, t + 1))
        plt.plot(data[t][type_tag].to_numpy()[time_mask])
        plt.gca().set_ylabel(type_tag)
        
        
        # Create vector data
        # NOTE: this only works for signals with the same sampling rate
        if (t == 0): 
            # first data type
            data_vec = np.power(np.diff(data[t][type_tag].to_numpy()), 2)
        else:
            data_vec = np.add(data_vec, np.power(np.diff(data[t][type_tag].to_numpy()), 2))

        
    data_vec = np.sqrt(data_vec)
    p_ind, p_val = find_peaks(data_vec[0 : sum(timestamps_rel < time_window[1])], height=height)
    
    plt.sca(plt.subplot(len(type_tags) + 1, 1, len(type_tags) + 1))
    
    masked_timestamps = timestamps_rel[time_mask]
    
    plt.plot(masked_timestamps, data_vec[time_mask])
    plt.plot([masked_timestamps[1], masked_timestamps[len(masked_timestamps) - 1]], [height, height])
    plt.plot(timestamps_rel[p_ind], data_vec[p_ind], 'r*')
    plt.gca().set_ylabel("vec(diff())")
    plt.gca().set_xlabel("Time since file begin (sec)")
    
    #np.set_printoptions(precision=16)
    np.set_printoptions(formatter={'float': '{: 10.6f}'.format})
    
    print("***\nTap indexes: ", p_ind)
    print("Tap RelativeTimestamp: ", timestamps_rel[p_ind])
    print("Tap LocalTimestamp: ", timestamps[p_ind])
    
    file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + 'taps' + '.csv'
    print('\n' + file_path)
    
    tap_data= {'Indexes': p_ind,
        'RelativeTimestamp': timestamps_rel[p_ind],
        'LocalTimestamp': timestamps[p_ind]}
    df = pd.DataFrame(tap_data);
    df.to_csv(file_path, float_format='%10.6f', index=False)