# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import argparse


def load_data(file_path, timestamp_header):
    """
    Load data from a file.

    Parameters:
    - file_path:
        Path to the data file.
    - timestamp_header:
        The column header for timestamps.

    Returns:
    - timestamps:
        Numpy array of timestamps.
    - data: Pandas
        DataFrame containing all data columns.
    """
    data = pd.read_csv(file_path)
    timestamps = data[timestamp_header].to_numpy()
    data_values = data.drop(columns=[timestamp_header])
    return timestamps, data_values


def extract_data(file_path,
                 timestamp_header,
                 column_name,
                 time_window=[0, 50000,],
                 data_column=None,):
    """
    Extract and organize data from a single file.

    Parameters:
    - file_path:
        Path to the data file.
    - timestamp_header:
        The column header for timestamps.
    - column_name:
        The column header for the data.
    - time_window:
        A list with the beginning and ending relative time stamp
        to examine, ex: [0, 50000]
    - data_column:
        Pandas Series of data associated with the specified column
        (default: None).

    Returns:
    - data_array: Structured array containing organized data.
    """
    timestamps, data_values = load_data(file_path, timestamp_header)
    local_times = timestamps.copy()

    # Use the specified data_column if provided,
    # otherwise use the specified column from data_values.
    if data_column is not None:
        column_data = data_column.to_numpy()
    else:
        column_data = data_values[column_name].to_numpy()

    # Ensure timestamps_rel and column_data have the same length
    min_length = min(len(timestamps), len(column_data))
    timestamps_rel = timestamps[:min_length]
    column_data = column_data[:min_length]
    # Create time segment.
    timestamps_rel -= timestamps_rel[0]
    time_mask = np.where((timestamps_rel >= time_window[0]) &
                         (timestamps_rel < time_window[1]))
    # Now we are going to extract the data for only the selected times:
    timestamps_rel = timestamps_rel[time_mask]
    column_data = column_data[time_mask]
    local_times = local_times[time_mask]

    data_array = np.array([(file_path,
                          timestamps_rel,
                          column_data,
                          local_times)],
                          dtype=object)
    return data_array


def detect_taps(source_list,
                time_window=[0, 50000],
                min_height=0.25,
                filt_win_len=1,
                output_file="taps"):
    """
    Finds the taps for a data sources in n dimensions

    Parameters:
    - source_list: A list of tuples for each dimension of data in form of:
        [(filepath, time_stamp_col_name, data_col_name),
        (filepath, time_stamp_col_name, data_col_name),...]
    - time_window:
        A list of two integers indicating the window of time that
        should be examined from source one
    - height:
        The minimum height that should be considered for tap detection.
    - filt_win_len:
        The window length that should be passed to the convolve
        filter.
    - output_file:
        A name for where the image displaying the vectors and taps should
        be saved, should not contain extension

    Notes:
    - There should be one tuple per dimension of data
    - This function assumes that the first row of each
      file is the header of the file and the file is in .csv format

    Returns:
    - None
    """

    # ensure correct types
    if not isinstance(source_list, list):
        print("Stopping - Error - First parameter should be of type list.")
        return None

    print("=" * 15, " Beginning Tap Detection ", "=" * 15)
    print("Time Window: ", time_window)
    print("Height: ", min_height)

    # Create single magnitude vector.
    (source_vec,
     source_rel_times,
     source_local_times,
     all_dimensions) = load_data_and_create_mag_vector(source_list,
                                                       time_window,
                                                       filt_win_len)

    # Find the peaks.
    tap_indexes, _ = signal.find_peaks(source_vec, min_height)

    print("***\nTap Indexes: ", tap_indexes)
    print("***\nRelative Timestamps of Taps: ",
          source_rel_times[tap_indexes])

    # Write taps to file.
    print("=" * 15, " Saving Taps to File ", "=" * 15)
    tap_data = {'Indexes':
                tap_indexes,
                'RelativeTimeStamp':
                source_rel_times[tap_indexes],
                'Timestamp':
                source_local_times[tap_indexes],
                }
    df = pd.DataFrame(tap_data)
    df.to_csv(output_file + ".csv", float_format='%10.6f', index=False)

    print("=" * 15, " Creating Plots for Validation ", "=" * 15)
    plot_taps([(source_vec,
                tap_data,
                all_dimensions,
                source_rel_times),],
              [output_file],
              output_file)

    print("=" * 15, " Finished! ", "=" * 15)
    return None


