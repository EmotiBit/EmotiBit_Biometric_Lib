## Overview
The Python DataViewer is a tool developed to help visualize the data captured on EmotiBit. It is an interactive tool where you can view the entire data at once, zoom in and out of any part in the time series, compare data accross different channels and get an overall sense of the data captured.
![][EmotiBit-PythonDataViewer]

## Getting Started

### Requirements

- Make sure that the `emotibit-env` Python virutal environment is activated
  - Follow the instructions [here](../../README.md) to setup `emotibit-env` if you have not done so already

- Put all parsed EmotiBit data files in a directory. The path to the directory and the file basename will be passed to `dataviewer_example.py`

### Steps to load data

- While in the activated `venv`, run `python dataviewer_example.py -p <path to files> -n <file basename w/o extension>` while in the `dataviewer_example` directory
- For example, if your data to be visualized looks like the image shown below:
  - ![][Example-dataDirectory]
  - Then the command would be `python dataviewer_example.py -p "C:\Users\cfl\Documents\EmotiBit\DataAnalysis\exampleData" -n "2021-04-26_16-59-17-085213"`
- A plot showing all the data from the EmotiBit should now be shown

### Command Line Options

- `-u` if passed, will lead to green lines to display where there are user notes
- `-t` is followed by space separated tag names (ex. EA, PI, PR). If a tag name follows `-t`, then DC markers (instances where the sensor data goes out of bounds) will not be plotted for that data tag

[EmotiBit-PythonDataViewer]: ../../../assets/PythonDataViewer.jpg "EmotiBit-PythonDataViewer"
[Example-dataDirectory]: ../../../assets/Example-dataDirectory.png "Example-dataDirectory"
