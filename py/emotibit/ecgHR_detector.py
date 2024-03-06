# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import tool
import numpy as np
from scipy import signal

def detectHR(inputFrequency = 250, maxHartReatBPM = 200, filename = "ecgHR.csv", height = 250):

    maxHartReatHertz = maxHartReatBPM / 60 # divide by 60 seconds per minute
    minumiumSampleSeparation = inputFrequency / maxHartReatHertz # gives the number of samples as a minimum between beats

    file = pd.read_csv("./cytonhr2_converted.csv")
    filtered = tool.band_filter(file[ " EXG Channel 0"], np.array([5, 49]), fs = 250)
    ind, val = signal.find_peaks(filtered, 
                                 height = height, 
                                 distance = minumiumSampleSeparation)
    
    hr = 1 / (np.diff(ind) / inputFrequency) * 60

    emotibit = pd.read_csv("ebhr2_HR.csv")

    createValidationPlot(filtered, ind)

    hrTimeStamps = file[' Timestamp'][ind][:-1] # we dont need the last one
    print(hrTimeStamps)
    
    plt.clf()
    #plt.step(hrTimeStamps, hr, where = "pre")
    plt.step(emotibit['LocalTimestamp'], emotibit['HR'], where = "pre")
    plt.savefig("emotihrplot.png")

    df = pd.DataFrame({'Timestamp': hrTimeStamps,
                       'HR':hr})
    df.to_csv(filename)


def createValidationPlot(filtered, ind, fileName = "ecg_hr_detection_validation_plot.png"):

    plt.plot(filtered)
    plt.scatter(ind, filtered[ind], color = "orange")
    plt.savefig(fileName)

def main():
    detectHR()

if __name__ == "__main__":
    main()