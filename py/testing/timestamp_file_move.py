# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:23:33 2020

@author: consu
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import shutil

type_tags = ['EA']
file_dir = r"C:\priv\gd\Dropbox\CFL\EmotiBit\EmotiBit CFL Share (1)\Conferences_Talks\2020-02-14 Duke CS101 Lab\data"
file_base_names = [f.name for f in os.scandir(file_dir) if f.is_dir()]


for type_tag in type_tags:
    for f in range(len(file_base_names)):
        file_base = file_base_names[f]
        in_file_path = file_dir +'/' + file_base + '/' + file_base + '_' + type_tag + '.csv'
        out_file_path = file_dir +'/' + file_base + '/' + file_base + '_' + type_tag + '_norm.csv'

        source = file_dir + '/' + file_base + '/' + file_base + '_' + type_tag + '.csv'
        destination = file_dir + '/' + file_base + '_' + type_tag + '.csv'
        print('Copying: ' + source + ' to ' + destination)
        shutil.copy(source, destination)  
        
        source = file_dir + '/' + file_base + '/' + file_base + '_' + type_tag + '_norm.csv'
        destination = file_dir + '/' + file_base + '/' + file_base + '_' + type_tag + '.csv'
        print('Moving: ' + source + ' to ' + destination)
        shutil.move(source, destination)  
        print('****')
        
        
        