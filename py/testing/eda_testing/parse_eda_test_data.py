# -*- coding: utf-8 -*-
"""
Created on Feb 5 2025

@author: Sean Montgomery <produceconsumerobot@gmail.com>
"""
import sys
import json
import os
sys.path.append('G:/My Drive/Dropbox/LocalDev/Sean/EmotiBit/EmotiBit_Biometric_Lib/py/')
import emotibit.utils as eb_utils
import argparse

parser = argparse.ArgumentParser(description="""Script to log EmotiBit test conditions and parse test data. Provides a pipeline for direct processing of EmotiBit Oscilloscope dataLog.txt output.
Example:
python ./parse_test_data.py -t Sean -c v7 -s 'C:/Program Files/EmotiBit/EmotiBit Oscilloscope/data/dataLog.txt' -d 'c:/priv/test'""", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-t', '--tester', type=str, required=True, help='Name of tester')
parser.add_argument('-c', '--condition', type=str, required=True, help='Testing conditions identifier')
parser.add_argument('-i', '--emotibit_info', type=str, required=False, help='EmotiBit info string from EmotiBit serial console used to specify hardware and firmware')
parser.add_argument('-s', '--src_path', type=str, required=False, default='C:/Program Files/EmotiBit/EmotiBit Oscilloscope/data/dataLog.txt', help='Path to EmotiBit raw data file')
parser.add_argument('-d', '--dst_dir', type=str, required=True, help='Path to destination directory')
parser.add_argument('-ts', '--ts_to_filebase', type=bool, required=False, default=True, help='Boolean to use the first timesync timestamp for the subdirectory and parsed file base names')
parser.add_argument('-f', '--dst_filebase', type=str, required=False, default='', help='Specifies the subdirectory and parsed file base names')
parser.add_argument('-p', '--parser_path', type=str, required=False, default='C:/Program Files/EmotiBit/EmotiBit DataParser/EmotiBitDataParser.exe', help='Path to the EmotiBitDataParser executable')
parser.add_argument('-rm', '--rm_src', type=bool, required=False, default=False, help='Boolean to remove the original EmotiBit raw data file')

args = parser.parse_args()

testing_info_suffix = '_testingInfo'
testing_info = {}
testing_info['Tester'] = args.tester
testing_info['Condition'] = args.condition
testing_info['EmotiBit Info'] = args.emotibit_info

# Parse the data
dst_filebase = eb_utils.parse_data(src_path=args.src_path, dst_dir=args.dst_dir, parser_path = args.parser_path, dst_filebase = args.dst_filebase, ts_to_filebase = args.ts_to_filebase, rm_src = False)

# Save the dictionary to a JSON file
with open(os.path.join(args.dst_dir, dst_filebase, dst_filebase + testing_info_suffix + '.json'), 'w') as f:
    json.dump(testing_info, f)
