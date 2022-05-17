#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  15 3:06:23 2019

@author: Nitin
"""

import sys
import emotibit.dataviewer as dataviewer

# specify the location of the folder which contains the parsed data
file_dir = r"path/to/parsed/data"  # Ex. C:\Users\dev\data
# specify the base file name of teh parsed data
file_base = r"base-file-name"  # 2019-12-10_11-55-54-038975

# arguments for command line
# usernote_toggle False hide_dc EA,ER

hide_DC_tags = ["EA", "SA", "SR", "SF","PI", "PR", "PG", "HR", "TH", "AX", "AY", "AZ", "GX", "GY", "GZ",
						   "MX", "MY", "MZ", "DC", "DO", "UN"] 
hide_DO = True
userNote_toggle = True
for i, argument in enumerate(sys.argv[1:]):
    if i % 2 == 0:  # even position counting from after file name
        if argument == "hide_dc":
            hide_DC_tags = sys.argv[i+2].split(',')

        elif argument == "usernote_toggle":
            if sys.argv[i+2] == "False":
                userNote_toggle = False

analysis = dataviewer.DataViewer(file_dir, file_base, hide_DC_tags, userNote_toggle, hide_DO)