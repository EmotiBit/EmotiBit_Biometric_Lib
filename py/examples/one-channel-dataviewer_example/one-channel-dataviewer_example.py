import emotibit.datasyncer as syncer
import matplotlib.pyplot as plt
import locale
import platform

my_syncer = syncer.DataSyncer()

# Load EmotiBit data
file_dir0 = r"C:\Users\nitin\Documents\EmotiBit\DataAnalysis\controlledTest\2020-01-20_12-00-37-85653-gsr-calibration-01\dataParsed"
file_base = r"2020-01-20_12-00-37-85653"
file_ext = ".csv"
data_types = ["PI"]
file_names0 = []
for data_type in data_types:
    file_names0.append(file_base + "_" + data_type + file_ext)
data_col0 = 7
data_start_row1 = 2
myLocale = locale.getlocale() # Store current locale
if platform.system() == "Darwin":
    location = 'en_US'
elif platform.system() == "Windows":
    location = 'USA'
my_syncer.load_data(file_dir0, file_names0, data_col0)
locale.setlocale(locale.LC_NUMERIC, myLocale)  # Set locale back to orignal
print("Data0.len = " + str(len(my_syncer.time_series[0].data)))
base_val = my_syncer.time_series[0].timestamp[0]
for i in range(len(my_syncer.time_series)):
    my_syncer.time_series[i].timestamp[:] = [stamp - base_val for stamp in my_syncer.time_series[i].timestamp]

# Start of main plotting
# generate the figure with subplots
# axes = plt.figure()
plt.plot(my_syncer.time_series[0].timestamp, my_syncer.time_series[0].data, linestyle='-', zorder=10, alpha=0.9)