def plot_taps(tuple_list, label_list=None, filename="taps"):
    """
    Plots the vectors and the detected taps to allow for
    validation of the tap detector results.

    Parameters:
    - List of tuples for each data source, example:
            [(vector1, tap_dict1, all_dimensions1, source_rel_times),
             (vector2, tap_dict2, all_dimensions2, source_two_rel_times)]
            where:
            - vector1 is the vector of the combined magnitudes
              of all of the vectors in all_dimensions1
            - tap_dict1 is a dictionary that is defined as follows:
                - {'Indexes': indexes of the time stamps,
                   'RelativeTimeStamp': the relative time stamps of the taps,
                   'LocalTimeStamp': the local time stamps of the taps
                   }
            - all_dimensions1 is an array with all of the
              dimensions of data for that source
                - typically, this means that allDimensions 1 has 3 columns,
                  one for x, y, and z
            - relTimes1 is a single-dimensional array of all of the
                relative timestamps for that source of data
    - list of labels for each of the provided data sources (optional)
    - name for the output image (optional)
        (do not include a file extension, .png will be appended for you)

    Notes:
    - ...

    Returns:
    - Does not return any values but saves a single image,
        taps.png containing all six plots annotated with the taps
    """
    fig = plt.figure(1, figsize=(8.5, 15))

    # Loop over all of the provided data sources.
    index = 1
    for tuple in tuple_list:
        # The tuple should be:
        # (magnitude_vector, tap_dictionary, all_dimensions_array)

        # Create a new subplot and fill with data
        # for the combined magnitude vector.
        ax = fig.add_subplot(len(tuple_list) * 3, 1, index)
        if (label_list is not None):
            label = label_list[int((index - 1) / 2)]
        else:
            label = "Source " + str(int((index) / 2) + 1)

        # Create a subplot with the x axis as the relative timestamps.
        create_magnitude_vector_subplot(ax,
                                        tuple[0],
                                        tuple[1],
                                        tuple[3],
                                        label)
        index += 1

        # Create another subplot with the x axis as the index.
        ax = fig.add_subplot(len(tuple_list) * 3, 1, index)
        create_magnitude_vector_index_subplot(ax, tuple[0], tuple[1], label)
        index += 1

        # Create another subplot to fill with all of the raw dimensional data.
        ax = fig.add_subplot(len(tuple_list) * 3, 1, index)
        create_all_dimension_subplot(ax,
                                     tuple[0],
                                     tuple[1],
                                     tuple[2],
                                     tuple[3],
                                     label)
        index += 1

    fig.tight_layout()
    fig.savefig(filename + '.png', dpi=600)


def create_magnitude_vector_subplot(subplot, vector, taps, rel_times, label):
    """
    Plots the magnitude vector and the detected taps to allow
    for validation of the tap detector results.

    Parameters:
    - a subplot to plot on
    - a magnitude vector
    - a dictionary of all of the tap information
        Example: {'Indexes': indexes of the time stamps,
                  'RelativeTimeStamp': the relative time stamps of taps,
                  'Timestamp': the local time stamps of the taps
                  }
    - an array of the relative timestamps
    - a label for the data source

    Notes:
    - ...

    Returns:
    - none
    """
    # Plot the magnitude vector agains the times,
    # uses [:-1] because there are only n - 1 differences between n samples.
    subplot.plot(rel_times[:-1], vector)
    subplot.plot(rel_times[taps['Indexes']], vector[taps['Indexes']], 'o')
    subplot.title.set_text("Combined Magnitude Vector - " + label)
    subplot.set_xlabel("Relative Timestamp")
    subplot.set_ylabel("Acceleration")


def create_magnitude_vector_index_subplot(subplot, vector, taps, label):
    """
    Plots the magnitude vector and the detected taps to
    allow for validation of the tap detector results.
    Uses the index of the acceleration vector as the x axis.

    Parameters:
    - a subplot to plot on
    - a magnitude vector
    - a dictionary of all of the tap information
        Example: {'Indexes': indexes of the time stamps,
                  'RelativeTimeStamp': the relative time stamps of taps,
                  'LocalTimeStamp': the local time stamps of the taps}
    - a label for the data source

    Notes:
    - ...

    Returns:
    - none
    """
    subplot.plot(vector)
    subplot.plot(np.arange(0, len(vector), 1)[taps['Indexes']],
                 vector[taps['Indexes']], 'o')
    subplot.title.set_text("Combined Magnitude Vector - " + label)
    subplot.set_xlabel("Index")
    subplot.set_ylabel("Acceleration")


