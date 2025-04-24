import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# URL to the Excel file on GitHub
url = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Frequency/FCR_pris_2023.xlsx"
url_1 = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Frequency/frequency_price_activated.xlsx"
url_2022 = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Frequency/FCR_pris_2022.xlsx"
url_2021 = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Frequency/FCR_pris_2021.xlsx"
url_2024 = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Frequency/FCR_pris_2024.xlsx"


# Fetch the file from GitHub
response = requests.get(url, verify=False)
response.raise_for_status()  # Check if the request was successful
response_1 = requests.get(url_1, verify=False)
response_1.raise_for_status()  # Check if the request was successful
response_2022 = requests.get(url_2022, verify=False)
response_2022.raise_for_status()  # Check if the request was successful
response_2021 = requests.get(url_2021, verify=False)
response_2021.raise_for_status()  # Check if the request was successful
response_2024 = requests.get(url_2024, verify=False)
response_2024.raise_for_status()  # Check if the request was successful

# Read the Excel file into a DataFrame
df = pd.read_excel(BytesIO(response.content))
df_1 = pd.read_excel(BytesIO(response_1.content))
df_2022 = pd.read_excel(BytesIO(response_2022.content))
df_2021 = pd.read_excel(BytesIO(response_2021.content))
df_2024 = pd.read_excel(BytesIO(response_2024.content))
#________________Storing the values in a matrix_______________________________________________________________________
#region 11,03 SEK to 1 EUR
#Storing FCR-N prices in a matrix SEK/MWh
#region
FCR_N=np.zeros((24,365))
FCR_N_1=np.zeros((8760,1))
FCR_N_upp=np.zeros((8760,1)) 
FCR_N_ned=np.zeros((8760,1))

for i in range(365):
    for j in range(24):
         FCR_N[j,i]=(df.iloc[i*24+j,1])*11.03

for i in range(8760):
    FCR_N_1[i]=(df.iloc[i,1])*11.03

for i in range(8760):
    FCR_N_upp[i]=(df_1.iloc[i,2])*11.03

for i in range(8760):
    FCR_N_ned[i]=(df_1.iloc[i,4])*11.03

#endregion
#Storing FCR-D up prices in a matrix SEK/MWh
FCR_D_up_2023=np.zeros((24,365))
FCR_D_up_2021=np.zeros((24,365))
FCR_D_up_2022=np.zeros((24,365))
FCR_D_up_2024=np.zeros((24,366))
FCR_D_up_1=np.zeros((8760,1))

for i in range(365):
    for j in range(24):
         FCR_D_up_2023[j,i]=(df.iloc[i*24+j,8])*11.03

for i in range(365):
    for j in range(24):
         FCR_D_up_2022[j,i]=(df_2022.iloc[i*24+j,8])*11.03

FCR_D_up_2022_8760 = FCR_D_up_2022.reshape(-1, order='F')

for i in range(365):
    for j in range(24):
         FCR_D_up_2021[j,i]=(df_2021.iloc[i*24+j,8])*11.03

FCR_D_up_2021_8760 = FCR_D_up_2021.reshape(-1, order='F')


for i in range(366):
    for j in range(24):
         FCR_D_up_2024[j,i]=(df_2024.iloc[i*24+j,8])*11.03

FCR_D_up_2024 = np.delete(FCR_D_up_2024, 59, axis=1)  # Remove the 60th column (day)


FCR_D_up_2024_8760 = FCR_D_up_2024.reshape(-1, order='F')

for i in range(8760):
    FCR_D_up_1[i]=(df.iloc[i,8])


#Storing FCR-D down prices in a matrix SEK/MWh
FCR_D_down_2023=np.zeros((24,365))
FCR_D_down_2021=np.zeros((24,365))
FCR_D_down_2022=np.zeros((24,365))
FCR_D_down_2024=np.zeros((24,366))
FCR_D_down_1=np.zeros((8760,1))

for i in range(365):
    for j in range(24):
         FCR_D_down_2023[j,i]=(df.iloc[i*24+j,15])*11.03

for i in range(365):
    for j in range(24):
         FCR_D_down_2022[j,i]=(df_2022.iloc[i*24+j,15])*11.03

FCR_D_down_2022_8760 = FCR_D_down_2022.reshape(-1, order='F')

for i in range(365):
    for j in range(24):
         FCR_D_down_2021[j,i]=(df_2021.iloc[i*24+j,15])*11.03


