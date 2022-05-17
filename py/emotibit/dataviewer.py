#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 12:34:23 2019

@author: Nitin
"""
import emotibit.datasyncer as syncer

# import numpy as np
# import csv
# import tkinter as tk
import matplotlib.pyplot as plt
import locale
import os
from matplotlib.widgets import Slider, CheckButtons
from bisect import bisect_left
import platform

# import pandas as pd


class DataViewer:
	def __init__(self, file_dir, file_base, hide_dc_tags, usernote_toggle):
		self.file_dir0 = file_dir
		self.file_base = file_base
		self.file_ext = ".csv"
		self.cmd_hide_dc_tags = hide_dc_tags
		self.cmd_usernote_toggle = usernote_toggle
		self.data_types = ["EA", "SA", "SR", "SF","PI", "PR", "PG", "HR", "TH", "AX", "AY", "AZ", "GX", "GY", "GZ",
						   "MX", "MY", "MZ", "DC", "DO", "UN"]  # add the aperiodic data types
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

		# reading data
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
		self.myLocale = locale.getlocale()  # Store current locale
		if platform.system() == "Darwin":
			location = 'en_US'
		elif platform.system() == "Windows":
			location = 'USA'
		# TODO: add support for linux
		locale.setlocale(locale.LC_NUMERIC, location)  # Switch to new locale to process file
		self.my_syncer.load_data(self.file_dir0, self.file_names0, self.data_col0)
		locale.setlocale(locale.LC_NUMERIC, self.myLocale)  # Set locale back to orignal

		# shifting the x axis to start from 0
		base_val = self.my_syncer.time_series[0].timestamp[0]  # subtracting the smallest val from EA
		for i in range(len(self.my_syncer.time_series)):
			self.my_syncer.time_series[i].timestamp[:] = [stamp - base_val for stamp in
														  self.my_syncer.time_series[i].timestamp]

		# Declaring all markers which are going to populate the plot apart from the data.
		# Achieved after reading non-data files
		# TODO: change the structure of markers to be in sync with data groups
		self.markers = {"points_DC": {"EA": [], "SA": [], "SR": [],
									  "PI": [], "PR": [], "PG": [],
									  "TH": [], "SF": [], "HR": [],
									  "AX": [], "AY": [], "AZ": [],
									  "GX": [], "GY": [], "GZ": [],
									  "MX": [], "MY": [], "MZ": []},
						"points_DO": {"EA": [], "SA": [], "SR": [],
									  "PI": [], "PR": [], "PG": [],
									  "TH": [], "SF": [], "HR": [],
									  "AX": [], "AY": [], "AZ": [],
									  "GX": [], "GY": [], "GZ": [],
									  "MX": [], "MY": [], "MZ": [], "DC": []},
						"points_UN": []}
		# Set to false to stop processing DC and DO files below. The Data parser needs a patch to handle DC/DO version 2 before reading that data
		self.parseDo = False 
		self.parseDc = False
		# reading all the markers from files and storing in markers dict
		for tag in self.data_groups["aperiodic"]:  # for each aperiodic signal
			if tag not in self.absentTags:
				for i, (timestamp, data) in enumerate(
						zip(self.my_syncer.time_series[self.data_types.index(tag)].timestamp,
							self.my_syncer.time_series[self.data_types.index(tag)].data)):  # for each line in the file
					if tag == "DC":
						if self.parseDc == True:
							self.markers["points_" + tag][data].append(timestamp)

					elif tag == "DO":
						if self.parseDo  == True:
							self.markers["points_" + tag][data].append(timestamp)

					else:
						print("Error: unknown tag:" + tag)
		# TODO: come up with a better fix
		if "UN" in self.data_types:
			for tag in self.data_groups["push_messages"]:
				if tag not in self.absentTags:
					for i, (timestamp, data) in enumerate(zip(self.my_syncer.time_series[self.data_types.index(tag)].timestamp,
															  self.my_syncer.time_series[self.data_types.index(
																  tag)].data)):  # for each line in the file
						if tag == "UN":
							self.markers["points_" + tag].append([timestamp, data])
						else:
							print("Error: Unknown tag")

		# Start of main plotting
		# generate the figure with subplots
		self.fig, self.axes = plt.subplots(nrows=9, ncols=2, sharex=True)

		# code for widgets
		plt.subplots_adjust(bottom=0.2, left=0.15)

		# uncomment the following lines to enable slider
		# axSlider = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')
		# self.slider = Slider(axSlider, 'data', 10, self.my_syncer.time_series[0].timestamp[-1] - 10, valinit=10)
		# self.slider.on_changed(self.slide_through_data)

		# self.sliderEnableToggle = False
		# axButton = plt.axes([0.1, 0.15, 0.1, 0.05])
		# self.sliderEnableButton = CheckButtons(axButton, labels=["Enable slider", ""], actives=[False])
		# self.sliderEnableButton.on_clicked(self.enable_slider)

		self.TextAxesLeft = self.fig.add_subplot(position=[self.axes[0, 0].get_position().x0,
														   self.axes[0, 0].get_position().y1,
														   self.axes[0, 0].get_position().x1-self.axes[0, 0].get_position().x0,
														   0.001],sharex=self.axes[0, 0])
		self.TextAxesLeft.set_xlim([self.my_syncer.time_series[0].timestamp[0], self.my_syncer.time_series[0].timestamp[-1]])
		self.TextAxesLeft.get_xaxis().set_visible(False)
		self.TextAxesLeft.get_yaxis().set_visible(False)

		self.TextAxesRight = self.fig.add_subplot(position=[self.axes[0, 1].get_position().x0,
														   self.axes[0, 1].get_position().y1,
														   self.axes[0, 1].get_position().x1 - self.axes[0, 1].get_position().x0,
														   0.001], sharex=self.axes[0, 0])
		self.TextAxesRight.set_xlim([self.my_syncer.time_series[0].timestamp[0], self.my_syncer.time_series[0].timestamp[-1]])
		self.TextAxesRight.get_xaxis().set_visible(False)
		self.TextAxesRight.get_yaxis().set_visible(False)

		self.indicator = self.fig.add_subplot(position=[self.axes[8, 0].get_position().x0,
															self.axes[8, 0].get_position().y0 - 0.075, 0.75, 0.015])
		self.indicator.get_yaxis().set_visible(False)
		# self.indicatorLeft.set_ylabel("Complete Time Series", rotation="horizontal")
		self.indicator.set_xlim(
			[self.my_syncer.time_series[0].timestamp[0], self.my_syncer.time_series[0].timestamp[-1]])


		# add callbacks to the plot
		for i in range(9):
			for j in range(2):
				self.axes[i, j].callbacks.connect('xlim_changed', self.on_xlims_change)
		self.selected_axes = None
		self.selected_time = None
		self.temp_highlights = []  # stores the axvspan used to temporarily highlight the cursor
		self.cid0 = self.fig.canvas.mpl_connect('button_press_event', self.on_mouse_click)
		self.cid1 = self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

		# instance variables to hold all the marker lines
		self.lines_data = []
		self.lines_DC = []
		self.lines_DO = []
		self.lines_UN = []
		self.init_plot()
		plt.show()

	def init_plot(self):
		self.lines_data = []
		self.lines_DC = []
		self.lines_DO = []
		self.lines_UN = []  # used for the slider

		for j in range(2):  # columns of subplot
			for i in range(9):  # rows in subplot
				line = self.axes[i, j].plot(self.my_syncer.time_series[j * 9 + i].timestamp,
											self.my_syncer.time_series[j * 9 + i].data, linestyle='-', zorder=10,
											alpha=0.9)
				self.lines_data.append(line)
				self.axes[i, j].autoscale(enable=True, axis='y', tight=True)

				# to draw background color
				for loss in self.my_syncer.dataLoss:
					# marking a window of len 64 red
					self.axes[i, j].axvspan(loss[1], loss[1]+64, facecolor='r', alpha=0.5)

				# plotting markers once on initialization

				# to mark DO
				for tag in self.markers["points_DO"].keys():
					if tag != "DC":
						try:
							plot_idx = (int(self.data_types.index(tag) % 9), int(self.data_types.index(tag) / 9))
							for point in self.markers["points_DO"][tag]:  # for every point in the list
								line = self.axes[plot_idx[0], plot_idx[1]].axvline(x=point, color='k', label="DO", zorder=1, lw=0.75)
								self.lines_DO.append(line)
						except ValueError:
							print("Value Error")

				# to mark UN
				if self.cmd_usernote_toggle:
					for (point, note) in self.markers["points_UN"]:
						line = self.axes[i, j].axvline(x=point, color='g', label="UN")
						self.lines_UN.append(line)

				# to add the signal tag on the y-axis
				self.axes[i, j].set_ylabel(self.data_types[j * 9 + i])

		# to mark UN text on Text axes
		# TODO: Make the fontsize Accessible to the User
		for (point, note) in self.markers["points_UN"]:
			self.TextAxesLeft.text(point, 1, note, fontsize=12, rotation=45)
			self.TextAxesRight.text(point, 1, note, fontsize=12, rotation=45)

		# to mark DC
		for tag in self.markers["points_DC"].keys():
			if tag not in self.cmd_hide_dc_tags:
				plot_idx = (int(self.data_types.index(tag) % 9), int(self.data_types.index(tag) / 9))
				for point in self.markers["points_DC"][tag]:  # for every point in the list
					line = self.axes[plot_idx[0], plot_idx[1]].axvline(x=point, color='y', label="DC", zorder=1, lw=0.75)
					self.lines_DC.append(line)

		# to add the legend
		# plt.figlegend((self.lines_data[0], self.lines_DC[0], self.lines_UN[0]), labels=("Data", "DC", "UN"), loc='lower center', ncol=3, labelspacing=0.)
		self.fig.suptitle(self.file_base)



	def updateUN(self, new_xlim=(0, 0)):

		"""
		Function to update the User notes displayed on the top of the subplots
		:param new_xlim: limits of the x axis in the current plot
		:return: None
		"""
		if not self.TextAxesLeft.texts:
			return
		for text_left, text_right in zip(self.TextAxesLeft.texts, self.TextAxesRight.texts):
			if not (new_xlim[0] <= text_left.get_position()[0] <= new_xlim[1]):
				text_left.set_visible(False)
				text_right.set_visible(False)
			else:
				text_left.set_visible(True)
				text_right.set_visible(True)


	def on_xlims_change(self, axes):
		"""
		Function used to set the visibility of user note tags when zooming in on the plots.
		only hand;es user note tags. not the lines drawn on the subplots.
		:param axes: axes where the xlims were changed
		:return: None
		"""
		new_xlim = tuple(axes.get_xlim())
		self.updateUN(new_xlim=new_xlim)
		self.indicator.clear()
		self.indicator.set_xlim(self.my_syncer.time_series[0].timestamp[0], self.my_syncer.time_series[0].timestamp[-1])
		self.indicator.axvspan(new_xlim[0], new_xlim[1], facecolor="g")

	def on_mouse_click(self, event):
		"""
		Function used to update the instance variable:selected_axes which is then used by the
		hide_DC function
		:param event: mouse click event
		:return: None
		"""
		print("mouse click detected")
		if event.inaxes:
			self.selected_axes = event.inaxes
			self.selected_time = event.xdata
		else:
			if len(self.temp_highlights):
				for highlight in self.temp_highlights:
					highlight.remove()
				self.temp_highlights = []
				self.fig.canvas.draw()


	def on_key_press(self, event):
		"""
		Function that hides DC lines on the selected subplot
		:param event: key press event
		:return: None
		"""
		print("entered key press change:", event.key)
		if event.key == " ":  # hide the markers
			for line in self.lines_DC:
				if line in self.selected_axes.lines:
					line.set_visible(not line.get_visible())
			plt.pause(0.005)
			self.fig.canvas.draw()
		# TODO: replace the hard coded "10" with limits input by the user
		elif event.key == "right":
			if self.sliderEnableToggle:
				if self.slider.val + 10 <= self.my_syncer.time_series[0].timestamp[-1] - 10:
					self.slider.set_val(self.slider.val + 10)

		elif event.key == "left":
			if self.sliderEnableToggle:
				if self.slider.val - 10 >= self.my_syncer.time_series[0].timestamp[0] + 10:
					self.slider.set_val(self.slider.val - 10)
		elif event.key == "m":
			if not len(self.temp_highlights):  # if the length == 0
				for j in range(2):
					for i in range(9):
						# TODO: change the hardcoded width of window
						highlight = self.axes[i, j].axvspan(self.selected_time - 1, self.selected_time + 1, facecolor='y', alpha=0.5)
						self.temp_highlights.append(highlight)
				self.fig.canvas.draw()

		elif event.key == "a":
			new_xlim = self.axes[0, 0].get_xlim()
			for j in range(2):
				for i in range(9):
					x_low_index = int((new_xlim[0]/self.my_syncer.time_series[j * 9 + i].timestamp[-1]) * len(self.my_syncer.time_series[j * 9 + i].timestamp)) - 1
					x_high_index = int((new_xlim[1]/self.my_syncer.time_series[j * 9 + i].timestamp[-1]) * len(self.my_syncer.time_series[j * 9 + i].timestamp)) - 1
					new_ymin = min(self.my_syncer.time_series[j * 9 + i].data[x_low_index: x_high_index])
					new_ymax = max(self.my_syncer.time_series[j * 9 + i].data[x_low_index: x_high_index])
					self.axes[i, j].set_ylim([new_ymin, new_ymax])
			self.fig.canvas.draw()

	@staticmethod
	def take_closest(myList, myNumber):
		"""
		Assumes myList is sorted. Returns closest value to myNumber.

		If two numbers are equally close, return the smallest number.
		"""
		pos = bisect_left(myList, myNumber)
		if pos == 0:
			return myList[0]
		if pos == len(myList):
			return myList[-1]
		before = myList[pos - 1]
		after = myList[pos]
		if after - myNumber < myNumber - before:
			return after
		else:
			return before

	def clear_subplots(self):
		"""
		Clears all subplots
		:return: None
		"""
		for i in range(9):
			for j in range(2):
				self.axes[i, j].clear()
		self.fig.canvas.draw()

	def enable_slider(self, label):
		"""
		Function attached to the enable slider checkbox.
		if enabled, redraws the plot to contain only part of data
		if disabled, redraws the plot to contain the whole data
		:param label: the label of the checkbox clicked
		:return: None
		"""
		self.sliderEnableToggle = not self.sliderEnableToggle
		# print(self.sliderEnableToggle)
		if self.sliderEnableToggle:
			self.clear_subplots()
			self.fig.canvas.draw()
			for j in range(2):  # columns of subplot
				for i in range(9):  # rows in subplot
					# TODO: replace the hard coded "10" with limits input by the user
					closest = self.take_closest(self.my_syncer.time_series[j * 9 + i].timestamp, 20)
					last_idx = self.my_syncer.time_series[j * 9 + i].timestamp.index(closest)
					self.axes[i, j].plot(self.my_syncer.time_series[j * 9 + i].timestamp[:last_idx], self.my_syncer.time_series[j * 9 + i].data[:last_idx], linestyle='-', zorder=10, alpha=0.9)
					self.axes[i, j].autoscale(enable=True, axis='y')
					self.axes[i, j].autoscale(enable=True, axis='x')
			self.fig.canvas.draw()

		else:
			self.clear_subplots()
			self.fig.canvas.draw()
			# connect the callbacks again
			for i in range(9):
				for j in range(2):
					self.axes[i, j].callbacks.connect('xlim_changed', self.on_xlims_change)
			self.init_plot()
			self.fig.canvas.draw()

	def slide_through_data(self, val):
		"""
		Function to update the plots to slide through the entire data.
		Takes in the value of the slider, updates the plot acordingly

		:param val: value of the slider
		:return: None
		"""
		if self.sliderEnableToggle:
			print('sliding', val)
			self.clear_subplots()
			for j in range(2):
				for i in range(9):
					# TODO: replace the hard coded "10" with limits input by the user
					closest_low = self.take_closest(self.my_syncer.time_series[j * 9 + i].timestamp, val - 10)
					closest_high = self.take_closest(self.my_syncer.time_series[j * 9 + i].timestamp, val + 10)
					begin_idx = self.my_syncer.time_series[j * 9 + i].timestamp.index(closest_low)
					end_idx = self.my_syncer.time_series[j * 9 + i].timestamp.index(closest_high)
					self.axes[i, j].plot(self.my_syncer.time_series[j * 9 + i].timestamp[begin_idx:end_idx], self.my_syncer.time_series[j * 9 + i].data[begin_idx:end_idx], linestyle='-', zorder=10, alpha=0.9)
					for line in self.lines_DC:
						if line.axes == self.axes[i, j]:
							if closest_low <= line.get_xdata()[0] <= closest_high:
								self.axes[i, j].axvline(x=line.get_xdata()[0], color='r', label="DC", zorder=1, lw=0.75)

					for line in self.lines_UN:
						if not isinstance(line, tuple):  # means the line does not belong to first row of plots
							if line.axes == self.axes[i, j]:
								if closest_low <= line.get_xdata()[0] <= closest_high:
									self.axes[i, j].axvline(x=line.get_xdata()[0], color='g', label="UN", zorder=1,
															lw=0.75)
						else:
							if line[0].axes == self.axes[i, j]:
								if closest_low <= line[0].get_xdata()[0] <= closest_high:
									self.axes[i, j].axvline(x=line[0].get_xdata()[0], color='g', label="UN", zorder=1,
															lw=0.75)
									self.axes[i, j].text(line[1].get_position()[0], self.axes[i, j].get_ylim()[1],
														 line[1].get_text(), fontsize=6,
														 rotation=45)
			self.fig.canvas.draw()
