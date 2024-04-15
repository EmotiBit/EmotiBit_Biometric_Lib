# -*- coding: utf-8 -*-
"""
timestamp_coverter.py
A script that will take two data file (ex. EmotiBit and Cyton) and convert the second file to the EmotiBit timestamps
Requires the input of detected taps
"""
import pandas as pd
import argparse

def calculateSlope(sourceOneFirstTaps, sourceOneSecondTaps, sourceTwoFirstTaps, sourceTwoSecondTaps):
    """
    @input souceOneFirstTaps: List of timestamps of the first set of taps from source one
    @input sourceOneSecondTaps: List of timestamps of the second set of taps from souce once
    @input sourceTwoFirstTaps: List of timestamps of the first set of taps from source two
    @input sourceTwoSecondTaps: List of timestamps of the second set of taps from source two

    Calculates the slope by averaging the points in the front and back and then using equation of linear line.
    Source one is the intended output (Emotibit most likely) - and the "y" value
    Source two is the intended input - and the "x" value

    @output Returns the slope of the line created by the average of the two points provided.
    """
    # ensure matching length of taps
    if(len(sourceOneFirstTaps) != len(sourceTwoFirstTaps)):
        print("Error - Length of first taps between source one and source two does not match: ", len(sourceOneFirstTaps), len(sourceTwoFirstTaps))
        return
    if(len(sourceOneSecondTaps) != len(sourceTwoSecondTaps)):
        print("Error - Length of second taps between source one and source two does not match: ", len(sourceOneSecondTaps), len(sourceTwoSecondTaps))
        return

    # get values to put into a standard linear slope formula
    y1 = sum(sourceOneFirstTaps) / len(sourceOneFirstTaps)
    x1 = sum(sourceTwoFirstTaps) / len(sourceTwoFirstTaps)
    y2 = sum(sourceOneSecondTaps) / len(sourceOneSecondTaps)
    x2 = sum(sourceTwoSecondTaps) / len(sourceTwoSecondTaps)

    return ((y2 - y1) / (x2 - x1))

def calculateB(slope, sourceOneFirstTaps, sourceTwoFirstTaps):
    """
    @input slope: a value for the slope of the line
    @input sourceOneFirstTaps: the list of tap times from source one for the first set of taps
    @input sourceTwoFirstTaps: the list of tap times from source two for the first set of taps

    Calculates the "b" in y = mx + b, given y, m, and x. Use after using the calculateSlope function
    y = mx + b ===> y - mx = b 

    @output Returns a single float value, b
    """
    # ensure same length
    if(len(sourceOneFirstTaps) != len(sourceTwoFirstTaps)):
        return

    y = sum(sourceOneFirstTaps) / len(sourceOneFirstTaps)
    x = sum(sourceTwoFirstTaps) / len(sourceTwoFirstTaps)
    return y - slope * x

def updateTimeStamps(df, columnName, m, b):

    """
    @input df: The df which is to have its timestamps converted
    @input columname: The name of the column in the df which holds the timestamps that are to be converted
    @input m: The slope for the linear conversion
    @input b: The y-intercept for the linear conversion

    Converts the timestamps of a df given a slope and intercept using y = mx + b 

    @output Returns the df with the timestamps in column name as the output of y = mx + b
    """
    df[columnName] = (df[columnName] * m) + b
    return df

def convertTimestamps(sourceOneFirstTaps, sourceOneSecondTaps, sourceTwoFirstTaps, sourceTwoSecondTaps, dfToConvert, columnName, outputFile = None):
    """
    @input sourceOneFirstTaps: A list of times of the taps from file one for section one of taps
    @input sourceOneSecondTaps: A list of times of the taps from file one for section two of taps
    @input sourceTwoFirstTaps: A list of times of the taps from file two for section one of taps
    @input sourceTwoSecondTaps: A list of times of the taps from file two for section two of taps
    @input dfToConvert: A df of the file that needs to be converted
    @input columnName: The name of the df to convert
    @input outputFile: The name of the file to write the new df to. (Optional: If not provided, the df will only be returned from this function but not written to file)

    @output Returns the dfToConvert, after converting the timestamps to the new values.
    """
    slope = calculateSlope(sourceOneFirstTaps, sourceOneSecondTaps, sourceTwoFirstTaps, sourceTwoSecondTaps)
    b = calculateB(slope, sourceOneFirstTaps, sourceTwoFirstTaps)
    print("==== INFO ====")
    print("SLOPE: ", slope)
    print("Y-INTERCEPT: ", b)
    print("==== END INFO ====")
    dfToConvert = updateTimeStamps(dfToConvert, columnName, slope, b)

    if(outputFile is not None):
        dfToConvert.to_csv(outputFile)
    return dfToConvert

def main():
    """
    Provides the command line interface of the timestamp converter
    Note that by importing this file the convertTimeStamps() function can be directly used without the CLI
    The convertTimeStamps() function returns a df so CLI usage can be optional
    """
    print("==== TIMESTAMP CONVERTER =====")
    parser = argparse.ArgumentParser()
    parser.add_argument("-tf1", "--tapfile1", action = "store", type = str, nargs = 1, help = "Path to the .csv file containing the taps for source one.")
    parser.add_argument("-dc1", "--datacolumn1", action = "store", type = str, nargs = 1, help = "Name of the data column in the first file.")
    parser.add_argument("-tf2", "--tapfile2", action = "store", type = str, nargs = 1, help = "Path to the .csv file containing the taps for source two.")
    parser.add_argument("-dc2", "--datacolumn2", action = "store", type = str, nargs = 1, help = "Name of the data column in the second file.")
    parser.add_argument("-f", "--fileToConvert", action = "store", type = str, nargs = 1, help = "File that should be converted to new timestamps (should align with the taps for file two).")
    parser.add_argument("-fc", "--fileToConvertColumn", action = "store", type = str, nargs = 1, help = "Name of the column that should be converted to new timestamps in the file to convet.")
    parser.add_argument("-o", "--output", action = "store", type = str, nargs = "?", help = "Output file name. (Optional: If not provided, df is returned and not written to a file).")
    args = parser.parse_args()
    tapsOne = pd.read_csv(args.tapfile1[0])[args.datacolumn1[0]].to_list()
    tapsTwo = pd.read_csv(args.tapfile2[0])[args.datacolumn2[0]].to_list()
    
    if(len(tapsOne) % 2 != 0):
        print("Error - The number of taps should be even. Source one has this many taps: ", len(tapsOne))
        return
    if(len(tapsTwo) % 2 != 0):
        print("Error = The number of taps should be even. Source two has this many taps: ", len(tapsTwo))
        return

    halfOftapsOne = int(len(tapsOne) / 2)
    halfOftapsTwo = int(len(tapsTwo) / 2)
    fileToConvert = pd.read_csv(args.fileToConvert[0])
    outputFileName = None
    if(args.output is not None):
        outputFileName = args.output

    df = convertTimestamps(tapsOne[:halfOftapsOne], tapsOne[halfOftapsOne:], tapsTwo[:halfOftapsTwo], tapsTwo[halfOftapsTwo:], fileToConvert, args.fileToConvertColumn[0], outputFileName)
    print("===== FINISHED! =====")
    return df

if __name__ == "__main__":
    main()