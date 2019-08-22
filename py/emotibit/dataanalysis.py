#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 12:34:23 2019

@author: nitin
"""
import datasyncer as syncer

import numpy as np
# import csv
# import tkinter as tk 
import matplotlib.pyplot as plt
import locale
import os
import random
# import pandas as pd




class DataAnalysis:

	# file_dir0 = ""
	# file_base = ""
	# file_ext = ""
	# data_types = []
	# data_groups = {}
	# file_names0 = []
	# data_col0 = []
	# data_start_row1 = 2
	# my_syncer = syncer.DataSyncer()

	def __init__(self,file_dir,file_base, hide_dc_tags, usernote_toggle):

		self.file_dir0 = file_dir
		self.file_base = file_base
		self.file_ext = ".csv"
		self.data_types = ["EA", "EL", "ER", "PI", "PR", "PG", "T0", "TH", "H0", "AX", "AY", "AZ", "GX", "GY", "GZ", "MX", "MY", "MZ", "DC", "DO", "UN"]# add the aperiodic data types
		# TODO: try to come up with better grouping with less redundancy
		self.data_groups = {"accelerometer": ["AX", "AY", "AZ"],
							"gyroscope": ["GX", "GY", "GZ"],
							"magnetometer": ["MX", "MY", "MZ"],
							"heart-rate": ["PG", "PI", "PR"],
							"temp-hum": ["T0", "H0", "TH"],
							"imu": ["AX", "AY", "AZ", "GX", "GY", "GZ", "MX", "MY", "MZ"],
							"eda": ["EA", "EL", "ER"],
							"aperiodic": ["DC", "DO"],
							"push_messages": ["UN"]}
		self.my_syncer = syncer.DataSyncer()
		self.file_names0 = []
		self.absentTags = []
		for data_type in self.data_types:
			if os.path.isfile(self.file_dir0 + "/" + self.file_base + "_" + data_type + self.file_ext):
				self.file_names0.append(file_base + "_" + data_type + self.file_ext)
			else:
				self.absentTags.append(data_type)
		for tag in self.absentTags:
			self.data_types.remove(tag)
		self.data_col0 = [7]
		self.data_start_row1 = 2
		self.myLocale = locale.getlocale() # Store current locale
		locale.setlocale(locale.LC_NUMERIC, 'en_US') # Switch to new locale to process file
		self.my_syncer.load_data(self.file_dir0, self.file_names0, self.data_col0)
		locale.setlocale(locale.LC_NUMERIC, self.myLocale) # Set locale back to orignal

		# shifting the x axis to start from 0
		base_val = self.my_syncer.time_series[0].timestamp[0] # subtracting the smallest val from EA
		for i in range(len(self.my_syncer.time_series)):
			self.my_syncer.time_series[i].timestamp[:] = [ stamp - base_val for stamp in self.my_syncer.time_series[i].timestamp ]


		
		# for i in range(len(self.data_types)):
		# 	print(len(self.my_syncer.time_series[i].timestamp),"->",my_syncer.time_series[i].timestamp[0],":",my_syncer.time_series[i].timestamp[-1])
			# T = len(my_syncer.time_series)
		
		# code test: generating random samples from the timeseries to test multiple backgrounds
		# self.points_UN = sorted(random.sample(range(0,int(self.my_syncer.time_series[i].timestamp[-1] - 10)),2))
		# self.points_DC = sorted(random.sample(range(0,int(self.my_syncer.time_series[i].timestamp[-1] - 10)),1))

		# All markers which are going to populate the plot apart from the data
		# TODO: change the structure of markers to be in sync with data groups
		self.markers = {"points_DC": {"EA":[], "EL":[], "ER":[],
									  "PI":[], "PR":[], "PG":[],
									  "T0":[], "TH":[], "H0":[],
									  "AX":[], "AY":[], "AZ":[],
									  "GX":[], "GY":[], "GZ":[],
									  "MX":[], "MY":[], "MZ":[]},
						"points_UN": [],
						"points_DO": []}

		# reading all the markers from files and storing in markers dict
		for tag in self.data_groups["aperiodic"]:# for each aperiodic signal
			if tag not in self.absentTags:
				for i, (timestamp, data) in enumerate(zip(self.my_syncer.time_series[self.data_types.index(tag)].timestamp, self.my_syncer.time_series[self.data_types.index(tag)].data)) : # for each line in the file
					if tag == "DC":
						self.markers["points_"+tag][data].append(timestamp)

					elif tag == "DO":
						self.markers["points_"+tag].append((timestamp,data))

					else:
						print("Error: unknown tag")

		for tag in self.data_groups["push_messages"]:
			# if len(self.my_syncer.time_series[self.data_types.index(tag)].timestamp)%2 != 0:
				# print("corrupted list. Odd number entries")
			for i, (timestamp, data) in enumerate(zip(self.my_syncer.time_series[self.data_types.index(tag)].timestamp,
													  self.my_syncer.time_series[self.data_types.index(tag)].data)):  # for each line in the file
				if tag == "UN":
					self.markers["points_" + tag].append([timestamp, data])
				else:
					print("Error: Unknown tag")

		# generate the figure with subplots
		self.fig, self.axes = plt.subplots(9, 2, sharex = True)

		# add callbacks to the plot
		self.axes[0,0].callbacks.connect('xlim_changed', self.on_xlims_change)
		# self.cid = self.fig.canvas.mpl_connect('key_press_event', lambda evt, var=self.axes: self.hide_DC(evt, var))
		self.cid = self.fig.canvas.mpl_connect('key_press_event', self.hide_DC)

		for j in range(2):# columns of subplot
			for i in range(9):# rows in subplot
				self.axes[i,j].plot(self.my_syncer.time_series[j*9+i].timestamp,self.my_syncer.time_series[j*9+i].data,linestyle = '-',zorder=10, alpha=0.9)
				self.axes[i,j].autoscale(enable = True, axis = 'y')

				# to draw background color
				# axes[i,j].axvspan(points_UN[0],points_UN[1],facecolor = 'y',alpha = 0.5)
				
				# to mark DC
				self.lines_DC = []
				self.toggle_DC = True # displaying the lines
				for tag in self.markers["points_DC"].keys():
					if tag not in hide_dc_tags:
						plot_idx = (int(self.data_types.index(tag)%9),int(self.data_types.index(tag)/9))
						for point in self.markers["points_DC"][tag]: # for every point in the list
							line = self.axes[plot_idx[0],plot_idx[1]].axvline(x=point, color='r', label="DC", zorder=1, lw=0.8)
							self.lines_DC.append(line)

				# to mark UN
				if usernote_toggle:
					for (point,note) in self.markers["points_UN"]:
						self.axes[i,j].axvline(x=point, color='g', label="UN")
						if (j*9+i == 0 or j*9+i == 9):
							self.axes[i,j].text(point, self.axes[i, j].get_ylim()[1], note, fontsize=6, rotation=45)

				# to mark DO



				# to add the signal tag on the y-axis
				self.axes[i,j].set_ylabel(self.data_types[j*9+i])
				
				# to add the legend
				plt.figlegend(labels = ("Data","DC","UN"), loc = 'lower center', ncol=5, labelspacing=0. )
				self.fig.suptitle(self.file_base)

		plt.show()
	
	def on_xlims_change(self, axes):
		print("entered xlims change")
		new_xlim = axes.get_xlim()
		if not axes.texts:
			return
		for text_left, text_right in zip(axes.texts, self.axes[0, 1].texts):
			if not (new_xlim[0] <= text_left.get_position()[0] <= new_xlim[1]):
				text_left.set_visible(False)
				text_right.set_visible(False)
			else:
				text_left.set_visible(True)
				text_left.y = axes.get_ylim()[1]
				text_right.set_visible(True)
				text_right.y = self.axes[0, 1].get_ylim()[1]

	def hide_DC(self, event):
		print("entered key press change")
		if event.key == " ": # hide the markers
			# TODO: Fix the lines_DC visibility issue
			self.toggle_DC = not self.toggle_DC
			print("self.toggle_DC :	", self.toggle_DC)
			for line in self.lines_DC:
				line.set_visible(self.toggle_DC)
				# line.remove()
	# TODO: add functionality to scroll the plots.