def create_all_dimension_subplot(subplot,
                                 vector,
                                 taps,
                                 all_dims,
                                 rel_times,
                                 label):
    """
    Plots the magnitude vector and the detected taps and all
        the raw dimension data to allow for validation of
        the tap detector results.
    Raw dimensions data will be converted to the differences between
        each timestamp to match the magnitude vector.

    Parameters:
    - a subplot to plot on
    - a magnitude vector
    - a dictionary of all of the tap information
        Example: {'Indexes': indexes of the time stamps,
                  'RelativeTimeStamp': the relative time stamps of the taps,
                  'LocalTimeStamp': the local time stamps of the taps}
    - multidimensional array of all of the raw data
    - an array of the relative timestamps
    - a label for the data source

    Notes:
    - ...

    Returns:
    - none
    """
    # Plot the magnitude vector.
    subplot.plot(rel_times[:-1], vector)
    subplot.plot(rel_times[taps['Indexes']], vector[taps['Indexes']], 'o')
    for dimIndex in range(0, len(all_dims)):
        # Plot each dimension of raw data.
        subplot.plot(rel_times, all_dims[dimIndex])
    subplot.title.set_text("All Vectors - " + label)
    subplot.set_xlabel("Relative Timestamp")
    subplot.set_ylabel("Acceleration")


def load_data_and_create_mag_vector(list_of_dimension_tuples,
                                    time_window=[0, 50000],
                                    window=1):
    """
    Creates a single vector of the combined magnitudes
    of n vectors and applies a hann filter.

    Parameters:
    - list_of_dimension_tuples: A list of tuples that give the
        information of the location of the vectors to be combined.
        The format of the list of tuples should be as such:
          [(filepath, timeStampColName, dataColName),
          (filepath, timeStampColName, dataColName),...]
    - time_window: A list of two values indicating the beginning
        and ending times that are to be examined.
    - window: The parameter passed to the hann filter that determines
        the length of the hann filter's window.

    Notes:
    - There should be one tuple per dimension of data
    - This function assumes that the first row of each file is the
      header of the file and the file is in .csv format.
    - Each dimension's vector of data is independently filtered with
        a hann filter, where the window size is supplied by the user.
    - After being filtered, the vector is squared and summed
        with the other vectors then the square root is taken
        to complete the combination of the vectors.
    - Finally, the differences between each timestamp are found.

    Returns:
    - numpy.ndarray:
        of the combined magnitude at each timestamp that has been
        passed through the hann filter
    - numpy.ndarray:
        the corresponding relative time stamps
        for each magnitude (relative to beginning of file)
    - numpy.ndarray:
        the corresponding local time stamp for each magnitude
    - numpy.ndarray:
        an array containing the raw data for all
        the provided dimensions (ncol = number of tuples in the list)
    """
    temp_vector = []
    rel_times = []
    local_times = []
    all_dims = []

    for dimension_tuple, i in zip(list_of_dimension_tuples,
                                  range(0, len(list_of_dimension_tuples))):
        if (len(dimension_tuple) != 3):
            print("Stopping - Error: Tuple is not of length 3\nTuple: ",
                  dimension_tuple)
            return None

        data = extract_data(dimension_tuple[0],
                            dimension_tuple[1],
                            dimension_tuple[2],
                            time_window)

        # extract timestamps and raw data to return later
        all_dims.append(data[0][2])
        rel_times = data[0][1]
        local_times = data[0][3]
        normalized_hann_window = (signal.windows.hann(window)
                                  / sum(signal.windows.hann(window)))

        # Notes about filtering:
        # The convolve filter will add a small amount of phase shift
        # as long as the window size is chosen carefully,
        # the phase shift should not be large enough to be impactful for the
        # analysis. Users of this script should be careful to ensure
        # that the window size they choose does not introduce a phase shift of
        # more than one or two timestamps, as then it may introduce
        # too much error for the analysis task you are trying to achieve.

        if (i == 0):
            # First vector is used to initialize the magnitude vector.
            temp_vector = data[0][2].copy()
            temp_vector = np.convolve(temp_vector,
                                      normalized_hann_window,
                                      mode="same")
            temp_vector = np.power(temp_vector, 2)
        else:
            # Following vectors are added to the initalized magnitude vector.
            new_dim_vec = data[0][2].copy()
            new_dim_vec = np.convolve(new_dim_vec,
                                      normalized_hann_window,
                                      mode="same")
            new_dim_vec = np.power(new_dim_vec, 2)
            temp_vector = np.add(temp_vector, new_dim_vec)

    # Complete calculation of the magnitude vector
    # by taking the sqrt and then finding the diffs.
    mag_vec = np.sqrt(temp_vector)
    mag_vec = np.diff(mag_vec)
    return mag_vec, rel_times, local_times, all_dims


