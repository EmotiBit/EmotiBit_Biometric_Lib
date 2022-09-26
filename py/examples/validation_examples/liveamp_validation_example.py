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

try:
    import IPython
    IPython.get_ipython().magic("matplotlib qt")
except:
    plt.ion()


liveamp_file_name = r'C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share\Science\data\measurement sensors\2022-09-21\20220921-2336.xdf'


file_dir = r"C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share\Science\data\measurement sensors\2022-09-21"
file_base = r"2022-09-21_23-34-20-381606"
timestamp_id = "LslMarkerSourceTimestamp"

bandpass = [0.1, 5]
eb_eda_amp = 5
liveamp_ind = {}
liveamp_ind["EA"] = 0 
liveamp_ind["AX"] = 2 
liveamp_ind["AY"] = 3 
liveamp_ind["AZ"] = 4 


liveamp_data, header = pyxdf.load_xdf(liveamp_file_name)

# fig, ax1 = plt.subplots()
# for stream in liveamp_data:
#     y = stream['time_series']

#     if isinstance(y, list):
#         # list of strings, draw one vertical line for each marker
#         for timestamp, marker in zip(stream['time_stamps'], y):
#             plt.axvline(x=timestamp)
#             print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
#     elif isinstance(y, np.ndarray):
#         # numeric data, draw as lines
#         plt.plot(stream['time_stamps'], y)
#     else:
#         raise RuntimeError('Unknown stream format')

# plt.show()



# setup twin axes
fig, ax1 = plt.subplots(1)
ax2 = ax1.twinx()
# setup data containers
liveamp_plot_data = []
liveamp_plot_timestamps = []
emotibit_plot_data = []
emotibit_plot_timestamps = []
# setup TypeTags
type_tags = ["AX", "AY", "AZ"]

for i in range(len(type_tags)):
    #ax2.append(ax1[i].twinx())
    #ax1[i].title.set_text(type_tags[i])
    
    
    # Plot AX data from liveamp
    stream = liveamp_data[0]
    ts = stream['time_series']
    if (i == 0):
        liveamp_plot_data = np.square(ts[:, liveamp_ind[type_tags[i]]] / 1000)
        liveamp_plot_timestamps = stream['time_stamps']
    else:
        liveamp_plot_data += np.square(ts[:, liveamp_ind[type_tags[i]]] / 1000)
    
    # Plot emotibit Accel X
    data = []
    t = 0
    file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + type_tags[i] + '.csv'
    print(file_path)
    data.append(pd.read_csv(file_path))
    if (i == 0):
        emotibit_plot_data = np.square(data[t][type_tags[i]])
        emotibit_plot_timestamps = data[t][timestamp_id].to_numpy()
    else:
        emotibit_plot_data += np.square(data[t][type_tags[i]])

plt.plot(liveamp_plot_timestamps, liveamp_plot_data, color="red")
ax1.set_ylabel("LiveAmp", color="red", fontsize=14)
plt.show()
plt.plot(emotibit_plot_timestamps, emotibit_plot_data, color="black")
ax2.set_ylabel("EmotiBit",  color="black",  fontsize=14)

# setup twin axes
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
# Plot EDA data from liveamp
stream = liveamp_data[0]
ts = stream['time_series']
y = ts[:, liveamp_ind["EA"]] / 25000

if isinstance(y, list):
    # list of strings, draw one vertical line for each marker
    for timestamp, marker in zip(stream['time_stamps'], y):
        plt.axvline(x=timestamp)
        print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
elif isinstance(y, np.ndarray):
    # numeric data, draw as lines
    y = bt.band_filter(y, np.array(bandpass), 250, order=4)
    #ax1.plot(stream['time_stamps'], y, color="red")
    plt.plot(stream['time_stamps'], y, color="red")
else:
    raise RuntimeError('Unknown stream format')

ax1.set_ylabel("LiveAmp", color="red", fontsize=14)
#ax1.set_ylim()

plt.show()



# Plot EmotiBit EDA 
type_tag = "EA"    
data = []   
file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + type_tag + '.csv'
print(file_path)
data.append(pd.read_csv(file_path))

# Create time segment
# NOTE: this only works for signals with the same sampling rate
t = 0
timestamps = data[t][timestamp_id].to_numpy()

emotibit_eda = bt.band_filter(data[t][type_tag], np.array(bandpass), 15, order=4)
plt.plot(timestamps, emotibit_eda*eb_eda_amp, color="black")
#ax2.plot(timestamps, emotibit_eda, color="black")
ax2.set_ylabel("EmotiBit",  color="black",  fontsize=14)

