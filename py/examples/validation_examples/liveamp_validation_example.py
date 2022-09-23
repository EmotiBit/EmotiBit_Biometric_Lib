# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:49:41 2022

@author: consu
"""

import pyxdf
import matplotlib.pyplot as plt
import numpy as np

try:
    import IPython
    IPython.get_ipython().magic("matplotlib qt")
except:
    plt.ion()


file_name = r'C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share\Science\data\measurement sensors\2022-09-21\20220921-2336.xdf'

data, header = pyxdf.load_xdf(file_name)

for stream in data:
    y = stream['time_series']

    if isinstance(y, list):
        # list of strings, draw one vertical line for each marker
        for timestamp, marker in zip(stream['time_stamps'], y):
            plt.axvline(x=timestamp)
            print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
    elif isinstance(y, np.ndarray):
        # numeric data, draw as lines
        plt.plot(stream['time_stamps'], y)
    else:
        raise RuntimeError('Unknown stream format')

plt.show()