# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import os
import sys
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data(file_path, timestamp_header):
    """
    Load data from a file.

    Parameters:
    - file_path: Path to the data file.
    - timestamp_header: The column header for timestamps.

    Returns:
    - timestamps: Numpy array of timestamps.
    - data: Pandas DataFrame containing all data columns.
    """
    data = pd.read_csv(file_path)
    timestamps = data[timestamp_header].to_numpy()
    data_values = data.drop(columns=[timestamp_header])
    return timestamps, data_values

def extract_data(file_path, timestamp_header, column_name, data_column=None):
    """
    Extract and organize data from a single file.

    Parameters:
    - file_path: Path to the data file.
    - timestamp_header: The column header for timestamps.
    - column_name: The column header for the data.
    - data_column: Pandas Series of data associated with the specified column (default: None).

    Returns:
    - data_array: Structured array containing organized data.
    """
    timestamps, data_values = load_data(file_path, timestamp_header)
    localTimes = timestamps.copy()
    # Use the specified data_column if provided, otherwise use the specified column from data_values
    if data_column is not None:
        column_data = data_column.to_numpy()
    else:
        column_data = data_values[column_name].to_numpy()

    # Ensure timestamps_rel and column_data have the same length
    min_length = min(len(timestamps), len(column_data))
    timestamps_rel = timestamps[:min_length]
    column_data = column_data[:min_length]

    # Create time segment
    timestamps_rel -= timestamps_rel[0]

    data_array = np.array([(file_path, timestamps_rel, column_data, localTimes)],
                          dtype=object)
    return data_array

def detectTaps(sourceOneList, sourceTwoList, timeWindow = [0, 50000], height = 0.25):
    """
    Finds the taps for two data sources in n dimensions

    Parameters:
    - sourceOneList: A list of tuples for each dimension of data in the form of [(filepath, timeStampColName, dataColName),(filepath, timeStampColName, dataColName),...]
    - souceTwoList: A list of tuples for each dimension of data in the form of [(filepath, timeStampColName, dataColName),(filepath, timeStampColName, dataColName),...]
    
    Notes:
    - There should be one tuple per dimension of data
    - This function assumes that the first row of each file is the header of the file and the file is in .csv format
    - This function assumes that the number of timestamps from each source is the same for all dimensions from that source
        - i.e. sourceA_AX has the same number of timestamps as sourceB_AY

    Returns:
    - ? - TBD 
    """

    # ensure correct types
    if not isinstance(sourceOneList, list):
        print("Stopping - Error - First parameter should be of type list.")
        return 
    if not isinstance(sourceTwoList, list):
        print("Stopping - Error - Second paramter should be of type list.")
        return
    
    print("=" * 15, " Beginning Tap Detection ", "=" * 15)
    print("Time Window: ", timeWindow)
    print("Height: ", height)
    
    # create single magnitude vector for each file
    sourceOneVec, sourceOneRelTimes, sourceOneLocalTimes = createMagnitudeVectorWithRelTime(sourceOneList)
    sourceTwoVec, sourceTwoRelTimes, sourceTwoLocalTimes = createMagnitudeVectorWithRelTime(sourceTwoList)

    # find the peaks
    sourceOneTapInd, sourceOneTapVal = find_peaks(sourceOneVec[0 : sum(sourceOneRelTimes < timeWindow[1])], height)
    sourceTwoTapInd, sourceTwoTapVal = find_peaks(sourceTwoVec[0 : sum(sourceTwoRelTimes < timeWindow[1])], height)

    # create a mask for the relative times that fits the provided time window (default: [0, 50000])
    time_mask_one = np.where((sourceOneRelTimes > timeWindow[0]) & (sourceOneRelTimes < timeWindow[1]))
    time_mask_two = np.where((sourceTwoRelTimes > timeWindow[0]) & (sourceTwoRelTimes < timeWindow[1]))

    # remove any taps that come before the time window (the after ones are already accounted for when peaks are found)
    sourceOneTapInd = sourceOneTapInd[sourceOneTapInd > time_mask_one[0][0]]
    sourceTwoTapInd = sourceTwoTapInd[sourceTwoTapInd > time_mask_two[0][0]]

    print("***\nTap Indexes for Source One: ", sourceOneTapInd)
    print("***\nRelative Timestamps of Taps for Source One: ", sourceOneRelTimes[sourceOneTapInd])

    print("***\nTap Indexes for Source Two: ", sourceTwoTapInd)
    print("***\nRelative Timestamps of Taps for Source Two: ", sourceTwoRelTimes[sourceTwoTapInd])

    # TODO write taps to file
    print("=" * 15, " Saving Taps to File ", "=" * 15)
    tap_data_one = {'Indexes' : sourceOneTapInd,
                    'RelativeTimeStamp' : sourceOneRelTimes[sourceOneTapInd],
                    'LocalTimeStamp' : sourceOneLocalTimes[sourceOneTapInd],
                    }
    df = pd.DataFrame(tap_data_one)
    df.to_csv("./sourceOneTaps.csv", float_format='%10.6f', index = False)

    tap_data_two = {'Indexes' : sourceTwoTapInd,
                    'RelativeTimeStamp' : sourceTwoRelTimes[sourceTwoTapInd],
                    'LocalTimeStamp' : sourceTwoLocalTimes[sourceTwoTapInd],
                    }
    df = pd.DataFrame(tap_data_two)
    df.to_csv("./sourceTwoTaps.csv", float_format='%10.6f', index = False)

    print("=" * 15, " Finished! ", "=" * 15)


