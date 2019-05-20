# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:06:41 2019

@author: smmontgom
"""

import emotibit.datasyncer as syncer
import matplotlib.pyplot as plt
my_syncer = syncer.DataSyncer()

# Load EmotiBit data
file_dir0 = "C:/priv/gd/Dropbox/CFL/RiskSensor/Data_EmotiBit/Validation study_PPG_EDA/Participant 0007/EmotiBit"
file_name0 = "2019-05-10_09-11-40-723.csv_PI.csv"
data_col0 = 6
my_syncer.load_data(file_dir0, file_name0, data_col0)
print("Data0.len = " + str(len(my_syncer.time_series[0].data)))

# Load Flexcomp data
FLEXCOMP_TIME = 0
FLEXCOMP_EKG = 1
FLEXCOMP_BVP = 2
FLEXCOMP_SC = 5
file_dir1 = "C:/priv/gd/Dropbox/CFL/RiskSensor/Data_EmotiBit/Validation study_PPG_EDA/Participant 0007/Flexcomp"
file_name1 = "ID_0007_exp_10min_rest_2_2019-05-10_0938.txt"
data_col1 = FLEXCOMP_BVP
timestamp_col1 = FLEXCOMP_TIME
data_start_row1 = 8
delimiter1 = ';'
#decimal = '.'
import locale
myLocale = locale.getlocale()
locale.setlocale(locale.LC_NUMERIC, 'French_Canada.1252')
my_syncer.load_data(file_dir1, file_name1, data_col1, timestamp_col1, data_start_row1, delimiter1)
locale.setlocale(locale.LC_NUMERIC, myLocale)

print("Data0.len = " + str(len(my_syncer.time_series[0].data)))
print("Data1.len = " + str(len(my_syncer.time_series[1].data)))


# Plot histogram of timestamps
my_syncer.plot_timestamp_hist()
# Select sync times
my_syncer.select_sync_times()

