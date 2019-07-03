"""
Created on Tue June 25 2019

@author: Marie-Eve Bilodeau marie-eve.bilodeau.1@etsmtl.net
"""

import emotibit.datasyncer as syncer
import matplotlib.pyplot as plt
import locale
import numpy
import emotibit.datarealigner as realign

my_syncer = syncer.DataSyncer()
my_realigner = realign.DataRealigner()

def get_data_from_datasyncer():

    # As per datasyncer example
    # Load EmotiBit data 
    file_dir0 = "C:/Users/marie/Documents/Maîtrise/Emotibit/Validation study PPG_EDA/Participant 00013/Golden_p13/p13_data"
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
    #print("Data0 = ", my_syncer.time_series[0].data)
    #print("Timestamp0 = ", my_syncer.time_series[0].timestamp)
    my_syncer.time_series[0].timestamp = numpy.subtract(my_syncer.time_series[0].timestamp, numpy.floor(my_syncer.time_series[0].timestamp[0]))

    # Load Flexcomp data
    # ToDo: Utilize flexcompparser to handle more mundane settings
    FLEXCOMP_TIME = 0
    FLEXCOMP_EKG = 1
    FLEXCOMP_BVP = 2
    FLEXCOMP_SC = 5
    file_dir1 = "C:/Users/marie/Documents/Maîtrise/Emotibit/Validation study PPG_EDA/Participant 00013/Golden_p13/p13_data"
    file_name1 = "ID_00013_exp_10min_rest_1_2019-05-24_1437.txt"
    data_cols1 = [FLEXCOMP_BVP] #, FLEXCOMP_SC]
    timestamp_col1 = FLEXCOMP_TIME
    data_start_row1 = 8
    delimiter1 = ';'
    myLocale = locale.getlocale() # Store current locale
    locale.setlocale(locale.LC_NUMERIC, 'French_Canada.1252') # Switch to new locale to process file
    my_syncer.load_data(file_dir1, file_name1, data_cols1, timestamp_col1, data_start_row1, delimiter1)
    locale.setlocale(locale.LC_NUMERIC, myLocale) # Set locale back to orignal

get_data_from_datasyncer()
# Flexcomp first then Emotibit
my_realigner.load_data(my_syncer.time_series[1].timestamp, my_syncer.time_series[1].data, my_syncer.time_series[0].timestamp, my_syncer.time_series[0].data)  
# Remove DC from signal and match amplitude, 
# for PPG data, Inverting the wave can help
INVERT = True
my_realigner.match_data_sets(INVERT)

plt.figure()
plt.title('Before Realignment')
plt.plot(my_realigner.timestamp[0],my_realigner.data[0],'b')
plt.plot(my_realigner.timestamp[1],my_realigner.data[1],'r')
plt.show()

""" 1 minute works well for rest PPG data, for non-rest data take a longer section
    For EDA data, 4 min works well """
SPLINE_START_TIME = 100
SPLINE_STOP_TIME = 160
MAX_DELAY = 30   # align on a delay of max 30 sec
FLEXCOMP_SAMPLING_RATE = 256

delay = my_realigner.get_delay_and_realign_data(SPLINE_START_TIME, SPLINE_STOP_TIME, MAX_DELAY, FLEXCOMP_SAMPLING_RATE)
print(delay)

plt.figure()
plt.title('Realigned Data')
plt.plot(my_realigner.timestamp[0],my_realigner.data[0],'g')
plt.plot(my_realigner.timestamp[1],my_realigner.data[1],'y')
plt.show()
