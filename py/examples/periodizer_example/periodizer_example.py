# -*- coding: utf-8 -*-
"""
Basic example using emotibit.signal.periodizer to transform an aperiodic signal
`D0` into a periodic signal to perform filtering and other DSP operations

@author: consu
"""

import emotibit.signal as ebsig
import pandas as pd
import scipy.signal as scisig
import matplotlib.pyplot as plt

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

data_dir = r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Mike/'
data_file_base = '2023-04-16_15-42-05-608122'
data_typetag = 'D0'
ref_typetag = 'EA'
fs = 15
cutoff_freq = 0.33
threshold = cutoff_freq / 2
output_typetag = 'D0_filt' + str(cutoff_freq) + 'Hz' + '_th' + str(threshold)
t_col_name = "LslMarkerSourceTimestamp"


data_file_path = data_dir + data_file_base + '/' + data_file_base + '_' + data_typetag + '.csv'
ref_file_path = data_dir + data_file_base + '/' + data_file_base + '_' + ref_typetag + '.csv'
data = pd.read_csv(data_file_path)
temp = pd.read_csv(ref_file_path)
t_start =  temp.loc[0, t_col_name]
t_end =  temp.loc[len(temp) - 1, t_col_name]

output_df = ebsig.periodize(data,t_col_name,fs,t_start,0,t_end)

temp2 = output_df[data_typetag]
plt.plot(temp2)
temp2 = butter_lowpass_filter(temp2, cutoff_freq, fs, order=1)
plt.plot(temp2)
temp2 = temp2 > (threshold)
plt.plot(temp2)
output_df[data_typetag] = temp2 * 1

output_file_path = data_dir + data_file_base + '/' + data_file_base + '_' + output_typetag + '.csv'
output_df.to_csv(output_file_path, index=False)
