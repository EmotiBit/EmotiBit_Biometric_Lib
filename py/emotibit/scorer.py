# -*- coding: utf-8 -*-
import pandas as pd
import emotibit.emotibit_signal as ebsig
import matplotlib.pyplot as plt
import scipy.stats as scistats
import statsmodels.api as sm
import argparse

try:
    import IPython
    IPython.get_ipython.magic("matplotlib qt")
except AttributeError:
    plt.ion()


def resample(file_one_name,
             file_one_timestamp_col,
             file_one_data_col,
             file_two_name,
             file_two_timestamp_col,
             file_two_data_col,
             desired_frequency=100):
    """
    @input file_one_name:
        String of the path to the first tile. (The data you are testing
        (dependent variable))
    @input file_one_data_col:
        String name of the column containing the data in file one.
    @input file_one_time_col:
        String name of the column containing the timestamp data in file one.
    @input fileTwoDataName:
        String of the path to the second file.
        (The data you are assuming to be truth and testing against
        (independent variable))
    @input file_two_data_col:
        String name of the column containing the data in file two.
    @input file_two_timestamp_column:
        String name of the column containing the timestamp data in file two.
    @input desired_frequency:
        OPTIONAL: int of the desired frequency to resample to,
        defaults to 100hz.

    @output: Two resampled dfs

    @info: Resamples the two given data sources to the desired frequency.
    Aligns the second source to the first source. Ensure that the sources
    cover the same amount of time,
    or that the second source overlaps the first source.
    """
    file_one = pd.read_csv(file_one_name)
    file_two = pd.read_csv(file_two_name)

    # Find the overlapping time range between two files
    start_time = max(file_one[file_one_timestamp_col].iloc[0], file_two[file_two_timestamp_col].iloc[0])
    end_time = min(file_one[file_one_timestamp_col].iloc[-1], file_two[file_two_timestamp_col].iloc[-1])

    # Trim file_one to the overlap
    file_one_trimmed = file_one.loc[
        (file_one[file_one_timestamp_col] >= start_time) &
        (file_one[file_one_timestamp_col] <= end_time)
    ].reset_index(drop=True)

    # Trim file_two to the overlap
    file_two_trimmed = file_two.loc[
        (file_two[file_two_timestamp_col] >= start_time) &
        (file_two[file_two_timestamp_col] <= end_time)
    ].reset_index(drop=True)

    # We are resampling the data to desired frequency,
    # this has some implications:
    # For heart rate, HR doesn't really have frequency in quite the same way
    # as other measurements, since it is derivative.
    # This means that we are oversampling all of the data,
    # and that also introduces some bias:
    # For example, if the HR is slow, there are more timepoints sampled
    # of that HR than if the HR is fast, since the resampled
    # frequency is the same thorughout the data.
    # So, if the algorithm is really good when HR is fast and really
    # bad when HR is slow, this method will make the
    # performance look even worse than it really is.
    # So why keep the oversampling? It solves a different (bigger?)
    # problem of being able to compare the HRs at each time point.
    # If we have the same number of samples and they are perfectly lined up,
    # then we are able to compare them and generate
    # some metrics for how close they are.
    resampled_one = ebsig.periodize(file_one_trimmed,
                                    file_one_timestamp_col,
                                    desired_frequency,
                                    start_t=start_time,
                                    start_val=file_one_trimmed[file_one_data_col].iloc[0],
                                    end_t=end_time)
    resampled_two = ebsig.periodize(file_two_trimmed,
                                    file_two_timestamp_col,
                                    desired_frequency,
                                    start_t=start_time,
                                    start_val=file_two_trimmed[file_two_data_col].iloc[0],
                                    end_t=end_time)
    
    return resampled_one, resampled_two


