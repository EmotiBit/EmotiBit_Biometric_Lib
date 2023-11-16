# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 09:21:07 2023

@author: consu
"""

import emotibit.signal as ebsig
import numpy as np
import pandas as pd
import scipy.signal as scisig
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

try:
    import IPython
    IPython.get_ipython().magic("matplotlib qt")
except:
    plt.ion()

def butter_lowpass_filter(data, fc, fs, order=4):
    # Source: https://github.com/guillaume-chevalier/filtering-stft-and-laplace-transform
    w = fc / (fs / 2) # Normalize the frequency
    b, a = scisig.butter(5, w, 'low')
    y = scisig.filtfilt(b, a, data)
    return y


# **** Enter parameters here **** 
# Removing data directories with super short recordings and no LSL Markers
data_dirs = [
    #r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Mike/2023-04-16_11-51-49-659678',
    r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Mike/2023-04-16_15-42-05-608122',
    r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Mike/2023-04-16_16-20-45-696359',
    #r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Bob/2023-04-16_11-50-07-982348',
    r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Bob/2023-04-16_15-42-28-096912',
    #r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Jared/2023-04-16_11-47-34-166828',
    #r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Jared/2023-04-16_11-47-48-309342',
    r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Jared/2023-04-16_15-53-49-307046',
    r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Jared/2023-04-16_16-21-18-728199',
    #r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/John/2023-04-16_11-50-45-628347',
    r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/John/2023-04-16_15-43-36-324819',
    r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/John/2023-04-16_16-21-22-226004',
    #r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Diane/2023-04-16_11-49-17-193487',
    r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Diane/2023-04-16_15-46-43-622974',
    ]

people = [
    {
     'name':'Mike',
     'plot_color':'r'
     },
    {
     'name':'Bob',
     'plot_color':'b'
     },
    {
     'name':'Jared',
     'plot_color':'g'
     },
    {
     'name':'John',
     'plot_color':'k'
     },
    {
     'name':'Diane',
     'plot_color':'m'
     }
    ]

#data_dir = r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Mike/'
#data_file_base = '2023-04-16_15-42-05-608122'
data_typetag = 'D0'
ref_typetag = 'EA'
fs = 15
# cuttoff and threshold determined to result in ~1 minute window
#cutoff_freq = 0.33
cutoff_freq = 0.05
threshold = cutoff_freq / 7.5
output_typetag = 'D0_filt' + str(cutoff_freq) + 'Hz' + '_th' + str(threshold)
t_col_name = "LslMarkerSourceTimestamp"
t_start = 405670
t_end = 410600
# **** End parameters **** 

# Global variables 
t_starts = []
t_ends = []
# End global variables 

# Find beginning and end times of all files
if t_start < 0 or t_end < 0:
    for temp_dir in data_dirs:
        data_dir, data_file_base = temp_dir.rsplit('/', 1)
        ref_file_path = data_dir + '/' + data_file_base + '/' + data_file_base + '_' + ref_typetag + '.csv'
        temp = pd.read_csv(ref_file_path)
        t_starts.append(temp.loc[0, t_col_name])
        t_ends.append(temp.loc[len(temp) - 1, t_col_name])
    
if t_start < 0:
    t_starts = np.array(t_starts)
    t_start = min(t_starts[t_starts > 0])
if t_end < 0:
    t_ends = np.array(t_ends)
    t_end = max(t_ends[t_ends > 0])

# Cycle through all data files to create coincidence sum 
fig1, axes1 = plt.subplots(len(people),1,sharex=True)
#ax1.clear()
coin_sum = np.array([])
per_data = []
for temp_dir in data_dirs:
    data_dir, person, data_file_base = temp_dir.rsplit('/', 2)
    plot_color = ''
    person_ind = -1
    temp_ind = -1
    for p in people:
        temp_ind = temp_ind + 1
        if p['name'] == person:
            person_ind = temp_ind
            plot_color = p['plot_color']
    if person_ind >= 0:
        data_file_path = data_dir + '/' + person  + '/' + data_file_base+ '/' + data_file_base + '_' + data_typetag + '.csv'
        data = pd.read_csv(data_file_path)
        
        per_data.append(ebsig.periodize(data,t_col_name,fs,t_start,0,t_end))
        
for i in len(per_data):
    press = np.diff(per_data[i][data_typetag])
    
        
        output_df = ebsig.periodize(data,t_col_name,fs,t_start,0,t_end)
        
        temp2 = output_df[data_typetag]
        axes1[person_ind].plot(output_df[t_col_name], temp2, color='gold')
        temp2 = butter_lowpass_filter(temp2, cutoff_freq, fs, order=1)
        axes1[person_ind].plot(output_df[t_col_name], temp2, color='orange')
        temp2 = (temp2 > threshold )* 1
        axes1[person_ind].plot(output_df[t_col_name], temp2, color=plot_color, label=person)
        #output_df[data_typetag] = temp2
        if (len(coin_sum) == 0):
            coin_sum = temp2
        else:
            coin_sum = coin_sum + temp2
            
    #output_file_path = data_dir + data_file_base + '/' + data_file_base + '_' + output_typetag + '.csv'
    #output_df.to_csv(output_file_path, index=False)
            




plt.plot(coin_sum, linestyle=(0, (1, 10)), marker='*', color='gray', label='multi-flow')
ax1.set_ylim([-0.1, max(coin_sum) + 0.1])
ax1.legend()
plt.title('Pedal-presses: ' + output_typetag)

coin_hist_w, coin_hist_b = np.histogram(coin_sum, bins=max(coin_sum)+1, range=[-.5, max(coin_sum)+0.5])
coin_hist_w = coin_hist_w / fs / 60
#plt.figure(2)
ax2 = plt.subplot(2,1,2)
ax2.clear()
plt.plot(coin_hist_b[1:]-0.5, coin_hist_w, linestyle=(0, (1, 10)), marker='*', color='gray')
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
#plt.hist(coin_hist_b[:-1], coin_hist_b, weights=coin_hist_w)
#plt.title('Minutes of pedal-press coincidence')
plt.xlabel('# of people simultaneously pressing pedal')
plt.ylabel('minutes')


    #output_file_path = data_dir + data_file_base + '/' + data_file_base + '_' + output_typetag + '.csv'
    #output_df.to_csv(output_file_path, index=False)
