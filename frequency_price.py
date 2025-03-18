import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# URL to the Excel file on GitHub
url = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Frequency/FCR_pris.xlsx"

# Fetch the file from GitHub
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Read the Excel file into a DataFrame
df = pd.read_excel(BytesIO(response.content))

#________________Storing the values in a matrix_______________________________________________________________________
#region 11,03 SEK to 1 EUR
#Storing FCR-N prices in a matrix SEK/MWh
FCR_N=np.zeros((24,365))

for i in range(365):
    for j in range(24):
         FCR_N[j,i]=(df.iloc[i*24+j,5])*11.03

#Storing FCR-D up prices in a matrix SEK/MWh
FCR_D_up=np.zeros((24,365))

for i in range(365):
    for j in range(24):
         FCR_D_up[j,i]=(df.iloc[i*24+j,12])*11.03


#Storing FCR-D down prices in a matrix SEK/MWh
FCR_D_down=np.zeros((24,365))

for i in range(365):
    for j in range(24):
         FCR_D_down[j,i]=(df.iloc[i*24+j,19])*11.03

#endregion
#_______FCR-N_______________________________________________________________________________
#region Arranges the corresponding loads for each day into the right season
#Winter: December, January, February
#Spring: March, April, May
#Summer: June, July, August
#Autumn: September, October, November
price_winter_FCR_N = FCR_N[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
price_spring_FCR_N = FCR_N[:, 59:151]
price_summer_FCR_N = FCR_N[:, 151:243]
price_autumn_FCR_N = FCR_N[:, 243:334]

price_winter_mean_FCR_N=np.zeros((24))
for i in range(24):
    price_winter_mean_FCR_N[i]=sum(price_winter_FCR_N[i])/len(price_winter_FCR_N[i])

price_spring_mean_FCR_N=np.zeros((24))
for i in range(24):
    price_spring_mean_FCR_N[i]=sum(price_spring_FCR_N[i])/len(price_spring_FCR_N[i])

price_summer_mean_FCR_N=np.zeros((24))
for i in range(24):
    price_summer_mean_FCR_N[i]=sum(price_summer_FCR_N[i])/len(price_summer_FCR_N[i])

price_autumn_mean_FCR_N=np.zeros((24))
for i in range(24):
    price_autumn_mean_FCR_N[i]=sum(price_autumn_FCR_N[i])/len(price_autumn_FCR_N[i])


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
price_winter_FCR_D_up = FCR_D_up[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
price_spring_FCR_D_up = FCR_D_up[:, 59:151]
price_summer_FCR_D_up = FCR_D_up[:, 151:243]
price_autumn_FCR_D_up = FCR_D_up[:, 243:334]

price_winter_mean_FCR_D_up=np.zeros((24))
for i in range(24):
    price_winter_mean_FCR_D_up[i]=sum(price_winter_FCR_D_up[i])/len(price_winter_FCR_D_up[i])

price_spring_mean_FCR_D_up=np.zeros((24))
for i in range(24):
    price_spring_mean_FCR_D_up[i]=sum(price_spring_FCR_D_up[i])/len(price_spring_FCR_D_up[i])

price_summer_mean_FCR_D_up=np.zeros((24))
for i in range(24):
    price_summer_mean_FCR_D_up[i]=sum(price_summer_FCR_D_up[i])/len(price_summer_FCR_D_up[i])

price_autumn_mean_FCR_D_up=np.zeros((24))
for i in range(24):
    price_autumn_mean_FCR_D_up[i]=sum(price_autumn_FCR_D_up[i])/len(price_autumn_FCR_D_up[i])


# # Create subplots
# fig, axs = plt.subplots(2, 2, figsize=(10, 5))
# fig.suptitle('Mean FCR-D up Prices During Different Seasons')
# # Plot mean FCR-N price during winter
# axs[0, 0].plot(price_winter_mean_FCR_D_up/1000)
# axs[0, 0].set_title('Winter')
# axs[0, 0].set_ylabel('SEK/kWh')
# axs[0, 0].set_xlabel('Hour of the day')
# axs[0, 0].set_xlim(0, 23)
# axs[0, 0].grid(True)

# # Plot mean FCR-N price during spring
# axs[0, 1].plot(price_spring_mean_FCR_D_up/1000)
# axs[0, 1].set_title('Spring')
# axs[0, 1].set_ylabel('SEK/kWh')
# axs[0, 1].set_xlabel('Hour of the day')
# axs[0, 1].grid(True)

# # Plot mean FCR-N price during summer
# axs[1, 0].plot(price_summer_mean_FCR_D_up/1000)
# axs[1, 0].set_title('Summer')
# axs[1, 0].set_ylabel('SEK/kWh')
# axs[1, 0].set_xlabel('Hour of the day')
# axs[1, 0].set_xlim(0, 23)
# axs[1, 0].grid(True)

# # Plot mean FCR-N price during autumn
# axs[1, 1].plot(price_autumn_mean_FCR_D_up/1000)
# axs[1, 1].set_title('Autumn')
# axs[1, 1].set_ylabel('SEK/kWh')
# axs[1, 1].set_xlabel('Hour of the day')
# axs[1, 1].grid(True)

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
price_winter_FCR_D_down = FCR_D_down[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
price_spring_FCR_D_down = FCR_D_down[:, 59:151]
price_summer_FCR_D_down = FCR_D_down[:, 151:243]
price_autumn_FCR_D_down = FCR_D_down[:, 243:334]

price_winter_mean_FCR_D_down=np.zeros((24))
for i in range(24):
    price_winter_mean_FCR_D_down[i]=sum(price_winter_FCR_D_down[i])/len(price_winter_FCR_D_down[i])

price_spring_mean_FCR_D_down=np.zeros((24))
for i in range(24):
    price_spring_mean_FCR_D_down[i]=sum(price_spring_FCR_D_down[i])/len(price_spring_FCR_D_down[i])

price_summer_mean_FCR_D_down=np.zeros((24))
for i in range(24):
    price_summer_mean_FCR_D_down[i]=sum(price_summer_FCR_D_down[i])/len(price_summer_FCR_D_down[i])

price_autumn_mean_FCR_D_down=np.zeros((24))
for i in range(24):
    price_autumn_mean_FCR_D_down[i]=sum(price_autumn_FCR_D_down[i])/len(price_autumn_FCR_D_down[i])


# # Create subplots
# fig, axs = plt.subplots(2, 2, figsize=(10, 5))
# fig.suptitle('Mean FCR-D down Prices During Different Seasons')

# # Plot mean FCR-N price during winter
# axs[0, 0].plot(price_winter_mean_FCR_D_down)
# axs[0, 0].set_title('Winter')
# axs[0, 0].set_ylabel('SEK/MWh')
# axs[0, 0].set_xlabel('Hour of the day')
# axs[0, 0].set_xlim(0, 23)
# axs[0, 0].grid(True)

# # Plot mean FCR-N price during spring
# axs[0, 1].plot(price_spring_mean_FCR_D_down)
# axs[0, 1].set_title('Spring')
# axs[0, 1].set_ylabel('SEK/MWh')
# axs[0, 1].set_xlabel('Hour of the day')
# axs[0, 1].grid(True)

# # Plot mean FCR-N price during summer
# axs[1, 0].plot(price_summer_mean_FCR_D_down)
# axs[1, 0].set_title('Summer')
# axs[1, 0].set_ylabel('SEK/MWh')
# axs[1, 0].set_xlabel('Hour of the day')
# axs[1, 0].set_xlim(0, 23)
# axs[1, 0].grid(True)

# # Plot mean FCR-N price during autumn
# axs[1, 1].plot(price_autumn_mean_FCR_D_down)
# axs[1, 1].set_title('Autumn')
# axs[1, 1].set_ylabel('SEK/MWh')
# axs[1, 1].set_xlabel('Hour of the day')
# axs[1, 1].grid(True)

# Adjust layout
plt.tight_layout()
plt.show()

#endregion