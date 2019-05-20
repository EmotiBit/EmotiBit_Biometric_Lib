# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 15:57:57 2019

@author: Sean Montgomery <produceconsumerobot@gmail.com>
"""

#__all__ = ['data0', 'data1', 'load_data_0', 'load_data_1', 'plotTimestampHist']
__version__ = '0.0.1'


import numpy
import csv
import matplotlib.pyplot as plt
import locale
#import pandas as pd
#fileDir = "C:\priv\gd2\Dropbox\CFL\RiskSensor\Data_EmotiBit\Data EmotiBit vs Flexcomp\Pretest\Participant_0005\EmotiBit"
#fileName = "2019-02-14_11-20-53-788.csv_PI.csv"
#a = read(fileDir + fileName)
#print(numpy.array(a[0]))
#plt.plot(numpy.array(a[1]), label='Loaded from file!')


#class datasyncer:
    
class TimeSeries:
    timestamp = []
    data = []   

    def __init__(self):
        self.timestamp = []
        self.data = []

class CsvFileInfo:
    file_dir = None
    file_name = None
    file_path = None
    data_col = 1
    timestamp_col = 0
    data_start_row = 0
    delimiter = ","
    
    def __init__(self):
        self.file_dir = None
        self.file_name = None
        self.file_path = None
        self.data_col = 1
        self.timestamp_col = 0
        self.data_start_row = 0
        self.delimiter = ","
  
class DataSyncer:
    
    time_series = []
    csv_file_info = []
    
    def __init__(self):
        self.time_series = []
        self.csv_file_info = []        
    
    #class DataType(Enum):
    #    EMOTIBIT = 0
    #    FLEXCOMP_INFINITY = 1
    #    length = 2
           
    def load_data(self, file_dirs, file_names, data_cols, timestamp_col = 0, data_start_row = 0, delimiter = ","):
        """Load data from csv file
        """
        if not isinstance(file_dirs, list):
            file_dirs = [file_dirs]
        if not isinstance(file_names, list):
            file_names = [file_names]
        if not isinstance(data_cols, list):
            data_cols = [data_cols]
        for file_dir in file_dirs:    
            for file_name in file_names:
                file_path = file_dir + "/" + file_name
                for data_col in data_cols:
                    # ToDo: improve efficiency by parsing file once for all data_cols
                    last_index = len(self.time_series)
                    self.time_series.append(TimeSeries())
                    self.csv_file_info.append(CsvFileInfo())
                        
                    self.csv_file_info[last_index].file_dir = file_dir
                    self.csv_file_info[last_index].file_name = file_name
                    self.csv_file_info[last_index].file_path = file_path
                    self.csv_file_info[last_index].data_col = data_col
                    self.csv_file_info[last_index].timestamp_col = timestamp_col
                    self.csv_file_info[last_index].data_start_row = data_start_row
                    self.csv_file_info[last_index].delimiter = delimiter
                    
                    dialects = csv.list_dialects()
                    print("csv dialects:")
                    print(*dialects, "\n")
                    counter = 0
                    print("Loading data into time_series[" + str(last_index) + "] from " + file_path)
                    with open(file_path, newline='') as csvfile:
                         dataReader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
                         for row in dataReader:
                             if(counter >= data_start_row and len(row) > timestamp_col and len(row) > data_col and not row[timestamp_col].isalpha()):
                                 try:
                                     self.time_series[last_index].timestamp.append(locale.atof(row[timestamp_col]))
                                     self.time_series[last_index].data.append(locale.atof(row[data_col]))
                                 except ValueError:
                                     print(str(counter) + row[timestamp_col] + ", " + row[data_col])
                             else:                 
                                 print("**** Skipping row " + str(counter) + " ****")
                                 print(row)
                             counter += 1
        
    def plot_timestamp_hist(self, nbins=100):
        """Plot histograms of diff(timestamps)
        """
        #fig, axs = plt.subplots(nrows=1, ncols=len(self.time_series), num="Timestamp Histogram")
        plt.close("Timestamp Histogram")
        fig, axs = plt.subplots(nrows=1, ncols=len(self.time_series), num="Timestamp Histogram")
        fig.set_size_inches([12, 4])
        if (len(self.time_series) > 1):
            for t in range(len(self.time_series)):
                plt.sca(axs[t])
                plt.cla()
                axs[t].hist(numpy.diff(self.time_series[t].timestamp), nbins)
                #print(self.csv_file_info[t].file_name + " col:" + str(self.csv_file_info[t].data_col))
                axs[t].set_title(self.csv_file_info[t].file_name + " col:" + str(self.csv_file_info[t].data_col))
        else:
            plt.hist(numpy.diff(self.time_series[0].timestamp), nbins)
            plt.title(self.csv_file_info[t].file_name + " col:" + str(self.csv_file_info[t].data_col))
        fig.tight_layout()
    
    def select_sync_times(self):
        """Plot data to manually select sync times across data files
        """
        plt.close("Select Sync Times")
        fig, axs = plt.subplots(nrows=len(self.time_series), ncols=1, num="Select Sync Times")
        fig.set_size_inches([14, 7])
        for t in range(len(self.time_series)):
            plt.sca(axs[t])
            plt.cla()
            axs[t].plot(self.time_series[t].timestamp, self.time_series[t].data)
            #print(self.csv_file_info[t].file_name + " col:" + str(self.csv_file_info[t].data_col))
            axs[t].set_title(self.csv_file_info[t].file_name + " col:" + str(self.csv_file_info[t].data_col))
        fig.tight_layout()
    
    def test(self):
        print("test worked yay")