def score(data_one,
          data_one_column,
          data_two,
          data_two_column,
          plot_base_name,
          name_one="Source One",
          name_two="Source Two",
          data_label="Data"):
    """
    @input data_one:
        df of the first set of data (the data you are testing)
    @input data_one_column:
        string name of the column of interest in data_one
    @input data_two:
        df of the second set of data
        (the data you are assuming to be the "truth"/independent variable)
    @input dataTwoColmn:
        string name of the column of interset in data_two

    @info: df One and df Two should already be resampled so
        that they have the same sampling rate and identical timestamps

    @output: The statistics from the comparison and saves plots to the current directory
    """

    # Plot two data sources along temporal axis
    plot_both(data_one[data_one_column],
                  data_two[data_two_column],
                  plot_base_name,
                  data_label,
                  name_one,
                  name_two)
    # We use this simple linear regression to get some stats,
    # mainly interested in r, the correlation between the two
    # note that because the relationship is not necessarily linear,
    # r is not necessarily the best metric, but we still record it
    # so we can understand how the value of r fits into the bigger picture
    (slope,
     intercept,
     r,
     p,
     std_err) = scistats.linregress(data_one[data_one_column],
                                    data_two[data_two_column])
    # We choose to use spearman's rank correlation since
    # it can help us to understand if they are well correlated,
    # even if the distribution is non-parametric.
    spearman_r = scistats.spearmanr(data_one[data_one_column],
                                    data_two[data_two_column])
    rho = spearman_r[0]
    # We also decided to report the kendall rank correlation coefficient.
    # Another way of looking at how well the two signals are correlated.
    tau, _ = scistats.kendalltau(data_one[data_one_column],
                                 data_two[data_two_column])

    # Scatter plot to show linear regression line
    scatter_plot(data_one[data_one_column],
                  data_two[data_two_column],
                  slope,
                  intercept,
                  r,
                  rho,
                  tau,
                  plot_base_name,
                  data_label,
                  name_one,
                  name_two)
    
    # Bland-Altman mean difference plot to visualize the agreement between the two data sources
    mean_diff_plot(
      data_one[data_one_column], 
      data_two[data_two_column],
      plot_base_name,
      data_label,
      name_one,
      name_two
    )

    return slope, intercept, r, rho, tau, p, std_err


def plot_both(data_one,
              data_two,
              plot_base_name,
              data_label,
              name_one="Source One",
              name_two="Source Two"):
    """
    @input: data_one_hr: series of data for data one
    @input: data_two_hr: series of data for data two
    @input: name_one: OPTIONAL: name for data one, defaults to 'Source One'
    @input: name_two: OPTIONAL: name for data two, defaults to 'Source Two'
    """

    plt.clf()
    plt.rcParams.update(plt.rcParamsDefault)
    plt.figure(figsize=(5, 4))
    plt.plot(data_one, label=name_one)
    plt.plot(data_two, label=name_two)
    plt.legend(loc="upper left")
    plt.xlabel("Time")
    plt.ylabel(data_label)
    plt.title(name_one + " and " + name_two + " " + data_label)
    plt.savefig(plot_base_name + "_resampled.png", dpi=500, bbox_inches='tight')

def scatter_plot(data_one,
                 data_two,
                 slope,
                 intercept,
                 r,
                 rho,
                 tau,
                 plot_base_name,
                 data_label,
                 name_one="Source One",
                 name_two="Source Two"):
    """
    @input data_one_hr:
        series of data containing the HR for data one
        (the dependent variable, which is being tested)
    @input data_two_hr:
        series of data containing the HR for data two
        (the independent/truth variable, which is being tested against)
    @input slope:
        float of the slope value of the regression line for the scatter plot
    @input intercept:
        float of the intercept value of regression line for the scatter plot
    @input name_one: OPTIONAL:
        a string for the label of data_one
    @input name_two: OPTIONAL:
        a string for the label of data_two
    """

    plt.clf()
    plt.rc('xtick', labelsize=3.5)
    plt.rc('ytick', labelsize=3.5)
    plt.rc('axes', linewidth=0.5)
    plt.figure(figsize=(5, 5))
    plt.scatter(data_one, data_two, s=0.5)
    plt.xlabel(name_one, fontsize=7)
    plt.ylabel(name_two, fontsize=7)
    plt.title(name_one + " vs. " + name_two + " " + data_label + ", with Regression Line",
              fontsize=7)
    plt.text(min(data_one),
             max(data_two),
             f"Slope: {slope:.4f}\nIntercept: {intercept:.4f}"
             f"\nr: {r:.4f}\nrho: {rho:.4f}\ntau: {tau:.4f}",
             fontsize=8,
             verticalalignment='top',)

    def slope_line(x):
        return slope * x + intercept
    this_slope_line = list(map(slope_line, data_one))

    plt.plot(data_one, this_slope_line, color="magenta", linewidth=0.5)
    plt.tick_params(axis="both", which="major", labelsize=7)
    plt.savefig(plot_base_name + "_scatter.png", dpi=500, bbox_inches='tight')
    plt.rcParams.update(plt.rcParamsDefault)

