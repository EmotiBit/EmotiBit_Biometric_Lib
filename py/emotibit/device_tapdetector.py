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

def extract_data(file_path, timestamp_header, column_name, timeWindow = [0, 50000], data_column=None):
    """
    Extract and organize data from a single file.

    Parameters:
    - file_path: Path to the data file.
    - timestamp_header: The column header for timestamps.
    - column_name: The column header for the data.
    - timeWindow: A list with the beginning and ending relative time stamp to examine, ex: [0, 50000]
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
    timeMask = np.where((timestamps_rel >= timeWindow[0]) & (timestamps_rel < timeWindow[1]))
    # now we are going to extract the data for only the selected times:
    timestamps_rel = timestamps_rel[timeMask]
    column_data = column_data[timeMask]
    localTimes = localTimes[timeMask]

    data_array = np.array([(file_path, timestamps_rel, column_data, localTimes)],
                           dtype=object)
    return data_array

def detectTaps(sourceOneList, sourceTwoList, timeWindowOne = [0, 50000], timeWindowTwo = [0, 50000], heightOne = 0.25, heightTwo = 0.25, windowOne = 1, windowTwo = 1, outputFile = "taps", nameOne = "Source One", nameTwo = "SourceTwo"):
    """
    Finds the taps for two data sources in n dimensions

    Parameters:
    - sourceOneList: A list of tuples for each dimension of data in the form of [(filepath, timeStampColName, dataColName),(filepath, timeStampColName, dataColName),...]
    - souceTwoList: A list of tuples for each dimension of data in the form of [(filepath, timeStampColName, dataColName),(filepath, timeStampColName, dataColName),...]
    - timeWindowOne: A list of two integers indicating the window of time that should be examined from source one
    - timeWindowTwo: A list of two integers indicating the window of time that should be examined from source two
    - heightOne: The height that should be considered for tap detection from source one.
    - heightTwo: The height that should be considered for tap detection from source two.
    - windowOne: The window length that should be passed to the convolve filter for source one.
    - windowTwo: The window length that should be passed to the convolve filter for source two.
    - outputFile: A name for where the image displaying the vectors and taps should be saved, should not contain extension
    - nameOne: A name for the first data source, used in the labeling of the plots.
    - nameTwo: A name for the second data source, used in the labeling of the plots.
    
    Notes:
    - There should be one tuple per dimension of data
    - This function assumes that the first row of each file is the header of the file and the file is in .csv format

    Returns:
    - None 
    """

    # ensure correct types
    if not isinstance(sourceOneList, list):
        print("Stopping - Error - First parameter should be of type list.")
        return 
    if not isinstance(sourceTwoList, list):
        print("Stopping - Error - Second paramter should be of type list.")
        return
    
    print("=" * 15, " Beginning Tap Detection ", "=" * 15)
    print("Time Window One: ", timeWindowOne)
    print("Height One: ", heightOne)
    print("Time Window Two: ", timeWindowTwo)
    print("Height Two: ", heightTwo)
    
    # create single magnitude vector for each file
    sourceOneVec, sourceOneRelTimes, sourceOneLocalTimes, allDimensionsOne = loadDataAndCreateMagVector(sourceOneList, timeWindowOne, windowOne)
    sourceTwoVec, sourceTwoRelTimes, sourceTwoLocalTimes, allDimensionsTwo = loadDataAndCreateMagVector(sourceTwoList, timeWindowTwo, windowTwo)

    # find the peaks
    sourceOneTapInd, sourceOneTapVal = signal.find_peaks(sourceOneVec, heightOne)
    sourceTwoTapInd, sourceTwoTapVal = signal.find_peaks(sourceTwoVec, heightTwo)

    print("***\nTap Indexes for Source One: ", sourceOneTapInd)
    print("***\nRelative Timestamps of Taps for Source One: ", sourceOneRelTimes[sourceOneTapInd])
    print("***\nTap Indexes for Source Two: ", sourceTwoTapInd)
    print("***\nRelative Timestamps of Taps for Source Two: ", sourceTwoRelTimes[sourceTwoTapInd])

    # write taps to file
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

    print("=" * 15, " Creating Plots for Validation ", "=" * 15)
    plotTaps([(sourceOneVec, tap_data_one, allDimensionsOne, sourceOneRelTimes), (sourceTwoVec, tap_data_two, allDimensionsTwo, sourceTwoRelTimes)], [nameOne, nameTwo], outputFile)
    print("=" * 15, " Finished! ", "=" * 15)
    return

def plotTaps(tupleList, labelList = None, filename = "taps"):
    """
    Plots the vectors and the detected taps to allow for validation of the tap detector results

    Parameters:
    - List of tuples for each data source, example:
            [(vector1, tapDict1, allDimensions1, sourceOneRelTimes), (vector1, tapDict2, allDimensions2, sourceTwoRelTimes)]
            where:
            - vector1 is the vector of the combined magintudes of all of the vectors in allDimensions1
            - tapDict1 is a dictionary that is defined as follows:
                - {'Indexes': indexes of the time stamps, 'RelativeTimeStamp': the relative time stamps of the taps, 'LocalTimeStamp': the local time stamps of the taps}
            - allDimensions1 is an array with all of the dimensions of data for that source
                - typically, this means that allDimensions 1 has 3 columns, one for x, y, and z
            - relTimes1 is a single-dimensional array of all of the relative timestamps for that source of data
    - list of labels for each of the provided data sources (optional)  
    - name for the output image (optional) (do not include a file extension, .png will be appended for you)    

    Notes:
    - ...

    Returns:
    - Does not return any values but saves a single image, taps.png containing all six plots annotated with the taps
    """
    fig = plt.figure(1, figsize=(8.5, 15))
    
    # loop over all of the provided data sources
    index = 1
    for tuple in tupleList:
        # the tuple should be (magnitudeVector, tapDictionary, allDimensionsArray)
        
        # create a new subplot and fill with data for the combined magnitude vector
        ax = fig.add_subplot(len(tupleList) * 3, 1, index)
        if(labelList is not None):
            label = labelList[int((index - 1) / 2)]
        else:
            label = "Source " + str(int((index) / 2) + 1)

        # create a subplot with the x axis as the relative timestamps
        createMagnitudeVectorSubPlot(ax, tuple[0], tuple[1], tuple[3], label)
        index += 1

        # create another subplot with the x axis as the index
        ax = fig.add_subplot(len(tupleList) * 3, 1, index)
        createMagniutdeVectorIndexSubplot(ax, tuple[0], tuple[1], label)
        index += 1

        # create another subplot to fill with all of the raw dimensional data
        ax = fig.add_subplot(len(tupleList) * 3, 1, index)
        createAllDimensionSubPlot(ax, tuple[0], tuple[1], tuple[2], tuple[3], label)
        index += 1

    fig.tight_layout()
    fig.savefig(filename + '.png', dpi = 600)

def createMagnitudeVectorSubPlot(subplot, vector, taps, relTimes, label):
    """
    Plots the magnitude vector and the detected taps to allow for validation of the tap detector results

    Parameters:
    - a subplot to plot on
    - a magnitude vector
    - a dictionary of all of the tap information
        Example: {'Indexes': indexes of the time stamps, 'RelativeTimeStamp': the relative time stamps of the taps, 'LocalTimeStamp': the local time stamps of the taps}
    - an array of the relative timestamps
    - a label for the data source
    
    Notes:
    - ...

    Returns:
    - none
    """
    subplot.plot(relTimes[:-1], vector) # plot the magnitude vector agains the times, uses [:-1] because there are only n - 1 differences between n samples
    subplot.plot(relTimes[taps['Indexes']], vector[taps['Indexes']], 'o')
    subplot.title.set_text("Combined Magnitude Vector - " + label)
    subplot.set_xlabel("Relative Timestamp")
    subplot.set_ylabel("Acceleration")
    
def createMagniutdeVectorIndexSubplot(subplot, vector, taps, label):
    """
    Plots the magnitude vector and the detected taps to allow for validation of the tap detector results
    Uses the index of the acceleration vector as the x axis

    Parameters:
    - a subplot to plot on
    - a magnitude vector
    - a dictionary of all of the tap information
        Example: {'Indexes': indexes of the time stamps, 'RelativeTimeStamp': the relative time stamps of the taps, 'LocalTimeStamp': the local time stamps of the taps}
    - a label for the data source
    
    Notes:
    - ...

    Returns:
    - none
    """
    subplot.plot(vector) # plot the magnitude vector
    subplot.plot(np.arange(0, len(vector), 1)[taps['Indexes']], vector[taps['Indexes']], 'o') # plot the taps on top of it
    subplot.title.set_text("Combined Magnitude Vector - " + label)
    subplot.set_xlabel("Index")
    subplot.set_ylabel("Acceleration")

def createAllDimensionSubPlot(subplot, vector, taps, allDims, relTimes, label):
    """
    Plots the magnitude vector and the detected taps and all the raw dimension data to allow for validation of the tap detector results
    Raw dimensions data will be converted to the differences between each timestamp to match the magnitude vector

    Parameters:
    - a subplot to plot on
    - a magnitude vector
    - a dictionary of all of the tap information
        Example: {'Indexes': indexes of the time stamps, 'RelativeTimeStamp': the relative time stamps of the taps, 'LocalTimeStamp': the local time stamps of the taps}
    - multidimensional array of all of the raw data
    - an array of the relative timestamps
    - a label for the data source
    
    Notes:
    - ...

    Returns:
    - none
    """
    subplot.plot(relTimes[:-1], vector) # plot the magnitude vector
    subplot.plot(relTimes[taps['Indexes']], vector[taps['Indexes']], 'o') # plot taps
    for dimIndex in range(0, len(allDims)):
        subplot.plot(relTimes, allDims[dimIndex]) # plot each dimension of raw data
    subplot.title.set_text("All Vectors - " + label)
    subplot.set_xlabel("Relative Timestamp")
    subplot.set_ylabel("Acceleration")

def loadDataAndCreateMagVector(listOfDimensionTuples, timeWindow = [0, 50000], window = 1):
    """
    Creates a single vector of the combined magnitudes of n vectors and applies a hann filter.

    Parameters:
    - listOfDimensionTuples: A list of tuples that give the information of the location of the vectors to be combined
        The format of the list of tuples should be as such: [(filepath, timeStampColName, dataColName),(filepath, timeStampColName, dataColName),...]
    - timeWindow: A list of two values indicating the beginning and ending times that are to be examined
    - window: The parameter passed to the hann filter that determines the length of the hann filter's window.
    
    Notes:
    - There should be one tuple per dimension of data
    - This function assumes that the first row of each file is the header of the file and the file is in .csv format
    - Each dimension's vector of data is independently filtered with a hann filter, where the window size is supplied by the user
    - After being filtered, the vector is squared and summed with the other vectors then the square root is taken to complete the combination of the vectors
    - Finally, the differences between each timestamp are found.

    Returns:
    - numpy.ndarray: of the combined magnitude at each timestamp that has been passed through the hann filter
    - numpy.ndarray: the corresponding relative time stamps for each magnitude (relative to beginning of file)
    - numpy.ndarray: the corresponding local time stamp for each magnitude
    - numpy.ndarray: an array containing the raw data for all the provided dimensions (ncol = number of tuples in the list)
    """
    tempVec = []
    relTimes = []
    localTimes = []
    allDims = []

    for dimensionTuple, i in zip(listOfDimensionTuples, range(0, len(listOfDimensionTuples))):
        if(len(dimensionTuple) != 3):
            print("Stopping - Error: Tuple is not of length 3\nTuple: ", dimensionTuple)
            return
        
        data = extract_data(dimensionTuple[0], dimensionTuple[1], dimensionTuple[2], timeWindow)

        # extract timestamps and raw data to return later
        allDims.append(data[0][2])
        relTimes = data[0][1]
        localTimes = data[0][3]
        normalizedHannWindow = signal.windows.hann(window) / sum(signal.windows.hann(window))

        # note about filtering:
        # the convolve filter will add a small amount of phase shift
        # as long as the window size is chosen carefully, the phase shift should not be large enough to be impactful for the analysis
        # users of this script should be careful to ensure that the window size they choose does not introduce a phase shift of more than
        # one or two timestamps, as then it may introduce too much error for the analysis task you are trying to achieve.

        if (i == 0): 
            # first vector is used to initialize the magnitude vector
            tempVec = data[0][2].copy()
            tempVec = np.convolve(tempVec, normalizedHannWindow, mode = "same")
            tempVec = np.power(tempVec, 2)
        else:
            # following vectors are then added to the initalized magnitude vector
            newDimVec = data[0][2].copy()
            newDimVec = np.convolve(newDimVec, normalizedHannWindow, mode = "same")
            newDimVec = np.power(newDimVec, 2)
            tempVec = np.add(tempVec, newDimVec)

    # complete calculation of the magnitude vector by taking the sqrt and then finding the diffs
    magVec = np.sqrt(tempVec)
    magVec = np.diff(magVec)
    return magVec, relTimes, localTimes, allDims    
            
def main():
    """
    Runs the tap detector
    CLI Usage is found by running this file with the -h command

    """

    sourceOneTupleList = []
    sourceTwoTupleList = []

    parser = argparse.ArgumentParser()
    parser.add_argument("-sof", "--sourceOneFiles", action="store", type = str, nargs = "+", help="Path(s) to one or more files for the input data from source one. If more than one file is given, the given files will be pairwise matched with the data columns provided, which could require passing the same filename more than once so that all data columns can be matched.")
    parser.add_argument("-sod", "--sourceOneDimensions", action="store", type = int, nargs=1, help="Integer number of dimensions of data from source one.")
    parser.add_argument("-sot", "--sourceOneTimestamps", action="store", type = str, nargs=1, help="String of the column name for which timestamps can be found for source one.")
    parser.add_argument("-soa", "--sourceOneData", action="store", type = str, nargs="+", help="String(s) of the column(s) where the data for source one can be found. Number of strings given should match the number of dimensions given")
    parser.add_argument("-stf", "--sourceTwoFiles", action="store", type = str, nargs = "+", help="Path(s) to one or more files for the input data from source two. If more than one file is given, the given files will be pairwise matched with the data columns provided, which could require passing the same filename more than once so that all data columns can be matched")
    parser.add_argument("-std", "--sourceTwoDimensions", action="store", type = int, nargs=1, help="Integer number of dimensions of data from source two.")
    parser.add_argument("-stt", "--sourceTwoTimestamps", action="store", type = str, nargs="+", help="String of the column name for which timestamps can be found for source two.")
    parser.add_argument("-sta", "--sourceTwoData", action="store", type = str, nargs="+", help="String(s) of the column(s) where the data for source one can be found. Number of strings given should match the number of dimensions given")
    parser.add_argument("-tw1", "--timeWindowOne", action = "store", type = float, nargs="*", help="Two floats indicating the starting and ending relative timestamps for source one. (Optional: Default is 0.0 50000.0)")
    parser.add_argument("-tw2", "--timeWindowTwo", action = "store", type = float, nargs="*", help="Two floats indicating the starting and ending relative timestamps for source two. (Optional: Default is 0.0 50000.0)")
    parser.add_argument("-h1", "--heightOne", action= "store", type = float, nargs = "?", help="Single float value passed to the peak finding function for source one. (Optional: Default is 0.25)")
    parser.add_argument("-h2", "--heightTwo", action = "store", type = float, nargs="?",  help="Single float value passed to the peak finding function for source two. (Optional: Default is 0.25)")
    parser.add_argument("-f", "--frequency", action = "store", type = float, nargs = "?", help="Single float value indicating the frequencies that the source files should be changed into for tap detection.")
    parser.add_argument("-w1", "--windowOne", action = "store", type = int, nargs = "?", help="Single integer specifying the window size for the convolve filter for data source one.")
    parser.add_argument("-w2", "--windowTwo", action = "store", type = int, nargs = "?", help="Single integer specifying the window size for the convolve filter for data source two.")
    parser.add_argument("-o", "--outputFile", action = "store", type = str, nargs="?", help="Name of the output .png file for all of the plots. Defaults to \"taps.png\"")
    parser.add_argument("-n1", "--nameOne", action="store", type = str, nargs = "?", help="Name for the source one data source, defaults to \"Source One\"")
    parser.add_argument("-n2", "--nameTwo", action = "store", type = str, nargs="?", help="Name for the source two data source, defaults to \"Source Two\"")
    args = parser.parse_args()

    # get the source one files into the tuple list
    if(len(args.sourceOneFiles) == 1):
        if(len(args.sourceOneData) != args.sourceOneDimensions):
            print("Error - Number of data columns specified for source one does not match specified number of dimensions")
            return
        for dataCol in args.sourceOneData:
            sourceOneTupleList.append((args.sourceOneFiles[0], args.sourceOneTimestamps[0], dataCol))
    else:
        # pairwise match
        if(len(args.sourceOneFiles) != args.sourceOneDimensions[0]):
            print("Error - Number of files specified for source one is not one and does not match number of dimensions specified")
            return
        if(len(args.sourceOneFiles) != len(args.sourceOneData)):
            print("Error - NUmber of files specified for source one is not one and doese not mach number of data columns specified")
            return
        for fileName, dataCol in zip(args.sourceOneFiles, args.sourceOneData):
            sourceOneTupleList.append((fileName, args.sourceOneTimestamps[0], dataCol))

    # get the source two files into the tuple list
    if(len(args.sourceTwoFiles) == 1):
        if(len(args.sourceTwoData) != args.sourceTwoDimensions[0]):
            print("Error - Number of data columns specified for source two does not match specified number of dimensions")
            return
        for dataCol in args.sourceTwoData:
            sourceTwoTupleList.append((args.sourceTwoFiles[0], args.sourceTwoTimestamps[0], dataCol))
    else:
        # pairwise match
        if(len(args.sourceTwoFiles) != args.sourceTwoDimensions):
            print("Error - Number of files specified for source two is not one and does not match number of dimensions specified")
            return
        if(len(args.sourceTwoFiles) != len(args.sourceTwoData)):
            print("Error - NUmber of files specified for source two is not one and doese not mach number of data columns specified")
            return
        for fileName, dataCol in zip(args.sourceTwoFiles, args.sourceTwoData):
            sourceTwoTupleList.append((fileName, args.sourceTwoTimestamps[0], dataCol))
        
    # collect the other arguments
    timeWindowOne = [0, 50000]
    timeWindowTwo = [0, 50000]
    if(args.timeWindowOne is not None):
        if(len(args.timeWindowOne) != 2):
            print("Error - Exactly 2 float arguments must be given for time window one. (-tw1 --timeWindowOne)")
            return
        timeWindowOne = [args.timeWindowOne[0], args.timeWindowOne[1]]
    if(args.timeWindowTwo is not None):
        if(len(args.timeWindowTwo) != 2):
            print("Error - Exactly 2 float arguments must be given for time window two. (-tw2 --timeWindowTwo)")
            return  
        timeWindowTwo = [args.timeWindowTwo[0], args.timeWindowTwo[1]]

    heightOne = 0.25
    heightTwo = 0.25
    if(args.heightOne is not None):
        heightOne = args.heightOne
    if(args.heightTwo is not None):
        heightTwo = args.heightTwo

    windowOne = 1
    windowTwo = 1
    if(args.windowOne is not None):
        windowOne = args.windowOne
    if(args.windowTwo is not None):
        windowTwo = args.windowTwo

    fileName = "taps"
    if(args.outputFile is not None):
        fileName = args.outputFile

    sourceNameOne = "Source One"
    sourceNameTwo = "Source Two"
    if(args.nameOne is not None):
        sourceNameOne = args.nameOne
    if(args.nameTwo is not None):
        sourceNameTwo = args.nameTwo

    # call the tap detector
    detectTaps(sourceOneList=sourceOneTupleList, 
               sourceTwoList=sourceTwoTupleList, 
               timeWindowOne=timeWindowOne, 
               timeWindowTwo=timeWindowTwo,
               heightOne=heightOne,
               heightTwo=heightTwo,
               windowOne=windowOne,
               windowTwo=windowTwo,
               outputFile = fileName,
               nameOne=sourceNameOne,
               nameTwo=sourceNameTwo)
    return

if __name__=="__main__":
    main()