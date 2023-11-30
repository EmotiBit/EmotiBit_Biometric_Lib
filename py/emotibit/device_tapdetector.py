# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
import os
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np

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

    data_array = np.array([(file_path, timestamps_rel, column_data)],
                          dtype=object)

    return data_array

# TODO reconfigure detect function to use the data array made in extract data to extract peaks with vector math in the original function

"""    

def detect(file_dir="", file_base_names="", timestamp_id="",
           time_window=[0, 50000], height=0.25):
    #
    Detects tap times and saves the results in a file named *_taps.csv.
    

    Parameters:
    - file_dir: Base directory of the parsed data files.
    - file_base_names: Array of file bases of the data files.
    - timestamp_id: Timestamp identifier to use for timestamps of taps.
    - time_window: Window (in secs) from the beginning of the file to look for taps.
    - height: Height of the threshold for detecting peaks.
    #
    print('***\ntapdetector.detect()')
    
    # Extract data for each file
    data_array = extract_data(file_dir, file_base_names, timestamp_id, time_window)
    
    type_tags = []
    time_mask = []
    
    for entry in data_array:
        file_base, timestamps_rel, data_window = entry['FileName'], entry['RelativeTimestamp'], entry['Data']

        # TODO: this logic creates a time segment and conducts vector math to plot the taps but this needs to be adjusted to work properly
        
        for f in range(len(file_base_names)):
            file_base = file_base_names[f]
            #print("File: ", file_base)
            
            data = []
            data_vec = []
            for t in range(len(type_tags)):
                type_tag = type_tags[t]
                        
                file_path = file_dir + '\\' + file_base_names + '_' + type_tag + '.csv'
                print(file_path)
                data.append(pd.read_csv(file_path))
                
                # TODO Create time segment is already in extract_data function but not time mask so take out unnecessary code
                # NOTE: this only works for signals with the same sampling rate and is already implemented in extract data
                #timestamps = data[t][timestamp_id].to_numpy()
                #timestamps_rel = timestamps - timestamps[0]
                #time_mask = np.where((timestamps_rel > time_window[0]) & (timestamps_rel < time_window[1]))
                
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
            
            new_file_path = file_dir + '\\' + file_base_names '_' + 'taps' + '.csv'
            print('Saving: ' + new_file_path)
            
            tap_data= {'Indexes': p_ind,
                'RelativeTimestamp': timestamps_rel[p_ind],
                timestamp_id: timestamps[p_ind]}
            df = pd.DataFrame(tap_data);
            df.to_csv(file_path, float_format='%10.6f', index=False)
            
            


    # Plot taps for each file
    plot_taps(data_array, height)

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