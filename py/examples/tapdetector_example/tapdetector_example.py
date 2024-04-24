"""
Created on Mon Jan 29 2024
An example of how to use the tap detector functions in code.
CLI usage is also supported and documentation can be found in README
"""

from tapdetector import detectTaps

"""
In this example EmotiBit files are used.
Emotibit stores the 3 dimensions of acceleration data in 3 separate files.
This file will give an example of how to use the tap detector in this situation

Additional information about using the tap detector can be found using CLI usage
via the -h command when running tapdetector.py:
./py tapdetector.py -h
"""


def main():

    source_list = [
        (".\emotibit4_AX.csv", "LocalTimestamp", "AX"),
        (".\emotibit4_AY.csv", "LocalTimestamp", "AY"),
        (".\emotibit4_AZ.csv", "LocalTimestamp", "AZ"),
        ]

    detectTaps(source_list=source_list,
               time_window=[20, 40],
               heightone=0.25,
               window=1,
               output_file="taps",)


if __name__ == "__main__":
    main()
