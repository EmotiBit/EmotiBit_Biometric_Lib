# -*- coding: utf-8 -*-
"""
@emotibit info
@brief helper for EmotiBit _info.json 
@example info.print_info(file_dir = r"C:\priv\myDir", 
                            file_base_names = ["2022-06-07_15-23-33-810389"])

Created on Wed Jul 20 05:43:45 2022

@author: consu
"""

def print_info(file_dir = "", file_base_names = "", print_len = -1):
    """
    @fn     print_info()
    @brief  batch prints EmotiBit _info.json file to console
    @param  file_dir Base directory of the parsed data files
    @param  file_base_names array of file bases of the data files. Expected 
            organization is file_dir/file_base_names[i]/file_base_names[i]_XX.csv
    @param  print_len Max length of each print. -1 = print whole file.
    """
    
    for f in range(len(file_base_names)):
        file_base = file_base_names[f]
        file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + 'info.json'
        with open(file_path) as f:
            contents = f.read()
            if (print_len > -1):
                contents = contents[0:print_len]
            print(contents)
        