# Scorer Example
## About
The HR scorer example takes in two heart rate signals and provides a measure of how similar they are, along with plotting a graph of the two signals.

To do this, the script will resample both files at the given rate and then will conduct a linear regression, using data one as the dependent variable and data two as the independent variable.

`scorer.py` provides the following metrics for evaluation of signal similarity: 
- Slope: The slope of the line created in the linear regression. An ideal situation would see a slope of 1.
- Intercept: The intercept of the line created in the linear regression. An ideal situation would see an intercept of 0.
- R: The correlation coefficient between the two metrics. If each data point from the two signals are the exact same value for every time stamp, then this value would be 1.
- P: The p-value associated with R.
- err: The standard error value.

`scorer.py` will also output three plots (raw resampled data, scatterplot w/ regression line, and mean-difference plot) to visually compare data.

**Note:** `scorer.py` is capable of comparing any two different signals and providing statistics of how similar they are. This example simply chooses to compare HR signals, but the same process can be applied to any metric.

## Quickstart Usage
### Using `scorer_example.py`
1) Activate the EmotiBit-pyenv environment
    - Follow the instructions [here](https://github.com/EmotiBit/EmotiBit_Biometric_Lib/tree/master/py) to setup Anaconda if you have not done so already
2) Unzip the SampleData.zip file into the `scorer_example` directory
3) Run `python scorer.py` while in the `scorer_example` directory

### Using CLI
`scorer.py` can also be run from command line. The steps on how to do so using the HR data is below.
1) Activate the EmotiBit-pyenv environment
2) Unzip the SampleData.zip file into the `scorer_example` directory
3) Run ```python ../../emotibit/scorer.py -f1 ebhr6_HR_trim.csv -t1 LocalTimestamp -d1 HR -f2 ecgHR6.csv -t2 Timestamp -d2 HR -f 100 -n1 EmotiBit -n2 Cyton -o cyton -l HR```
    - Update the path to `scorer.py` or either of the data files if needed

#### Explanation of Arguments in Example:
- f1: Provides the path to the file of the signal that is being considered the dependent variable in the analysis.
- t1: Provides the column name in the first file that contains the timestamps of the data.
- d1: Provides the column name in the first file that contains the data.
- f2: Provides the path to the file of the signal that is being considred the independent vairable in the analysis.
- t2: Provides the column name in the second file the contains the timestamps of the data.
- d2: Provides the name of the column in the second file the contains all of the data.
- f: Provides the frequency to resample to (in hertz).
- n1: Provides a name for the dependent variable.
- n2: Provides a name for the independent variable.
- o: Provides the plot base name that will be used when saving the images of the plots.
- l: Label for the data being plotted.

### Format of Files
The scorer requires that two files are provided. The files must conform to these requirements:

1. There is a column of data
1. There is a corresponding column of timestamps (should be the same length as the data column)

### Output
The values of the scoring are shown in the terminal and a plot is saved/opened for viewing to validate results. These results can then be put in the README of an algorithm repository so that the algorithm's performance against a "gold standard" device can be evaluated.

### Notes on Scoring Methodology
To score the files, they are first resampled to the specified rate. This rate should be the sampling rate of the slower device to avoid creating precision that does not truly exist.

Then, a linear regression is completed between the two sets of resamped data and statistics are reported.

It should be noted that due to the way that correlation coefficients are calculated, data with low variance tends to have lower R values than data with high variance. (For example, if your HR data is someone sitting still for several minutes as opposed to standing up and sitting down during the recording, then your R value will likely be lower.) Keep this scoring methodology in mind when scoring your own data to ensure that the results you are getting correctly answer the questions you are asking.