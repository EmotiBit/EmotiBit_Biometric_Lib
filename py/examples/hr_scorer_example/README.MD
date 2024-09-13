## HR Scorer
### About
The HR Scorer is designed to take in two heart rate signals and provide a measure of how similar they are. 

To do this, the script will resample both files at the given rate and then will conduct a linear regression, using data one as the dependent variable and data two as the indpendent variable.

The HR Scorer provides the following metrics for evaluation of signal similarity: 
- Slope: The slope of the line created in the linear regression. An ideal situation would see a slope of 1.
- Intercept: The intercept of the line created in the linear regression. An ideal situation would see an intercept of 0.
- R: The correlation coefficient between the two heart rates. If the heart rates are the exact same values for every time stamp, then this value would be 1.
- P: The p-value associated with R.
- err: The standard error value.

### Quickstart Usage
Sample files have been provided in the .zip folder. The example file will work as long as those files are in the same directory as the example file. Here is how the HR scorer can be used with the sample data via CLI:

```py hr_scorer.py -hr1 ebhr6_HR_trim.csv -t1 LocalTimestamp -d1 HR -hr2 ecgHR6.csv -t2 Timestamp -d2 HR -f 100 -n1 EmotiBit -n2 Cyton```

#### Explanation of Arguments in Example:
- hr1: Provides the path to the file of the HR signal that is being considered the dependent variable in the analysis.
- t1: Provides the column name in the first file that contains the timestamps of the HR data.
- d1: Provides the column name in the first file that contains the HR data.
- hr2: Provides the path to the file of the HR signal that is being considred the independent vairable in the analysis.
- t2: Provides the column name in the second file the contains the timestamps of the HR data.
- d2: Provides the name of the column in the second file the contains all of the HR data.
- f: Provides the frequency to resample to (in hertz).
- n1: Provides a name for the dependent variable.
- n2: Provides a name for the independent variable.

### Format of Files
The HR scorer requires that two files are provided. The files must conform to these requirements:

1. There is a column of HR data
1. There is a corresponding column of timestamps (should be the same length as the HR column)

### Output
The values of the scoring are shown in the terminal and two plots are saved/opened for viewing to validate results.

### Notes on Scoring Methodology
To score the files, they are first resampled to the specified rate. This rate should be the sampling rate of the slower device to avoid creating precision that does not truly exist.

Then, a linear regression is completed between the two sets of resamped data and statistics are reported.

It should be noted that due to the way that correlation coefficients are calculated, data with low variance tends to have lower R values than data with high variance. (For example, if your HR data is someone sitting still for several minutes as opposed to standing up and sitting down during the recording, then your R value will likely be lower.) Keep this scoring methodology in mind when scoring your own data to ensure that the results you are getting correctly answer the questions you are asking.