FCR_D_down_2021_8760 = FCR_D_down_2021.reshape(-1, order='F')

for i in range(366):
    for j in range(24):
         FCR_D_down_2024[j,i]=(df_2024.iloc[i*24+j,15])*11.03

FCR_D_down_2024 = np.delete(FCR_D_down_2024, 59, axis=1)  # Remove the 60th column (day)



FCR_D_down_2024_8760 = FCR_D_down_2024.reshape(-1, order='F')

#2023
for i in range(8760):
    FCR_D_down_1[i]=(df.iloc[i,15])*11.03

#endregion
#_______FCR-N_______________________________________________________________________________
#region Arranges the corresponding loads for each day into the right seasongg
#Winter: December, January, February
#Spring: March, April, May
#Summer: June, July, August
#Autumn: September, October, November
# price_winter_FCR_N = FCR_N[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
# price_spring_FCR_N = FCR_N[:, 59:151]
# price_summer_FCR_N = FCR_N[:, 151:243]
# price_autumn_FCR_N = FCR_N[:, 243:334]

# price_winter_mean_FCR_N=np.zeros((24))
# for i in range(24):
#     price_winter_mean_FCR_N[i]=sum(price_winter_FCR_N[i])/len(price_winter_FCR_N[i])

# price_spring_mean_FCR_N=np.zeros((24))
# for i in range(24):
#     price_spring_mean_FCR_N[i]=sum(price_spring_FCR_N[i])/len(price_spring_FCR_N[i])

# price_summer_mean_FCR_N=np.zeros((24))
# for i in range(24):
#     price_summer_mean_FCR_N[i]=sum(price_summer_FCR_N[i])/len(price_summer_FCR_N[i])

# price_autumn_mean_FCR_N=np.zeros((24))
# for i in range(24):
#     price_autumn_mean_FCR_N[i]=sum(price_autumn_FCR_N[i])/len(price_autumn_FCR_N[i])


# # Create subplots
# fig, axs = plt.subplots(2, 2, figsize=(10, 5))
# fig.suptitle('Mean FCR-N Prices During Different Seasons')

# # Plot mean FCR-N price during winter
# axs[0, 0].plot(price_winter_mean_FCR_N/1000)
# axs[0, 0].set_title('Winter')
# axs[0, 0].set_ylabel('SEK/kWh')
# axs[0, 0].set_xlabel('Hour of the day')
# axs[0, 0].set_xlim(0, 23)
# axs[0, 0].grid(True)

# # Plot mean FCR-N price during spring
# axs[0, 1].plot(price_spring_mean_FCR_N/1000)
# axs[0, 1].set_title('Spring')
# axs[0, 1].set_ylabel('SEK/kWh')
# axs[0, 1].set_xlabel('Hour of the day')
# axs[0, 1].grid(True)

# # Plot mean FCR-N price during summer
# axs[1, 0].plot(price_summer_mean_FCR_N/1000)
# axs[1, 0].set_title('Summer')
# axs[1, 0].set_ylabel('SEK/kWh')
# axs[1, 0].set_xlabel('Hour of the day')
# axs[1, 0].set_xlim(0, 23)
# axs[1, 0].grid(True)

# # Plot mean FCR-N price during autumn
# axs[1, 1].plot(price_autumn_mean_FCR_N/1000)
# axs[1, 1].set_title('Autumn')
# axs[1, 1].set_ylabel('SEK/kWh')
# axs[1, 1].set_xlabel('Hour of the day')
# axs[1, 1].grid(True)

# # Adjust layout
# plt.tight_layout()
# plt.show()

#endregion

#_______FCR-D-up_______________________________________________________________________________
#region Arranges the corresponding loads for each day into the right season
#Winter: December, January, February
#Spring: March, April, May
#Summer: June, July, August
#Autumn: September, October, November

# #2023
# price_winter_FCR_D_up_2023 = FCR_D_up_2023[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
# price_spring_FCR_D_up_2023 = FCR_D_up_2023[:, 59:151]
# price_summer_FCR_D_up_2023 = FCR_D_up_2023[:, 151:243]
# price_autumn_FCR_D_up_2023 = FCR_D_up_2023[:, 243:334]

# price_winter_mean_FCR_D_up_2023=np.zeros((24))
# for i in range(24):
#     price_winter_mean_FCR_D_up_2023[i]=sum(price_winter_FCR_D_up_2023[i])/len(price_winter_FCR_D_up_2023[i])

