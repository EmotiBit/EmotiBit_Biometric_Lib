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

#__filePath0 = ""
#__timestampCol0 = 0
#__dataCol0 = 1
#__filePath1 = ""
#__timestampCol1 = 0
#__dataCol1 = 1
#__outputPath = ""
    
class DataSyncer:
    
    time_series = []
    
    def __init__(self):
        self.time_series = []
        
    
    #class DataType(Enum):
    #    EMOTIBIT = 0
    #    FLEXCOMP_INFINITY = 1
    #    length = 2
        
    #def __init__(self, filePath0, timestampCol0, dataColumn0, filePath1, timestampCol1, dataColumn1, outputPath):
    #    self.__filePath0 = filePath0
    #    self.__timestampCol0 = timestampCol0
    #    self.__dataColumn0 = dataColumn0
    #    self.__filePath1 = filePath1
    #    self.__timestampCol1 = timestampCol1
    #    self.__dataColumn1 = dataColumn1
    #    self.__outputPath = outputPath
    
    def load_data(self, file_dir, file_name, data_col, timestamp_col = 0, data_start_row = 0, delimiter = ","):
        #global time_series
        
    #    if timestamp_col == None:
    #        timestampCol = 0
    #        print("Defaulting to timestamp_col = " + str(timestampCol))
    #    if data_start_row == None:
    #        data_start_row = 0
    #        print("Defaulting to data_start_row = " + str(data_start_row))
    #    if delimiter == None:
    #        delimiter = ','
    #        print("Defaulting to delimiter = " + str(delimiter))
            
        last_index = len(self.time_series)
        
        self.time_series.append(TimeSeries())
        counter = 0
        filePath = file_dir + "/" + file_name
        print("Loading data into time_series[" + str(last_index) + "] from " + filePath)
        with open(filePath, newline='') as csvfile:
             dataReader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
             for row in dataReader:
                 if(counter >= data_start_row and len(row) > timestamp_col and len(row) > data_col and not row[timestamp_col].isalpha()):
                     try:
                         self.time_series[last_index].timestamp.append(float(row[timestamp_col]))
                         self.time_series[last_index].data.append(float(row[data_col]))
                     except ValueError:
                         print(str(counter) + row[timestamp_col] + ", " + row[data_col])
                 else:                 
                     print("**** Skipping row " + str(counter) + " ****")
                     print(row)
                 counter += 1
    
    #def load_data(fileDir, fileName, dataCol, timestampCol = None, dataStartRow = None, delimiter = None):
    #    global data0
    #    data0 = _load_data(fileDir, fileName, dataCol, timestampCol, dataStartRow, delimiter)
    #    print("Data0.len = " + str(len(data0.data)))
    #    print("Data1.len = " + str(len(data1.data)))
    
    #def load_data_1(fileDir, fileName, dataCol, timestampCol = None, dataStartRow = None, delimiter = None):
    #    global data1
    #    data1 = _load_data(fileDir, fileName, dataCol, timestampCol, dataStartRow, delimiter)
    #    print("Data0.len = " + str(len(data0.data)))
    #    print("Data1.len = " + str(len(data1.data)))
    
    def plot_timestamp_hist(self, nbins=20):
        #global time_series
        fig, axs = plt.subplots(nrows=1, ncols=len(self.time_series), tight_layout=True, num="Timestamp Histogram")
        if (len(self.time_series) > 1):
            for t in range(len(self.time_series)):
                plt.sca(axs[t])
                plt.cla
                axs[t].hist(numpy.diff(self.time_series[t].timestamp), nbins)
        else:
            plt.hist(numpy.diff(self.time_series[0].timestamp), nbins)
    
    
    def test(self):
        print("test worked yay")
