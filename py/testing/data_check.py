# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:56:37 2020

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
ylims = [0, 10]
fig_size = [1700.0, 900.0]

file_base = file_base_names[0]

for type_tag in type_tags:
    fig = plt.figure(type_tag)
    fig.clf()
    fig_dpi = fig.get_dpi()
    fig.set_size_inches(fig_size[0]/float(fig_dpi),fig_size[1]/float(fig_dpi))
    fig, axs = plt.subplots(nrows=len(file_base_names), ncols=1, num=type_tag)
    plt.clf
    plt.subplots_adjust(left=.2)
    for f in range(len(file_base_names)):
        file_base = file_base_names[f]
        eda_data = pd.read_csv(file_dir +'/' + file_base + '/' + file_base + '_' + type_tag + '.csv');
        ts_diff_epoch = np.diff(eda_data.EpochTimestamp)
        ts_diff_emotibit = np.diff(eda_data.EmotiBitTimestamp) / 1000

        plt.sca(axs[f])
        
            
        plt.plot(eda_data.EpochTimestamp, eda_data[type_tag])
        ylim = plt.ylim()
        plt.ylim(max(ylim[0], ylims[0]), min(ylim[1], ylims[1]))
        h = plt.ylabel(file_base)
        h.set_rotation(0)
        axs[f].yaxis.set_label_position("right")
        axs[f].yaxis.set_label_coords(-0.125,.65)
        axs[f].get_xaxis().set_ticks([])
        if (f == 0):
            plt.title(type_tag)