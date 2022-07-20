# -*- coding: utf-8 -*-
"""
@emotibit info
@brief helper for EmotiBit _info.json 
@example info.print_info(file_dir = r"C:\priv\myDir", 
                            file_base_names = ["2022-06-07_15-23-33-810389"],
                            delim = ",")

Created on Wed Jul 20 06:14:05 2022

@author: consu
"""


import pandas as pd

def print_user_notes(file_dir = "", file_base_names = "", delim = ", "):
    """
    @fn     print_user_notes()
    @brief  batch prints contents of user note (UN) files to console
    @param  file_dir Base directory of the parsed data files
    @param  file_base_names array of file bases of the data files. Expected 
            organization is file_dir/file_base_names[i]/file_base_names[i]_XX.csv
    @param  delim delimiter between notes
    """
    output = ''
       
    for f in range(len(file_base_names)):
        file_base = file_base_names[f]
        file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + 'UN' + '.csv'
        user_notes = pd.read_csv(file_path);
        for note in user_notes['UN']:
            output = output + note + delim
        if (f < len(file_base_names) - 1): # Don't add an extra \n
            output = output + '\n'
    print(output)
        