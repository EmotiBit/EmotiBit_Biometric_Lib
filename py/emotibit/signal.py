# -*- coding: utf-8 -*-
"""
@package signal
Signal processing module for EmotiBit

@author: consu
"""

import numpy as np
import pandas as pd


def periodize(input_df, timestamp_col_name, fs, start_t = None, start_val = None, end_t = None):
    """ Periodizes an aperiodic signal to the passed sampling frequency
    @param input_df data frame with data and timestamp columns
    @param timestamp_col_name column header of timestamps
    @param target sampling rate of output dataframe
    @param start_t optional start time of the periodized output dataframe
    @param start_val optional starting value of the periodized output dataframe
    @param end_t optional end time of the periodized output dataframe
    @return periodized dataframe
    """
    if (len(input_df) == 0):
        return
    val = start_val
    if (start_t == None):
        start_t = input_df.loc[0][timestamp_col_name]
    if (start_val == None):
        val = float('nan');
    if (end_t == None):
        end_t = input_df.loc[len(input_df) - 1][timestamp_col_name]
        
    timestamps = np.arange(start_t, end_t, 1/fs)
    t_col = input_df.columns.get_loc(timestamp_col_name)
    
    ind = 0
    # output_df = pd.DataFrame()
    output_list = []
    for t in timestamps:
        output_list.append(input_df.loc[ind].tolist())
        if (t >= input_df.loc[ind,timestamp_col_name]):
            val = input_df.iloc[ind,-1]
            ind = min(ind + 1, len(input_df)-1)
        l_ind = len(output_list) - 1
        output_list[l_ind][len(output_list[l_ind]) - 1] = val        
        output_list[l_ind][t_col] = t
    
    output_df = pd.DataFrame(output_list, columns = list(input_df.columns))
    return output_df
            
            