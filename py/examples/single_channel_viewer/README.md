# Description
- Use this tool to view a single data stream from multiple recordings. The example stacks the specified stream from multiple files and plots it into a single plot
- You also have a provision to create different plots, each for a category. The example categorizes on "people". So, therefore, each plot represents multiple recordings form a single person


# About the Tool
## Usage
- This tool is developed and tested in `Spyder`
- Update the root_path with the path to the directory containing the user data. Tested with the following dir. structure
```
database = [
    {
     'name':"Bob",
     'root_path':r'D:\dev\CFL\EmotiBit\data analysis\data_xenbox\Data-20230511T212157Z-001\Data\Bob',
     'data':pd.DataFrame()
     },
    {
     'name':"Diane",
     'root_path':r'D:\dev\CFL\EmotiBit\data analysis\data_xenbox\Data-20230511T212157Z-001\Data\Diane',
     'data':pd.DataFrame()
     },
.
.
.
```
```
Data
├── Bob
│   ├── 2023-04-16_11-50-07-982348
│   │   ├── 2023-04-16_11-50-07-982348_EA.csv
│   │   └── 2023-04-16_11-50-07-982348_AX.csv
│   └── 2023-04-16_15-42-28-096912
│       ├── 2023-04-16_15-42-28-096912_EA.csv
│       └── 2023-04-16_15-42-28-096912_AX.csv
└── Diane
    ├── 2023-04-16_11-50-45-628347
    │   ├── 2023-04-16_11-50-45-628347_EA.csv
    │   └── 2023-04-16_11-50-45-628347_AX.csv
    └── 2023-04-16_15-43-36-324819
        ├── 2023-04-16_15-43-36-324819_EA.csv
        └── 2023-04-16_15-43-36-324819_AX.csv
```
- Specify the directory for the output file
  - `output_dir = r'D:\dev\CFL\EmotiBit\data analysis\data_xenbox\Data-20230511T212157Z-001\Data'`
- 
## Add comments post-hoc
- Users have hte provision to add comments to annotate the data being plotted.
- To annotate, click anywhere within the plot. This marks the location on the x-axis. 
- After clicking, press `c`. A dialog box will appear asking for user comment.
- add comment and press enter.
- The comment will be stored in a file, with tis location specified in the code.
![image](https://github.com/EmotiBit/EmotiBit_Biometric_Lib/assets/31810812/c572beb5-a9c6-4416-b982-10735058ad20)

## Known Issues
- The individual plots do not yet have auto y-scale. This causes some issues with data analysis as plots do not resize.
- Some searching suggests there is no "easy fix".
- A fix needs to be implemented using plot callbacks and is being currently worked on.
  - https://stackoverflow.com/questions/53326158/interactive-zoom-with-y-axis-autoscale
