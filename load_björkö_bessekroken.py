# To run script both pandas and openpyxl must be installed. If not, install them by running the following commands:
# pip install pandas
# pip install openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# URL to the Excel file on GitHub
url = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/björkö_load/Skarviksvägen 89.xlsx"

# Fetch the file from GitHub
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Read the Excel file into a DataFrame
df = pd.read_excel(BytesIO(response.content))

# Extract values from the fourth column third row-2185th row (index 3)
load_values = df.iloc[7:372, 4:28].values

load_df = pd.DataFrame(np.transpose(load_values))

load=np.transpose(load_values)

yearly_load = load.sum(axis=0)
total = yearly_load.sum()/1000
print("*The total load for full year is", round(total, 1), "MWh")

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

load_winter = load[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
load_spring = load[:, 59:151]
load_summer = load[:, 151:243]
load_autumn = load[:, 243:334]

# Calculate the sum of all values in each row of load_jan
load_jan_sums = load_jan.T.sum(axis=0)/31
#print("Total load in January:", load_jan_sums)
#print(load_jan)
#print(load_jan_sums)

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

load_winter_weekday = []
load_winter_weekend = []
load_spring_weekday = []
load_spring_weekend = []
load_summer_weekday = []
load_summer_weekend = []
load_autumn_weekday = []
load_autumn_weekend = []

for i, value in enumerate(winter_daytype):
    if value == 0:
        load_winter_weekday.append(load_winter[:, i])
    if value == 1:
        load_winter_weekend.append(load_winter[:, i])

for i, value in enumerate(spring_daytype):
    if value == 0:
        load_spring_weekday.append(load_spring[:, i])
    if value == 1:
        load_spring_weekend.append(load_spring[:, i])

for i, value in enumerate(summer_daytype):
    if value == 0:
        load_summer_weekday.append(load_summer[:, i])
    if value == 1:
        load_summer_weekend.append(load_summer[:, i])

for i, value in enumerate(autumn_daytype):
    if value == 0:
        load_autumn_weekday.append(load_autumn[:, i])
    if value == 1:
        load_autumn_weekend.append(load_autumn[:, i])

# load_winter_weekday = np.array(load_winter_weekday).T
# load_winter_weekend = np.array(load_winter_weekend).T
# load_spring_weekday = np.array(load_winter_weekday).T
# load_spring_weekend = np.array(load_winter_weekend).T
# load_summer_weekday = np.array(load_winter_weekday).T
# load_summer_weekend = np.array(load_winter_weekend).T
# load_autumn_weekday = np.array(load_winter_weekday).T
# load_autumn_weekend = np.array(load_winter_weekend).T


#_____________________________________________________________________________________________
# tick_locations = [0, 6, 12, 18, 24]

# #Winter
# plt.figure()
# plt.suptitle('Bessekroken load profile')
# plt.subplot(4, 3, 1)
# plt.plot(sum((load_winter_weekday))/len(load_winter_weekday))
# plt.ylim(0,4)
# plt.title('Mean weekday load')
# plt.ylabel('Winter: \n Load (kWh)')
# plt.xticks(tick_locations)
# plt.grid(True)

# plt.subplot(4, 3, 2)
# plt.plot(sum((load_winter_weekend))/len(load_winter_weekend))
# plt.ylim(0,4)
# plt.title('Mean weekend load')
# plt.xticks(tick_locations)
# plt.grid(True)

# plt.subplot(4, 3, 3)
# plt.plot((sum(load_winter.T))/len(load_winter.T))
# plt.ylim(0,4)
# plt.title('Mean load')
# plt.xticks(tick_locations)
# plt.grid(True)
# plt.show(block=False)

# #Spring
# plt.subplot(4, 3, 4)
# plt.plot(sum((load_spring_weekday))/len(load_spring_weekday))
# plt.ylim(0,4)
# plt.ylabel('Spring: \n Load (kWh)')
# plt.xticks(tick_locations)
# plt.grid(True)

# plt.subplot(4, 3, 5)
# plt.plot(sum((load_spring_weekend))/len(load_spring_weekend))
# plt.ylim(0,4)
# plt.xticks(tick_locations)
# plt.grid(True)

# plt.subplot(4, 3, 6)
# plt.plot((sum(load_spring.T))/len(load_spring.T))
# plt.ylim(0,4)
# plt.xticks(tick_locations)
# plt.grid(True)
# plt.show(block=False)

# #Summer
# plt.subplot(4, 3, 7)
# plt.plot(sum((load_summer_weekday))/len(load_summer_weekday))
# plt.ylim(0,4)
# plt.ylabel('Summer: \n Load (kWh)')
# plt.xticks(tick_locations)
# plt.grid(True)

# plt.subplot(4, 3, 8)
# plt.plot(sum((load_summer_weekend))/len(load_summer_weekend))
# plt.ylim(0,4)
# plt.xticks(tick_locations)
# plt.grid(True)

# plt.subplot(4, 3, 9)
# plt.plot((sum(load_summer.T))/len(load_summer.T))
# plt.ylim(0,4)
# plt.xticks(tick_locations)
# plt.grid(True)
# plt.show(block=False)

# #Autumn
# plt.subplot(4, 3, 10)
# plt.plot(sum((load_autumn_weekday))/len(load_autumn_weekday))
# plt.ylim(0,4)
# plt.xlabel('Time')
# plt.ylabel('Autumn: \n Load (kWh)')
# plt.xticks(tick_locations)
# plt.grid(True)

# plt.subplot(4, 3, 11)
# plt.plot(sum((load_autumn_weekend))/len(load_autumn_weekend))
# plt.xlabel('Time')
# plt.ylim(0,4)
# plt.xticks(tick_locations)
# plt.grid(True)

# plt.subplot(4, 3, 12)
# plt.plot((sum(load_autumn.T))/len(load_autumn.T))
# plt.ylim(0,4)
# plt.xlabel('Time')
# plt.xticks(tick_locations)
# plt.grid(True)
# plt.show(block=False)

#________________other plots_______________________________________________________________

# plt.figure()
# plt.subplot(1, 3, 1)
# plt.plot(sum(np.transpose(load_jan))/len(load_jan))
# plt.ylim(0,10)
# plt.title('Total Load in January')
# plt.xlabel('Hour in the Day')
# plt.ylabel('Load (kWh)')
# plt.grid(True)

# plt.subplot(1, 3, 2)
# plt.plot(sum(np.transpose(load_jan_weekday))/len(load_jan_weekday))
# plt.ylim(0,10)
# plt.title('Weekday Load')
# plt.xlabel('Hour in the Day')
# plt.ylabel('Load (kWh)')
# plt.grid(True)

# plt.subplot(1, 3, 3)
# plt.plot(sum(np.transpose(load_jan_weekend))/len(load_jan_weekend))
# plt.ylim(0,10)
# plt.title('Weekend Load')
# plt.xlabel('Hour in the Day')
# plt.ylabel('Load (kWh)')
# plt.grid(True)
# plt.show(block=False)

# # Boxplot for the loads in July
# plt.figure()
# plt.subplot(1, 3, 1)
# plt.plot(sum(np.transpose(load_jul))/len(load_jul))
# plt.ylim(0,8)
# plt.title('Total Load in July')
# plt.ylabel('Load (kWh)')
# plt.xticks(tick_locations)
# plt.grid(True)

# plt.subplot(1, 3, 2)
# plt.plot(sum(np.transpose(load_jul_weekday))/len(load_jul_weekday))
# plt.ylim(0,10)
# plt.title('Weekday Load')
# plt.xlabel('Hour in the Day')
# plt.xticks(tick_locations)
# plt.grid(True)

# plt.subplot(1, 3, 3)
# plt.plot(sum(np.transpose(load_jul_weekend))/len(load_jul_weekend))
# plt.ylim(0,10)
# plt.title('Weekend Load')
# plt.xlabel('Hour in the Day')
# plt.xticks(tick_locations)
# plt.grid(True)
# plt.show(block=False)

# plt.figure(figsize=(10, 5))
# plt.plot(range(1, 366), yearly_load, label='Daily Electricity Load')
# plt.xlabel('Day of the Year')
# plt.ylabel('Daily Load (kWh)')
# plt.title('Daily Electricity Load in 2024')
# plt.legend()
# plt.grid(True)
# plt.show(block=False)

# # Keep the plots open
plt.show()
