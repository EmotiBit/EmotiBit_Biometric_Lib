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
import dataanalysis as dataanalysis

# my_syncer = syncer.DataSyncer()

# Load EmotiBit data - specify file name and path

####### Bike Ride
# file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/BikeRide-data/2019-08-02_18-42-37-748087/dataParsed"
# file_base = "2019-08-02_18-42-37-748087_bike_ride"

# file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/BikeRide-data/2019-08-07_18-27-36-662165/dataParsed"
# file_base = "2019-08-07_18-27-36-662165_bike_ride"

# file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/BikeRide-data/2019-08-08_08-57-51-136245/dataParsed"
# file_base = "2019-08-08_08-57-51-136245_bike"

# file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/BikeRide-data/2019-08-08_18-48-01-072150/dataParsed"
# file_base = "2019-08-08_18-48-01-072150_bike"

# file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/BikeRide-data/2019-08-12_18-29-32-836054/dataParsed"
# file_base = "2019-08-12_18-29-32-836054_bike"


####### controlled tests
# file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/ControlledTest/2019-08-22_14-10-33-300661/dataParsed"
# file_base = "2019-08-22_14-10-33-300661"

# file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/ControlledTest/2019-08-22_15-37-09-112706/dataParsed"
# file_base = "2019-08-22_15-37-09-112706"

# file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/ControlledTest/2019-08-22_17-09-06-681058/dataParsed"
# file_base = "2019-08-22_17-09-06-681058"

# file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/ControlledTest/2019-08-22_17-35-16-340558/dataParsed"
# file_base = "2019-08-22_17-35-16-340558"

# file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/ControlledTest/2019-08-29_14-09-44-104742/dataParsed"
# file_base = "2019-08-29_14-09-44-104742"

file_dir0 = "/Users/nitin/GoogleDrive/MacBookPro/DocumentsRemote/CFLunpaid/Emotibit/dataAnalysis/ControlledTest/2019-09-06_11-38-52-689420_GSR_SENSITIVITY_BRD06_V01C/dataUnparsed"
file_base = "2019-09-06_11-38-52-689420"

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

analysis = dataanalysis.DataAnalysis(file_dir0, file_base, hide_DC_tags, userNote_toggle)