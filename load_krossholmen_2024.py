# To run script both pandas and openpyxl must be installed. If not, install them by running the following commands:
# pip install pandas
# pip install openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path_to_file = "/Users/a518244/Python/energy-optimization/krossholmen_load/Consumption_2024.xlsx"

df = pd.read_excel(path_to_file)

# Extract values from the fourth column third row-2185th row (index 3)
load_values = df.iloc[6:8791, 4].values

load_matrix = np.array(load_values, dtype=float)

# Initialize an empty 2D array with appropriate dimensions
rows = 24
cols = -(-len(load_matrix) // rows)  # Calculate number of columns needed, rounding up
load = np.zeros((rows, cols))

# Fill the matrix "load" with values
for i, value in enumerate(load_matrix):
    row = i % rows
    col = i // rows
    load[row, col] = value*1000

load_df = pd.DataFrame(load)
#print(load_df)

yearly_load = load.sum(axis=0)
total = yearly_load.sum()/1000
print("*The total load for full year is", total, "MWh")

# Correct slicing syntax
load_jan = load[:, 0:31]
load_feb = load[:, 31:60]
load_mar = load[:, 60:91]
load_apr = load[:, 91:121]
load_may = load[:, 121:152]
load_jun = load[:, 152:182]
load_jul = load[:, 182:213]
load_aug = load[:, 213:244]
load_sep = load[:, 244:274]
load_oct = load[:, 274:305]
load_nov = load[:, 305:335]
load_dec = load[:, 335:366]

# Calculate the sum of all values in each row of load_jan
load_jan_sums = load_jan.sum(axis=0) / 24
#print("Total load in January:", load_jan_sums)

jan_daytype = np.array([0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0])

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

for i, value in enumerate(jan_daytype):
    if value == 0:
        load_jul_weekday.append(load_jul[:, i])
    if value == 1:
        load_jul_weekend.append(load_jul[:, i])

load_jul_weekday = np.array(load_jul_weekday).T
load_jul_weekend = np.array(load_jul_weekend).T

#print("Weekday loads:", load_jul_weekday)
#print("Weekend loads:", load_jul_weekend)

# Boxplot for the loads in January
plt.figure()
plt.subplot(1, 3, 1)
plt.boxplot(np.transpose(load_jan))
plt.ylim(0,240)
plt.title('Total Load in January')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)

plt.subplot(1, 3, 2)
plt.boxplot(np.transpose(load_jan_weekday))
plt.ylim(0,240)
plt.title('Weekday Load')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)

plt.subplot(1, 3, 3)
plt.boxplot(np.transpose(load_jan_weekend))
plt.ylim(0,240)
plt.title('Weekend Load')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)
plt.show(block=False)

# Boxplot for the loads in July
plt.figure()
plt.subplot(1, 3, 1)
plt.boxplot(np.transpose(load_jul))
plt.ylim(0,240)
plt.title('Total Load in July')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)

plt.subplot(1, 3, 2)
plt.boxplot(np.transpose(load_jul_weekday))
plt.ylim(0,240)
plt.title('Weekday Load')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)

plt.subplot(1, 3, 3)
plt.boxplot(np.transpose(load_jul_weekend))
plt.ylim(0,240)
plt.title('Weekend Load')
plt.xlabel('Hour in the Day')
plt.ylabel('Load (kWh)')
plt.grid(True)
plt.show(block=False)

plt.figure(figsize=(10, 5))
plt.plot(range(1, 367), yearly_load, label='Daily Electricity Load')
plt.xlabel('Day of the Year')
plt.ylabel('Daily Load (kWh)')
plt.title('Daily Electricity Load in 2024')
plt.legend()
plt.grid(True)
plt.show(block=False)

# Keep the plots open
plt.show()