# price_spring_mean_FCR_D_up_2023=np.zeros((24))
# for i in range(24):
#     price_spring_mean_FCR_D_up_2023[i]=sum(price_spring_FCR_D_up_2023[i])/len(price_spring_FCR_D_up_2023[i])

# price_summer_mean_FCR_D_up_2023=np.zeros((24))
# for i in range(24):
#     price_summer_mean_FCR_D_up_2023[i]=sum(price_summer_FCR_D_up_2023[i])/len(price_summer_FCR_D_up_2023[i])

# price_autumn_mean_FCR_D_up_2023=np.zeros((24))
# for i in range(24):
#     price_autumn_mean_FCR_D_up_2023[i]=sum(price_autumn_FCR_D_up_2023[i])/len(price_autumn_FCR_D_up_2023[i])

# #2021
# price_winter_FCR_D_up_2021 = FCR_D_up_2021[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
# price_summer_FCR_D_up_2021 = FCR_D_up_2021[:, 151:243]

# price_winter_mean_FCR_D_up_2021=np.zeros((24))
# for i in range(24):
#     price_winter_mean_FCR_D_up_2021[i]=sum(price_winter_FCR_D_up_2021[i])/len(price_winter_FCR_D_up_2021[i])

# price_summer_mean_FCR_D_up_2021=np.zeros((24))
# for i in range(24):
#     price_summer_mean_FCR_D_up_2021[i]=sum(price_summer_FCR_D_up_2021[i])/len(price_summer_FCR_D_up_2021[i])

# #2022
# price_winter_FCR_D_up_2022 = FCR_D_up_2022[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
# price_summer_FCR_D_up_2022 = FCR_D_up_2022[:, 151:243]

# price_winter_mean_FCR_D_up_2022=np.zeros((24))
# for i in range(24):
#     price_winter_mean_FCR_D_up_2022[i]=sum(price_winter_FCR_D_up_2022[i])/len(price_winter_FCR_D_up_2022[i])

# price_summer_mean_FCR_D_up_2022=np.zeros((24))
# for i in range(24):
#     price_summer_mean_FCR_D_up_2022[i]=sum(price_summer_FCR_D_up_2022[i])/len(price_summer_FCR_D_up_2022[i])

# #2024
# price_winter_FCR_D_up_2024 = FCR_D_up_2024[:, np.concatenate((np.arange(334, 366), np.arange(0, 59)))]
# price_summer_FCR_D_up_2024 = FCR_D_up_2024[:, 151:243]

# price_winter_mean_FCR_D_up_2024=np.zeros((24))
# for i in range(24):
#     price_winter_mean_FCR_D_up_2024[i]=sum(price_winter_FCR_D_up_2024[i])/len(price_winter_FCR_D_up_2024[i])

# price_summer_mean_FCR_D_up_2024=np.zeros((24))
# for i in range(24):
#     price_summer_mean_FCR_D_up_2024[i]=sum(price_summer_FCR_D_up_2024[i])/len(price_summer_FCR_D_up_2024[i])

# # Create subplots with 1x2 layout
# fig, axs = plt.subplots(1, 2, figsize=(12, 5))
# fig.suptitle('Mean FCR-D up Prices During Different Seasons')

# # Plot winter and spring in the first subplot
# axs[0].plot(price_winter_mean_FCR_D_up_2024 / 1000, label='Winter')
# axs[0].set_title('Winter')
# axs[0].set_ylabel('SEK/kWh')
# axs[0].set_xlabel('Hour of the day')
# axs[0].set_xlim(0, 23)
# axs[0].grid(True)
# axs[0].legend()

# # Plot summer and autumn in the second subplot
# axs[1].plot(price_summer_mean_FCR_D_up_2024 / 1000, label='Summer')
# axs[1].set_title('Summer')
# axs[1].set_ylabel('SEK/kWh')
# axs[1].set_xlabel('Hour of the day')
# axs[1].set_xlim(0, 23)
# axs[1].grid(True)
# axs[1].legend()

# # Adjust layout
# plt.tight_layout()
# plt.show()

#endregion

#_______FCR-D-down_______________________________________________________________________________
#region Arranges the corresponding loads for each day into the right season
#Winter: December, January, February
#Spring: March, April, May
#Summer: June, July, August
#Autumn: September, October, November
#2023
# price_winter_FCR_D_down_2023 = FCR_D_down_2023[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
# price_spring_FCR_D_down_2023 = FCR_D_down_2023[:, 59:151]
# price_summer_FCR_D_down_2023 = FCR_D_down_2023[:, 151:243]
# price_autumn_FCR_D_down_2023 = FCR_D_down_2023[:, 243:334]

