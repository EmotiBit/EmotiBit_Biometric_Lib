# -*- coding: utf-8 -*-
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as scisig
import emotibit.signal as ebsig

try:
    import IPython
    IPython.get_ipython.magic("matplotlib qt")
except AttributeError:
    plt.ion()


def detect_hr(ecg_file,
              ecg_column,
              ecg_timestamp,
              hr_file,
              hr_column,
              hr_timestamp,
              input_frequency,
              filename,
              plot_file,
              max_heart_rate_bpm=180,
              height=250):
    """
    @input ecg_file:
        String of path to the file containing the ECG data
    @input ecg_column:
        String of the column name in the ECG file containing the ECG data
    @input ecg_timestamp:
        String of the column name in the ECG file containing the timestamps
        in the ECG data
    @input hr_file:
        String of the path to the file containing the HR data
    @input hr_column:
        String of the column name in the HR file containing the HR data
    @input hr_timestamp:
        String of the column name containing the timestamps in the HR data
    @input input_frequency:
        OPTIONAL: int Frequency of the ECG data, defaults to 250 hertz.
    @input maxHeartRateBPM:
        OPTIONAL: int of the maximum heart rate to consider valid in BPM.
        Defaults to 180 BPM.
    @input filename:
        OPTIONAL: string of the filename to write the detected ECG HR to.
        Defaults to 'ecgHR.csv'.
    @input height:
        OPTIONAL: int of the minimum height to use in ECG peak detection.
        Defaults to 250.
    @input plot_file:
        OPTIONAL: string of the filename to use to write the plot of HR data.
        Defaults to 'detectedHR.png'.

    @output: df: a dataframe containing the heart rate values
    and the timestamps of those heart rate values
    """

    # Providing a maximum allowed heart rate will allow the
    # find_peaks function to discard any duplicate readings
    # by enforcing a minimum space between beats.
    max_heart_rate_hertz = max_heart_rate_bpm / 60
    minimum_sample_separation = input_frequency / max_heart_rate_hertz

    file = pd.read_csv(ecg_file)
    # We filter the data so that we can more easily find the peaks.
    filtered = ebsig.band_filter(file[ecg_column],
                                 np.array([5, 49]),
                                 fs=input_frequency)
    ind, _ = scisig.find_peaks(filtered,
                               height=height,
                               distance=minimum_sample_separation)
    # Plot HR detections and filtered ECG data.
    if plot_file is not None:
        create_validation_plot(filtered, ind)
    # Calculate hr.
    hr = 1 / (np.diff(ind) / input_frequency) * 60
    hr_timestamps = file[ecg_timestamp][ind][1:]  # We dont need the first one.
    # Save hr with hr timestamps.
    df = pd.DataFrame({'Timestamp': hr_timestamps,
                       'HR': hr})
    if filename is not None:
        df.to_csv(filename)

    # Plot both HRs on one plot.
    known_hr = None
    if (hr_file is not None):
        known_hr = pd.read_csv(hr_file)
    if plot_file is not None and known_hr is not None:
        create_hr_plot(known_hr[hr_timestamp],
                       known_hr[hr_column],
                       file[ecg_timestamp][ind][1:],
                       hr,
                       plot_file)
    return df


def create_hr_plot(known_hr_timestamps,
                   known_hr_values,
                   detected_hr_timestamps,
                   detected_hr_values,
                   filename):
    """
    @input: known_hr_timestamps:
        The column of timestamps of the HR data from the known HR file.
    @input: known_hr_values:
        The column of values of the HR data from the known HR file.
    @input: detected_hr_timestamps:
        The column of timestamps of the ECG HR data
    @input: detected_hr_values:
        The column of values of HR data from the ECG HR data
    @input: filename:
        String of the name of where this plot should be saved

    @output: None: Saves a plot to a file.
    """

    plt.clf()
    plt.step(known_hr_timestamps,
             known_hr_values,
             where="pre",
             color="blue",
             label="Known HR")
    plt.step(detected_hr_timestamps,
             detected_hr_values,
             where="post",
             color="purple",
             label="HR from ECG")
    plt.xlabel("Timestamp")
    plt.legend(loc="upper left")
    plt.ylabel("Heart Rate")
    plt.title("Heart Rate")
    plt.savefig(filename, dpi=600)


