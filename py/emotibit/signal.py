# -*- coding: utf-8 -*-
"""
@package signal
Signal processing module for EmotiBit

@author: consu
"""

import numpy as np
import pandas as pd
import scipy.signal as scisig


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
        val = float('nan')
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
            
def butter_lowpass(cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a lowpass filter

    Args:
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        b, a ([nbarray, nbarray]): Numerator (b) and denominator (a) polynomials of the IIR filter.
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    #b, a = butter(order, normal_cutoff, btype='low', analog=False)
    b, a = scisig.bessel(order, normal_cutoff, btype='lowpass', analog=False, norm='delay')
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a lowpass filter

    Args:
        data (array): Data to filter
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        y, group_delay ([nbarray, nbarray]): The output of the digital filter and the group_delay of the filter.
    """
    b, a = butter_lowpass(cutoff, fs, order=order)
    #b, a = signal.bessel(cutoff, fs, 'low', order=order, analog=True, norm='delay')
    w, h = scisig.freqz(b, a, fs=fs)
    #print(w)
    group_delay = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
    y = scisig.lfilter(b, a, data)
    return y, group_delay

def lowpass_filter(data, cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a lowpass filter

    Args:
        data (array): Data to filter
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        dataf (nbarray): The filtered data.
    """
    y, gd1 = butter_lowpass_filter(data, cutoff, fs, order)
    #print(gd1)
    delay = np.int(np.round(gd1[np.int(cutoff.mean()/((fs/2.0)/511.0))]))
    #print(delay)
    dataf = np.zeros(data.shape)
    dataf[0:dataf.shape[0]-delay] = y[delay:]
    
    return dataf

def butter_bandpass(cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a bandpass filter

    Args:
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        b, a ([nbarray, nbarray]): Numerator (b) and denominator (a) polynomials of the IIR filter.
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scisig.bessel(order, normal_cutoff, btype='bandpass', analog=False, norm='delay')
    return b, a

def butter_bandpass_filter(data, cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a bandpass filter

    Args:
        data (array): Data to filter
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        y, group_delay ([nbarray, nbarray]): The output of the digital filter and the group_delay of the filter.
    """
    b, a = butter_bandpass(cutoff, fs, order=order)
    w, h = scisig.freqz(b, a, fs=fs)
    group_delay = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
    y = scisig.lfilter(b, a, data)
    return y, group_delay

def band_filter(data, cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a bandpass filter

    Args:
        data (array): Data to filter
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        dataf (nbarray): The filtered data.
    """
    y, gd1 = butter_bandpass_filter(data, cutoff, fs, order)
    delay = int(np.round(gd1[int(cutoff.mean()/((fs/2.0)/511.0))]))
    dataf = np.zeros(data.shape)
    dataf[0:dataf.shape[0]-delay] = y[delay:]
    
    return dataf  

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]

def interp_nan(y):
    """Interpolation for nan values

    Args:
        y (nbarray): Array containing nan values

    Returns:
        y (nbarray): Corrected array
    """
    nans, x = nan_helper(y)
    y[nans] = np.interp(x(nans), x(~nans), y[~nans])

    return y

def zero_mean(signal):
    """Convert data to zero mean and unit variance 

    Args:
        signal (nbarray) : Signal to convert

    Returns
        unit (array): Signal converted
    """
    unit = (signal - signal.mean())/signal.std()
    
    return unit    