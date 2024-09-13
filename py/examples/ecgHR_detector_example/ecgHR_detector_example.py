"""
Created on Mar 13 2024
An example of how to use the ECG HR detector functions in code.
CLI usage is also supported and documentation can be found by using -h
"""

from emotibit.ecgHR_detector import detect_hr

"""
This example calls the detectHR function using a cyton file that has had
its timestamps aligned and an emotibit file with HR to compare the HR detection results to.

For more information see the README
"""

def main():

    hr = detect_hr("cytonHR2_newTime.csv",
                  " EXG Channel 0",
                  " Timestamp",
                  "ebhr2_HR.csv",
                  "HR",
                  "LocalTimestamp",
                  250,
                  "ecgHR.csv",
                  "detectedHR.png")
    print(hr)
    
if __name__ == "__main__":
    main()