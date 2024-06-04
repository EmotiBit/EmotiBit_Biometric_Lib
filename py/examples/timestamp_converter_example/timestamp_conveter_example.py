"""
Created on Mar 13 2024
An example of how to use the timestamp converter functions in code.
CLI usage is also supported and documentation can be found by using -h
"""

from emotibit.timestamp_converter import convertTimestamps
import pandas as pd

"""
In this example a Cyton file has its timestamps converted to line up with an 
Emotibit's timestamps. 

Before using the timestamp converter, the files were run through the tapDetector,
which produced the sourceOneTaps and the sourceTwoTaps files. For more usage information,
see the README.
"""

def main():

    # read the tap files and the file to convert
    # reads in the column from each source and converts it to a list
    tapsOne = pd.read_csv("sourceOneTaps.csv")['LocalTimeStamp'].to_list()
    tapsTwo = pd.read_csv("sourceTwoTaps.csv")['LocalTimeStamp'].to_list()
    fileToConvert = pd.read_csv("cytonhr2.txt")

    # programatically determine the halfway point through the tap files
    halfOftapsOne = int(len(tapsOne) / 2)
    halfOftapsTwo = int(len(tapsTwo) / 2)

    # convert the file
    df = convertTimestamps(tapsOne[:halfOftapsOne], 
                           tapsOne[halfOftapsOne:], 
                           tapsTwo[:halfOftapsTwo], 
                           tapsTwo[halfOftapsTwo:], 
                           fileToConvert, 
                           ' Timestamp', 
                           'ConvertedFile.csv')
    print(df)
    
if __name__ == "__main__":
    main()