# Tap Detector

## About
The tap detector is designed to take input from two different sources of data and to "align" them together by detecting taps between the two devices. For example, two devices recording at the same time can be tapped against each other. Then, the resulting data files from both devices can be used with the tap detector to find the corresponding taps in either file so that their timestamps can be aligned. Data smoothing is done using a hann filter, whose window is specified by the user for each source of data.

Within this directory, there are three examples:

```tapdetector_example.py``` which shows how to use the tapDetector in full.

```tapdetector_extractdata_example.py``` which shows how to use the individual ```extract_data()``` function included.

```tapdetector_loaddata_example.py``` which shows how to use the individual ```load_data()``` function included.

The tapdetector was written and tested using a specific anaconda environment, see the quick start example for more information on finding and using this environment.

## Usage

### Quick start example using sample data
There is sample data to use with the tapDetector provided in ```ExampleDataForTapDetector.zip```. This section will show you how to use that data in the tapDetector.

After extracting the data from the .zip file, ensure that all the sample data files are your working directory. Then, ensure that you have enabled the ```EmotiBit-pyenv.yml``` anaconda environment. This environment can be found in the ```EmotiBit-pyenv.yml``` file found [in EmotiBit_Biometric_Lib/py/anaconda-environments/](../../anaconda-environments).

Once you have extracted the sample data and activated your anaconda environment, you can run the tapdetector with the sample data with the following command (ensure that your current working directory is the same as where the sample data files are located, we recommend making this somewhere that is **not** within the EmotiBit repository to clutter/conflicting file names):

```python <path-to-tapdetector.py> -sof .\emotibit5_AX.csv .\emotibit5_AY.csv .\emotibit5_AZ.csv -sod 3 -sot LocalTimestamp -soa AX AY AZ -stf .\cyton5.txt -std 3 -stt " Timestamp" -sta " Accel Channel 0" " Accel Channel 1" " Accel Channel 2" -n1 EmotiBit -n2 Cyton -o taps5 -w2 13 -h2 0.08```

Note: Not all python installations on all platforms use the ```python``` command, if using ```python``` does not work on your system, use ```py``` or whatever the appropriate command is for your system.

An explanation of arguments in this example:
- ```-sof .\emotibit5_AX.csv .\emotibit5_AY.csv .\emotibit5_AZ.csv``` is used to specify the names of the files where the data from source one can be found. 
- ```-sod 3``` is used to specify that there are three dimensions of data in source one.
- ```-sot LocalTimestamp``` is used to indicate the name of the timestamp column in the source one files.
- ```-soa AX AY AZ``` is used to provide the names of the columns of the data in each of the files provided.
- ```stf .\cyton5.txt``` is used to specify the filename where the source two data can be found.
- ```-std 3``` is used to indicate that there are three dimensions of data in source two.
- ```-stt " Timestamp"``` is used to indicate the name of the timestamp in the source two file.
- ```-sta " Accel Channel 0" " Accel Channel 1" " Accel Channel 2"``` is used to provie the names of the columns of data in the file provided.
- ```-n1 EmotiBit``` is used to give a name to source one, shown on the validation plot.
- ```-n2 Cyton``` is used to give a name to source two, shown on the validation plot.
- ```-o taps5``` is used to give a filename to the validation plot. An extension is not given as it is automatically appended.
- ```-w2 13``` is used to set the size of the hann window for filtering in source two.
- ```-h2 0.08``` is used to set the height threshold for tap detection for source two.


The above command was tuned to work well with the files provided. After running the tapdetector, you will have 3 outputed files in your working directory: a .png showing the tap detection, and two .csv files recording the tap information.

### CLI Options

To access the full list of command line options available when using the tapDetector, run the tapDetector using the -h flag.

### Notes on data compatibility

To be more accommodating to different devices, the tapdetector allows different input sources to have their data spread across different numbers of files. All files from one source must share the same name for their timestamp column. 

For the best outcome, it is best that you data is padded with 30 seconds between sets of taps for data to return to baseline. At least 2 sets of taps are recommended.

