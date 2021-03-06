# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 22:19:31 2020

@author: consu
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### Add the type tage in the list which you want test
type_tags = ['PR', 'PI', 'PG', 'EA', 'EL', 'ER', 'H0', 'AX', 'AY', 'AZ', 
             'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'T0']
### Use the data parser to parse the file. Add the path to the folder below.
### Make sure the data is stored as <file_dir>/filename/filename_[type_tag]. 
### ex: C:\Users\nitin\Documents\EmotiBit\DataAnalysis\unControlledTest\2020-04-09_10-41-19-913922\2020-04-09_10-41-19-913922_PR.csv
file_dir = r"C:\Users\nitin\Documents\EmotiBit\DataAnalysis\unControlledTest"

file_base_names = ["2020-04-09_10-41-19-913922", "2020-04-09_10-41-19-913922"]
nbins = 100
fig_size = [1700.0, 900.0]

for type_tag in type_tags:
    fig_name = type_tag + ' Timestamp'
    fig = plt.figure(fig_name)
    fig.clf()
    fig_dpi = fig.get_dpi()
    fig.set_size_inches(fig_size[0]/float(fig_dpi),fig_size[1]/float(fig_dpi))
    fig, axs = plt.subplots(nrows=len(file_base_names), ncols=2, num=fig_name)
    plt.clf
    plt.subplots_adjust(left=.3)
    for f in range(len(file_base_names)):
        file_base = file_base_names[f]
        file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + type_tag + '.csv'
        print(file_path)
        eda_data = pd.read_csv(file_path);
        ts_diff_epoch = np.diff(eda_data.EpochTimestamp)
        ts_diff_emotibit = np.diff(eda_data.EmotiBitTimestamp) / 1000

        plt.sca(axs[f][0])
        h = plt.ylabel(file_base)
        h.set_rotation(0)
        axs[f][0].yaxis.set_label_position("left")
        axs[f][0].yaxis.set_label_coords(-0.35,.35)
        
        plt.plot(ts_diff_emotibit[1:ts_diff_emotibit.size])
        plt.plot(ts_diff_epoch[1:ts_diff_epoch.size])
        plt.xlim(0,60*10)
        plt.sca(axs[f][1])
        
        
        #counts, bins = np.histogram(ts_diff_emotibit)
        #axs[f][1].hist(bins[:-1], bins, weights=counts, label='EmotiBit')
        #counts, bins = np.histogram(ts_diff_epoch)
        #axs[f][1].hist(bins[:-1], bins, weights=counts, label='Epoch')
        x_range = [0, 0.15]
        plt.xlim(x_range);
        axs[f][1].hist(ts_diff_emotibit, nbins, range=x_range, label='EmotiBit')
        axs[f][1].hist(ts_diff_epoch, nbins, range=x_range, label='Epoch')
        if(f == 0):
            axs[f][1].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.)
            plt.title(fig_name)
            
        if (f < len(file_base_names) - 1):
            axs[f][0].get_xaxis().set_ticks([])
            axs[f][1].get_xaxis().set_ticks([])
            
        

