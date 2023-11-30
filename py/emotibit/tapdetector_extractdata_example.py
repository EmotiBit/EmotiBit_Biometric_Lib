# -*- coding: utf-8 -*-
"""

@author: pam
"""
import sys
import pandas as pd
from device_tapdetector import extract_data

# Example usage:
file_path = r'C:\Users\pam\CFL_Data\2023-09-29_11-20-15-348181_AX.csv'
#file_dir = r"C:\priv\myDir"
timestamp_header = 'LocalTimestamp'
column_name = 'AX'  

result = extract_data(file_path, timestamp_header, column_name)
print(result)

