import numpy as np
import pandas as pd

from scipy import signal
from scipy.signal import lfilter, detrend

from numpy import linalg as LA

def butter_lowpass(cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a lowpass filter

    Args:
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        b, a ([nbarray, nbarray]): Numerator (b) and denominator (a) polynomials of the IIR filter.
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    #b, a = butter(order, normal_cutoff, btype='low', analog=False)
    b, a = signal.bessel(order, normal_cutoff, btype='lowpass', analog=False, norm='delay')
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a lowpass filter

    Args:
        data (array): Data to filter
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        y, group_delay ([nbarray, nbarray]): The output of the digital filter and the group_delay of the filter.
    """
    b, a = butter_lowpass(cutoff, fs, order=order)
    #b, a = signal.bessel(cutoff, fs, 'low', order=order, analog=True, norm='delay')
    w, h = signal.freqz(b, a, fs=fs)
    #print(w)
    group_delay = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
    y = lfilter(b, a, data)
    return y, group_delay

def lowpass_filter(data, cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a lowpass filter

    Args:
        data (array): Data to filter
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        dataf (nbarray): The filtered data.
    """
    y, gd1 = butter_lowpass_filter(data, cutoff, fs, order)
    #print(gd1)
    delay = np.int(np.round(gd1[np.int(cutoff.mean()/((fs/2.0)/511.0))]))
    #print(delay)
    dataf = np.zeros(data.shape)
    dataf[0:dataf.shape[0]-delay] = y[delay:]
    
    return dataf

def butter_bandpass(cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a bandpass filter

    Args:
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        b, a ([nbarray, nbarray]): Numerator (b) and denominator (a) polynomials of the IIR filter.
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.bessel(order, normal_cutoff, btype='bandpass', analog=False, norm='delay')
    return b, a

def butter_bandpass_filter(data, cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a bandpass filter

    Args:
        data (array): Data to filter
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        y, group_delay ([nbarray, nbarray]): The output of the digital filter and the group_delay of the filter.
    """
    b, a = butter_bandpass(cutoff, fs, order=order)
    w, h = signal.freqz(b, a, fs=fs)
    group_delay = -np.diff(np.unwrap(np.angle(h))) / np.diff(w)
    y = lfilter(b, a, data)
    return y, group_delay

def band_filter(data, cutoff, fs, order=4):
    """Calculate coefficients (a, b) for a bandpass filter

    Args:
        data (array): Data to filter
        cutoff (array): Critical frequencies
        fs (int): Sampling frequency
        order (int, optional): Filter order. Defaults to 4.

    Returns:
        dataf (nbarray): The filtered data.
    """
    y, gd1 = butter_bandpass_filter(data, cutoff, fs, order)
    delay = int(np.round(gd1[int(cutoff.mean()/((fs/2.0)/511.0))]))
    dataf = np.zeros(data.shape)
    dataf[0:dataf.shape[0]-delay] = y[delay:]
    
    return dataf

def get_RR_segment(RR, RR_pos, start, stop, fs):
    """Get the RR segment between start and stop position

    Args:
        RR (list): 
        RR_pos ([list]): Peaks position
        start (float): Start position in second
        stop (float): Stop position in second
        fs (int): Critical frequency

    Returns:
        [array]: The RR segments between Start and Stop
    """
    # Start and Stop are in seconds
    ind = np.where((RR_pos/fs > start) & (RR_pos/fs < stop))[0]

    return RR[ind]

def get_HR_series(wd, window_size=8, window_stride=2, fs=100):
    """Get the HR series

    Args:
        wd (dict): [description]
        window_size (int, optional): [description]. Defaults to 8.
        window_stride (int, optional): [description]. Defaults to 2.
        fs (int, optional): [description]. Defaults to 100.

    Returns:
        [type]: [description]
    """
    length = len(wd["hr"])/fs

    ind = np.where(np.array(wd["RR_masklist"])==0)[0]

    RR = np.array(wd["RR_list"])[ind]
    RR_pos = np.array(wd["peaklist"])[ind]

    HR = []

    for t in range(0, int(length)-window_size, window_stride):
        HR.append(60000/get_RR_segment(RR, RR_pos, t, t+window_size, fs).mean())

    return np.array(HR)

def get_RMSSD(wd):
    """Calculate RMSSD from wd

    Args:
        wd (dict): working data from Heartpy

    Returns:
        RMSSD (float): RMSSD value
    """
    RR = np.array(wd["RR_list_cor"])

    RMSSD = 0

    for i in range(RR.shape[0]-1):
        RMSSD += (RR[i+1]-RR[i])**2

    RMSSD = np.sqrt((1/(RR.shape[0]-1))*(RMSSD))/1000

    return RMSSD

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]

def interp_nan(y):
    """Interpolation for nan values

    Args:
        y (nbarray): Array containing nan values

    Returns:
        y (nbarray): Corrected array
    """
    nans, x = nan_helper(y)
    y[nans] = np.interp(x(nans), x(~nans), y[~nans])

    return y

from sklearn.linear_model import LinearRegression

def find_ts_param(path):
    """Generate the timestamp from "TS" in Emotibit data

    Args:
        path (string): Path of the Emotibit file

    Returns:
        a, b (float, float): Coefficients of the linear function
    """
    TL_df = pd.read_csv(path, names = ["Ind", "A1", "A2", "A3", "A4", "A5", "TL"])
    TL_df.TL = pd.to_datetime(TL_df.TL, format="%Y-%m-%d_%H-%M-%S-%f")
    TL_df['TS'] = TL_df.TL.values.astype(np.int64) / 10 ** 9
    TL = TL_df.values

    reg = LinearRegression()

    mdl = reg.fit(TL[:,0:1], TL[:,-1])

    a = mdl.coef_[0]
    b = mdl.intercept_
    
    return a, b

def load_merge_signals(path, sig, ppg_filter=True, G_filter=True):
    """Load and merge Emotibit CSV files

    Args:
        path (string): Path of the folder containing csv files
        sig (list): List of each signal to be load and merge
        ppg_filter (bool, optional): Apply filter to PPG signals. Defaults to True.
        G_filter (bool, optional): Apply filter to gyroscope signals. Defaults to True.

    Returns:
        M_df (dataframe): Dataframe containing all "sig" merged together.
    """
    
    S_df = []
    
    for s in sig:
        #S_df.append(load_emotibit(path+s+".csv"))
        S_df.append(load_emotibit(path[:-4]+s+path[-4:]+".csv"))
    
    i = 0

    M_df = pd.merge_asof(S_df[i][["EpochTimestamp", sig[i]]], S_df[i+1][["EpochTimestamp", sig[i+1]]], left_on="EpochTimestamp", right_on="EpochTimestamp", direction="nearest")

    for i in range(1, len(S_df)-1):
        M_df = pd.merge_asof(M_df, S_df[i+1][["EpochTimestamp", sig[i+1]]], left_on="EpochTimestamp", right_on="EpochTimestamp", direction="nearest")
    
    if ppg_filter:
        # Butterworth filter before extracting windows
        M_df["PI"] = band_filter(M_df["PI"], np.array([0.4, 4]), 25)
        M_df["PG"] = band_filter(M_df["PG"], np.array([0.4, 4]), 25)
        M_df["PR"] = band_filter(M_df["PR"], np.array([0.4, 4]), 25)
        
    if G_filter:
        # Butterworth filter before extracting windows
        M_df["GX"] = band_filter(M_df["GX"], np.array([0.4, 4]), 25)
        M_df["GY"] = band_filter(M_df["GY"], np.array([0.4, 4]), 25)
        M_df["GZ"] = band_filter(M_df["GZ"], np.array([0.4, 4]), 25)
    
    return M_df

def load_merge_signals_7_12(path, sig, ppg_filter=True, G_filter=True):
    """Load and merge Emotibit CSV files for participants 7 to 12 only

    Args:
        path (string): Path of the folder containing csv files
        sig (list): List of each signal to be load and merge
        ppg_filter (bool, optional): Apply filter to PPG signals. Defaults to True.
        G_filter (bool, optional): Apply filter to gyroscope signals. Defaults to True.

    Returns:
        M_df (dataframe): Dataframe containing all "sig" merged together.
    """
    
    a, b = find_ts_param(path[:-4]+"TL"+path[-4:]+".csv")
    
    S_df = []
    
    for s in sig:
        print(s)
        #S_df.append(load_emotibit(path+s+".csv"))
        S_df.append(pd.read_csv(path[:-4]+s+path[-4:]+".csv", names = ["Ind", "A1", "A2", "A3", "A4", "A5", s]))
        S_df[-1]["TS"] = S_df[-1]["Ind"]*a+b
    
    i = 0

    M_df = pd.merge_asof(S_df[i][["TS", sig[i]]], S_df[i+1][["TS", sig[i+1]]], left_on="TS", right_on="TS", direction="nearest")

    for i in range(1, len(S_df)-1):
        M_df = pd.merge_asof(M_df, S_df[i+1][["TS", sig[i+1]]], left_on="TS", right_on="TS", direction="nearest")
    
    if ppg_filter:
        # Butterworth filter before extracting windows
        M_df["PI"] = band_filter(M_df["PI"], np.array([0.4, 4]), 25)
        M_df["PG"] = band_filter(M_df["PG"], np.array([0.4, 4]), 25)
        M_df["PR"] = band_filter(M_df["PR"], np.array([0.4, 4]), 25)
        
    if G_filter:
        # Butterworth filter before extracting windows
        M_df["GX"] = band_filter(M_df["GX"], np.array([0.4, 4]), 25)
        M_df["GY"] = band_filter(M_df["GY"], np.array([0.4, 4]), 25)
        M_df["GZ"] = band_filter(M_df["GZ"], np.array([0.4, 4]), 25)
        
    M_df["EpochTimestamp"] = M_df["TS"]
    
    return M_df

def zero_mean(signal):
    """Convert data to zero mean and unit variance 

    Args:
        signal (nbarray) : Signal to convert

    Returns
        unit (array): Signal converted
    """
    unit = (signal - signal.mean())/signal.std()
    
    return unit

def stress_detector(df, resample="50L", n_smooth=100, th=0.0015, normalization="no_norm"):
    """Detect SCRs in EDA data

    Args:
        df (dataframe): Dataframe with EDA data
        resample (str, optional): Resampling parameter (50L = 50 ms). Defaults to "50L".
        n_smooth (int, optional): Smoothing parameter. Defaults to 100.
        th (float, optional): Threshold for the stress detection. Defaults to 0.0015.
        normalization (str, optional): Signal normalization (zero_mean). Defaults to "no_norm".
        corr_sig (str, optional): [description]. Defaults to "signal".

    Returns:
        df_eda (dataframe): Dataframe containing additional information for EDA data
    """
    
    from sklearn.metrics import f1_score

    fc = df[["Time", "EDA_FC"]][df["EDA_FC"].notna()].copy()
    fc["Time_ts"] = pd.to_datetime(fc['Time'], unit='s')

    fc = fc.resample(resample, on="Time_ts").mean()

    em = df[["Time", "EA"]][df["EA"].notna()].copy()
    em["Time_ts"] = pd.to_datetime(em['Time'], unit='s')

    em = em.resample(resample, on="Time_ts").mean()

    df_merge = pd.merge_asof(fc, em, "Time_ts", direction="nearest", suffixes=("","_y"))

    df_merge = df_merge[df_merge["EA"].notna()].copy()
    
    sig_fc = df_merge["EDA_FC"].values
    sig_em = df_merge["EA"].values

    if normalization == "zero_mean":
        sig_fc = zero_mean(sig_fc)
        sig_em = zero_mean(sig_em)

    smo_fc = smooth(sig_fc, n_smooth)
    d_sig_fc = np.diff(smo_fc)

    smo_em = smooth(sig_em, n_smooth)
    d_sig_em = np.diff(smo_em)

    d_sig_fc_th = d_sig_fc.copy()
    d_sig_fc_th[d_sig_fc_th<th] = 0
    d_sig_fc_th[d_sig_fc_th>=th] = 1

    d_sig_em_th = d_sig_em.copy()
    d_sig_em_th[d_sig_em_th<th] = 0
    d_sig_em_th[d_sig_em_th>=th] = 1
    
    plot_shift = (n_smooth/2)*0.2
    
    df_eda = df_merge[["Time"]][df_merge["EA"].notna()].copy()
    df_eda["EDA_FC_NORM"] = sig_fc
    df_eda["EDA_EM_NORM"] = sig_em
    df_eda["EDA_FC_SMO"] = smo_fc[:-n_smooth+1]
    df_eda["EDA_EM_SMO"] = smo_em[:-n_smooth+1]
    df_eda["EDA_FC_D"] = d_sig_fc[:-n_smooth+2]
    df_eda["EDA_EM_D"] = d_sig_em[:-n_smooth+2]
    df_eda["EDA_FC_TH"] = d_sig_fc_th[:-n_smooth+2]
    df_eda["EDA_EM_TH"] = d_sig_em_th[:-n_smooth+2]
    df_eda["EDA_PLOT_SHIFT"] = np.tile(plot_shift, sig_fc.shape)
    
    return df_eda

def load_emotibit(path):
    """Load Emotibit csv files using Pandas

    Args:
        path (string): Path of the csv file

    Returns:
        em_df (dataframe): Dataframe with Emotibit data
    """
    # Use Pandas to load csv files
    em_df = pd.read_csv(path)

    return em_df

def load_flexcomp(path):
    """Load Flexcomp csv files using Pandas

    Args:
        path (string): Path of the csv file

    Returns:
        em_df (dataframe): Dataframe with Flexcomp data
    """
    fc_df = pd.read_csv(path, sep=";", skiprows=[0,1,2,3,4,5,7], decimal=",")
    
    return fc_df

def sync_pos(em_df, fc_df, em_fs=25, fc_fs=256, margin=2):
    """Algorithm to synchronize Flexcomp and Emotibit. (Not perfect)

    Args:
        em_df (dataframe): Emotibit dataframe
        fc_df (dataframe): Flexcomp dataframe
        em_fs (int, optional): Emotibit critical frequency. Defaults to 25.
        fc_fs (int, optional): Flexcomp critical frequency. Defaults to 256.
        margin (int, optional): Margin to search peaks. Defaults to 2.

    Returns:
        [em_mid_s, em_mid_e] (list): Timestamp start and end values
        [fc_mid_s, fc_mid_e] (list): Timestamp start and end values
        em_df (dataframe): Emotibit dataframe
        fc_df (dataframe): Flexcomp dataframe
        error (float): Error between the total length between Emotibit and Flexcomp
    """
    # Emotibit
    em_A = np.abs(np.diff(em_df["AX"].values))+np.abs(np.diff(em_df["AY"].values))+np.abs(np.diff(em_df["AZ"].values))

    S = np.argsort(em_A[0:20*em_fs])[::-1]

    em_mid_s = np.int((S[0:6].min() + S[0:6].max())/2) + margin*em_fs

    S = np.argsort(em_A[-20*em_fs:])[::-1]

    em_mid_e = em_A.shape[0] - 20*em_fs + np.int((S[0:6].min() + S[0:6].max())/2) - margin*em_fs

    em_df = em_df[em_mid_s:em_mid_e]
    
    # Flexcomp
    fc_A = np.abs(np.diff(fc_df["TT-AV Sync - 1J"].values))

    S = np.array(np.where(fc_A[0:20*fc_fs]>0.1)[0])

    fc_mid_s = np.int((S.min() + S.max())/2) + margin*fc_fs

    S = np.array(np.where(fc_A[-20*fc_fs:]>0.1)[0])

    fc_mid_e = fc_A.shape[0] - 20*fc_fs + (np.int((S.min() + S.max())/2)) - margin*fc_fs
    
    fc_df = fc_df[fc_mid_s:fc_mid_e]
    
    error = np.abs((fc_df["Time"].values[-1] - fc_df["Time"].values[0]) - (em_df["EpochTimestamp"].values[-1] - em_df["EpochTimestamp"].values[0]))
    print()
    
    fc_df.loc[:,"Time"] = fc_df.loc[:,"Time"] - fc_df["Time"].values[0]
    em_df.loc[:,"Time"] = em_df.loc[:,"EpochTimestamp"] - em_df["EpochTimestamp"].values[0]

    return [em_mid_s, em_mid_e], [fc_mid_s, fc_mid_e], em_df, fc_df, error

def sync_pos_without_button(em_df, fc_df):
    """Algorithm to synchronize Flexcomp and Emotibit. (Not perfect)

    Args:
        em_df (dataframe): Emotibit dataframe
        fc_df (dataframe): Flexcomp dataframe

    Returns:
        [0, em_mid_e] (list): Timestamp start and end values
        [0, fc_mid_e] (list): Timestamp start and end values
        em_df (dataframe): Emotibit dataframe
        fc_df (dataframe): Flexcomp dataframe
        error (float): Error between the total length between Emotibit and Flexcomp
    """
    # Emotibit
    em_df = em_df[:]
    
    # Flexcomp
    fc_df = fc_df[:]
    
    #Error
    error = np.abs((fc_df["Time"].values[-1] - fc_df["Time"].values[0]) - (em_df["EpochTimestamp"].values[-1] - em_df["EpochTimestamp"].values[0]))
    
    fc_df.loc[:,"Time"] = fc_df.loc[:,"Time"] - fc_df["Time"].values[0]
    em_df.loc[:,"Time"] = em_df.loc[:,"EpochTimestamp"] - em_df["EpochTimestamp"].values[0]

    return [0, em_df.values.shape[0]], [0, fc_df.values.shape[0]], em_df, fc_df, error

def adjust_EDA(df, Filter=True, EL_only=False):
    """ Correct the calculation of EDA using ER and EL 

    Parameters
    ----------
    df1 : dataframe
        Dataframe containing the columns "EA", "EL", "ER".
    
    Returns
    -------
    ind : Array(1D)
        Array of the index
    eda : Array(1D)
        Array of the data
        
    """
    
    el = df["EL"][df["EL"].notna()].values
    er = df["ER"][df["ER"].notna()].values

    el = lowpass_filter(el, np.array([2]), 19.5)
    er = lowpass_filter(er, np.array([2]), 19.5)
    
    eda = (er - 1.65)/10
    if EL_only:
        eda = el
    else:
        eda += el
    
    eda = (3.3-eda)/(5*eda)
    
    return df["EA"].index, eda

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise(ValueError, "smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise(ValueError, "Input vector needs to be bigger than window size.")


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise(ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

def merge_nearest(left, right, on, column):
    """Merge columns in the array "column" from the right dataframe to the left dataframe with the "on" column 

    Args:
        left (dataframe): [description]
        right (dataframe): [description]
        on (string): Column name of the commun timestamp 
        column (list): Columns to merge from the right dataframe to the left dataframe

    Returns:
        left (dataframe): Dataframe containing dataframe "left" with new columns from dataframe "right"
    """
    t = right[on].values
    tdf = left[on].values

    ind = []

    for i in t:
        index = np.argmin(np.abs(tdf-i))
        ind.append(index)

    ind = np.array(ind)
    
    for c in column:
        temp = np.zeros(tdf.shape)
        temp[:] = np.nan
        temp[ind] = right[c]
        left[c] = temp
        
    return left

def sqi_calculator(data, beats, fs, IN, w, verbose=1):
    """Calculate the Signal Quality Index (SQI)

    Args:
        data (timeseries): 1D timeseries of data (ecg or ppg)
        beats (nbarray): index of beats (qrs spikes or ppg pulses)
        fs (float): sampling rate
        IN (float): threshold for average correlation coefficient (default 0.66 ecg, 0.86 ppg)
        w (float): window size (default: 10s)
        verbose (int, optional): To print. Defaults to 1.

    Returns:
        R2 (float): average correlation coefficient
        SQI (int): 0 if bad and 1 if good
    """

    # find mean RR interval to define size of template
    hrs = np.floor(np.mean(np.diff(beats)))
    q = np.concatenate(([0], beats, [fs/10]))

    ## Apply rules: Rule 1 (40<HR) || Rule 1 (HR<180) || Rule 2 (are there any gaps > 3s?) || Rule 3 (ratio of max to min RR interval should be less than 2.2)
    if len(beats) < (30*w/60):
        if verbose: print("HR<30")
        return -1, -1
    elif len(beats) > (180*w/60):
        if verbose: print("HR>180")
        return -1, -1
    elif np.size(np.where(np.diff(q)>3*fs))>0:
        if verbose: print("Gap>3s")
        return -1, -1
#     elif np.max(np.diff(beats))/np.min(np.diff(beats))>2.2:
#         print("max/min>2.2 :{}".format(np.max(np.diff(beats))/np.min(np.diff(beats))))
#         print(beats)
#         return 0, 0
    else:
        hr = 60*fs/hrs
        ts = []
        j = np.where(beats>hrs/2)[0]
        l = np.where(beats+np.int(hrs/2)<len(data))[0]

        if len(l) == 0:
            print("Less than 1 beats in signal")
            #return 0
        else:
            # Find all QRS windows
            for k in range(j[0], l[-1]+1):
                t = data[beats[k]-np.int(hrs/2):beats[k]+np.int(hrs/2)]
                tt = t/LA.norm(t)
                ts.append(tt)


    # Find all templates in current window
    ts = np.array(ts)
    avtempl=np.mean(ts, axis=0)

    r2 = []

    for k in range(ts.shape[0]):
        r2.append(np.corrcoef(avtempl, ts[k,:])[0,1])

    R2 = np.mean(np.abs(r2))

    if R2<IN:
        SQI=0
        if verbose: print("Corr<Thr")
    else:
        SQI=1
        
    return R2, SQI

def normalize_detrend(x):
    """Normalize and detrend signal

    Args:
        x (nbarray): Signal to normalize and detrend

    Returns:
        x_detrend (nbarray): Normalized and detrended signal 
    """
    x_norm = (x-x.mean())/(x.std())
    
    x_detrend = detrend(x_norm, axis=0)
    
    return x_detrend

def cross_corr_lags(x, y, lags=20):
    """Execute the cross correlation between x and y within a lag interval and return the highest correlation

    Args:
        x (nbarray): Signal x
        y (nbarray): Signal y
        lags (int, optional): Lag limit [-lags, lags]. Defaults to 20.
    Returns:
        cc[pos] (float): The highest cross correlation between x and y within -lags and lags.
    """
    lag = []
    cc = []

    for l in range(lags,0,-1):
        lag.append(-l)
        cc.append(np.corrcoef(x[:-l,0], y[l:,0])[0,1])

    lag.append(0)
    cc.append(np.corrcoef(x[:,0], y[:,0])[0,1])

    for l in range(1,lags+1):
        lag.append(l)
        cc.append(np.corrcoef(x[l:,0], y[:-l,0])[0,1])
    
    pos = np.argmax(cc)
    print(lag[pos], cc[pos])
    
    return cc[pos]