# price_winter_mean_FCR_D_down_2023=np.zeros((24))
# for i in range(24):
#     price_winter_mean_FCR_D_down_2023[i]=sum(price_winter_FCR_D_down_2023[i])/len(price_winter_FCR_D_down_2023[i])

# price_spring_mean_FCR_D_down_2023=np.zeros((24))
# for i in range(24):
#     price_spring_mean_FCR_D_down_2023[i]=sum(price_spring_FCR_D_down_2023[i])/len(price_spring_FCR_D_down_2023[i])

# price_summer_mean_FCR_D_down_2023=np.zeros((24))
# for i in range(24):
#     price_summer_mean_FCR_D_down_2023[i]=sum(price_summer_FCR_D_down_2023[i])/len(price_summer_FCR_D_down_2023[i])

# price_autumn_mean_FCR_D_down_2023=np.zeros((24))
# for i in range(24):
#     price_autumn_mean_FCR_D_down_2023[i]=sum(price_autumn_FCR_D_down_2023[i])/len(price_autumn_FCR_D_down_2023[i])


# #2021
# price_winter_FCR_D_down_2021 = FCR_D_down_2021[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
# price_summer_FCR_D_down_2021 = FCR_D_down_2021[:, 151:243]

# price_winter_mean_FCR_D_down_2021=np.zeros((24))
# for i in range(24):
#     price_winter_mean_FCR_D_down_2021[i]=sum(price_winter_FCR_D_down_2021[i])/len(price_winter_FCR_D_down_2021[i])

# price_summer_mean_FCR_D_down_2021=np.zeros((24))
# for i in range(24):
#     price_summer_mean_FCR_D_down_2021[i]=sum(price_summer_FCR_D_down_2021[i])/len(price_summer_FCR_D_down_2021[i])

# #2022
# price_winter_FCR_D_down_2022 = FCR_D_down_2022[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
# price_summer_FCR_D_down_2022 = FCR_D_down_2022[:, 151:243]

# price_winter_mean_FCR_D_down_2022=np.zeros((24))
# for i in range(24):
#     price_winter_mean_FCR_D_down_2022[i]=sum(price_winter_FCR_D_down_2022[i])/len(price_winter_FCR_D_down_2022[i])

# price_summer_mean_FCR_D_down_2022=np.zeros((24))
# for i in range(24):
#     price_summer_mean_FCR_D_down_2022[i]=sum(price_summer_FCR_D_down_2022[i])/len(price_summer_FCR_D_down_2022[i])

# #2024
# price_winter_FCR_D_down_2024 = FCR_D_down_2024[:, np.concatenate((np.arange(334, 366), np.arange(0, 59)))]
# price_summer_FCR_D_down_2024 = FCR_D_down_2024[:, 151:243]

# price_winter_mean_FCR_D_down_2024=np.zeros((24))
# for i in range(24):
#     price_winter_mean_FCR_D_down_2024[i]=sum(price_winter_FCR_D_down_2024[i])/len(price_winter_FCR_D_down_2024[i])

# price_summer_mean_FCR_D_down_2024=np.zeros((24))
# for i in range(24):
#     price_summer_mean_FCR_D_down_2024[i]=sum(price_summer_FCR_D_down_2024[i])/len(price_summer_FCR_D_down_2024[i])

# # Create subplots with 1x2 layout
# fig, axs = plt.subplots(1, 2, figsize=(12, 5))
# fig.suptitle('Mean FCR-D down Prices During Different Seasons')

# # Plot winter and spring in the first subplot
# axs[0].plot(price_winter_mean_FCR_D_down_2024 / 1000, label='Winter')
# axs[0].set_title('Winter')
# axs[0].set_ylabel('SEK/kWh')
# axs[0].set_xlabel('Hour of the day')
# axs[0].set_xlim(0, 23)
# axs[0].grid(True)
# axs[0].legend()

# # Plot summer and autumn in the second subplot
# axs[1].plot(price_summer_mean_FCR_D_down_2024 / 1000, label='Summer')
# axs[1].set_title('Summer')
# axs[1].set_ylabel('SEK/kWh')
# axs[1].set_xlabel('Hour of the day')
# axs[1].set_xlim(0, 23)
# axs[1].grid(True)
# axs[1].legend()

# # Adjust layout
# plt.tight_layout()
# plt.show()

#endregion