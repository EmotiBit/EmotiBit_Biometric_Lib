# Full Experiment Example
This repository contains several different scripts for working with biometric signals from EmotiBit (and other devices) to create derivative metrics and to compare signals to each other to see how similar they are.

This README describes the full process of conducting an experiment between two devices all the way to scoring how similar the heart rate readings from the devices are to each other.

## Data Collection
The first step is data collection. Collection should be done on two devices at the same time, tapping the devices against each other at the beginning and the end of the session so that the data from the devices can be properly aligned.

You can find a detailed description on performing data collection [here](../device_tapdetector_example/README.md#completing-the-tapping-procedure).

At the end of your data collection process, you should have one set of acceleration and heart data from each device, in a .csv format. Ensure that any required parsing or other preprocessing that might be necessary to use the data is completed before moving to the next step.

## Tap Detection
The second step is tap detection. The taps that you performed in the data collection step need to be detected and their timestamps recorded so that they can be used in a later step to align the data between devices.

Tap detection is done with the tap detector script and the files collected during your data collection. Tap detector directions can be found [here](../device_tapdetector_example/README.md)

At the end of this step, you should now have two tap files. In each file, there should be a column of the timestamp when taps hapenned. There should be the same amount of timestamps as taps that you performed, and the number of taps in each file should be the same.

## Timestamp Conversions
Now that you have your raw data and the tap data, you can realign the timestamps of one of your data sources to the other source. To do this you will use the tap files and the raw data files.

You can find detailed instructions for timestamp converting [here](../timestamp_converter_example/README.md)

At the end of this step, you should now have one of your raw data sources rewritten with new timestamps so that it is lined up with your other data source.

## ECG HR Detection
This step only applies if your data is ECG data that has not had HR detected from it yet. If all of your data is already HR data, you can skip this step.

If you have ECG data that needs to have HR detected from it, you can do so using the ecgHR_detector. You can find detailed instructions on using it [here](../ecgHR_detector_example/README.md).

At the end of this step, you should now have HR data with timestamps for any ECG data you had.

## HR Scoring
In this final step, data is resampled to a consistent rate and then an analysis between the two files is done. You will need two HR data files for this step.

The process for using the hr_scorer is shown [here](../hr_scorer_example/README.MD).

At the end of this step you will have multiple metrics for comparing the similarity of the two HR files.