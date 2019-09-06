# -*- coding: utf-8 -*-
"""
Created on Wed May 22 21:41:48 2019

@author: produceconsumerobot
"""

import time

date_time = '09.05.2019 13:50:53'
pattern = '%d.%m.%Y %H:%M:%S'
epoch = int(time.mktime(time.strptime(date_time, pattern)))
print(epoch)
