# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 06:16:03 2022

@author: consu
"""

import numpy as np
import pandas as pd

data_type_tags = ["AX","EA"]
data_min_threshes = [-7, 0.98]
battery_type_tag = "BV"

file_dir = r"C:\priv\local\EmotiBit_Data\ESP32 Test Data 2022-06-27"

file_base_names = [
 "2022-07-18_16-32-31-833549",\
 "2022-07-18_16-37-26-372411",\
 "2022-07-18_18-09-54-431729"\
 ]

timestamp_header = "LocalTimestamp"

all_results = []

for f in range(len(file_base_names)):
    file_base = file_base_names[f]
    print("\n")
    print(file_base)
    file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + battery_type_tag + '.csv'
    battery_data = pd.read_csv(file_path);

    total_runtime = round((battery_data[timestamp_header][len(battery_data[timestamp_header]) - 1] - battery_data[timestamp_header][0])/60/60,2)
    clean_runtime = total_runtime
    first_clip_time = -1
    clip_type_tag = ""
    noise_battery = - 1
    final_battery = battery_data[battery_type_tag][len(battery_data[battery_type_tag]) - 1]
    starting_battery = battery_data[battery_type_tag][1]
    first_timestamp = battery_data[timestamp_header][1]
    
    for d in range(len(data_type_tags)):
        data_type_tag = data_type_tags[d]
        data_min_thresh = data_min_threshes[d]
        
        file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + data_type_tag + '.csv'
        data = pd.read_csv(file_path);
        clip_indexes = np.where(data[data_type_tag] < data_min_thresh)
        if (len(clip_indexes[0]) > 0):
            if (first_clip_time == -1):
                first_clip_time = data[timestamp_header][clip_indexes[0][0]]
                clip_type_tag = data_type_tag
            else:
                if (first_clip_time > data[timestamp_header][clip_indexes[0][0]]):
                    first_clip_time = data[timestamp_header][clip_indexes[0][0]]
                    clip_type_tag = data_type_tag            
            
            clean_runtime = round((first_clip_time - first_timestamp)/60/60,2)
            
            battery_indexes = np.where(battery_data[timestamp_header] > first_clip_time)
            if (len(battery_indexes[0]) > 0):
                noise_battery = battery_data[battery_type_tag][battery_indexes[0][0]]
                
    print("Total runtime (h) = " + str(total_runtime))   
    print("First clip time = " + str(first_clip_time))
    print("Runtime at first clip (h) = " + str(clean_runtime))       
    print("First clip battery level = " + str(noise_battery))
    print("Final battery level = " + str(final_battery))
    print("Starting battery level = " + str(starting_battery))
    print("Clip TypeTag = " + str(clip_type_tag))
    result = file_base \
        + ", " + str(total_runtime) \
        + ", " + str(first_clip_time) \
        + ", " + str(clean_runtime) \
        + ", " + str(noise_battery) \
        + ", " + str(final_battery) \
        + ", " + str(starting_battery) \
        + ", " + str(clip_type_tag)
    all_results.append(result)
    print(result)
print("")
print("All Results:")
for result in all_results:
    print(result)
    

    
            
        
        
    
    
    