# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as scisig
import emotibit.signal as ebsig
import argparse

try:
    import IPython
    IPython.get_ipython.magic("matplotlib qt")
except:
    plt.ion()


def detectHR(ecgFile, ecgColumn, ecgTimestamp, hrFile, hrColumn, hrTimestamp, inputFrequency, filename, plotFile, maxHeartReatBPM = 180, height = 250):
    """
    @input ecgFile: String of path to the file containing the ECG data
    @input ecgColumn: String of the column name in the ECG file containing the ECG data
    @input ecgTimestamp: String of the column name in the ECG file containing the timestamps in the ECG data
    @input hrFile: String of the path to the file containing the HR data
    @input hrColumn: String of the column name in the HR file containing the HR data
    @input hrTimestamp: String of the column name containing the timestamps in the HR data
    @input inputFrequency: OPTIONAL: int Frequency of the ECG data, defaults to 250 hertz.
    @input maxHeartRateBPM: OPTIONAL: int of the maximum heart rate to consider valid in BPM. Defaults to 180 BPM.
    @input filename: OPTIONAL: string of the filename to write the detected ECG HR to. Defaults to 'ecgHR.csv'.
    @input height: OPTIONAL: int of the minimum height to use in ECG peak detection. Defaults to 250.
    @input plotFile: OPTIONAL: string of the filename to use to write the plot of HR data to. Defaults to 'detectedHR.png'.
    
    @output: df: a dataframe containing the heart rate values and the timestamps of those heart rate values
    """

    # to give better input parameters to the find_peaks() function
    maxHeartReatHertz = maxHeartReatBPM / 60 # divide by 60 seconds per minute
    minumiumSampleSeparation = inputFrequency / maxHeartReatHertz # gives the number of samples as a minimum between beats

    # read in file with ECG Data
    file = pd.read_csv(ecgFile)
    filtered = ebsig.band_filter(file[ecgColumn], np.array([5, 49]), fs = inputFrequency)
    ind, _ = scisig.find_peaks(filtered, 
                                 height = height, 
                                 distance = minumiumSampleSeparation)
    # plot HR detections and filtered ECG data
    if plotFile is not None:
        createValidationPlot(filtered, ind)
    # calculate hr
    hr = 1 / (np.diff(ind) / inputFrequency) * 60
    hrTimeStamps = file[ecgTimestamp][ind][1:] # we dont need the first one
    # save hr with hr timestamps
    df = pd.DataFrame({'Timestamp': hrTimeStamps,
                       'HR':hr})
    if filename is not None:
        df.to_csv(filename)

    # plot both HRs on one plot
    knownHR = None
    if(hrFile is not None):
        knownHR = pd.read_csv(hrFile)
    if plotFile is not None and knownHR is not None:
        createHRPlot(knownHR[hrTimestamp], knownHR[hrColumn], file[ecgTimestamp][ind][1:], hr, plotFile)
    return df

def createHRPlot(knownHRTimestamps, knownHRValues, detectedHRTimestamps, detectedHRValues, filename):
    """
    @input: knownHRTimestamps: The column of timestamps of the HR data from the known HR file.
    @input: knownHRValues: The column of values of the HR data from the known HR file.
    @input: detectedHRTimestamps: The column of timestamps of the ECG HR data
    @input: detectedHRValues: The column of values of HR data from the ECG HR data
    @input: filename: String of the name of where this plot should be saved
    
    @output: None: Saves a plot to a file.
    """
    
    plt.clf()
    plt.step(knownHRTimestamps, knownHRValues, where = "pre", color = "blue", label = "Known HR")
    plt.step(detectedHRTimestamps, detectedHRValues, where = "post", color = "purple", label = "HR from ECG")
    plt.xlabel("Timestamp")
    plt.legend(loc = "upper left")
    plt.ylabel("Heart Rate")
    plt.title("Heart Rate")
    plt.savefig(filename, dpi = 600)

