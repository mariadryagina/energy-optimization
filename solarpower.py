#region
from numpy import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt 
import windpower
import el_price
from Frequency import frequency_price

# spot_price_2023=el_price.spotprice_2023
# spot_price_2024_winter=el_price.spotprice_2024_winter
# spot_price_2024_summer=el_price.spotprice_2024_summer

# price_winter_FCR_N=frequency_price.price_winter_mean_FCR_N
# pric_summer_FCR_N=frequency_price.price_summer_mean_FCR_N

# price_winter_FCR_D_up=frequency_price.price_winter_mean_FCR_D_up_2023
# price_summer_FCR_D_up=frequency_price.price_summer_mean_FCR_D_up_2023

# price_winter_FCR_D_down=frequency_price.price_winter_mean_FCR_D_down_2023
# price_summer_FCR_D_down=frequency_price.price_summer_mean_FCR_D_down_2023

import requests
from io import BytesIO
#endregion
# region URL to the Excel file on GitHub
url = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Self-produced_electricity/solardata_2023.xlsx"

# Fetch the file from GitHub
response = requests.get(url, verify=False)
response.raise_for_status()  # Check if the request was successful

# Read the Excel file into a DataFrame
df = pd.read_excel(BytesIO(response.content))

if df.shape[0]==8760:
      a=365
else:
      a=366

#Creting a matrix with zeros
I=zeros((24,a))

#Storing values from excel in I
for i in range(a):
    for j in range(24):
         I[j,i]=df.iloc[i*24+j,2]
#endregion
#Function begins___________________________________________________________________________#
# I - irradiation in W/m^2
#A - amount of panels in m^2
#eta - efficency of PV farm
def solar(A, eta):
    P_s = (I * A * eta) / 1000
    
    return P_s
#__________________________________________________________________________________________#
# region Calling on function
# P_s2=solar(167,0.20)
# P_wind2=windpower.wind(1) #1 turbine rated 5,5kW


# solarpower_2023_winter = P_s2[:, concatenate((arange(334, 365), arange(0, 59)))]
# solarpower_2023_spring = P_s2[:, 59:151]
# solarpower_2023_summer = P_s2[:, 151:243]
# solarpower_2023_autumn = P_s2[:, 243:334]

# windpower_2023_winter = P_wind2[:, concatenate((arange(334, 365), arange(0, 59)))]
# windpower_2023_spring = P_wind2[:, 59:151]
# windpower_2023_summer = P_wind2[:, 151:243]
# windpower_2023_autumn = P_wind2[:, 243:334]

# #Calculating the sum of the array for the mean solar power during a winter day
# solarpower_2023_winter_1=zeros(24)
# for i in range(24):
#     solarpower_2023_winter_1[i] = sum(solarpower_2023_winter[i])/len(solarpower_2023_winter[i])

# #Calculating the sum of the array for the mean solar power during a summer day
# solarpower_2023_summer_1=zeros(24)
# for i in range(24):
#     solarpower_2023_summer_1[i] = sum(solarpower_2023_summer[i])/len(solarpower_2023_summer[i])

# #Calculating the sum of the array for the mean wind power during a winter day
# windpower_2023_winter_1=zeros(24)
# for i in range(24):
#     windpower_2023_winter_1[i] = sum(windpower_2023_winter[i])/len(windpower_2023_winter[i])

# #Calculating the sum of the array for the mean wind power during a summer day
# windpower_2023_summer_1=zeros(24)
# for i in range(24):
#     windpower_2023_summer_1[i] = sum(windpower_2023_summer[i])/len(windpower_2023_summer[i])

# #Calculating the sum of the array for the yearly spot price in SE3 1X24
# spot_price_2023_winter_1=zeros(24)
# for i in range(24):
#     spot_price_2023_winter_1[i] = sum(spot_price_2024_winter[i])/len(spot_price_2024_winter[i])

# #Calculating the sum of the array for the yearly spot price in SE3 1X24
# spot_price_2023_summer_1=zeros(24)
# for i in range(24):
#     spot_price_2023_summer_1[i] = sum(spot_price_2024_summer[i])/len(spot_price_2024_summer[i])
#endregion
#_______________Plotting________________________________________________________________________________
# # region Create subplots for mean winter and summer daily load in Krossholmen with two y-axes
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
# #fig.suptitle('Mean Solar and Wind Power Production in Krossholmen and Prices in Different Markets')

