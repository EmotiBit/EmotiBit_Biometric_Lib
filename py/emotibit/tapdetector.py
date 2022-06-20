# -*- coding: utf-8 -*-
"""
@emotibit tapdetector
@brief detects taps on the accelerometer data using 3D vector of the change in 
acceleration. Can be used for tap synchronizing EmotiBit with other devices.
@example tapdetector.detect(file_dir = r"C:\priv\myDir", 
                            file_base_names = ["2022-06-07_15-23-33-810389"], 
                            timestamp_id = "LocalTimestamp",
                            time_window = [11, 14], 
                            height = 0.13)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def detect(file_dir = "", file_base_names = "", timestamp_id = "LocalTimestamp", 
           time_window = [0, 50000], height = 0.25):
    """
    @fn     detect()
    @brief  Detects tap times and saves the results in a file named *_taps.csv
    @param  file_dir Base directory of the parsed data files
    @param  file_base_names array of file bases of the data files. Expected 
            organization is file_dir/file_base_names[i]/file_base_names[i]_XX.csv
    @param  timestamp_id timestamp identifier to use for timestamps of taps
    @param  time_window Window (in secs) from the beginning of the file to look for taps
    @param  height Height of the threshold for detecting peaks
    @ToDo   Add multiple time_windows as input
    """
    print('***\ntapdetector.detect()')

    type_tags = ['AX', 'AY', 'AZ']
    time_mask = []
    
    
    fig_name = "taps"
    fig = plt.figure(fig_name)
    fig.clf()
    fig, axs = plt.subplots(nrows=len(type_tags) + 1, ncols=1, num=fig_name)
    
    print("type_tags: ", type_tags)
    print("time_window: ", time_window)
    print("height: ", height)
    print("timestamp_id: ", timestamp_id)
    print("Directory: ", file_dir)
    print("file_base_names: ", file_base_names)
    
    
    # ToDo Add multiple time_windows
    # ToDo Add multiple timestamp_ids
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
            timestamps = data[t][timestamp_id].to_numpy()
            timestamps_rel = timestamps - timestamps[0]
            time_mask = np.where((timestamps_rel > time_window[0]) & (timestamps_rel < time_window[1]))
            
            # Plot data
            plt.sca(plt.subplot(len(type_tags) + 1, 1, t + 1))
            plt.plot(data[t][type_tag].to_numpy()[time_mask])
            plt.gca().set_ylabel(type_tag)
            plt.gca().axes.xaxis.set_visible(False)
            
            
            # Create vector data
            # NOTE: this only works for signals with the same sampling rate
            if (t == 0): 
                # first data type
                data_vec = np.power(np.diff(data[t][type_tag].to_numpy()), 2)
            else:
                data_vec = np.add(data_vec, np.power(np.diff(data[t][type_tag].to_numpy()), 2))
    
            
        data_vec = np.sqrt(data_vec)
        p_ind, p_val = find_peaks(data_vec[0 : sum(timestamps_rel < time_window[1])], height=height)
        p_ind = p_ind[p_ind > time_mask[0][0]] # Remove indexes less than time_window[0]
        
        
        plt.sca(plt.subplot(len(type_tags) + 1, 1, len(type_tags) + 1))
        
        time_mask = time_mask[0][0 : min(len(time_mask[0]) - 1, len(timestamps_rel) - 1)]
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
        print("Tap " + timestamp_id + ": ", timestamps[p_ind])
        
        file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + 'taps' + '.csv'
        print('Saving: ' + file_path)
        
        tap_data= {'Indexes': p_ind,
            'RelativeTimestamp': timestamps_rel[p_ind],
            timestamp_id: timestamps[p_ind]}
        df = pd.DataFrame(tap_data);
        df.to_csv(file_path, float_format='%10.6f', index=False)