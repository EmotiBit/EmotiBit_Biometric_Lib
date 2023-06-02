# -*- coding: utf-8 -*-
"""
hyperscanning_viewer.py
Plots EmotiBit data from multiple people and multiple data files per person.
Change usage parameter in specified section to match desired inputs and run. 

Utilize the pan, zoom
and home/reset buttons to traverse data. 

The following keystrokes provide
additional functionality:
    'c': Creates a [c]omment entry for storage in an output note file. Note the
        the timestamp corresponds the x-position clicked before hitting 'c'.
    'a': [a]uto-rescales the y-limits. At present a mouse click is
        required after pressing 'a' to update the QT plot engine.
    't': [t]ransposes the subplots, swapping plot rows and columns. Note this 
        presently breaks the home/reset button.
    'r': [r]esets the figure. 
    'e': Toggles titles and labels for [e]ach subplot 
    
ToDo:
    - Remove click requirement for 'a' functionality
    - Separate the example code from the functions
    - Fix home functionality after 't'
    - Add vertical lines at comment times and some way to see comment 
    - Consider making click after 'c' select time
    - Add vertical line at click on all plots

Created on Fri May 24 15:37:34 2023

@author: produceconsumerobot
"""
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import tkinter
import tkinter.simpledialog as simpledialog
import numpy as np
import os
import csv

try:
    import IPython
    IPython.get_ipython().magic("matplotlib qt")
except:
    plt.ion()

# **** Set usage parameters here ****
    
fig_size = [15, 12]
typetags_in_cols = False
label_each_subplot = False
output_note_typetag = 'analysis_notes'

# select the directory where the output will be stored.
output_dir = r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data'

signals = {
    'typetags': ['TH','T1','D0','AX','EA'],
    'marker_styles': ['-','-','*','-','-']
    }

#update the following dictionary where all the data can be found
# Currently, keep all the files from a single person under 1 directory. sub-directories are allowed
database = [
    {
     'name':"Mike",
     'root_path':r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Mike',
     },
    {
     'name':"Bob",
     'root_path':r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Bob',
     },
    {
     'name':"Jared",
     'root_path':r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Jared',
     },
    {
     'name':"John",
     'root_path':r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/John',
     },
    {
     'name':"Diane",
     'root_path':r'G:/.shortcut-targets-by-id/1KogPeL5zzT7nFPtEZ5wjIY4poPyVxgWN/EmotiBit Test Data/XenboX/XenboX at TRI 2023-04-16/Data/Diane',
     }
    ]

# **** END usage parameters ****

# change the output notes file name if required
output_file_path = os.path.join(output_dir, output_note_typetag + '.csv')

if (typetags_in_cols):
    num_rows = len(database)
    num_cols = len(signals['typetags'])
else:
    num_rows = len(signals['typetags'])
    num_cols = len(database)

fig, axes = plt.subplots(num_rows,num_cols, sharex=True) # creates number of subplots equal to entries in the database
xlims = []

#%% Read all files into dataframes
x_axis_col = 'LslMarkerSourceTimestamp'
#x_axis_col = 'LocalTimestamp'
for db_i in range(len(database)):
    database[db_i]['data'] = {}
    for typetag in signals['typetags']:
        print('-->' + database[db_i]['name'])
        basepath = pathlib.Path(database[db_i]['root_path'])
        file_list = list(basepath.rglob("*" + typetag + "*"))
        filepath_list = []
        for file in file_list:
            print(file.stem)
            filepath_list.append(str(file.resolve()))
        for f in range(len(filepath_list)):
            filepath = filepath_list[f]
            temp = pd.read_csv(filepath)
            if (f == 0):
                database[db_i]['data'][typetag] = pd.DataFrame()
            if x_axis_col in temp.columns:
                if(0 in temp[x_axis_col].unique()):
                    print(filepath.split('//')[-1] + ": " + x_axis_col +' timestamp missing. discarding.')
                else:
                    print(filepath.split('//')[-1] + ': good file')
                    database[db_i]['data'][typetag] = database[db_i]['data'][typetag].append(temp)
            else:
                print(filepath.split('//')[-1] + ": " + x_axis_col +' not present. discarding.')

print('data loading complete...')
global_x_loc = 0
global_comment = ""
global_subplot_clicked = 0
user_note_headers = list(database[0]['data'][typetag].columns)
user_note_headers[-1] = output_note_typetag
notes_df = pd.DataFrame(columns=user_note_headers)
notes_file = pathlib.Path(output_file_path)
if not notes_file.is_file():
    notes_df.to_csv(output_file_path, mode='a', index=False)

