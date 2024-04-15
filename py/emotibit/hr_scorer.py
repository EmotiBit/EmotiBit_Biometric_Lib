# -*- coding: utf-8 -*-
import pandas as pd
import emotibit.signal as ebsig
import matplotlib.pyplot as plt
import scipy.stats as scistats
import argparse
from sklearn import linear_model

try:
    import IPython
    IPython.get_ipython.magic("matplotlib qt")
except:
    plt.ion()

def resample(fileOneName, fileOneTimestampColumn, fileTwoName, fileTwoTimestampColumn, desiredFrequency = 100):
    """
    @input fileOneName: String of the path to the first tile. (The data you are testing (dependent variable))
    @input fileOneDataColumn: String name of the column containing the HR data in file one.
    @input fileOneTimestampColumn: String name of the column containing the timestamp data in file one.
    @input fileTwoDataName: String of the path to the second file. (The data you are assuming to be truth and testing against (independent variable))
    @input fileTwoDataColumn: String name of the column containing the HR data in file two.
    @input fileTwoTimestampColumn: String name of the column containing the timestamp data in file two.
    @input desiredFrequency: OPTIONAL: int of the desired frequency to resample to, defaults to 100hz.
    
    @output: Two resampled dfs
    
    @info: Resamples the two given data sources to the desired frequency. Aligns the second source to the first source. Ensure that the sources
    cover the same amount of time, or that the second source overlaps the first source.
    """
    fileOne = pd.read_csv(fileOneName)
    fileTwo = pd.read_csv(fileTwoName)
    
    # trim file two so that it matches the size of file one
    # works on the assumption that file one is shorter, otherwise there will be unmatched data.
    fileTwoTrimmed = fileTwo.loc[(fileTwo[fileTwoTimestampColumn] >= fileOne[fileOneTimestampColumn][0]) & (fileTwo[fileTwoTimestampColumn] <= fileOne[fileOneTimestampColumn].iloc[-1])]
    fileTwoTrimmed = fileTwoTrimmed.reset_index(drop = True)

    # resample the data from both
    # we are resampling the HR data to desired frequency, this has some implications:
        # HR doesn't really have frequency in quite the same way as other measurements, since it is derivative
        # This means that we are oversampling all of the data, and that also introduces some bias:
            # For example, if the HR is slow, there are more timepoints sampled of that HR than if the HR is fast, since the resampled frequency is the same thorughout the data
            # So, if the algorithm is really good when HR is fast and really bad when HR is slow, this method will make the performance look even worse than it really is
        # So why keep the oversampling? It solves a different (bigger?) problem of being able to compare the HRs at each time point.
        # If we have the same number of samples and they are perfectly lined up, then we are able to compare them and generate some metrics for how close they are.
    resampledOne = ebsig.periodize(fileOne, fileOneTimestampColumn, desiredFrequency, start_t = fileOne[fileOneTimestampColumn][0], end_t = fileOne[fileOneTimestampColumn].iloc[-1])
    resampledTwo = ebsig.periodize(fileTwoTrimmed, fileTwoTimestampColumn, desiredFrequency, start_t = fileOne[fileOneTimestampColumn][0], end_t = fileOne[fileOneTimestampColumn].iloc[-1])
    
    # it is possible that file two has been left with some NAs in the beginning, this fixes those
    fileTwoEarlyPart = fileTwo[fileTwo[fileTwoTimestampColumn] < fileOne[fileOneTimestampColumn][0]]
    fillInHR = fileTwoEarlyPart["HR"].iloc[-1] # gets the last HR before the start of file one
    resampledTwo = resampledTwo.fillna(fillInHR) # fills in the missing values with that value

    return resampledOne, resampledTwo

