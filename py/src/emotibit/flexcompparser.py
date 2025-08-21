# -*- coding: utf-8 -*-
"""
Created on Tue May 28 16:50:21 2019

@author: Sean Montgomery <produceconsumerobot@gmail.com>
"""

__version__ = '0.0.1'

#import csv
import time

class Parser:
    
    session_date_time_row = 4
    start_end_time_row = 5
    date_pattern = "%Y-%m-%d"
    time_pattern = "%H:%M:%S,%f"
    
    session_date = ""
    session_time = ""
    start_time = ""
    end_time = ""
    
    def __init__(self, file_path):
        with open(file_path) as f:
            i = 1
            while(i < self.session_date_time_row):
                tmp = f.readline()
                #print(tmp)
                i += 1
                
            session_date_time = f.readline()
            splt = session_date_time.split(" ")
            #print(splt)
            
            splt2 = splt[2].split("\t")
            #print(splt2)
            self.session_date = splt2[0]
            print("Session Date: " + self.session_date)  
            
            splt2 = splt[4].split("\n")
            #print(splt2)
            self.session_time = splt2[0]
            print("Session Time: " + self.session_time)
            

            i += 1
            while(i < self.start_end_time_row):
                tmp = f.readline()
                #print(tmp)
                i += 1
            start_end_time = f.readline()
            #print(start_end_time)
            splt = start_end_time.split(" ")
            splt2 = splt[4].split("\n")
            self.end_time = splt2[0]
            print("End Time: " + self.end_time)
    
    def get_session_epoch(self):
        return time.mktime(time.strptime(self.session_date + " " + self.session_time + ",000", self.date_pattern + " " + self.time_pattern))

    def get_end_epoch(self):
        end_float = self.end_time.split(",")
        return time.mktime(time.strptime("1970-01-01 " + self.end_time + "000", self.date_pattern + " " + self.time_pattern)) + float(end_float[1])/1000 - time.mktime(time.gmtime(0))
    
    def get_start_epoch(self):
        return self.get_session_epoch() - self.get_end_epoch()

    