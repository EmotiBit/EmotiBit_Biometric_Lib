"""
Created on Mar 25 2024
An example of how to use the timestamp converter functions in code.
CLI usage is also supported and documentation can be found by using -h
"""

from emotibit.hr_scorer import resample, score
import pandas as pd

"""
In this example detected HR from ECG data and EmotiBit HR data are compared and scored
"""

def main():

    # first, we need to resample the data, the function will read the files and do that for us
    ebResampled, cyResampled = resample("ebhr6_HR_trim.csv", "LocalTimestamp", "ecgHR6.csv", "Timestamp", 100)
    # then, score them
    slope, intercept, r, p, err = score(ebResampled, "HR", cyResampled, "HR", None, "EmotiBit", "Cyton")
    # and print results
    print("Slope: ", slope, "\nIntercept: ", intercept, "\nR: ", r, "\nP: ", p, "\nerr: ", err)
    
    
if __name__ == "__main__":
    main()