def score(dataOne, dataOneColumn, dataTwo, dataTwoColumn, plotBaseName, nameOne = "Source One", nameTwo = "Source Two"):
    """
    @input dataOne: df of the first set of data (the data you are testing)
    @input dataOneColumn: string name of the column of interest in dataOne
    @input dataTwo: df of the second set of data (the data you are assuming to be the "truth"/independent variable)
    @input dataTwoColmn: string name of the column of interset in dataTwo
    
    @info: df One and df Two should already be resampled so that they have the same sampling rate and identical timestamps
    
    @output: TBD
    """

    #dataOne.to_csv("emotiRes.csv") # write the resampled to a file to check them
    #dataTwo.to_csv("cytonRes.csv")  
    if plotBaseName is not None:
        plotBothHRs(dataOne[dataOneColumn], dataTwo[dataTwoColumn], plotBaseName, nameOne, nameTwo)
    # we use this simple linear regression to get some stats, mainly interested in r, the correlation between the two
    # note that because the relationship is not necessarily linear, r is not necessarily the best metric, but we still record it so we can understand how the value of r fits into the bigger picture
    slope, intercept, r, p, std_err = scistats.linregress(dataTwo[dataTwoColumn], dataOne[dataOneColumn])
    # we choose to use spearman's rank correlation since it can help us to understand if they are well correlated, even if the distribution is non-parametric
    spearman_r = scistats.spearmanr(dataTwo[dataTwoColumn], dataOne[dataOneColumn])
    rho = spearman_r[0]
    # we also decided to report the kendall rank correlation coefficient, another way of looking at how well the two signals are correlated 
    tau, p_val = scistats.kendalltau(dataTwo[dataTwoColumn], dataOne[dataOneColumn])

    if plotBaseName is not None:
        scatterPlot(dataOne[dataOneColumn], dataTwo[dataTwoColumn], slope, intercept, r, rho, tau, plotBaseName, nameOne, nameTwo)

    return slope, intercept, r, rho, tau, p, std_err
    
def plotBothHRs(dataOneHR, dataTwoHR, plotBaseName, nameOne = "Source One", nameTwo = "Source Two"):
    """
    @input: dataOneHR: series of data containing the HR for data one
    @input: dataTwoHR: series of data containing the HR for data two
    @input: nameOne: OPTIONAL: name for data one, defaults to 'Source One'
    @input: nameTwo: OPTIONAL: name for data two, defaults to 'Source Two'
    """
    
    plt.clf()
    plt.rcParams.update(plt.rcParamsDefault)
    plt.figure(figsize = (8, 6))
    plt.plot(dataOneHR, label = nameOne)
    plt.plot(dataTwoHR, label = nameTwo)
    plt.legend(loc = "upper left")
    plt.xlabel("Time")
    plt.ylabel("HR")
    plt.title(nameOne + " and " + nameTwo + " HR")
    plt.savefig(plotBaseName + "_resampletest.png", dpi = 600)
    