def createValidationPlot(filtered, ind, fileName = "hr_detection_validation_plot.png"):
    """
    @input filtered: A column of ECG data that has been filtered.
    @input ind: A sequences of indexes of the filtered data where the peaks have been detected.
    @input fileName: OPTIONAL: String of the filename to save this plot to.
    
    @output: None: A plot is written to the indicated filename.
    """

    plt.plot(filtered)
    plt.xlabel("Timestamp")
    plt.ylabel("ECG")
    plt.title("ECG Data with Detected Peaks")
    plt.scatter(ind, filtered[ind], color = "orange")
    plt.gcf().set_size_inches(14, 6)
    plt.savefig(fileName, dpi = 600)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ecg", "--ecgfile", action = "store", type = str, nargs = 1, help = "Path to the file containing the ECG data")
    parser.add_argument("-ecgCol", "--ecgColumn", action = "store", type = str, nargs = 1, help = "Name of the column storing the ECG data")
    parser.add_argument("-ecgt", "--ecgTimestamp", action = "store", type = str, nargs = 1, help = "Name of the column containing the timestamps for the ECG data")
    parser.add_argument("-f", "--frequency", action = "store", type = int, nargs = 1, help = "The frequency of the ECG data, defaults to 250 hertz.")
    parser.add_argument("-mhr", "--maxHeartRate", action = "store", type = int, nargs = "?", help = "[OPTINAL] The maximum heart rate that can be detected, used for reducing false detection, defaults to 180")
    parser.add_argument("-ht", "--height", action = "store", type = int, nargs = "?", help = "[OPTIONAL] The height threshold to be used for ECG HR detection, defaults to 250")
    parser.add_argument("-hr", "--hrfile", action = "store", type = str, nargs = "?", help = "[OPTIONAL] Path to the file containing containing already known HR Data (such as from EmotiBit)")
    parser.add_argument("-hrCol", "--hrColumn", action = "store", type = str, nargs = "?", help = "[OPTIONAL] of the column storing the HR data")
    parser.add_argument("-hrt", "--hrTimestamp", action = "store", type = str, nargs = "?", help ="[OPTIONAL] Name of the column containing the timestamps for the HR data")
    parser.add_argument("-o", "--output", action = "store", type = str, nargs = "?", help = "[OPTIONAL] Name for the output file of HR detected from the ECG file, does not write file if not provided.")
    parser.add_argument("-po", "--plotOutput", action = "store", type = str, nargs = "?", help = "[OPTIONAL] Name for the output file of the plot, does not write plot if not provided.")
    
    args = parser.parse_args()
    ecgFile = args.ecgfile[0]
    ecgColumn = args.ecgColumn[0]
    ecgTimestamps = args.ecgTimestamp[0]

    hrFile = None
    hrColumn = None
    hrTimestamps = None
    if args.hrfile is not None:
        hrFile = args.hrfile
    if args.hrColumn is not None:
        hrColumn = args.hrColumn
    if args.hrTimestamp is not None:
        hrTimestamps = args.hrTimestamp
           
    if not((hrFile != None and hrColumn != None and hrTimestamps != None) or (hrFile == None and hrColumn == None and hrTimestamps == None)):
       print("Error - You must either provide no values for any known HR files, or all values for a known HR.")
       return
    
    
    frequency = None
    maxHr = 180
    height = 250
    outputFile = "ecgHR.csv"
    plotFile = "detectedHR.png"
    if(args.frequency is not None):
        frequency = args.frequency[0]
    else:
        print("Error - The frequency of the ECG data was not provided.")
        return
    if(args.maxHeartRate is not None):
        maxHr = args.maxHeartRate
    if(args.height is not None):
        height = args.height
    outputFile = args.output
    plotFile = args.plotOutput
    
    
    detectHR(ecgFile, ecgColumn, ecgTimestamps, hrFile, hrColumn, hrTimestamps, frequency, outputFile, plotFile, maxHr,  height)

if __name__ == "__main__":
    main()