def mean_diff_plot(data_one,
              data_two,
              plot_base_name,
              data_label,
              name_one="Source One",
              name_two="Source Two"):
    plt.clf()
    plt.figure(figsize=(5, 5))
    sm.graphics.mean_diff_plot(data_one, data_two)
    plt.title(name_one + " vs. " + name_two + " - " + data_label + " Mean Difference Plot")
    plt.ylabel(name_one + " - " + name_two)
    plt.savefig(plot_base_name + "_mean-diff.png", dpi=500, bbox_inches='tight')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1",
                        "--file_one",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Path to the file containing data
                         for source one. This should be the
                         dependent source (the one you are testing).""")
    parser.add_argument("-t1",
                        "--timestamp_one",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Name of the column in source
                        one that contains the timestamps.""")
    parser.add_argument("-d1",
                        "--data_one",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Name of the column in source
                          one that contains the HR data.""")
    parser.add_argument("-f2",
                        "--file_two",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Path to the file containing data
                         for source two.
                         This should be the indpendent source
                         (Your source of truth,
                         what you are testing against).""")
    parser.add_argument("-t2",
                        "--timestamp_two",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Name of the column in source two
                          that contains the timestamps.""")
    parser.add_argument("-d2",
                        "--data_two",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Name of the column in source
                          two that contains the HR data.""")
    parser.add_argument("-f",
                        "--frequency",
                        action="store",
                        type=int,
                        nargs=1,
                        help="""Frequency of device with lower frequency.
                         (e.g. if source one is 250hz and source two is 125hz,
                         set this to 125).""")
    parser.add_argument("-o",
                        "--output",
                        action="store",
                        type=str,
                        nargs=1,
                        help="""Name for the outputs.
                          Name will be used to generate a plot output
                          such as <provided-name>-scatter.png.""")
    parser.add_argument("-n1",
                        "--name_one",
                        action="store",
                        type=str,
                        nargs="?",
                        help="OPTIONAL: Name for source one, used in plots.")
    parser.add_argument("-n2",
                        "--name_two",
                        action="store",
                        type=str,
                        nargs="?",
                        help="OPTIONAL: Name for source two, used in plots.")
    parser.add_argument("-l",
                        "--data_label",
                        action="store",
                        type=str,
                        nargs="?",
                        help="OPTIONAL: Label for the data.")
  
    args = parser.parse_args()

    file_one = args.file_one[0]
    time_col_one = args.timestamp_one[0]
    data_col_one = args.data_one[0]

    file_two = args.file_two[0]
    time_col_two = args.timestamp_two[0]
    data_col_two = args.data_two[0]

    plot_base_name = args.output[0]
    frequency = args.frequency[0]
    name_one = "Source One"
    if args.name_one is not None:
        name_one = args.name_one
    name_two = "Source Two"
    if args.name_two is not None:
        name_two = args.name_two
    data_label = "Data"
    if args.data_label is not None:
        data_label = args.data_label

    print("===== BEGINNING RESAMPLING to " + str(frequency) + " hz =====")
    data_one, data_two = resample(file_one,
                                  time_col_one,
                                  data_col_one,
                                  file_two,
                                  time_col_two,
                                  data_col_two,
                                  frequency)
    print("===== FINISHED RESAMPLING =====")
    print("===== BEGINNING SCORING =====")
    slope, intercept, r, rho, tau, p, std_err = score(data_one,
                                                      data_col_one,
                                                      data_two,
                                                      data_col_two,
                                                      plot_base_name,
                                                      name_one,
                                                      name_two,
                                                      data_label)
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
