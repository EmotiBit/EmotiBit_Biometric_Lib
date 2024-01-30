## Tap Detector
### About
The tap detector is designed to take input from two differnt sources of data and to "match" them together by detecting taps between the two devices. For example, two devices recording at the same time can be tapped against each other. Then, the resulting data files from both devices can be used with the tap detector to find the corresponding taps in either file so that their timestamps can be aligned.

### Command Line Usage
The tap detector can be used with the command line. The tap detector is designed to work whether all dimensions of your data (e.g. X, Y, Z) are in one file or are in multiple files. The following example that is shown uses Emotibit files which store dimensions seperately and a cyton file where all dimensions are in one file:

```$py device_tapdetector.py -sof .\emotibit_AX.csv .\emotibit_AY.csv .\emotibit_AZ.csv -sod 3 -sot LocalTimestamp -soa AX AY AZ -stf .\cyton.csv -std 3 -stt " Timestamp" -sta " Accel Channel 0" " Accel Channel 1" " Accel Channel 2" -tw1 0 10```

In the above example, the three EmotiBit files are provided and correspondingly, 3 data columns are provided. Only one timestamp column is provided and it is expected to be the same across all files for source one. Additionally, one cyton file is provided and then the data columns are provided.

**If you use more than one data input file, you must provide the explicit file for each data column** This means that if you were to provide two files, such as ```.\emotibit_AX .\emotibit_AYZ``` you could not then specify three data columns such as ```AX AY AZ```. Instead you would need to write ```.\emotibit_AX .\emotibit_AYZ .\emotibit_AYZ``` and then provide the corresponding columns: ```AX AY AZ```. In other words, when more than one file is provided, the tap detector will assume that each file only provides one dimension of data.

### All Arguments:
#### Required Arguments:
- -sof --sourceOneFiles **REQUIRED** One or more files containing the data from source one.
- -sod --sourceOneDimensions **REQUIRED** A single integer indicating the number of dimensions of data in source one.
- -sot --sourceOneTimestamps **REQUIRED** One string indicating the name of the timestamp column in the source one file(s).
- -soa --sourceOneData **REQUIRED** One or more strings indicating the name of the column(s) to find the data in. There should be the same number of strings as number of dimensions specified in the ```=sod``` argument
- -stf --sourceTwoFiles **REQUIRED** One or more files containing the data from source two.
- -std --sourceTwoDimensions **REQUIRED** A single integer indicating the number of dimensions of data in source two.
- -stt --sourceTwoTimestamps **REQUIRED** One string indicating the name of the timestamp column in the source two file(s).
- -sta --sourceTwoData **REQUIRED** One or more strings indicating the name of the column(s) to find the data in. There should be the same number of strings as number of dimensions specified in the ```-std``` argument

#### Optional Arguments
- -tw1 --timeWindowOne **OPTIONAL** Two float values to indicate the range of *relative* timestamps that should be processed from source one. Default is 0.0 and 50000.0
- -tw2 --timeWindowTwo **OPTIONAL** Two float values to indicate the range of *relative* timestamps that should be processed from source two. Default is 0.0 and 50000.0
- -h1 --heightOne **OPTIONAL** The height value that is passed to scipy's ```find_peaks``` function for source one. Default is 0.25
- -h2 --heightTwo **OPTIONAL** The height value that is passed to scipy's ```find_peaks``` function for source two. Default is 0.25
