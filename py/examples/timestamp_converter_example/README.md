## Timestamp Converter
### About
The timestamp converter is designed to take in a file, and the detected taps from that file and the file you wish to align it to, and realign the timestamps of said file.

For example, if you have recorded data on an EmotiBit and a Cyton board simultaneously, you can then use the tapDetector to find the locations of the taps in either file, then use the output from the tapDetector to realign the timestamps in the Cyton file so that the timestamps are lined up with the Emotibit data, allowing for easy comparison across files.

For more information about tapping devices, see the tapDetector example.

### Quickstart Usage
Sample files have been provided, here is how the timestamp converter CLI can be used with the sample data:

```py timestamp_converter.py -tf1 sourceOneTaps.csv -dc1 LocalTimeStamp -tf2 sourceTwoTaps.csv -dc2 LocalTimeStamp -f cytonhr2.txt -fc ' Timestamp' -o ConvertedFile.csv```

#### Explanation of Arguments in Example:
- tf1: Provides the path to the first file containing tap information.
- dc1: Provides the column name with the timestamps of the taps in the first file.
- tf2: Provides the path to the second file containing tap information.
- dc2: Provides the column name with the timestamps of the taps in the second file.
- f: Provides the name of the file to convert.
- fc: Provides the column name in the file to convert that should be conveted.
- o: Provides the name of the output (converted) file.

For a full list of available arguments and their usages, run the timestamp converter with the -h flag.

### Format of Tap Files
As noted, the timestamp converter requires two tap files to be provided. The first tap file should contain the taps from the time domain that you want to convert to, and the second tap file should contain the taps from the time domain you want to convert from. 

For example, if you wanted to align a Cyton file to an Emotibit data, the first tap file would hold the tap information from the EmotiBit, and the second tap file would hold the tap information from the Cyton.

There are 3 requirements for the tapFiles:
1. They contain a column of timestamps where taps occurred.
1. There are the same number of taps in both files.
1. The total number of taps in each file is even.

For more information on performing taps and tap detection, see the tapDetector example.