def auto_y_lim():
    for m in range(num_rows):
        for n in range(num_cols):
            if (typetags_in_cols):
                typetag = signals['typetags'][n]
                db_i = m
            else:
                typetag = signals['typetags'][m]
                db_i = n
            print('subplot {0},{1}'.format(m, n))
            x_lims = axes[m][n].get_xlim()
            print('x_lims = ', x_lims)
            
            # Find the indexes of the x limits
            x_data_arr = np.array(database[db_i]['data'][typetag][x_axis_col])
            x_inds = np.where((x_data_arr > x_lims[0]) & (x_data_arr < x_lims[1]))[0]
            if (len(x_inds) > 1): # Don't try to plot missing data
                x_inds = np.sort(x_inds)
                x_inds = range(x_inds[0], x_inds[len(x_inds) - 1])
                print('x_inds = ', x_inds[0], x_inds[len(x_inds) - 1])
                
                #print('len(data) = ', len(database[db_i]['data'][typetag][typetag]))
                y_data_arr = np.array(database[db_i]['data'][typetag][typetag])
                y_lims = [
                    min(y_data_arr[x_inds]),
                    max(y_data_arr[x_inds])
                    ]
                print('y_lims = ', y_lims[0], y_lims[1])
                
                #axes[m][n].set_ylim(y_lims[0], y_lims[1])
                axes[m][n].update({'ylim': [y_lims[0], y_lims[1]]})
                fig.canvas.blit(fig.bbox)
                
def plot_data():
     #%% plot data 
    global fig, axes, xlims
    new_xlims = True
    if (len(xlims) == 2):
        # save the xlims when replotting (for changing plot rows/cols)
        new_xlims = False
        xlims = axes[0][0].get_xlim()
        print('xlims = ', xlims)
    print('new_xlims = ', new_xlims)
    plt.close(fig) # ToDo: consider more elegant ways to preserv
    fig, axes = plt.subplots(num_rows,num_cols, sharex=True) # creates number of subplots equal to entries in the database
    plt.get_current_fig_manager().toolbar.pan()
    fig.set_size_inches(fig_size)
    
    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.connect('button_press_event', on_click)
    fig.suptitle( 'EmotiBit Hyperscanning Data')
    for m in range(num_rows):
        for n in range(num_cols):
            if (typetags_in_cols):
                typetag = signals['typetags'][n]
                marker_style = signals['marker_styles'][n]
                db_i = m
                plot_title = typetag
                plot_xlabel = database[db_i]['name']
            else:
                typetag = signals['typetags'][m]
                marker_style = signals['marker_styles'][m]
                db_i = n
                plot_title = database[db_i]['name']
                plot_xlabel = typetag
            if(x_axis_col in database[db_i]['data'][typetag].columns):
                #axes[m].title.set_text(database[db_i]['name'])
                line, = axes[m][n].plot(database[db_i]['data'][typetag][x_axis_col], database[db_i]['data'][typetag][typetag], marker_style, label=database[db_i]['name'])
                #axes[m].legend()
                if (label_each_subplot or n == num_cols - 1):
                    axes[m][n].yaxis.set_label_position("right")
                    axes[m][n].set_ylabel(plot_xlabel)
                if (label_each_subplot or m == 0):
                    axes[m][n].set_title(plot_title)
            if (new_xlims):
                xlims = axes[m][n].get_xlim()
            else:
                axes[m][n].set_xlim(xlims[0], xlims[1])
    auto_y_lim()
    plt.show()
    
#%% callback functions
def on_click(event):
    global global_subplot_clicked
    global global_x_loc
    print('x-axis: ' + str(event.xdata))
    global_x_loc = event.xdata
    for i in range(len(axes)):
        if event.inaxes == axes[i]:
            print('you clicked {0}/{1} subplot'.format(i, len(axes) - 1))
            global_subplot_clicked = i
            
def on_key(event):
    print('Key press:\'%s\'' %(event.key))
    if event.key == 'c':    # create comment
        root = tkinter.Tk()
        root.withdraw()
        w = simpledialog.askstring("Title", "Enter the comment to annotate the last mouse click")
        if w != None:
            print(str(global_x_loc) + ":" + w)
            df_row = list(database[global_subplot_clicked]['data'][typetag].iloc[(database[global_subplot_clicked]['data'][typetag][x_axis_col] - global_x_loc).abs().argsort()[0],:])
            df_row[-1] = w
            with open (output_file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(df_row)
                
    if event.key == 'a':    # auto y-lim
        auto_y_lim()
        
    if event.key == 't':    # toggle rows & cols in plot
        global typetags_in_cols, num_rows, num_cols
        typetags_in_cols = not typetags_in_cols
        print('typetags_in_cols = ', typetags_in_cols)
        if (typetags_in_cols):
            num_rows = len(database)
            num_cols = len(signals['typetags'])
        else:
            num_rows = len(signals['typetags'])
            num_cols = len(database)
        plot_data()
    if event.key == 'r': # reset the plot and start over
        # this is a hack because 't' breaks home/reset
        global xlims
        xlims = []
        plot_data()
    if event.key == 'e': # Adds titles and labels to [e]ach subplot 
        global label_each_subplot
        label_each_subplot = not label_each_subplot
        plot_data()

plot_data()
        
        

