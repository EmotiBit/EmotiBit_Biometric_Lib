# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:06:41 2019

@author: smmontgom
"""

import emotibit.datasyncer as syncer
import matplotlib.pyplot as plt
my_syncer = syncer.DataSyncer()

# Load EmotiBit data
file_dir0 = "C:/priv/gd2/Dropbox/CFL/RiskSensor/Data_EmotiBit/Data EmotiBit vs Flexcomp/Pretest/Participant_0001/23april pretests/23april pretests"
file_name0 = "2019-04-23_13-44-09-391.csv_AY.csv"
data_col0 = 6
my_syncer.load_data(file_dir0, file_name0, data_col0)
print("Data0.len = " + str(len(my_syncer.time_series[0].data)))

# Load Flexcomp data
FLEXCOMP_TIME = 0
FLEXCOMP_EKG = 1
FLEXCOMP_BVP = 2
FLECCOMP_SC = 5
file_dir1 = "C:/priv/gd2/Dropbox/CFL/RiskSensor/Data_EmotiBit/Data EmotiBit vs Flexcomp/Pretest/Participant_0001/23april pretests/23april pretests"
file_name1 = "ID 0001_test_2019-04-23_1353_1354_form.csv"
data_col1 = FLEXCOMP_BVP
timestamp_col1 = FLEXCOMP_TIME
data_start_row1 = 3
delimiter1 = ';'
my_syncer.load_data(file_dir1, file_name1, data_col1, timestamp_col1, data_start_row1, delimiter1)

print("Data0.len = " + str(len(my_syncer.time_series[0].data)))
print("Data1.len = " + str(len(my_syncer.time_series[1].data)))


# Plot histogram of timestamps
my_syncer.plot_timestamp_hist()
# Select sync times
my_syncer.select_sync_times()

