import sys
import os

from emotibit.scorer import resample, score, plot_both

"""
In this example detected HR from ECG data and EmotiBit HR data are compared and scored
"""

def main():
    # first, we need to resample the data, the function will read the files and do that for us
    ebResampled, cyResampled = resample("ebhr6_HR_trim.csv", "LocalTimestamp", "HR", "ecgHR6.csv", "Timestamp", "HR", 100)
    # then, score them
    slope, intercept, r, rho, tau, p, std_err = score(ebResampled, "HR", cyResampled, "HR", None, "EmotiBit", "Cyton")
    # and print results
    print("Slope: ", slope, "\nIntercept: ", intercept, "\nR: ", r, "\nP: ", p, "\nerr: ", std_err)

if __name__ == "__main__":
    main()