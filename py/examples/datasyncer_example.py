# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:06:41 2019

@author: Sean Montgomery <produceconsumerobot@gmail.com>
"""

import emotibit.datasyncer as syncer
import matplotlib.pyplot as plt
import locale
import numpy
import time
import emotibit.flexcompparser as flexcomp
my_syncer = syncer.DataSyncer()

# Load EmotiBit data
file_dir0 = "C:/priv/local/LocalDev/Sean/of_v0.9.8_vs_release/apps/CFL_SW_BiosensorModule/EmotiBitDataParser/Participant 00013/EmotiBit"
file_base = "2019-05-24_14-25-39-507"
file_ext = ".csv"
data_types = ["PI"]
file_names0 = []
for data_type in data_types:
    file_names0.append(file_base + "_" + data_type + file_ext)
data_col0 = 7
data_start_row1 = 2
myLocale = locale.getlocale() # Store current locale
locale.setlocale(locale.LC_NUMERIC, 'USA') # Switch to new locale to process file
my_syncer.load_data(file_dir0, file_names0, data_col0)
locale.setlocale(locale.LC_NUMERIC, myLocale) # Set locale back to orignal
print("Data0.len = " + str(len(my_syncer.time_series[0].data)))
#9 May 2019 14:02:01 - 00:11:07,813 = 13:50:53.187 = 1557424253.187
# 1557409853.187 + 4*60*60 = 1557424253.187
#my_syncer.time_series[0].timestamp = numpy.subtract(my_syncer.time_series[0].timestamp, 0)
#my_syncer.time_series[1].timestamp = numpy.subtract(my_syncer.time_series[1].timestamp, 0)

# Load Flexcomp data
# ToDo: Utilize flexcompparser to handle more mundane settings
FLEXCOMP_TIME = 0
FLEXCOMP_EKG = 1
FLEXCOMP_BVP = 2
FLEXCOMP_SC = 5
file_dir1 = "C:/priv/local/LocalDev/Sean/of_v0.9.8_vs_release/apps/CFL_SW_BiosensorModule/EmotiBitDataParser/Participant 00013/Flex comp"
file_name1 = "ID_00013_exp_10min_rest_1_2019-05-24_1437.txt"
data_cols1 = [FLEXCOMP_BVP] #, FLEXCOMP_SC]
timestamp_col1 = FLEXCOMP_TIME
data_start_row1 = 8
delimiter1 = ';'
myLocale = locale.getlocale() # Store current locale
locale.setlocale(locale.LC_NUMERIC, 'French_Canada.1252') # Switch to new locale to process file
my_syncer.load_data(file_dir1, file_name1, data_cols1, timestamp_col1, data_start_row1, delimiter1)
locale.setlocale(locale.LC_NUMERIC, myLocale) # Set locale back to orignal
my_flexcomp_parser = flexcomp.Parser(file_dir1 + "/" + file_name1)
my_syncer.time_series[1].timestamp = numpy.add(my_syncer.time_series[1].timestamp, my_flexcomp_parser.get_start_epoch())
#my_syncer.time_series[3].timestamp = numpy.add(my_syncer.time_series[3].timestamp, session_epoch - end_epoch)


# Plot histogram of timestamps
my_syncer.plot_timestamp_hist()
# Select sync times
my_syncer.select_sync_times()

#while (1):
#    m = plt.ginput(1);
#    print(m)

if (0):
    points = plt.ginput(2)
    diff = points[0][0] - points[1][0]
    print(str(points[0][0]) + " - " + str(points[1][0]) + " = " + str(diff))