# # Plot mean winter daily load in Krossholmen
# ax1.plot(range(24), solarpower_2023_winter_1, label='Solar Power', color='tab:blue')
# ax1.plot(range(24), windpower_2023_winter_1, label='Wind Power', color='tab:green')
# ax1.set_title('Winter')
# ax1.set_ylabel('kWh', color='tab:blue')
# ax1.set_xlabel('Time (h)')
# ax1.set_xlim(0, 23)
# ax1.set_ylim(0, (max(solarpower_2023_summer_1))+2)
# ax1.tick_params(axis='y', labelcolor='tab:blue')

# # Create a second y-axis for the spot price in winter
# ax1_2 = ax1.twinx()
# ax1_2.plot(range(24), spot_price_2023_winter_1, label='Spot Price', color='tab:orange')
# #ax1_2.plot(range(24), price_winter_FCR_N/1000, label='FCR-N', color='tab:purple')
# #ax1_2.plot(range(24), price_winter_FCR_D_up/1000, label='FCR-D up', color='tab:brown')
# #ax1_2.plot(range(24), price_winter_FCR_D_down/1000, label='FCR-D down', color='tab:red')
# ax1_2.set_ylabel('Spot Price (SEK/kWh)', color='tab:orange')
# #ax1_2.set_ylim(0, (max(spot_price_2023_winter_1)+0.05))
# ax1_2.tick_params(axis='y', labelcolor='tab:orange')


# # Plot mean summer daily load in Krossholmen
# ax2.plot(range(24), solarpower_2023_summer_1, label='Solar Power', color='tab:blue')
# ax2.plot(range(24), windpower_2023_summer_1, label='Wind Power', color='tab:green')
# ax2.set_title('Summer')
# ax2.set_ylabel('kWh', color='tab:blue')
# ax2.set_xlabel('Time (h)')
# ax2.set_xlim(0, 23)
# ax2.set_ylim(0, (max(solarpower_2023_summer_1)+2))
# ax2.tick_params(axis='y', labelcolor='tab:blue')

# # Combine legends from both y-axes
# lines1, labels1 = ax1.get_legend_handles_labels()
# lines2, labels2 = ax1_2.get_legend_handles_labels()
# ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

# # Create a second y-axis for the spot price in summer
# ax2_2 = ax2.twinx()
# ax2_2.plot(range(24), spot_price_2023_summer_1, label='Spot Price', color='tab:orange')
# #ax2_2.plot(range(24), pric_summer_FCR_N/1000, label='FCR-N', color='tab:purple')
# #ax2_2.plot(range(24), price_summer_FCR_D_up/1000, label='FCR-D up', color='tab:brown')
# #ax2_2.plot(range(24), price_summer_FCR_D_down/1000, label='FCR-D down', color='tab:red')
# ax2_2.set_ylabel('Spot Price (SEK/kWh)', color='tab:orange')
# ax2_2.set_ylim(0, 1.0)
# ax2_2.tick_params(axis='y', labelcolor='tab:orange')

# # Adjust layout
# fig.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to make room for the main title
# plt.show()

#endregion
#______________________________________________________________________________#
# region #Validation
# P_s3=36170 #kWh, the value calculated by the website from Jennifer. EU. 
# P_s4=sum(P_s2)*1000 #kWh

# error=round((abs(P_s3-P_s4)/P_s3)*100*1000)/1000
# print(f"Compared to the value calculated by the PV company the error is {error}")

#_______________________________________________________________________________#
# Creating a plot
# plt.figure(figsize=(10, 5))
# plt.plot(range(0, a), P_s2*1000, label='Yearly Solar Power Production')
# plt.xlabel('Days of the Year')
# plt.ylabel('Solar Power Production (kWh)')
# plt.title('Yearly Solar Power Production')
# #plt.legend()
# plt.grid(True)
# plt.show()

#endregion ____________________________________________________________________________#

