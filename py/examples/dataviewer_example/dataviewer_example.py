#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  15 3:06:23 2019

@author: Nitin
"""

# import emotibit.datasyncer as syncer
# import matplotlib.pyplot as plt
# import locale
# import numpy
# import emotibit.flexcompparser as flexcomp
import sys
import emotibit.dataviewer as dataviewer
# sys.path.append('/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/EmotiBit_Biometric_Lib/py')
# my_syncer = syncer.DataSyncer()

# Load EmotiBit data - specify file name and path

file_dir0 = r"C:\Users\nitin\Documents\EmotiBit\DataAnalysis\controlledTest\2019-12-10_11-55-54-038975\dataParsed"
file_base = r"2019-12-10_11-55-54-038975"

# arguments for command line
# usernote_toggle False hide_dc EA,ER

hide_DC_tags = []
userNote_toggle = True
for i, argument in enumerate(sys.argv[1:]):
    if i % 2 == 0:  # even position counting from after file name
        if argument == "hide_dc":
            hide_DC_tags = sys.argv[i+2].split(',')

        elif argument == "usernote_toggle":
            if sys.argv[i+2] == "False":
                userNote_toggle = False

analysis = dataviewer.DataViewer(file_dir0, file_base, hide_DC_tags, userNote_toggle)