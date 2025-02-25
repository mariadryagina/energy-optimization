# To run script both pandas and openpyxl must be installed. If not, install them by running the following commands:
# pip install pandas
# pip install openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path_to_file = "/Users/a518244/Python/energy-optimization/Consumption_2023.xlsx"

df = pd.read_excel(path_to_file)
#except FileNotFoundError:
#    print(f"File not found: {path_to_file}")
#    exit()
#except Exception as e:
#    print(f"Error reading the Excel file: {e}")
#    exit()

# Check the shape of the DataFrame
#print("DataFrame shape:", df.shape)

# Ensure the DataFrame has at least 8791 rows and 5 columns
#if df.shape[0] < 8791 or df.shape[1] < 5:
#    print("DataFrame does not have the expected number of rows or columns.")
#    exit()

# Extract values from the fourth column third row-2185th row (index 3)
load_values = df.iloc[6:8767, 2].values
#load_values = df.iloc[6:1790;4440:8767, 2].values
#except Exception as e:
#    print(f"Error extracting data: {e}")
#    exit()

# Create a matrix (reshape if needed, here assuming a 1D array)
load_matrix = np.array(load_values, dtype=float)
#except Exception as e:
#    print(f"Error creating matrix: {e}")
#    exit()

# Initialize an empty 2D array with appropriate dimensions
rows = 24
cols = -(-len(load_matrix) // rows)  # Calculate number of columns needed, rounding up
load = np.zeros((rows, cols))

# Fill the matrix "load" with values
for i, value in enumerate(load_matrix):
    row = i % rows
    col = i // rows
    load[row, col] = value

load_df = pd.DataFrame(load)

#16 mars (75) till 3 juli (185)
load[:,75:185]=0

yearly_load = load.sum(axis=0)
total = yearly_load.sum()
print("*The total load for full year is", total, "MWh")

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
print("Total load in January:", load_jan_sums)

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

print("Weekday loads:", load_jan_weekday)
print("Weekend loads:", load_jan_weekend)

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

print("Weekday loads:", load_jul_weekday)
print("Weekend loads:", load_jul_weekend)

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
plt.plot(range(1, 366), yearly_load, label='Daily Electricity Load')
plt.xlabel('Day of the Year')
plt.ylabel('Daily Load (kWh)')
plt.title('Daily Electricity Load in 2024')
plt.legend()
plt.grid(True)
plt.show(block=False)

# Keep the plots open
plt.show()