def createMagnitudeVectorWithRelTime(listOfDimensionTuples):
    """
    Creates a single vector of the combined magnitudes of n vectors

    Parameters:
    - listOfDimensionTuples: A list of tuples that give the information of the location of the vectors to be combined
    
    Notes:
    - There should be one tuple per dimension of data
    - This function assumes that the first row of each file is the header of the file and the file is in .csv format

    Returns:
    - numpy.ndarray: of the combinted magnitude at each timestamp
    - numpy.ndarray: the corresponding time stamps for each magnitude
    """
    tempVec = []
    relTimes = []
    localTimes = []
    for dimensionTuple, i in zip(listOfDimensionTuples, range(0, len(listOfDimensionTuples))):
        if(len(dimensionTuple) != 3):
            print("Stopping - Error: Tuple is not of length 3\nTuple: ", dimensionTuple)
            return
        
        # merge all dimensions into a single vector
        data = extract_data(dimensionTuple[0], dimensionTuple[1], dimensionTuple[2])

        # only add rel times the first time through
        if (i == 0): 
            tempVec = np.power(np.diff(data[0][2]), 2)
            relTimes = data[0][1]
            localTimes = data[0][3]
        else:
            tempVec = np.add(tempVec, np.power(np.diff(data[0][2]), 2))

    # find the taps
    print(localTimes)
    tempVec = np.sqrt(tempVec)
    return tempVec, relTimes, localTimes
   
