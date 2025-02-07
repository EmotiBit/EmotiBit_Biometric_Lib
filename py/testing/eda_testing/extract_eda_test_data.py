# -*- coding: utf-8 -*-
'''
Created on Feb 5 2025

@author: Sean Montgomery <produceconsumerobot@gmail.com>
'''
import numpy as np
import pandas as pd
import os
import argparse

def list_subdirectories(path):
    subdirectories = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            subdirectories.append(entry)
    return subdirectories

parser = argparse.ArgumentParser(description="""Script to extract EDL test data from files parsed with parse_test_data.py.
Example:
python ./extract_eda_test_data.py -s 'c:/priv/test' -o 5 -d 5""", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-s', '--src_dir', type=str, required=True, help='Path to parsed EmotiBit data files')
parser.add_argument('-o', '--offsets_begin', type=int, nargs='+', required=False, default=5, help='Offsets (secs) from detected change event to extract EDL test data. Separate offsets for each change event can be specified with an array of values.')
parser.add_argument('-d', '--durations', type=int, nargs='+', required=False, default=5, help='Durations (secs) from change event offsets to extract EDL test data. Separate durations for each change event can be specified with an array of values.')

args = parser.parse_args()

src_dir = args.src_dir
offsets_begin = args.offsets_begin
durations = args.durations


# Constants that likely don't need changing
data_ext = '.csv'
un_ext = '_UN.csv'
metric = 'EL'
metric_ext = '_' + metric + '.csv'
summary_suffix = '_EdlSummary'
edl_sat_thresh = 25000
ts_label = 'LocalTimestamp'
minKeyTimesJump = 0.2

d_print = False
dirs = list_subdirectories(src_dir)
for filebase in dirs:
    # Read experimental conditions from the user notes
    df = pd.read_csv(os.path.join(src_dir, filebase, filebase + un_ext))
    user_notes = df['UN'].tolist() # ToDo: consider an option to read list from a file for repetitive experimeEmotiBitTimestampnts
    print('user_notes:')
    print(user_notes)
    # ToDo: Consider whether we want the first note to be general experiment info

    # Find the EDA saturation events between experimental conditions
    df = pd.read_csv(os.path.join(src_dir, filebase, filebase + metric_ext))
    key_times = df.loc[df['EL'] < edl_sat_thresh, ts_label]

    # Detect change events when EDA saturates
    change_evts = key_times[np.append(np.diff(key_times), 0) > minKeyTimesJump]
    print('change_evts:')
    for num in change_evts:
        print(f'{num:10.6f}')

    # Enable single value or different values for each change event offset and duration
    if np.isscalar(offsets_begin) or len(offsets_begin) == 1:
        offsets_begin = np.full((len(change_evts)), offsets_begin)
    if np.isscalar(durations) or len(durations) == 1:
        durations = np.full((len(change_evts)), durations)

    if (len(change_evts) != len(user_notes)):
        print('WARNING: n change_evts %i != n user_notes %i', len(change_evts), len(user_notes))

    # Extract summary data from each change event
    cols = ['note', 'mean', 'stdev', 'stdev(diff)', 'SCR:Amp']
    summary = {}
    data = []
    for col in cols:
        summary[col] = []
    for n in range(len(change_evts)):
        if d_print: print(n)
        if d_print: print(len(df))
        evt = change_evts.iloc[n]
        if d_print: print(evt)
        if d_print: print(evt + offsets_begin[n])
        temp = df[ts_label][df[ts_label] > (evt + offsets_begin[n])].index    
        if d_print: print(temp)
        first_ind = temp[0] if len(temp) > 0 else len(df) - 1
        if d_print: print(first_ind)
        temp = df[ts_label][df[ts_label] > (evt + offsets_begin[n] + durations[n])].index
        if d_print: print(temp)
        last_ind = temp[0] if len(temp) > 0 else len(df) - 1
        if d_print: print(last_ind)
        data.append(df[metric].loc[first_ind:last_ind])
        file_name = os.path.join(src_dir, filebase, filebase + '_' + user_notes[n] + 'data' + data_ext)
        np.savetxt(file_name, data[n], delimiter=',')
        summary['note'].append(user_notes[n] if n < len(user_notes) else '')
        summary['mean'].append(np.mean(data[n]))
        summary['stdev'].append(np.std(data[n]))
        summary['stdev(diff)'].append(np.std(np.diff(data[n])))
        # ToDo: Read SCR:Amp from file
        summary['SCR:Amp'].append(0)
    print('Result:')    
    print(summary)

    # Save summary to csv file
    summ_df = pd.DataFrame.from_dict(summary)
    file_name = os.path.join(src_dir, filebase, filebase + summary_suffix + data_ext)
    print('Saving: ' + file_name)
    summ_df.to_csv(file_name, sep=',', encoding='utf-8', index=False, header=True)
