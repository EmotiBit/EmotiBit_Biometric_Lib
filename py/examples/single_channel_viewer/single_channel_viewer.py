# -*- coding: utf-8 -*-
"""
Created on Fri May 12 15:37:34 2023

@author: nitin
"""
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import tkinter
import tkinter.simpledialog as simpledialog
import os
import csv

typetag = 'EA' # common to all people
# select the directory where the output will be stored.
output_dir = r'D:\dev\CFL\EmotiBit\data analysis\data_xenbox\Data-20230511T212157Z-001\Data'
# change the output notes file name if required
output_file_path = os.path.join(output_dir, 'user_notes.csv')

#update the following dictionary where all the data can be found
# Currently, keep all the files from a single person under 1 directory. sub-directories are allowed
database = [
    {
     'name':"Bob",
     'root_path':r'D:\dev\CFL\EmotiBit\data analysis\data_xenbox\Data-20230511T212157Z-001\Data\Bob',
     'data':pd.DataFrame()
     },
    {
     'name':"Diane",
     'root_path':r'D:\dev\CFL\EmotiBit\data analysis\data_xenbox\Data-20230511T212157Z-001\Data\Diane',
     'data':pd.DataFrame()
     },
    {
     'name':"Jared",
     'root_path':r'D:\dev\CFL\EmotiBit\data analysis\data_xenbox\Data-20230511T212157Z-001\Data\Jared',
     'data':pd.DataFrame()
     },
    {
     'name':"John",
     'root_path':r'D:\dev\CFL\EmotiBit\data analysis\data_xenbox\Data-20230511T212157Z-001\Data\John',
     'data':pd.DataFrame()
     },
    {
     'name':"Mike",
     'root_path':r'D:\dev\CFL\EmotiBit\data analysis\data_xenbox\Data-20230511T212157Z-001\Data\Mike',
     'data':pd.DataFrame()
     }]


#%% Read all files into dataframes
x_axis_col = 'LslMarkerSourceTimestamp'
#x_axis_col = 'LocalTimestamp'
for db_i in range(len(database)):
    print('-->' + database[db_i]['name'])
    basepath = pathlib.Path(database[db_i]['root_path'])
    file_list = list(basepath.rglob("*EA*"))
    filepath_list = []
    for file in file_list:
        print(file.stem)
        filepath_list.append(str(file.resolve()))
    for filepath in filepath_list:
        temp = pd.read_csv(filepath)
        if x_axis_col in temp.columns:
            if(0 in temp[x_axis_col].unique()):
                print(filepath.split('\\')[-1] + ": " + x_axis_col +' timestamp missing. discarding.')
            else:
                print(filepath.split('\\')[-1] + ': good file')
                database[db_i]['data'] = database[db_i]['data'].append(temp)
        else:
            print(filepath.split('\\')[-1] + ": " + x_axis_col +' not present. discarding.')

global_x_loc = 0
global_comment = ""
global_subplot_clicked = 0
user_note_headers = list(database[0]['data'].columns)
user_note_headers[-1] = 'UserNote'
notes_df = pd.DataFrame(columns=user_note_headers)
notes_file = pathlib.Path(output_file_path)
if not notes_file.is_file():
    notes_df.to_csv(output_file_path, mode='a', index=False)

#%% callback functions
def on_click(event):
    print('x-axis: ' + str(event.xdata))
    global global_x_loc
    global_x_loc = event.xdata
    for i in range(len(axes)):
        if event.inaxes == axes[i]:
            print('you clicked {0}/{1} subplot'.format(i,len(axes)))
            global_subplot_clicked = i


def on_key(event):
    print('Key press:\'%s\'' %(event.key))
    if event.key == 'c':
        root = tkinter.Tk()
        root.withdraw()
        w = simpledialog.askstring("Title", "Enter the comment to annotate the last mouse click")
        if w != None:
            print(str(global_x_loc) + ":" + w)
            df_row = list(database[global_subplot_clicked]['data'].iloc[(database[global_subplot_clicked]['data'][x_axis_col] - global_x_loc).abs().argsort()[0],:])
            df_row[-1] = w
            with open (output_file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(df_row)

#%% plot data into 1 plot
num_plots = len(database)
fig, axes = plt.subplots(num_plots,1, sharex=True) # creates number of subplots equal to entries in the database

fig.canvas.mpl_connect('key_press_event', on_key)
plt.connect('button_press_event', on_click)
fig.suptitle( 'Data channel: '+ typetag)
for db_i in range(len(database)):
    if(x_axis_col in database[db_i]['data'].columns):
        #axes[db_i].title.set_text(database[db_i]['name'])
        line, = axes[db_i].plot(database[db_i]['data'][x_axis_col], database[db_i]['data']['EA'], label=database[db_i]['name'])
        axes[db_i].legend()
plt.show()