def main():
    """
    Runs the tap detector
    CLI Usage is found by running this file with the -h command

    """

    source_tuple_list = []

    parser = argparse.ArgumentParser()
    parser.add_argument("-sf",
                        "--sourceFiles",
                        action="store",
                        type=str,
                        nargs="+",
                        help="""Path(s) to one or more files for the input
                         data. If more than one file is given,
                         the given files will be pairwise matched with the data
                         columns provided, which could require passing the same
                         filename more than once so that all data columns can
                         be matched.""")
    parser.add_argument("-sd",
                        "--sourceDimensions",
                        action="store",
                        type=int,
                        nargs=1,
                        help="""Integer number of dimensions of
                         data.""")
    parser.add_argument("-st",
                        "--sourceTimestamps",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""String of the column name for which timestamps
                          can be found.""")
    parser.add_argument("-sa",
                        "--sourceData",
                        action="store",
                        type=str,
                        nargs="+",
                        help="""String(s) of the column(s) where the
                         data for can be found. Number of
                         strings given should match the number of
                         dimensions given""")
    parser.add_argument("-tw",
                        "--time_window",
                        action="store",
                        type=float,
                        nargs="*",
                        help="""Two floats indicating the starting and
                          ending relative timestamps.
                            (Optional: Default is 0.0 50000.0)""")
    parser.add_argument("-ht",
                        "--height",
                        action="store",
                        type=float,
                        nargs="?",
                        help="""Single float value passed to
                         the peak finding function.
                         (Optional: Default is 0.25)""")
    parser.add_argument("-w",
                        "--window",
                        action="store",
                        type=int,
                        nargs="?",
                        help="""Single integer specifying the window
                         size for the convolve filter.""")
    parser.add_argument("-o",
                        "--output_file",
                        action="store",
                        type=str,
                        nargs="?",
                        help="""Name of the output .png file
                         for all of the plots. Defaults to 'taps.png'""")
    args = parser.parse_args()

    # get the source one files into the tuple list
    if (len(args.sourceFiles) == 1):
        if (len(args.sourceData) != args.sourceDimensions):
            print("""Error - Number of data columns
                   specified for source one does not match
                   specified number of dimensions""")
            return None
        for data_column in args.sourceData:
            source_tuple_list.append((args.sourceFiles[0],
                                      args.sourceTimestamps[0],
                                      data_column))
    else:
        # pairwise match
        if (len(args.sourceFiles) != args.sourceDimensions[0]):
            print("""Error - Number of files specified is not one
                   and does not match
                   number of dimensions specified""")
            return None
        if (len(args.sourceFiles) != len(args.sourceData)):
            print("""Error - Number of files specified
                   is not one and does not
                   match number of data columns specified""")
            return None
        for fileName, data_column in zip(args.sourceFiles,
                                         args.sourceData):
            source_tuple_list.append((fileName,
                                      args.sourceTimestamps[0],
                                      data_column))

    # collect the other arguments
    time_window = [0, 50000]
    if (args.time_window is not None):
        if (len(args.time_window) != 2):
            print("""Error - Exactly 2 float arguments
                   must be given for time window one.
                   (-tw1 --time_window)""")
            return None
        time_window = [args.time_window[0], args.time_window[1]]

    height = 0.25
    if (args.height is not None):
        height = args.height

    window = 1
    if (args.window is not None):
        window = args.window

    fileName = "taps"
    if (args.output_file is not None):
        fileName = args.output_file

    # Call the tap detector.
    detect_taps(source_list=source_tuple_list,
                time_window=time_window,
                min_height=height,
                filt_win_len=window,
                output_file=fileName,)
    return None


if __name__ == "__main__":
    main()
