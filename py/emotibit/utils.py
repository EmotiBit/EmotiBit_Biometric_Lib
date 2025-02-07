# -*- coding: utf-8 -*-
"""
@author: Sean Montgomery <produceconsumerobot@gmail.com>

Created on Wed Jul 20 06:14:05 2022
"""


import pandas as pd
import matplotlib.pyplot as plt
import os, shutil, pathlib, fnmatch
import subprocess

def print_user_notes(file_dir = "", file_base_names = "", delim = ", "):
    """
    @fn     print_user_notes()
    @brief  batch prints contents of user note (UN) files to console
    @param  file_dir Base directory of the parsed data files
    @param  file_base_names array of file bases of the data files. Expected 
            organization is file_dir/file_base_names[i]/file_base_names[i]_XX.csv
    @param  delim delimiter between notes
    """
    output = ''
       
    for f in range(len(file_base_names)):
        file_base = file_base_names[f]
        file_path = file_dir + '\\' + file_base + '\\' + file_base + '_' + 'UN' + '.csv'
        user_notes = pd.read_csv(file_path);
        for note in user_notes['UN']:
            output = output + note + delim
        if (f < len(file_base_names) - 1): # Don't add an extra \n
            output = output + '\n'
    print(output)
def save_fig(save_dir = "", _dpi = 300):
    import os
    import pickle
    fig = plt.gcf()
    title = fig.canvas.get_window_title()
    if save_dir == "":
        save_dir = os.getcwd()
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.savefig(save_dir + "/" + title + ".png", transparent=False, dpi = _dpi)
    plt.savefig(save_dir + "/" + title + ".pdf", transparent=True, dpi = _dpi)
    with open(save_dir + "/" + title + ".fig", 'wb') as f:
        # pickle.dump(fig, open('FigureObject.fig.pickle', 'wb', f))
        pickle.dump(fig, f)
        # open with pickle.load(open('FigureObject.fig.pickle', 'rb'))
def parse_data(src_path, dst_dir, parser_path = r"C:\Program Files\EmotiBit\EmotiBit DataParser\EmotiBitDataParser.exe", dst_filebase = "", ts_to_filebase = False, rm_src = False):
    """
    @fn     parse_data()
    @brief  Calls the EmotiBitDataParser specified in parser_path to
        parse an EmotiBit data file
    @param  src_path        Path to the raw EmotiBit data file
    @param  dst_dir         Path to place the output data subdirectory
    @param  parser_path     Path to the EmotiBitDataParser executable
    @param  dst_filebase    Optional string input to specify filebase of output
    @param  ts_to_filebase  Optional boolean use the first timesync timestamp
        as the dst_filebase
    @param  rm_src          Optional boolean to remove the original raw
        Emotibit data file
    @return dst_filebase    The dst_filebase used
    """
    # ToDo: File/Path checks
    # ToDo: Create warning if src and dst drive are different
    
    data_ext = ".csv"
    
    # Create a new filename from the first TL timesync timestamp
    if ts_to_filebase:
        with open(src_path) as f:
            reading = True
            while reading:
                line = f.readline()
                split_line = line.split(",")
                if len(split_line) > 6 and split_line[3] == "TL":
                    dst_filebase = split_line[6].strip('\n')
                    print("Filename: " + dst_filebase)
                    reading = False
    # If dst_filebase is empty, set to src_filebase
    if dst_filebase == "":
        path = src_path.replace("\\", "/")
        split_line = path.split("/")
        dst_filebase = split_line[len(split_line) - 1]
        split_line = dst_filebase.split(".")
        dst_filebase = split_line[0]

    # Create move src to dst
    if not os.path.isdir(os.path.join(dst_dir, dst_filebase)):
        pathlib.Path(os.path.join(dst_dir, dst_filebase)).mkdir(parents=True, exist_ok=True)
    if rm_src:
        shutil.move(src_path, os.path.join(dst_dir, dst_filebase, dst_filebase + data_ext))
    else:
        shutil.copy(src_path, os.path.join(dst_dir, dst_filebase, dst_filebase + data_ext))
        
    # Parse data file in dst
    cwd = os.getcwd()
    print(os.path.join(dst_dir, dst_filebase))
    # cd to the parser directory to avoid ofDirectory errors
    path = parser_path.replace("\\", "/")
    path = parser_path.split("/")
    parser_dir = '/'.join(path[0:len(path)-1])
    print(parser_dir)
    os.chdir(parser_dir) 
    arguments = [os.path.join(dst_dir, dst_filebase, dst_filebase + data_ext)]
    cmd = [os.path.join(parser_path)] + arguments
    print(cmd)
    subprocess.run([os.path.join(parser_path)] + arguments)
    print(cwd)
    os.chdir(cwd)
    return dst_filebase
