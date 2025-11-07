"""
Created on Tue July 7 2019

@author: Marie-Eve Bilodeau <marie-eve.bilodeau.1@etsmtl.net>
"""

__version__ = '0.0.2'


import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

class DataRealigner:
    
    timestamp = []
    data = []

    def __init__(self):
        self.timestamp = []
        self.data = []        

    def load_data(self, timestamp0, data0, timestamp1, data1):
        """ Load data from array
        """
        self.timestamp.append(timestamp0)
        self.timestamp.append(timestamp1)	
        self.data.append(data0)	
        self.data.append(data1)

    def match_data_sets(self, invert):
        """ Remove DC and match amplitude
        """
        mean_y0 = np.mean(self.data[0])
        mean_y1 = np.mean(self.data[1])
        self.data[0] = np.subtract(self.data[0], mean_y0)
        self.data[1] = np.subtract(self.data[1], mean_y1)
        amp_y0 = np.amax(self.data[0]) - np.amin(self.data[0])
        amp_y1 = np.amax(self.data[1]) - np.amin(self.data[1])
        amp = amp_y1/amp_y0
        self.data[1] = np.divide(self.data[1], amp)
        if invert:
            self.data[1] = -self.data[1]

    def get_data_subsections(self, x, y, start, stop):
        """ Get subsection a data from start to stop time
        """
        id = [i for i in range(len(x)) if stop>=x[i]>=start]
        sub_x = [x[i] for i in id] 
        sub_y = [y[i] for i in id] 
        return sub_x, sub_y
	
    def spline_subsections(self, start, stop):
        """ Make a spline interpolation on given subsection
        """
        x0_new, y0_new = self.get_data_subsections(self.timestamp[0], self.data[0], start, stop)
        x1_new, y1_new = self.get_data_subsections(self.timestamp[1], self.data[1], start, stop)
        tck = interpolate.splrep(x1_new, y1_new, s=0)
        x1_new = x0_new
        y1_new = interpolate.splev(x1_new, tck, der=0)
        return x0_new, y0_new, x1_new, y1_new

    def get_delay_correlation(self, y0, y1, max_delay): 
        """ Get correlation between y0 and each delayed y1
            return the max correlation and its delayed id
        """
        delay_correlation = []
        for n in range(1, max_delay):
            delay_correlation.append(sum(np.array(y0[0:-n])*np.array(y1[n:])))
        max_correlation = np.amax(delay_correlation)
        id = [i for i in range(len(delay_correlation)) if delay_correlation[i]>=max_correlation]
        return max_correlation, id

    def get_delay(self, spline_start_time, spline_stop_time, max_delay, srate):
        """ Get max correlation of positive and negative delay
            return the delay in seconds
        """
        x0, y0, x1, y1 = self.spline_subsections(spline_start_time, spline_stop_time)
        max_neg, id_neg = self.get_delay_correlation(y0, y1, max_delay*srate)
        max_pos, id_pos = self.get_delay_correlation(y1, y0, max_delay*srate)
        max_correlation=np.amax([max_neg,max_pos])
        if max_correlation == max_neg:
            # Data 2 needs to be moved backward
            delay = -id_neg[0]/srate
        else:
            # Data 2 needs to be moved foward
            delay = id_pos[0]/srate
        return delay
		

    def realign_data(self, delay):
        """ Realign data1 with a given delay, match both data starting a ending time
        """
        self.timestamp[1] = np.add(self.timestamp[1], delay)
        start = np.amax([self.timestamp[0][0],self.timestamp[1][0]])
        stop = np.amin([self.timestamp[0][-1],self.timestamp[1][-1]])
        self.timestamp[0], self.data[0] = self.get_data_subsections(self.timestamp[0], self.data[0], start, stop)
        self.timestamp[1], self.data[1] = self.get_data_subsections(self.timestamp[1], self.data[1], start, stop)
   
    def get_delay_and_realign_data(self, spline_start_time,spline_stop_time, max_delay, srate):
        delay = self.get_delay(spline_start_time, spline_stop_time, max_delay, srate)
        self.realign_data(delay)
        return delay
    
    def upsample_emo_at_flex(self):
        """
            Upsample Emotibit Data at Flexcomp Timestamp
        """
        start = np.amax([self.timestamp[0][0],self.timestamp[1][0]])
        stop = np.amin([self.timestamp[0][-1],self.timestamp[1][-1]])
        self.timestamp[0], self.data[0], self.timestamp[1], self.data[1] = self.spline_subsections(start, stop)
        
    def downsample(self, start, stop):
        """ Make a spline interpolation at x1 sampling rate on given subsection
        """
        
        x0_new, y0_new = self.get_data_subsections(self.timestamp[0], self.data[0], start, stop)
        x1_new, y1_new = self.get_data_subsections(self.timestamp[1], self.data[1], start, stop)
        tck = interpolate.splrep(x0_new, y0_new, s=0)
        x0_new = x1_new
        y0_new = interpolate.splev(x0_new, tck, der=0)
        return x0_new, y0_new, x1_new, y1_new
            
    def downsample_flex_at_emo(self):
        """
             Downsample Flexcomp Data at Emotibit Timestamp
        """
        start = np.amax([self.timestamp[0][0],self.timestamp[1][0]])
        stop = np.amin([self.timestamp[0][-1],self.timestamp[1][-1]])
        self.timestamp[0], self.data[0], self.timestamp[1], self.data[1] = self.downsample(start, stop)