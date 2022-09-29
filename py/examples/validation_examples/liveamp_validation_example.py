# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:49:41 2022

@author: consu
"""

import pandas as pd
import pyxdf
import matplotlib.pyplot as plt
import numpy as np
import tool as bt
import scipy as scp
import statistics as stats
import math

try:
    import IPython
    IPython.get_ipython().magic("matplotlib qt")
except:
    plt.ion()

#fs_la = 250
fs_la = {}
fs_la["EA"] = 250
fs_la["AX"] = 250
fs_la["AY"] = 250
fs_la["AZ"] = 250
fs_la["ECG"] = 100
fs_eb = {}
fs_eb["EA"] = 15
fs_eb["AX"] = 25
fs_eb["AY"] = 25
fs_eb["AZ"] = 25
fs_eb["PI"] = 100

# ECG + EDA + Accel files
liveamp_file_name = r'C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share\Science\data\measurement sensors\2022-09-28\2022-09-28_09-53.xdf'
file_dir = r"C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share\Science\data\measurement sensors\2022-09-28"
file_base = r"2022-09-28_09-52-10-439680"
liveamp_ind = {}
liveamp_ind["EA"] = [0, 0] 
liveamp_ind["AX"] = [0, 1] 
liveamp_ind["AY"] = [0, 2] 
liveamp_ind["AZ"] = [0, 3] 
liveamp_ind["ECG"] = [1, 0] 
trim_durations = [30, 30]

# EDA + Accel files
# liveamp_file_name = r'C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share\Science\data\measurement sensors\2022-09-21\20220921-2336.xdf'
# file_dir = r"C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share\Science\data\measurement sensors\2022-09-21"
# file_base = r"2022-09-21_23-34-20-381606"
# liveamp_ind = {}
# liveamp_ind["EA"] = 0 
# liveamp_ind["AX"] = 2 
# liveamp_ind["AY"] = 3 
# liveamp_ind["AZ"] = 4 

simple_xdf_plot = 0

timestamp_id = "LslMarkerSourceTimestamp"

eda_bandpass = [0.1, 5]
eb_eda_amp = 5
ecg_bandpass = [5, 49]
ppg_bandpass = [1, 49]

def trim_data(data, timestamps, fs, trim_durations = [0, 0]):
    # Cut last 30 seconds. ToDo: add this as a general parameter
    out_data = data[int(trim_durations[0]*fs) : int(len(timestamps)-trim_durations[1]*fs) - 1]
    out_timestamps = timestamps[int(trim_durations[0]*fs) : int(len(timestamps)-trim_durations[1]*fs) - 1]
    return out_data, out_timestamps
    

def regression_plots(x, y, title = "", xlabel = "", ylabel = "", ylim = []):
    
    plot_data_eb = x["data"]
    plot_timestamps_eb = x["timestamps"]
    plot_data_la = y["data"]
    plot_timestamps_la = y["timestamps"]
    
    # Find overlapped timestamps and fs_la[type_tag]le data for regression
    shared_time = []
    shared_time.append(max(plot_timestamps_la[0], plot_timestamps_eb[0]))
    shared_time.append(min(plot_timestamps_la[len(plot_timestamps_la)-1], 
                           plot_timestamps_eb[len(plot_timestamps_eb)-1]))
    shared_ind_la = ((plot_timestamps_la > shared_time[0]) & (plot_timestamps_la < shared_time[1]))
    shared_ind_eb = ((plot_timestamps_eb > shared_time[0]) & (plot_timestamps_eb < shared_time[1]))
    
    n_resamp = 0
    if (sum(shared_ind_la) < sum(shared_ind_eb)):
        n_resamp = sum(shared_ind_la)
        plot_timestamp_rs = plot_timestamps_la[shared_ind_la]
    else:
        n_resamp = sum(shared_ind_eb)
        plot_timestamp_rs = plot_timestamps_eb[shared_ind_eb]
        
    plot_data_rs_la = scp.signal.resample(plot_data_la[shared_ind_la], n_resamp)
    plot_data_rs_eb = scp.signal.resample(plot_data_eb[shared_ind_eb], n_resamp)
       
    # Plot resampled overlapping data
    fig, ax = plt.subplots(2)
    ax[0].plot(plot_timestamp_rs, plot_data_rs_la, color="red", label=y["label"])
    ax[0].plot(plot_timestamp_rs, plot_data_rs_eb, color="black", label=x["label"])
    ax[0].legend()
    ax[0].set_xlabel(xlabel)
    ax[0].set_ylabel(ylabel)
    if (len(ylim) == 2):
        ax[0].set_ylim(ylim)
    
    
    # Remove outliers
    lims = [stats.mean(plot_data_rs_eb) - np.std(plot_data_rs_eb)*3,
            stats.mean(plot_data_rs_eb) + np.std(plot_data_rs_eb)*3]
    not_outliers = (plot_data_rs_eb > lims[0]) & (plot_data_rs_eb < lims[1])
    lims = [stats.mean(plot_data_rs_la) - np.std(plot_data_rs_la)*3,
            stats.mean(plot_data_rs_la) + np.std(plot_data_rs_la)*3]
    not_outliers = not_outliers & (plot_data_rs_la > lims[0]) & (plot_data_rs_la < lims[1])
    plot_data_rs_out_eb = plot_data_rs_eb[not_outliers]
    plot_data_rs_out_la = plot_data_rs_la[not_outliers]

    # Plot regression
    # fig, ax1 = plt.subplots()
    ax[1].scatter(plot_data_rs_out_eb, plot_data_rs_out_la)
    xlim_data = ax[1].get_xlim()
    xlim_diff = (xlim_data[1] - xlim_data[0]) * 0.4
    xlim_plt = [xlim_data[0] - xlim_diff, xlim_data[1] + xlim_diff]
    slope, intercept, r, p, std_err = scp.stats.linregress(plot_data_rs_out_eb, plot_data_rs_out_la)
    ax[1].plot(xlim_plt, [xlim_plt[0] * slope + intercept, xlim_plt[1] * slope + intercept])
    
    ax[1].set_xlabel(x["label"])
    ax[1].set_ylabel(y["label"])
    ax[1].text(xlim_data[1],  xlim_data[0]* slope + intercept, 
             "slope = {:.2f}".format(slope) + "\ny-cept = {:.2f}".format(intercept) 
             + "\nr = {:.2f}".format(r) + "\np = {:.2f}".format(p))
    if (len(ylim) == 2):
        ax[0].set_ylim(ylim)
    fig.suptitle(title)
    

liveamp_data, header = pyxdf.load_xdf(liveamp_file_name)

if (simple_xdf_plot):
    stream_counter = 0
    fig, ax1 = plt.subplots()
    for stream in liveamp_data:
        series_counter = 0
        for n in range(len(stream['time_series'][0])):
            y = stream['time_series'][:, n]
            plt.plot(stream['time_stamps'], y, label="" + str(stream_counter) + ":" + str(series_counter))
            series_counter += 1
        stream_counter += 1
    
    plt.show()
    plt.legend()
    quit()


#### Script Begin ####

### Accelerometer ###

# setup twin axes
fig, ax1 = plt.subplots(1)
ax2 = ax1.twinx()
# setup data containers
plot_data_la = []
plot_timestamps_la = []
plot_data_eb = []
plot_timestamps_eb = []
# setup TypeTags
type_tags = ["AX", "AY", "AZ"]

for i in range(len(type_tags)):
    #ax2.append(ax1[i].twinx())
    #ax1[i].title.set_text(type_tags[i])
    type_tag = type_tags[i]
    
    
    # Plot AX data from Brain Products
    stream = liveamp_data[liveamp_ind[type_tag][0]]
    ts = stream['time_series']
    if (i == 0):
        plot_data_la = np.square(ts[:, liveamp_ind[type_tag][1]] / 1000)
        plot_timestamps_la = stream['time_stamps']
    else:
        plot_data_la += np.square(ts[:, liveamp_ind[type_tag][1]] / 1000)
    
    # Plot emotibit Accel X
    data = []
    t = 0
    file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + type_tag + '.csv'
    print(file_path)
    data.append(pd.read_csv(file_path))
    if (i == 0):
        plot_data_eb = np.square(data[t][type_tag])
        plot_timestamps_eb = data[t][timestamp_id].to_numpy()
    else:
        plot_data_eb += np.square(data[t][type_tag])

plot_data_eb = np.sqrt(plot_data_eb)
plot_data_la = np.sqrt(plot_data_la)
     
# Trim beginning / end of data to remove junk & sync taps
plot_data_eb, plot_timestamps_eb = trim_data(plot_data_eb, plot_timestamps_eb, fs_eb[type_tag], trim_durations)   
plot_data_la, plot_timestamps_la = trim_data(plot_data_la, plot_timestamps_la, fs_la[type_tag], trim_durations)   


ax1.plot(plot_timestamps_la, plot_data_la, color="red")
ax1.set_ylabel("Brain Products", color="red", fontsize=14)
ax2.plot(plot_timestamps_eb, plot_data_eb, color="black")
ax2.set_ylabel("EmotiBit",  color="black",  fontsize=14)
ax1.set_xlabel("Time (seconds)")
plt.show()

reg_data_x = {}
reg_data_x["label"] = "EmotiBit"
reg_data_x["data"] = plot_data_eb
reg_data_x["timestamps"] = plot_timestamps_eb

reg_data_y = {}
reg_data_y["label"] = "Brain Products"
reg_data_y["data"] = plot_data_la
reg_data_y["timestamps"] = plot_timestamps_la

regression_plots(reg_data_x, reg_data_y, title="Accelerometer", 
                 xlabel="Time (seconds)", ylabel="Acceleration (G)",
                 ylim=[0, 2])

#######################################################
# EDA 
#######################################################

# setup twin axes
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
# Plot EDA data from Brain Products
type_tag = "EA"
stream = liveamp_data[liveamp_ind[type_tag][0]]
plot_timestamps_la = stream['time_stamps']
plot_data_la = stream['time_series'][:, liveamp_ind[type_tag][1]] / 25000 # uS / 25000 mV for Brain Products
plot_data_la, plot_timestamps_la = trim_data(plot_data_la, plot_timestamps_la, fs_la[type_tag], trim_durations) 
plt.plot(plot_timestamps_la, plot_data_la, color="red")
ax1.set_ylabel("Brain Products", color="red", fontsize=14)

# Plot EmotiBit EDA 
type_tag = "EA"    
data = []   
file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + type_tag + '.csv'
print(file_path)
data.append(pd.read_csv(file_path))

t = 0
plot_timestamps_eb = data[t][timestamp_id].to_numpy()
plot_data_eb = data[t][type_tag]
#plot_data_eb = plot_data_eb*eb_eda_amp
# Trim beginning / end of data to remove junk & sync taps
plot_data_eb, plot_timestamps_eb = trim_data(plot_data_eb, plot_timestamps_eb, fs_eb[type_tag], trim_durations) 
plt.plot(plot_timestamps_eb, plot_data_eb, color="black")
ax2.set_ylabel("EmotiBit",  color="black",  fontsize=14)
ax1.set_xlabel("Time (seconds)")
plt.show()

reg_data_x = {}
reg_data_x["label"] = "EmotiBit"
reg_data_x["data"] = plot_data_eb
reg_data_x["timestamps"] = plot_timestamps_eb

reg_data_y = {}
reg_data_y["label"] = "Brain Products"
reg_data_y["data"] = plot_data_la
reg_data_y["timestamps"] = plot_timestamps_la

regression_plots(reg_data_x, reg_data_y, title="EDA", xlabel="Time (seconds)", ylabel="EDA (uSiemens)")

# Bandpass filter EDA
plot_data_eb = bt.band_filter(plot_data_eb, np.array(eda_bandpass), fs_eb[type_tag], order=4)
plot_data_la = bt.band_filter(plot_data_la, np.array(eda_bandpass), fs_la[type_tag], order=4)
# Remove filter artifact (3x duration of bandpass[0])
reg_data_x["data"], reg_data_x["timestamps"] = trim_data(plot_data_eb, plot_timestamps_eb, fs_eb[type_tag], [4/eda_bandpass[0], 4/eda_bandpass[0]]) 
reg_data_y["data"], reg_data_y["timestamps"] = trim_data(plot_data_la, plot_timestamps_la, fs_la[type_tag], [4/eda_bandpass[0], 4/eda_bandpass[0]]) 

regression_plots(reg_data_x, reg_data_y, 
                 title="EDR (EDA Filtered {:.1f}".format(eda_bandpass[0]) + "-{:.1f}Hz)".format(eda_bandpass[1])
                 , xlabel="Time (seconds)", ylabel="EDR (uSiemens)")

#######################################################
# Heart Rate 
#######################################################

# setup twin axes
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
# Brain Products 
type_tag = "ECG"
stream = liveamp_data[liveamp_ind[type_tag][0]]
plot_timestamps_la = stream['time_stamps']
plot_data_la = -stream['time_series'][:, liveamp_ind[type_tag][1]] / 25000 # uS / 25000 mV for Brain Products
plot_data_la, plot_timestamps_la = trim_data(plot_data_la, plot_timestamps_la, fs_la[type_tag], trim_durations) 
#plt.plot(plot_timestamps_la, plot_data_la, color="red")

# Bandpass filter
plot_data_la = bt.band_filter(plot_data_la, np.array(ecg_bandpass), fs_la[type_tag], order=4)
plot_data_la, plot_timestamps_la = trim_data(plot_data_la, plot_timestamps_la, fs_la[type_tag], [5/ecg_bandpass[0], 5/ecg_bandpass[0]])
ax1.plot(plot_timestamps_la, plot_data_la, color="red")
ax1.set_ylabel("Brain Products (ECG)", color="red", fontsize=14)
# Detect Peaks
peaks_la, _ = scp.signal.find_peaks(plot_data_la, 0.015)
ax1.plot(plot_timestamps_la[peaks_la], plot_data_la[peaks_la], "o", color="red")

# EmotiBit 
type_tag = "PI"    
data = []   
file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + type_tag + '.csv'
print(file_path)
data.append(pd.read_csv(file_path))
t = 0
plot_timestamps_eb = data[t][timestamp_id].to_numpy()
plot_data_eb = -data[t][type_tag]
plot_data_eb, plot_timestamps_eb = trim_data(plot_data_eb, plot_timestamps_eb, fs_eb[type_tag], trim_durations) 
#plt.plot(plot_timestamps_eb, plot_data_eb, color="black")
# Bandpass filter
plot_data_eb = bt.band_filter(plot_data_eb, np.array(ppg_bandpass), fs_eb[type_tag], order=4)
plot_data_eb, plot_timestamps_eb = trim_data(plot_data_eb, plot_timestamps_eb, fs_eb[type_tag], [5/ppg_bandpass[0], 5/ppg_bandpass[0]]) 
ax2.plot(plot_timestamps_eb, plot_data_eb, color="black")
# Detect Peaks
peaks_eb, _ = scp.signal.find_peaks(plot_data_eb, 75, None, fs_eb[type_tag] / 2)
ax2.plot(plot_timestamps_eb[peaks_eb], plot_data_eb[peaks_eb], "o", color="black")
ax2.set_ylabel("EmotiBit (PPG)", color="black", fontsize=14)
ax1.set_xlabel("Time (seconds)")
plt.show()

# setup twin axes
# Calculate HR
# Brain Products
type_tag = "ECG"
ibis_la = np.diff(peaks_la)/fs_la[type_tag]
hr_la = 1 / ibis_la * 60
plot_data_la = hr_la
plot_timestamps_la = plot_timestamps_la[peaks_la[0:len(peaks_la)-1]]

# EmotiBit
type_tag = "PI" 
ibis_eb = np.diff(peaks_eb)/fs_eb[type_tag]
hr_eb = 1 / ibis_eb * 60
plot_data_eb = hr_eb
plot_timestamps_eb = plot_timestamps_eb[peaks_eb[0:len(peaks_eb)-1]]
plt.show()

reg_data_x = {}
reg_data_x["label"] = "EmotiBit"
reg_data_x["data"] = hr_eb
reg_data_x["timestamps"] = plot_timestamps_eb

reg_data_y = {}
reg_data_y["label"] = "Brain Products"
reg_data_y["data"] = hr_la
reg_data_y["timestamps"] = plot_timestamps_la

regression_plots(reg_data_x, reg_data_y, 
                 title="Heart Rate", xlabel="Time (seconds)", ylabel="Heart Rate (BPM)")