def detect(file_dir = "", file_base_names = "", timestamp_id = "LocalTimestamp", 
           time_window = [0, 50000], height = 0.25):
    """
    @fn     detect()
    @brief  Detects tap times and saves the results in a file named *_taps.csv
    @param  file_dir Base directory of the parsed data files
    @param  file_base_names array of file bases of the data files. Expected 
            organization is file_dir/file_base_names[i]/file_base_names[i]_XX.csv
    @param  timestamp_id timestamp identifier to use for timestamps of taps
    @param  time_window Window (in secs) from the beginning of the file to look for taps
    @param  height Height of the threshold for detecting peaks
    @ToDo   Add multiple time_windows as input
    """
    print('***\ntapdetector.detect()')

    type_tags = ['AX', 'AY', 'AZ']
    time_mask = []
    
    
    fig_name = "taps"
    fig = plt.figure(fig_name)
    fig.clf()
    fig, axs = plt.subplots(nrows=len(type_tags) + 1, ncols=1, num=fig_name)
    
    print("type_tags: ", type_tags)
    print("time_window: ", time_window)
    print("height: ", height)
    print("timestamp_id: ", timestamp_id)
    print("Directory: ", file_dir)
    print("file_base_names: ", file_base_names)
    
    
    # ToDo Add multiple time_windows
    # ToDo Add multiple timestamp_ids
    for f in range(len(file_base_names)):
        file_base = file_base_names[f]
        print("File: ", file_base)
        
        data = []
        data_vec = []
        for t in range(len(type_tags)):
            type_tag = type_tags[t]
                    
            file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + type_tag + '.csv'
            print(file_path)
            data.append(pd.read_csv(file_path))
            
            # Create time segment
            # NOTE: this only works for signals with the same sampling rate
            timestamps = data[t][timestamp_id].to_numpy()
            timestamps_rel = timestamps - timestamps[0]
            time_mask = np.where((timestamps_rel > time_window[0]) & (timestamps_rel < time_window[1]))
            
            # Plot data
            plt.sca(plt.subplot(len(type_tags) + 1, 1, t + 1))
            plt.plot(data[t][type_tag].to_numpy()[time_mask])
            plt.gca().set_ylabel(type_tag)
            plt.gca().axes.xaxis.set_visible(False)
            
            
            # Create vector data
            # NOTE: this only works for signals with the same sampling rate
            if (t == 0): 
                # first data type
                data_vec = np.power(np.diff(data[t][type_tag].to_numpy()), 2)
            else:
                data_vec = np.add(data_vec, np.power(np.diff(data[t][type_tag].to_numpy()), 2))
    
            
        data_vec = np.sqrt(data_vec)
        p_ind, p_val = find_peaks(data_vec[0 : sum(timestamps_rel < time_window[1])], height=height)
        p_ind = p_ind[p_ind > time_mask[0][0]] # Remove indexes less than time_window[0]
        
        
        plt.sca(plt.subplot(len(type_tags) + 1, 1, len(type_tags) + 1))
        
        time_mask = time_mask[0][0 : min(len(time_mask[0]) - 1, len(timestamps_rel) - 1)]
        masked_timestamps = timestamps_rel[time_mask]
        
        plt.plot(masked_timestamps, data_vec[time_mask])
        plt.plot([masked_timestamps[1], masked_timestamps[len(masked_timestamps) - 1]], [height, height])
        plt.plot(timestamps_rel[p_ind], data_vec[p_ind], 'r*')
        plt.gca().set_ylabel("vec(diff())")
        plt.gca().set_xlabel("Time since file begin (sec)")
        
        #np.set_printoptions(precision=16)
        np.set_printoptions(formatter={'float': '{: 10.6f}'.format})
        
        print("***\nTap indexes: ", p_ind)
        print("Tap RelativeTimestamp: ", timestamps_rel[p_ind])
        print("Tap " + timestamp_id + ": ", timestamps[p_ind])
        
        file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + 'taps' + '.csv'
        print('Saving: ' + file_path)
        
        tap_data= {'Indexes': p_ind,
            'RelativeTimestamp': timestamps_rel[p_ind],
            timestamp_id: timestamps[p_ind]}
        df = pd.DataFrame(tap_data)
        df.to_csv(file_path, float_format='%10.6f', index=False)

            
            
def main():
    # TODO create CLI functionality
    # TODO scrape off the comments on top of the cyton file automatically
    arguments = sys.argv
    num_arguments = len(arguments)
    # arguments - 1 for program name - 1 for start of window - 1 for end of window - 1 for height should be divisble by 3
    #if((len(num_arguments) - 4) % 3 != 0):
    #    print("Stopping - Error - Incorrect number of arguments specified")
    #    return
    
    


    detectTaps([("C:/Users/Kurtis/EmotiBit_Biometric_Lib/py/emotibit/emotibit_AX.csv","LocalTimestamp","AX"),
            ("C:/Users/Kurtis/EmotiBit_Biometric_Lib/py/emotibit/emotibit_AX.csv","LocalTimestamp","AX")],
            [("C:/Users/Kurtis/EmotiBit_Biometric_Lib/py/emotibit/cyton.csv"," Timestamp"," Accel Channel 0"),
             ("C:/Users/Kurtis/EmotiBit_Biometric_Lib/py/emotibit/cyton.csv"," Timestamp"," Accel Channel 1"),
             ("C:/Users/Kurtis/EmotiBit_Biometric_Lib/py/emotibit/cyton.csv"," Timestamp"," Accel Channel 2")])

if __name__=="__main__":
    main()


"""
def plot_taps(data_array, height):
    #
    Plot taps for a specific type of file.
    Parameters:
    - data_array: Structured array containing organized data for a specific type of file.
    - height: Height of the threshold for detecting peaks.

    #
        # Example: Plot data for each file
        plt.figure(file_base)
        plt.plot(timestamps_rel, data_window, label=f"{file_base}")
        plt.legend()
        plt.title(f"Taps for {file_base}")
        plt.xlabel("Time since file begin (sec)")
        plt.ylabel("Data")
"""