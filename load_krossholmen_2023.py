# To run script both pandas and openpyxl must be installed. If not, install them by running the following commands:
# pip install pandas
# pip install openpyxl
# pip install requests
# pip install matplotlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# URL to the Excel file on GitHub
url = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/krossholmen_load/Consumption_2023.xlsx"

# Fetch the file from GitHub
response = requests.get(url, verify=False)
response.raise_for_status()  # Check if the request was successful

# Read the Excel file into a DataFrame
df = pd.read_excel(BytesIO(response.content))

# Extract values from the fourth column third row-2185th row (index 3)
load_values = df.iloc[6:8767, 2].values

# Create a matrix (reshape if needed, here assuming a 1D array)
load_matrix = np.array(load_values, dtype=float)

# Initialize an empty 2D array with appropriate dimensions
rows = 24
cols = -(-len(load_matrix) // rows)  # Calculate number of columns needed, rounding up
load = np.zeros((rows, cols))

# Fill the matrix "load" with values
for i, value in enumerate(load_matrix):
    row = i % rows
    col = i // rows
    load[row, col] = value

# Print the size of the load matrix
print("Size of the load matrix:", load.shape)

load_df = pd.DataFrame(load)

#Sums up the load for each hour in a day into one value, creating an array with the load for each day (1 row, 365 columns)
yearly_load = load.sum(axis=0)
total = yearly_load.sum()
print("*The total load for full year is", round(total/1000, 1), "MWh")

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

#Arranges the corresponding loads for each day into the right season
#Winter: December, January, February
#Spring: March, April, May
#Summer: June, July, August
#Autumn: September, October, November
load_winter = load[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
load_spring = load[:, 59:151]
load_summer = load[:, 151:243]
load_autumn = load[:, 243:334]


#Arrays for daytype for each month, 0 = weekday, 1 = weekend
jan_daytype = np.array([1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0])
feb_daytype = np.array([0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0])
mar_daytype = np.array([0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0])
apr_daytype = np.array([1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1])
may_daytype = np.array([1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0])
jun_daytype = np.array([0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0])
jul_daytype = np.array([1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0])
aug_daytype = np.array([0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0])
sep_daytype = np.array([0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1])
oct_daytype = np.array([1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0])
nov_daytype = np.array([0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0])
dec_daytype = np.array([0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1])

winter_daytype = np.concatenate((dec_daytype, jan_daytype, feb_daytype))
spring_daytype = np.concatenate((mar_daytype, apr_daytype, may_daytype))
summer_daytype = np.concatenate((jun_daytype, jul_daytype, aug_daytype))
autumn_daytype = np.concatenate((sep_daytype, oct_daytype, nov_daytype))

#Empty matrixes for the next step
load_winter_weekday = []
load_winter_weekend = []
load_spring_weekday = []
load_spring_weekend = []
load_summer_weekday = []
load_summer_weekend = []
load_autumn_weekday = []
load_autumn_weekend = []

#for-loops positioning the load values for either weekday or weekend in different matrixes
#each row represents the load for one hour in the day
for i, value in enumerate(winter_daytype):
    if value == 0:
        load_winter_weekday.append(load_winter[:, i])
    if value == 1:
        load_winter_weekend.append(load_winter[:, i])
load_winter = load_winter.T

for i, value in enumerate(spring_daytype):
    if value == 0:
        load_spring_weekday.append(load_spring[:, i])
    if value == 1:
        load_spring_weekend.append(load_spring[:, i])
load_spring = load_spring.T

for i, value in enumerate(summer_daytype):
    if value == 0:
        load_summer_weekday.append(load_summer[:, i])
    if value == 1:
        load_summer_weekend.append(load_summer[:, i])
load_summer = load_summer.T

for i, value in enumerate(autumn_daytype):
    if value == 0:
        load_autumn_weekday.append(load_autumn[:, i])
    if value == 1:
        load_autumn_weekend.append(load_autumn[:, i])
load_autumn = load_autumn.T

#_____________________________________________________________________________________________
#PLOT
#position for the time on the x-axis
tick_locations = [0, 6, 12, 18, 24]

#Winter
plt.figure()
plt.suptitle('Krossholmen load profile')
plt.subplot(4, 3, 1)
plt.plot(sum((load_winter_weekday))/len(load_winter_weekday))
plt.ylim(0,200)
plt.title('Mean weekday load')
plt.ylabel('Winter: \n Load (kWh)')
plt.xticks(tick_locations)
plt.grid(True)

plt.subplot(4, 3, 2)
plt.plot(sum((load_winter_weekend))/len(load_winter_weekend))
plt.ylim(0,200)
plt.title('Mean weekend load')
plt.xticks(tick_locations)
plt.grid(True)

plt.subplot(4, 3, 3)
plt.plot((sum(load_winter))/len(load_winter))
plt.ylim(0,200)
plt.title('Mean load')
plt.xticks(tick_locations)
plt.grid(True)

#Spring
plt.subplot(4, 3, 4)
plt.plot(sum((load_spring_weekday))/len(load_spring_weekday))
plt.ylim(0,200)
plt.ylabel('Spring: \n Load (kWh)')
plt.xticks(tick_locations)
plt.grid(True)

plt.subplot(4, 3, 5)
plt.plot(sum((load_spring_weekend))/len(load_spring_weekend))
plt.ylim(0,200)
plt.xticks(tick_locations)
plt.grid(True)

plt.subplot(4, 3, 6)
plt.plot((sum(load_spring))/len(load_spring))
plt.ylim(0,200)
plt.xticks(tick_locations)
plt.grid(True)

#Summer
plt.subplot(4, 3, 7)
plt.plot(sum((load_summer_weekday))/len(load_summer_weekday))
plt.ylim(0,200)
plt.ylabel('Summer: \n Load (kWh)')
plt.xticks(tick_locations)
plt.grid(True)

plt.subplot(4, 3, 8)
plt.plot(sum((load_summer_weekend))/len(load_summer_weekend))
plt.ylim(0,200)
plt.xticks(tick_locations)
plt.grid(True)

plt.subplot(4, 3, 9)
plt.plot((sum(load_summer))/len(load_summer))
plt.ylim(0,200)
plt.xticks(tick_locations)
plt.grid(True)

#Autumn
plt.subplot(4, 3, 10)
plt.plot(sum((load_autumn_weekday))/len(load_autumn_weekday))
plt.ylim(0,200)
plt.xlabel('Time')
plt.ylabel('Autumn: \n Load (kWh)')
plt.xticks(tick_locations)
plt.grid(True)

plt.subplot(4, 3, 11)
plt.plot(sum((load_autumn_weekend))/len(load_autumn_weekend))
plt.xlabel('Time')
plt.ylim(0,200)
plt.xticks(tick_locations)
plt.grid(True)

plt.subplot(4, 3, 12)
plt.plot((sum(load_autumn))/len(load_autumn))
plt.ylim(0,200)
plt.xlabel('Time')
plt.xticks(tick_locations)
plt.grid(True)
plt.show(block=False)

plt.show()

