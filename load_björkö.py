# To run script both pandas and openpyxl must be installed. If not, install them by running the following commands:
# pip install pandas
# pip install openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path_to_file1 = "/Users/a518244/Python/energy-optimization/björkö_load/Skarviksvägen 8.xlsx"
path_to_file2 = "/Users/a518244/Python/energy-optimization/björkö_load/Skarviksvägen 11_0627.xlsx"
path_to_file3 = "/Users/a518244/Python/energy-optimization/björkö_load/Skarviksvägen 11_7218.xlsx"
path_to_file4 = "/Users/a518244/Python/energy-optimization/björkö_load/Strandsjövägen 7.xlsx"
path_to_file5 = "/Users/a518244/Python/energy-optimization/björkö_load/Strandsjövägen 19.xlsx"
path_to_file6 = "/Users/a518244/Python/energy-optimization/björkö_load/Strandsjövägen 26.xlsx"

df1 = pd.read_excel(path_to_file1)
df2 = pd.read_excel(path_to_file2)
df3 = pd.read_excel(path_to_file3)
df4 = pd.read_excel(path_to_file4)
df5 = pd.read_excel(path_to_file5)
df6 = pd.read_excel(path_to_file6)

# Extract values from the fourth column third row-2185th row (index 3)

load_values1 = df1.iloc[7:373, 4:28].values
load_values2 = df2.iloc[7:373, 4:28].values
load_values3 = df3.iloc[7:373, 4:28].values
load_values4 = df4.iloc[7:373, 4:28].values
load_values5 = df5.iloc[7:373, 4:28].values
load_values6 = df6.iloc[7:373, 4:28].values

load_values= load_values1 + load_values2 + load_values3 + load_values4 + load_values5 + load_values6

#load_df = pd.DataFrame(np.transpose(load_values))

load=np.transpose(load_values)

yearly_load = load.sum(axis=0)
total = yearly_load.sum()/1000
print("The total load for full year is", round(total, 1), "MWh")

# Correct slicing syntax
load_jan = load[:, 0:31]
load_feb = load[:, 31:59]
load_mar = load[:, 59:90]
load_apr = load[:, 90:120]
load_may = load[:, 120:151]
load_jun = load[:, 151:181]
load_jul = load[:, 181:212]
load_aug = load[:, 212:243]
load_sep = load[:, 243:273]
load_oct = load[:, 273:304]
load_nov = load[:, 304:334]
load_dec = load[:, 334:365]

# Calculate the sum of all values in each row of load_jan
load_jan_sums = load_jan.sum(axis=0) / 24
#print("Total load in January:", load_jan_sums)

jan_daytype = np.array([1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0])
jul_daytype = np.array([1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0])

load_jan_weekday = []
load_jan_weekend = []

for i, value in enumerate(jan_daytype):
    if value == 0:
        load_jan_weekday.append(load_jan[:, i])
    if value == 1:
        load_jan_weekend.append(load_jan[:, i])

load_jan_weekday = np.array(load_jan_weekday).T
load_jan_weekend = np.array(load_jan_weekend).T

#print("Weekday loads:", load_jan_weekday)
#print("Weekend loads:", load_jan_weekend)

#_____________________________________________________________________________________________

#July
#Calculate the sum of all values of each row
load_jul_weekday = []
load_jul_weekend = []

for i, value in enumerate(jul_daytype):
    if value == 0:
        load_jul_weekday.append(load_jul[:, i])
    if value == 1:
        load_jul_weekend.append(load_jul[:, i])

load_jul_weekday = np.array(load_jul_weekday).T
load_jul_weekend = np.array(load_jul_weekend).T

#________________________________________________________________________________________________
# Boxplot for the loads in January
plt.figure()
plt.subplot(1, 3, 1)
plt.boxplot(np.transpose(load_jan))
plt.ylim(0,60)
plt.title('Total Load in January')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)

plt.subplot(1, 3, 2)
plt.boxplot(np.transpose(load_jan_weekday))
plt.ylim(0,60)
plt.title('Weekday Load')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)

plt.subplot(1, 3, 3)
plt.boxplot(np.transpose(load_jan_weekend))
plt.ylim(0,60)
plt.title('Weekend Load')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)
plt.show(block=False)

# Boxplot for the loads in July
plt.figure()
plt.subplot(1, 3, 1)
plt.boxplot(np.transpose(load_jul))
plt.ylim(0,60)
plt.title('Total Load in July')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)

plt.subplot(1, 3, 2)
plt.boxplot(np.transpose(load_jul_weekday))
plt.ylim(0,60)
plt.title('Weekday Load')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)

plt.subplot(1, 3, 3)
plt.boxplot(np.transpose(load_jul_weekend))
plt.ylim(0,60)
plt.title('Weekend Load')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)
plt.show(block=False)

plt.figure(figsize=(10, 5))
plt.plot(range(1, 366), yearly_load, label='Daily Electricity Load')
plt.xlabel('Day of the Year')
plt.ylabel('Daily Load (kWh)')
plt.title('Daily Electricity Load in 2024')
plt.legend()
plt.grid(True)
plt.show(block=False)

# Keep the plots open
plt.show()