def create_validation_plot(filtered,
                           ind,
                           filename="hr_detection_validation_plot.png"):
    """
    @input filtered: A column of ECG data that has been filtered.
    @input ind: A sequences of indexes of the filtered
      data where the peaks have been detected.
    @input filename: OPTIONAL: String of the filename to save this plot to.

    @output: None: A plot is written to the indicated filename.
    """

    plt.plot(filtered)
    plt.xlabel("Timestamp")
    plt.ylabel("ECG")
    plt.title("ECG Data with Detected Peaks")
    plt.scatter(ind, filtered[ind], color="orange")
    plt.gcf().set_size_inches(14, 6)
    plt.savefig(filename, dpi=600)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ecg",
                        "--ecg_file",
                        action="store",
                        type=str,
                        nargs=1,
                        help="Path to the file containing the ECG data")
    parser.add_argument("-ecgCol",
                        "--ecg_column",
                        action="store",
                        type=str,
                        nargs=1,
                        help="Name of the column storing the ECG data")
    parser.add_argument("-ecgt",
                        "--ecg_timestamp",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Name of the column containing
                          the timestamps for the ECG data""")
    parser.add_argument("-f",
                        "--frequency",
                        action="store",
                        type=int,
                        nargs=1,
                        help="""The frequency of the ECG data,
                          defaults to 250 hertz.""")
    parser.add_argument("-mhr",
                        "--maxHeartRate",
                        action="store",
                        type=int,
                        nargs="?",
                        help="""[OPTINAL] The maximum heart rate
                          that can be detected, used for
                          reducing false detection, defaults to 180""")
    parser.add_argument("-ht",
                        "--height",
                        action="store",
                        type=int,
                        nargs="?",
                        help="""[OPTIONAL] The height threshold to be used
                          for ECG HR detection, defaults to 250""")
    parser.add_argument("-hr",
                        "--hr_file",
                        action="store",
                        type=str,
                        nargs="?",
                        help="""[OPTIONAL] Path to file containing containing
                          already known HR Data (such as from EmotiBit)""")
    parser.add_argument("-hrCol",
                        "--hr_column",
                        action="store",
                        type=str,
                        nargs="?",
                        help="[OPTIONAL] of the column storing the HR data")
    parser.add_argument("-hrt",
                        "--hr_timestamp",
                        action="store",
                        type=str,
                        nargs="?",
                        help="""[OPTIONAL] Name of the column
                          containing the timestamps for the HR data""")
    parser.add_argument("-o",
                        "--output",
                        action="store",
                        type=str,
                        nargs="?",
                        help="""[OPTIONAL] Name for the output file of HR
                        detected from the ECG file, does not write file
                          if not provided.""")
    parser.add_argument("-po",
                        "--plotOutput",
                        action="store",
                        type=str,
                        nargs="?",
                        help="""[OPTIONAL] Name for the output file of plot,
                          does not write plot if not provided.""")

    args = parser.parse_args()
    ecg_file = args.ecg_file[0]
    ecg_column = args.ecg_column[0]
    ecg_timestamps = args.ecg_timestamp[0]

    hr_file = None
    hr_column = None
    hr_timestamps = None
    if args.hr_file is not None:
        hr_file = args.hr_file
    if args.hr_column is not None:
        hr_column = args.hr_column
    if args.hr_timestamp is not None:
        hr_timestamps = args.hr_timestamp

    if not ((hr_file is not None
            and hr_column is not None
            and hr_timestamps is not None) or
            (hr_file is None
            and hr_column is None
            and hr_timestamps is None)):
        print("""Error - You must either provide no values
               for any known HR files, or all values for a known HR.""")
        return None

    frequency = None
    max_hr = 180
    # Derived by examining the data, could possibly need to change this
    # if using a different ECG measuring device or something
    # else in a setup changes.
    height = 250
    output_file = "ecgHR.csv"
    plot_file = "detectedHR.png"
    if (args.frequency is not None):
        frequency = args.frequency[0]
    else:
        print("Error - The frequency of the ECG data was not provided.")
        return None
    if (args.maxHeartRate is not None):
        max_hr = args.maxHeartRate
    if (args.height is not None):
        height = args.height
    output_file = args.output
    plot_file = args.plotOutput

    detect_hr(ecg_file,
              ecg_column,
              ecg_timestamps,
              hr_file,
              hr_column,
              hr_timestamps,
              frequency,
              output_file,
              plot_file,
              max_hr,
              height)


if __name__ == "__main__":
    main()
