#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: pam
"""
    
import sys
from device_tapdetector import load_data  

# Specify the file path and timestamp header
file_path = r'C:\Users\pam\CFL_Data\2023-09-29_11-20-15-348181_AX.csv'
#file_dir = r"C:\priv\myDir"
timestamp_header = 'LocalTimestamp'

# Call the load_data function
timestamps, data_values = load_data(file_path, timestamp_header)

# Print or use the loaded data as needed
print("Timestamps:", timestamps)
print("Data Values:", data_values)
    