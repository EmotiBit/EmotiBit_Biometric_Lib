# -*- coding: utf-8 -*-
"""

@author: pam

This example demonstrates how the extract_data() function found in the tapdetector can be used.
The function is used to extract and organize data from a single file, meaning that is both
reads in the file, but also extracts the desired information from the file.

The result of calling the extract_data() function is a structured array containing the requested data.
For more information about the usage of extract_data(), see the function definition in tapdetector.py
"""
from tapdetector import extract_data

# Example usage:
file_path = r'C:\Users\pam\CFL_Data\2023-09-29_11-20-15-348181_AX.csv'
timestamp_header = 'LocalTimestamp'
column_name = 'AX'  

result = extract_data(file_path, timestamp_header, column_name)
print(result)