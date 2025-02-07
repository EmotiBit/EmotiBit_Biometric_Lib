# -*- coding: utf-8 -*-
"""
Created on Feb 5 2025

@author: Sean Montgomery <produceconsumerobot@gmail.com>
"""
import pandas as pd
import os
import json
import argparse

parser = argparse.ArgumentParser(description="""Script to aggregate EDL test data from files parsed with extract_eda_test_data.py.
Example:
python ./aggregate_eda_test_data.py -s 'c:/priv/test' -n '500K' '1M' '2M' -f 500K-2M""", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-s', '--src_dir', type=str, required=True, help='Path to extracted EmotiBit EDL summary files')
parser.add_argument('-n', '--notes', type=str, nargs='+', required=True, help='User notes that specify testing change events to include in the aggregate data output')
parser.add_argument('-f', '--dst_filebase', type=str, required=False, default='', help='Specifies the output file base name')

args = parser.parse_args()

src_dir = args.src_dir
notes = args.notes

def list_subdirectories(path):
    subdirectories = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            subdirectories.append(entry)
    return subdirectories


# Constants that likely don't need changing
data_ext = '.csv'
summary_suffix = '_EdlSummary'
agg_filebase = args.dst_filebase + '_aggregateEdlTestData'
testing_info_suffix = '_testingInfo'
info_ext = '.json'

d_print = False
# Read the data from summary files and reshape into aggregate data
agg = {}
dirs = list_subdirectories(src_dir)
for d in dirs:
    include_file = True
    df = pd.read_csv(os.path.join(src_dir, d, d + summary_suffix + data_ext))
    # Check if file has target notes
    for c in df.columns:
        if c != 'note': # skip note column 
            for note in notes:
                if d_print: print(note)
                rows = (df['note'] == note).index
                if len(rows) == 0:
                    include_file = False
    if include_file:
        with open(os.path.join(src_dir, d, d + testing_info_suffix + info_ext)) as f:
            info = json.load(f)
            print(info)
            for field in ['Tester', 'Condition', 'EmotiBitInfo']:
                if field not in agg:
                    agg[field] = []
                if field in info:
                    agg[field].append(info[field])
                else:
                    agg[field].append('unknown')
        if 'Filename' not in agg:
            agg['Filename'] = []
        agg['Filename'].append(d)
        for c in df.columns:
            if c != 'note': # skip note column 
                for note in notes:
                    if d_print: print(note)
                    rows = (df['note'] == note).index
                    row = rows[0]
                    if note + ' ' + c not in agg:
                        agg[note + ' ' + c] = []
                    if d_print: print(df[c].loc[row])
                    agg[note + ' ' + c].append(df[c].loc[row])
print('Result:')
print(agg)

# Save aggregate to csv file
agg_df = pd.DataFrame.from_dict(agg)
file_name = os.path.join(src_dir, agg_filebase + data_ext)
print("Saving: " + file_name)
agg_df.to_csv(file_name, sep=',', encoding='utf-8', index=False, header=True)
