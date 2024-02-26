## Tap Detector
### About
The tap detector is designed to take input from two differnt sources of data and to "match" them together by detecting taps between the two devices. For example, two devices recording at the same time can be tapped against each other. Then, the resulting data files from both devices can be used with the tap detector to find the corresponding taps in either file so that their timestamps can be aligned. Data smoothing is done using a hann filter, whose window is specified by the user for each source of data.

Sample data is included in a .zip file to use. The following command/parameters works well for the sample data provided. Note that the sample data includes noise at the end.
```py .\py\emotibit\device_tapdetector.py -sof .\emotibit5_AX.csv .\emotibit5_AY.csv .\emotibit5_AZ.csv -sod 3 -sot LocalTimestamp -soa AX AY AZ -stf .\cyton5.txt -std 3 -stt " Timestamp" -sta " Accel Channel 0" " Accel Channel 1" " Accel Channel 2" -n1 EmotiBit -n2 Cyton -o taps5 -w2 13 -h2 0.08```

### Command Line Usage
The tap detector is designed to be used with the command line. The tap detector is designed to work whether all dimensions of your data (e.g. X, Y, Z) are in one file or are in multiple files. The following example that is shown uses Emotibit files which store dimensions seperately and a cyton file where all dimensions are in one file:

```$py device_tapdetector.py -sof .\emotibit_AX.csv .\emotibit_AY.csv .\emotibit_AZ.csv -sod 3 -sot LocalTimestamp -soa AX AY AZ -stf .\cyton.csv -std 3 -stt " Timestamp" -sta " Accel Channel 0" " Accel Channel 1" " Accel Channel 2" -tw1 0 10 -n1 EmotiBit -n2 Cyton -w1 1 -w2 13 -h1 0.1 -h2 0.4```

In the above example, the three EmotiBit files are provided and correspondingly, 3 data columns are provided. Only one timestamp column is provided and it is expected to be the same across all files for source one. Additionally, one cyton file is provided and then the data columns are provided.

**If you use more than one data input file, you must provide the explicit file for each data column.** This means that if you were to provide two files, such as ```.\emotibit_AX .\emotibit_AYZ``` you could not then specify three data columns such as ```AX AY AZ```. Instead you would need to write ```.\emotibit_AX .\emotibit_AYZ .\emotibit_AYZ``` and then provide the corresponding columns: ```AX AY AZ```. In other words, when more than one file is provided, the tap detector will assume that each file only provides one dimension of data.

### Completing the Tapping Procedure:
A prerequisite to using the tap detector is the proper collection of data. This section outlines the methods that should be use to collect the data.

Data should be collected from two sources simultaneously. The following is a set of generic steps to take for data collection of any two devices to use in the tap detector, you may need to take additional steps depending on the devices you are using and the best practices for using those devices.

1. **Setup your Environment(s)** - Ensure that you have a working environment for both devices you plan to use that allows you to record data.
1. **Open recording software(s)** - Start the data collection software for each device. Ensure that both devices have properly connected to their respective data collection software and are properly configured.
1. **Begin data recording** - Begin recording data on both devices. It is recommened to try and begin recording on both devices simultaneously, as this will make validation that the files have lined up properly easier, but it is not strictly required.
1. **Get devices into position** - Pick up both devices and hold them still, allowing the data settle to a baseline for at least 30 seconds. Do not make any sudden movements during this time.
1. **Perform the taps** - Quickly and firmly hit the devices against each other 3 times, making contact approximately once per second. The taps need to be strong enough to make a noticeable "spike" in the accelerometer data. The more pronounced and clear the taps are as compared to the baseline data and other noise that may be surrounding the taps, the better the tap detector will be able to identify the taps. **WARNING: While hitting the devices together strongly is important, take care to not damage the devices. For example, tap a connector on one board against the side of another board, avoid hitting chips or other electronics on either board to prevent damage.**
1. **Return to Baseline** - Allow the data to return to baseline again by holding the devices still for another 30 seconds. Steps 4 and 5 may be repeated as necessary to ensure sufficient data collection. It is recommened to collect at least 2 sets of taps.
1. **End data recording** - End the recording on both devices. Perform any processing necessary on the data. Some devices may record data in a format the can be immediately used, but some devices (such as EmotiBit) require a parsing/processing step. The tap detector requires that the data being input has the Acceleration Data and Timestamps available. 

### All Arguments:
- The complete list of arguments and their descriptions can be found by running the tapDetector with the -h flag. 