Additonally, ensure that you have already performed any processing necessary on the data. Some devices may record data in a format the can be immediately used, but some devices (such as EmotiBit) require a parsing/processing step. The tap detector requires that the data being input has the Acceleration Data and Timestamps available, and that the first row in each file is the headers of the data.

This section details how to handle different situations with the tapdetector:

### All my dimensions of data are in one file
- Provide **exactly** one filename
- Provide **exactly** one timestamp column name
- Provide the correct number of dimensions
- Provide a matching number of data column names

Example: ```-stf .\cyton.csv -std 3 -stt " Timestamp" -sta " Accel Channel 0" " Accel Channel 1" " Accel Channel 2"```

In this situation, the ```cyton.csv``` file holds all of the columns of data, ``` Accel Channel 0```, ``` Accel Channel 1```, ``` Accel Channel 2``` and ``` Timestamp```.

### All my dimensions of data are spread across multiple files
- Provide the correct number of dimensions
- Provide the filename of every dimension*
- Provide the data column name of every dimensions
- Provide **exactly** one timestamp column name

*This means that you need to explicitly say which filename is needed for each column, even if this means providing the same filename more than once.

Example: ```-sof .\emotibit_AX.csv .\emotibit_AY.csv .\emotibit_AZ.csv -sod 3 -sot LocalTimestamp -soa AX AY AZ```

In this situation, the ```emotibit_AX.csv``` file holds the ```AX``` column, the ```emotibit_AY.csv``` file holds the ```AY``` column, and the ```emotibit_AZ.csv``` holds the ```AZ``` file. All files contain the ```LocalTimestamp``` column that has the timestamps of the data.

### I have two files, but 3 columns of data
This is handled the same way as the above situation "All my dimensions of data are spread across multiple files". Here we will provide an explicit example of how a command would look like in this situation:

Example: ```-sof .\emotibit_AX_AY.csv .\emotibit_AX_AY.csv .\emotibit_AZ.csv -sod 3 -sot LocalTimestamp -soa AX AY AZ```

In this situation, the ```AX``` and ```AY``` columns are both held in the ```emotibit_AX_AY.csv``` file and the ```AZ``` column is held in the ```emotibit_AZ.csv``` file. 

## Completing Your Own Experiment with the Tap Detector
This section gives an overview of a full experiment using the tapdetector and properly collecting data.

Data should be collected from two sources simultaneously. The following is a set of generic steps to take for data collection of any two devices to use in the tap detector, you may need to take additional steps depending on the devices you are using and the best practices for using those devices.

1. **Setup your devices** - Ensure that you have two devices to record data with that are properly setup and ready to be used for data collection.
1. **Open recording software(s)** - Start the data collection software for each device. Ensure that both devices have properly connected to their respective data collection software and are properly configured.
1. **Begin data recording** - Begin recording data on both devices. It is recommened to try and begin recording on both devices simultaneously, as this will make validation that the files have lined up properly easier, but it is not strictly required.
1. **Get devices into position** - Pick up both devices and hold them still, allowing the data settle to a baseline for at least 30 seconds. Do not make any sudden movements during this time.
1. **Perform the taps** - Quickly and firmly hit the devices against each other 3 times, making contact approximately once per second. The taps need to be strong enough to make a noticeable "spike" in the accelerometer data. The more pronounced and clear the taps are as compared to the baseline data and other noise that may be surrounding the taps, the better the tap detector will be able to identify the taps. **WARNING: While hitting the devices together strongly is important, take care to not damage the devices. For example, tap a connector on one board against the side of another board, avoid hitting chips or other electronics on either board to prevent damage.**
1. **Return to Baseline** - Allow the data to return to baseline again by holding the devices still for another 30 seconds. Steps 4 and 5 may be repeated as necessary to ensure sufficient data collection. It is recommened to collect at least 2 sets of taps.
1. **End data recording** - End the recording on both devices. Perform any processing necessary on the data. Some devices may record data in a format the can be immediately used, but some devices (such as EmotiBit) require a parsing/processing step. The tap detector requires that the data being input has the Acceleration Data and Timestamps available. 

Now that you have your data recorded, you can use them in the tapdetector as shown in the above sections.