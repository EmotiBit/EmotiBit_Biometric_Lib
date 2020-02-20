# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 22:19:31 2020

@author: consu
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

type_tags = ['EA']
file_dir = r"C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share (1)\Conferences_Talks\2020-02-14 Duke CS101 Lab\data"
file_base_names = [f.name for f in os.scandir(file_dir) if f.is_dir()]



#for type_tag in type_tags:
#    for f in range(len(file_base_names)):
#        eda_data = pd.read_csv(file_dir +'/' + file_base + '/' + file_base + '_' + type_tag + '.csv');
#        
#  
## Destination path 
#destination = "/home/User/Documents/file.txt"
#
#        file_dir +'/' + file_base + '/' + file_base + '_' + type_tag + '.csv'
    

file_base = file_base_names[0]

for type_tag in type_tags:
    fig_name = type_tag + " original"
    fig = plt.figure(fig_name)
    fig.clf()
    fig, axs = plt.subplots(nrows=len(file_base_names), ncols=2, num=fig_name)
    plt.clf
    for f in range(len(file_base_names)):
    #for f in range(1):
        file_base = file_base_names[f]
        in_file_path = file_dir +'/' + file_base + '/' + file_base + '_' + type_tag + '.csv'
        out_file_path = file_dir +'/' + file_base + '/' + file_base + '_' + type_tag + '_norm.csv'
        
        start_timestamp = 0
        end_timestamp = 0
        
        # Read data to calculate average period
        with open(in_file_path, newline='') as csvfile:
            dataReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            row_counter = 0

            for row in dataReader:
                if (row_counter < 2):
                    print(row)
                    print(row[0])
                if (row_counter == 1):
                    start_timestamp = float(row[0])
                row_counter = row_counter + 1
                end_timestamp = row[0] # update end_timestamp to last read
        file_duration = float(end_timestamp) - start_timestamp
        sampling_period = file_duration / (row_counter - 2)
        
        print(end_timestamp)
        print('Total Duration: ' + str(file_duration))
        print('Sample Count: ' + str(row_counter - 1))
        print('Avg Period: ' + str(sampling_period))
        print('Avg Freq: ' + str(1 / sampling_period))
        print('****')
        
        normalized_data = [];
        # Read data and normalize timestamps
        with open(in_file_path, newline='') as csvfile:
            dataReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            
            row_counter = 0            
            for row in dataReader:
                if (row_counter > 1):
                    row[0] = str(start_timestamp + sampling_period * (row_counter - 1))

                row_counter = row_counter + 1
                normalized_data.append(row)
                
        # Write normalized timestamp data
        with open(out_file_path,'w', newline='') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerows(normalized_data)
#            for row in normalized_data:
#                wr.writerows(row) 
                
            

        
        

        
