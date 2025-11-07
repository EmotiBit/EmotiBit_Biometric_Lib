#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  15 3:06:23 2019

@author: Nitin
"""

import argparse
import emotibit.dataviewer as dataviewer

parser = argparse.ArgumentParser()
parser.add_argument(
  "-p",
  "--path",
  type=str,
  required=True,
  help="Directory path to the folder containing the data files."
)
parser.add_argument(
  "-n",
  "--base_filename",
  type=str,
  required=True,
  help="Base filename (without extension) of the data file to load."
)
parser.add_argument(
  "-u",
  "--user_notes",
  required=False,
  action='store_true',
  help="Toggle to display user notes if available in the data."
)
parser.add_argument(
  "-t",
  "--hide_dc_tags",
  type=str,
  required=False,
  nargs='*',
  default=None,
  help="Space-separated list of data tags for which cutoff markers should be hidden in the data viewer."
)

args = parser.parse_args()

file_dir = args.path
file_base = args.base_filename  

userNote_toggle = args.user_notes
hide_DC_tags = args.hide_dc_tags

analysis = dataviewer.DataViewer(file_dir, file_base, hide_DC_tags, userNote_toggle)
