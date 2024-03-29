# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 06:16:03 2022

@author: consu
"""

import numpy as np
import pandas as pd
import emotibit.info as info
import emotibit.utils as utils

data_type_tags = ["AX","AY","AZ","EA"]
data_min_threshes = [-7, -7, -7, 0]
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
    "2022-07-15_04-38-31-568274",\
    "2022-07-15_04-38-33-566755",\
    "2022-07-18_16-32-31-833549",\
    "2022-07-18_16-37-26-372411",\
    "2022-07-18_18-09-54-431729",\
    "2022-07-19_19-17-42-312824",\
    "2022-07-19_19-18-28-537625",\
    "2022-07-19_19-19-16-295558"\

 ]
    
timestamp_header = "LocalTimestamp"

print_info = True
print_user_notes = True

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
    wonkout_type_tag = ""
    noise_battery = - 1
    final_battery = battery_data[battery_type_tag][len(battery_data[battery_type_tag]) - 1]
    final_batt_time = battery_data[timestamp_header][len(battery_data[timestamp_header]) - 1]
    starting_battery = battery_data[battery_type_tag][1]
    first_timestamp = battery_data[timestamp_header][1]
    
    for d in range(len(data_type_tags)):
        data_type_tag = data_type_tags[d]
        data_min_thresh = data_min_threshes[d]
        
        file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + data_type_tag + '.csv'
        data = pd.read_csv(file_path);
        final_data_time = data[timestamp_header][len(data[timestamp_header]) - 1]
        
        # Check for missing parsed data
        if (abs(final_data_time - final_batt_time) > 5):
            print("\n")
            print("ERROR: data file durations don't match")
            print(battery_type_tag + ": " + str(final_batt_time))
            print(data_type_tag + ": " + str(final_data_time))
            exit(-1)
        
        clip_indexes = np.where(data[data_type_tag] < data_min_thresh)
        if (len(clip_indexes[0]) > 0):
            if (first_clip_time == -1):
                first_clip_time = data[timestamp_header][clip_indexes[0][0]]
                wonkout_type_tag = data_type_tag
            else:
                if (first_clip_time > data[timestamp_header][clip_indexes[0][0]]):
                    first_clip_time = data[timestamp_header][clip_indexes[0][0]]
                    wonkout_type_tag = data_type_tag            
            
            clean_runtime = round((first_clip_time - first_timestamp)/60/60,2)
            
            battery_indexes = np.where(battery_data[timestamp_header] > first_clip_time)
            if (len(battery_indexes[0]) > 0):
                noise_battery = battery_data[battery_type_tag][battery_indexes[0][0]]
                
    print("Total runtime (h) = " + str(total_runtime))   
    print("First wonkout time = " + str(first_clip_time))
    print("Runtime at first wonkout (h) = " + str(clean_runtime))       
    print("First wonkout battery level = " + str(noise_battery))
    print("Final battery level = " + str(final_battery))
    print("Starting battery level = " + str(starting_battery))
    print("Wonkout TypeTag = " + str(wonkout_type_tag))
    result = file_base \
        + ", " + str(total_runtime) \
        + ", " + str(first_clip_time) \
        + ", " + str(clean_runtime) \
        + ", " + str(noise_battery) \
        + ", " + str(final_battery) \
        + ", " + str(starting_battery) \
        + ", " + str(wonkout_type_tag)
    all_results.append(result)
    print(result)
    
if (print_info):
    print("")
    print("************")
    print("Info:")
    info.print_info(file_dir, file_base_names)
    
if (print_user_notes):
    print("")
    print("************")
    print("User Notes:")
    utils.print_user_notes(file_dir, file_base_names, ', ')

print("")
print("************")
print("All Results:")
for result in all_results:
    print(result)
            
        
        
    
    
    