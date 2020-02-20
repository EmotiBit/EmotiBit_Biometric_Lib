# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 22:19:31 2020

@author: consu
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

type_tags = ['EA']
file_dir = r"C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share (1)\Conferences_Talks\2020-02-14 Duke CS101 Lab\data"
file_base_names = [f.name for f in os.scandir(file_dir) if f.is_dir()]
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
        eda_data = pd.read_csv(file_dir +'/' + file_base + '/' + file_base + '_' + type_tag + '.csv');
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
            
        

