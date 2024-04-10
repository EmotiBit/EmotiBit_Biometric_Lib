## ECG HR Detector
### About
The ECG HR Detector is designed to take in raw ECG data and determine the HR from this data. After detecting the HR, it will plot the data against another HR signal for comparison. Additionally, the detected HR file is saved.

### Quickstart Usage
Sample data has been provided and can be used with the ECG HR Detector with the following command:

```py ecgHR_detector.py -ecg cytonHR2_newTime.csv -ecgCol ' EXG Channel 0' -ecgt ' Timestamp' -hr ebhr2_HR.csv -hrCol HR -hrt LocalTimestamp```

#### Explanation of Arguments in Example
- ecg: Provides the file with the ECG Data
- ecgCol: The column name in the ECG file containing the ECG Data
- ecgt: The column name in the ECG file containing timestamps
- hr: Provides the filename with HR data
- hrCol: Provides the column name in the HR file with the HR data
- hrt: Provides the column name in the HR file containing timestamps

For a full list of available arguments and their usages, run the ecgHR_detector with the -h argument.

### Usage Notes
- Ensure that the timestamps between the ECG file and HR have already been aligned. ECG HR detection will still work if they are not aligned, but the comparison plot will not be readable if they have not been aligned. If the data needs to be aligned, see the timestampConverter example.
- The output file will not have a consistent frequency. Timestamps with HR data will be provided, but the spacing between them will not be consistent.