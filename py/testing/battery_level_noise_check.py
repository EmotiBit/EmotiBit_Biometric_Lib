# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 06:16:03 2022

@author: consu
"""

import numpy as np
import pandas as pd

data_type_tag = "AX"
data_min_thresh = -7
battery_type_tag = "BV"

file_dir = r"C:\priv\local\EmotiBit_Data\ESP32 Test Data 2022-06-27"

file_base_names = [
 "2022-07-07_13-00-39-966600",\
 "2022-07-07_13-12-07-855649",\
 "2022-07-07_15-22-06-628480",\
 "2022-07-07_20-11-30-434677",\
 "2022-07-08_10-16-32-406912",\
 "2022-07-08_18-49-43-185783",\
 "2022-07-11_19-10-29-573358",\
 "2022-07-12_05-26-20-841536",\
 "2022-07-12_16-41-40-227799",\
 "2022-07-13_10-41-48-900345",\
 ]

timestamp_header = "LocalTimestamp"

all_results = []

for f in range(len(file_base_names)):
    file_base = file_base_names[f]
    file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + data_type_tag + '.csv'
    print("\n")
    print(file_base)
    data = pd.read_csv(file_path);
    file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + battery_type_tag + '.csv'
    battery_data = pd.read_csv(file_path);
    
    first_clip_time = -1
    total_runtime = round((data[timestamp_header][len(data[timestamp_header]) - 1] - data[timestamp_header][0])/60/60,2)
    clean_runtime = total_runtime
    first_clip_time = -1
    noise_battery = - 1
    final_battery = battery_data[battery_type_tag][len(battery_data[battery_type_tag]) - 1]
    clip_indexes = np.where(data[data_type_tag] < data_min_thresh)
    if (len(clip_indexes[0]) > 0):
        first_clip_time = data[timestamp_header][clip_indexes[0][0]]
        
        first_timestamp = data[timestamp_header][1]
        clean_runtime = round((first_clip_time - first_timestamp)/60/60,2)
        
        battery_indexes = np.where(battery_data[timestamp_header] > first_clip_time)
        if (len(battery_indexes[0]) > 0):
            noise_battery = battery_data[battery_type_tag][battery_indexes[0][0]]
    print("Total runtime (h) = " + str(total_runtime))   
    print("First clip time = " + str(first_clip_time))
    print("Runtime at first clip (h) = " + str(clean_runtime))       
    print("First clip battery level = " + str(noise_battery))
    print("Final battery level = " + str(final_battery))
    result = file_base + ", " + str(total_runtime) + ", " + str(first_clip_time) + ", " + str(clean_runtime) + ", " + str(noise_battery) + ", " + str(final_battery)
    all_results.append(result)
    print(result)
print("")
print("All Results:")
for result in all_results:
    print(result)
    

    
            
        
        
    
    
    