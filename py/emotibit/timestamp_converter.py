# -*- coding: utf-8 -*-
"""
timestamp_coverter.py
A script that will take two data files (ex. EmotiBit and Cyton)
and convert the second file to the EmotiBit timestamps.
Requires the input of detected taps
"""
import argparse
import pandas as pd


def calculate_slope(source_one_first_taps,
                    source_one_second_taps,
                    source_two_first_taps,
                    source_two_second_taps):
    """
    @input souceOneFirstTaps:
        List of timestamps of the first set of taps from source one
    @input source_one_second_taps:
        List of timestamps of the second set of taps from souce once
    @input source_two_first_taps:
        List of timestamps of the first set of taps from source two
    @input source_two_second_taps:
        List of timestamps of the second set of taps from source two

    Calculates the slope by averaging the points in the front
      and back and then using equation of linear line.
    Source one is the intended output (Emotibit most likely)
      and the "y" value
    Source two is the intended input - and the "x" value

    @output Returns the slope of the line created
      by the average of the two points provided.
    """
    # Ensure matching length of taps.
    if len(source_one_first_taps) != len(source_two_first_taps):
        print("""Error - Length of first taps between
               source one and source two does not match: """,
              len(source_one_first_taps), len(source_two_first_taps))
        return None
    if len(source_one_second_taps) != len(source_two_second_taps):
        print("""Error - Length of second taps between
               source one and source two does not match: """,
              len(source_one_second_taps), len(source_two_second_taps))
        return None

    # Get values to put into a standard linear slope formula.
    y1 = sum(source_one_first_taps) / len(source_one_first_taps)
    x1 = sum(source_two_first_taps) / len(source_two_first_taps)
    y2 = sum(source_one_second_taps) / len(source_one_second_taps)
    x2 = sum(source_two_second_taps) / len(source_two_second_taps)

    return ((y2 - y1) / (x2 - x1))


def calculate_b(slope, source_one_first_taps, source_two_first_taps):
    """
    @input slope:
        a value for the slope of the line
    @input source_one_first_taps:
        the list of tap times from source one for the first set of taps
    @input source_two_first_taps:
        the list of tap times from source two for the first set of taps

    Calculates the "b" in y = mx + b, given y, m, and x.
    Use after using the calculate_slope function.
    y = mx + b ===> y - mx = b

    @output Returns a single float value, b
    """
    # Ensure same length.
    if (len(source_one_first_taps) != len(source_two_first_taps)):
        return

    y = sum(source_one_first_taps) / len(source_one_first_taps)
    x = sum(source_two_first_taps) / len(source_two_first_taps)
    return y - slope * x


def update_time_stamps(df, column_name, m, b):

    """
    @input df: The df which is to have its timestamps converted
    @input columname: The name of the column in the df
      which holds the timestamps that are to be converted
    @input m: The slope for the linear conversion
    @input b: The y-intercept for the linear conversion

    Converts the timestamps of a df given a slope
        and intercept using y = mx + b

    @output Returns the df with the timestamps in
        column name as the output of y = mx + b
    """
    df[column_name] = (df[column_name] * m) + b
    return df


def convert_time_stamps(source_one_first_taps,
                        source_one_second_taps,
                        source_two_first_taps,
                        source_two_second_taps,
                        df_to_convert,
                        column_name,
                        output_file=None):
    """
    @input source_one_first_taps:
        A list of times of the taps from file one for section one of taps
    @input source_one_second_taps:
        A list of times of the taps from file one for section two of taps
    @input source_two_first_taps:
        A list of times of the taps from file two for section one of taps
    @input source_two_second_taps:
        A list of times of the taps from file two for section two of taps
    @input df_to_convert: A df of the file that needs to be converted
    @input column_name: The name of the df to convert
    @input output_file: The name of the file to write the new df to.
        (Optional: If not provided, the df will only be
         returned from this function but not written to file)

    @output Returns the df_to_convert,
    after converting the timestamps to the new values.
    """
    slope = calculate_slope(source_one_first_taps,
                            source_one_second_taps,
                            source_two_first_taps,
                            source_two_second_taps)
    b = calculate_b(slope, source_one_first_taps, source_two_first_taps)
    print("==== INFO ====")
    print("SLOPE: ", slope)
    print("Y-INTERCEPT: ", b)
    print("==== END INFO ====")
    df_to_convert = update_time_stamps(df_to_convert, column_name, slope, b)

    if (output_file is not None):
        df_to_convert.to_csv(output_file)
    return df_to_convert


def main():
    """
    Provides the command line interface of the timestamp converter.
    Note that by importing this file the convert_time_stamps() function
    can be directly used without the CLI.
    The convert_time_stamps() function returns a df so CLI is optional.
    """
    print("==== TIMESTAMP CONVERTER =====")
    parser = argparse.ArgumentParser()
    parser.add_argument("-tf1",
                        "--tapfile1",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Path to the .csv file containing
                          the taps for source one.""")
    parser.add_argument("-dc1",
                        "--datacolumn1",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Name of the data column
                          in the first file.""")
    parser.add_argument("-tf2",
                        "--tapfile2",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Path to the .csv file containing
                          the taps for source two.""")
    parser.add_argument("-dc2",
                        "--datacolumn2",
                        action="store",
                        type=str,
                        nargs=1,
                        help="Name of the data column in the second file.")
    parser.add_argument("-f",
                        "--fileToConvert",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""File that should be converted to new timestamps
                          (should align with the taps for file two).""")
    parser.add_argument("-fc",
                        "--fileToConvertColumn",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Name of the column that should be converted
                          to new timestamps in the file to convert.""")
    parser.add_argument("-o",
                        "--output",
                        action="store",
                        type=str,
                        nargs="?",
                        help="""Output file name. (Optional: If not provided,
                         df is returned and not written to a file).""")
    args = parser.parse_args()
    taps_one = pd.read_csv(args.tapfile1[0])[args.datacolumn1[0]].to_list()
    taps_two = pd.read_csv(args.tapfile2[0])[args.datacolumn2[0]].to_list()

    if (len(taps_one) % 2 != 0):
        print("""Error - The number of taps should be even.
               Source one has this many taps: """, len(taps_one))
        return
    if (len(taps_two) % 2 != 0):
        print("""Error = The number of taps should be even.
              Source two has this many taps: """, len(taps_two))
        return

    haf_of_taps_one = int(len(taps_one) / 2)
    haf_of_taps_two = int(len(taps_two) / 2)
    fileToConvert = pd.read_csv(args.fileToConvert[0])
    outputFileName = None
    if (args.output is not None):
        outputFileName = args.output

    df = convert_time_stamps(taps_one[:haf_of_taps_one],
                             taps_one[haf_of_taps_one:],
                             taps_two[:haf_of_taps_two],
                             taps_two[haf_of_taps_two:],
                             fileToConvert,
                             args.fileToConvertColumn[0],
                             outputFileName)
    print("===== FINISHED! =====")
    return df


if __name__ == "__main__":
    main()
