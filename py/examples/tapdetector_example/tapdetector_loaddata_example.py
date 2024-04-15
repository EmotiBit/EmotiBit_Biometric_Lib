#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: pam

This example shows how to use the load_data() function found in the tapdetector.
The load_data() function loads the data from a .csv file, and separates the timestamp column from the rest of the data.
The result of calling the function is a numpy array of the timestamps and a pandas data frame of the rest of the data.

For additional information about the function, see the function definition of the file within tapdetector.py
"""
from tapdetector import load_data  

# Specify the file path and timestamp header
file_path = r'C:\Users\pam\CFL_Data\2023-09-29_11-20-15-348181_AX.csv'
timestamp_header = 'LocalTimestamp'

# Call the load_data function
timestamps, data_values = load_data(file_path, timestamp_header)

# Print or use the loaded data as needed
print("Timestamps:", timestamps)
print("Data Values:", data_values)
    