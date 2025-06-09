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
