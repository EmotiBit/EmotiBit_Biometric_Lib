"""
Created on Mon Jan 29 2024
An example of how to use the tap detector functions in code.
CLI usage is also supported and documentation can be found in README
"""

from emotibit.device_tapdetector import detectTaps

"""
In this example EmotiBit files is used and a Cyton file is used.
Emotibit stores the 3 dimensions of acceleration data in 3 separate files.
Cyton stores all of the dimensions in a single file.
This file will give an example of how to use the tap detector in this situation

The input to the tap detector function is two lists of information on where the function can find the column information
They are structured as lists of tuples as follows:
[(file1, timeStampCol, dataCol),(file2, timeStampCol, dataCol)...],[(file1, timeStampCol, dataCol)...]

The first list of tuples is for all the information for the first data source.
The second list of tuples is for all the information for the second data source.
"""

sourceOneList = [(".\emotibit_AX.csv", "LocalTimestamp", "AX"),
                 (".\emotibit_AX.csv", "LocalTimestamp", "AX")]

sourceTwoList =  [(".\cyton.csv", " Timestamp", " Accel Channel 0"),
                 (".\cyton.csv", " Timestamp", " Accel Channel 1"),
                 (".\cyton.csv", " Timestamp", " Accel Channel 2")]

detectTaps(sourceOneList=sourceOneList, sourceTwoList=sourceTwoList)