# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:06:41 2019

@author: smmontgom
"""

import emotibit.datasyncer as syncer
import matplotlib.pyplot as plt
import locale
import numpy
import time
my_syncer = syncer.DataSyncer()

# Load EmotiBit data
file_dir0 = "C:/priv/local/LocalDev/Sean/of_v0.9.8_vs_release/apps/CFL_SW_BiosensorModule/EmotiBitDataParser/bin/data/Newfolder"
file_base = "2019-05-23_23-51-46-531_"
file_ext = ".csv"
data_types = ["H0", "EA", "AX"]
file_names0 = []
for data_type in data_types:
    file_names0.append(file_base + data_type + file_ext)
data_col0 = 7
data_start_row1 = 2
myLocale = locale.getlocale() # Store current locale
locale.setlocale(locale.LC_NUMERIC, 'USA') # Switch to new locale to process file
my_syncer.load_data(file_dir0, file_names0, data_col0)
locale.setlocale(locale.LC_NUMERIC, myLocale) # Set locale back to orignal
print("Data0.len = " + str(len(my_syncer.time_series[0].data)))
#9 May 2019 14:02:01 - 00:11:07,813 = 13:50:53.187 = 1557424253.187
# 1557409853.187 + 4*60*60 = 1557424253.187
my_syncer.time_series[0].timestamp = numpy.subtract(my_syncer.time_series[0].timestamp, 0)
my_syncer.time_series[1].timestamp = numpy.subtract(my_syncer.time_series[1].timestamp, 0)

# Load Flexcomp data
FLEXCOMP_TIME = 0
FLEXCOMP_EKG = 1
FLEXCOMP_BVP = 2
FLEXCOMP_SC = 5
file_dir1 = "C:/priv/gd/Dropbox/CFL/RiskSensor/Data_EmotiBit/Validation study_PPG_EDA/Participant 0006/Flexcomp"
file_name1 = "ID_0006_exp_10min_rest_1_2019-05-09_1410_1425.txt"
data_cols1 = [] # [FLEXCOMP_BVP, FLEXCOMP_SC]
timestamp_col1 = FLEXCOMP_TIME
data_start_row1 = 8
delimiter1 = ';'
myLocale = locale.getlocale() # Store current locale
locale.setlocale(locale.LC_NUMERIC, 'French_Canada.1252') # Switch to new locale to process file
my_syncer.load_data(file_dir1, file_name1, data_cols1, timestamp_col1, data_start_row1, delimiter1)
locale.setlocale(locale.LC_NUMERIC, myLocale) # Set locale back to orignal

print("Data0.len = " + str(len(my_syncer.time_series[0].data)))
print("Data1.len = " + str(len(my_syncer.time_series[1].data)))

session_date = "2019-05-09"
session_time = "14:25:06"
end_time = "00:10:39,000"
date_pattern = "%Y-%m-%d"
time_pattern = "%H:%M:%S,%f"
end_float = end_time.split(",")
session_epoch = time.mktime(time.strptime(session_date + " " + session_time + ",000", date_pattern + " " + time_pattern))
end_epoch = time.mktime(time.strptime("1970-01-01 " + end_time + "000", date_pattern + " " + time_pattern)) + float(end_float[1])/1000 - time.mktime(time.gmtime(0))
print(session_epoch - end_epoch)
#my_syncer.time_series[2].timestamp = numpy.add(my_syncer.time_series[2].timestamp, session_epoch - end_epoch)
#my_syncer.time_series[3].timestamp = numpy.add(my_syncer.time_series[3].timestamp, session_epoch - end_epoch)


# Plot histogram of timestamps
my_syncer.plot_timestamp_hist()
# Select sync times
my_syncer.select_sync_times()

