"""
Created on Mon Jan 29 2024
An example of how to use the tap detector functions in code.
CLI usage is also supported and documentation can be found in README
"""

from tapdetector import detectTaps

"""
In this example EmotiBit files are used and a Cyton file is used.
Emotibit stores the 3 dimensions of acceleration data in 3 separate files.
Cyton stores all of the dimensions in a single file.
This file will give an example of how to use the tap detector in this situation

Additional information about using the tap detector can be found using CLI usage
via the -h command when running device_tapdetector.py:
./py device_tapdetector.py -h
"""

def main():

    sourceOneList = [(".\emotibit4_AX.csv", "LocalTimestamp", "AX"),
                    (".\emotibit4_AY.csv", "LocalTimestamp", "AY"),
                    (".\emotibit4_AZ.csv", "LocalTimestamp", "AZ")]

    sourceTwoList =  [(".\cyton4.txt", " Timestamp", " Accel Channel 0"),
                    (".\cyton4.txt", " Timestamp", " Accel Channel 1"),
                    (".\cyton4.txt", " Timestamp", " Accel Channel 2")]

    detectTaps(sourceOneList=sourceOneList, 
            sourceTwoList=sourceTwoList,
            timeWindowOne=[20, 40],
            timeWindowTwo=[25, 35],
            heightOne=0.25,
            heightTwo=0.07,
            windowOne=1,
            windowTwo=13,
            outputFile="taps",
            nameOne="EmotiBit",
            nameTwo="Cyton")
    
if __name__ == "__main__":
    main()