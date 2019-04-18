# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:06:41 2019

@author: smmontgom
"""

import emotibit.datasyncer as syncer
import matplotlib.pyplot as plt
my_syncer = syncer.DataSyncer()

# Load EmotiBit data
file_dir0 = "C:\priv\gd2\Dropbox\CFL\RiskSensor\Data_EmotiBit\Data EmotiBit vs Flexcomp\Pretest\Participant_0004\EmotiBit"
file_name0 = "2019-02-13_10-30-58-576.csv_PI.csv"
data_col0 = 6
my_syncer.load_data(file_dir0, file_name0, data_col0)
print("Data0.len = " + str(len(my_syncer.time_series[0].data)))

# Load Flexcomp data
file_dir1 = "C:\priv\gd2\Dropbox\CFL\RiskSensor\Data_EmotiBit\Data EmotiBit vs Flexcomp\Pretest\Participant_0004\Flexcompinfinity"
file_name1 = "ID0004_test_2019-02-13_1030_1059_form.csv"
data_col1 = 1
timestamp_col1 = 0
data_start_row1 = 3
delimiter1 = ';'
my_syncer.load_data(file_dir1, file_name1, data_col1, timestamp_col1, data_start_row1, delimiter1)

print("Data0.len = " + str(len(my_syncer.time_series[0].data)))
print("Data1.len = " + str(len(my_syncer.time_series[1].data)))


# Plot histogram of timestamps
my_syncer.plot_timestamp_hist()
# Select sync times
my_syncer.select_sync_times()