def scatterPlot(dataOneHR, dataTwoHR, slope, intercept, r, rho, tau, plotBaseName, nameOne = "Source One", nameTwo = "Source Two"):
    """
    @input dataOneHR: series of data containing the HR for data one (the dependent variable, which is being tested)
    @input dataTwoHR: series of data containing the HR for data two (the independent/truth variable, which is being tested against)
    @input slope: float of the slope value of the regression line for the scatter plot
    @input intercept: float of the intercept value of the regression line for the scatter plot
    @input nameOne: OPTIONAL: a string for the label of dataone
    @input nameTwo: OPTIONAL: a string for the label of dataTwo
    """
    
    plt.clf()
    plt.rc('xtick', labelsize = 3.5)
    plt.rc('ytick', labelsize = 3.5)
    plt.rc('axes', linewidth = 0.5)
    plt.figure(figsize = (3.3, 3.3))
    plt.scatter(dataTwoHR, dataOneHR, s = 0.5)
    plt.xlabel(nameTwo, fontsize = 7)
    plt.ylabel(nameOne, fontsize = 7)
    plt.title(nameTwo + " vs. " + nameOne + " HR, with Regression Line", fontsize = 7)
    plt.text(min(dataTwoHR), max(dataOneHR) - 39, f"Slope: {slope:.4f}\nIntercept: {intercept:.4f}\nr: {r:.4f}\nrho: {rho:.4f}\ntau: {tau:.4f}", fontsize = 5)
    
    def slopeLine(x):
        return slope * x + intercept
    thisSlopeLine = list(map(slopeLine, dataTwoHR))
    
    plt.plot(dataTwoHR, thisSlopeLine, color = "magenta", linewidth = 0.5)
    plt.tick_params(axis = "both", which = "major", labelsize = 7)
    plt.savefig(plotBaseName + "_scatter.png", dpi = 200)
    plt.rcParams.update(plt.rcParamsDefault)
    
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-hr1", "--heartRateOne", action = "store", type = str, nargs = 1, help = "Path to the file containing HR data for source one. This should be the dependent source (the one you are testing).")
    parser.add_argument("-t1", "--timestampOne", action = "store", type = str, nargs = 1, help = "Name of the column in source one that contains the timestamps.")
    parser.add_argument("-d1", "--dataOne", action = "store", type = str, nargs = 1, help = "Name of the column in source one that contains the HR data.")
    parser.add_argument("-hr2", "--heartRateTwo", action = "store", type = str, nargs = 1, help = "Path to the file containing HR data for source two. This should be the indpendent source (Your source of truth, which you are testing against).")
    parser.add_argument("-t2", "--timestampTwo", action = "store", type = str, nargs = 1, help = "Name of the column in source two that contains the timestamps.")
    parser.add_argument("-d2", "--dataTwo", action = "store", type = str, nargs = 1, help = "Name of the column in source two that contains the HR data.")
    parser.add_argument("-f", "--frequency", action = "store", type = int, nargs = 1, help = "Frequency of device with lower frequency. (e.g. if source one is 250 hz and source two is 125 hz, set this to 125).")
    parser.add_argument("-n1", "--nameOne", action = "store", type = str, nargs = "?", help = "OPTIONAL: Name for source one, used in plots.")
    parser.add_argument("-n2", "--nameTwo", action = "store", type = str, nargs = "?", help = "OPTIONAL: Name for source two, used in plots.")  
    parser.add_argument("-o", "--output", action = "store", type = str, nargs = "?", help = "OPTIONAL: Name for the outputs. Name will be used to generate a plot output such as <provided-name>-scatter.png and <provided-name>-resampledHR.png. If no name is provided, plots are not written")
    args = parser.parse_args()
    
    fileOne = args.heartRateOne[0]
    timeColOne = args.timestampOne[0]
    dataColOne = args.dataOne[0]
    # print(fileOne, timeColOne, dataColOne)
    
    fileTwo = args.heartRateTwo[0]
    timeColTwo = args.timestampTwo[0]
    dataColTwo = args.dataTwo[0]
    # print(fileTwo, timeColTwo, dataColTwo)
    
    frequency = args.frequency[0]
    nameOne = "Source One"
    if args.nameOne is not None:
        nameOne = args.nameOne
    nameTwo = "Source Two"
    if args.nameTwo is not None:
        nameTwo = args.nameTwo
    # print(frequency, nameOne, nameTwo)
    plotBaseName = None
    if args.output is not None:
        plotBaseName = args.output
    
    
    print("===== BEGINNING RESAMPLING to " + str(frequency) + " hz =====")
    dataOne, dataTwo = resample(fileOne, timeColOne, fileTwo, timeColTwo, frequency)
    print("===== FINISHED RESAMPLING =====")
    print("===== BEGINNING SCORING =====")
    slope, intercept, r, rho, tau, p, std_err = score(dataOne, dataColOne, dataTwo, dataColTwo, plotBaseName, nameOne, nameTwo)
    print("===== FINISHED SCORING =====")
    print("\nSLOPE: ", slope)
    print("INTERCEPT: ", intercept)
    print("R: ", r)
    print("RHO: ", rho)
    print("TAU: ", tau)
    print("P: ", p)
    print("STD_ERR: ", std_err)
    print("\n=== END ===")
    
if __name__ == "__main__":
    main()