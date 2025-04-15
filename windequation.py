import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
from math import *
import requests
from io import BytesIO
from scipy.interpolate import interp1d

# URL to the Excel file on GitHub
url = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Self-produced_electricity/winddata1_2023.xlsx"

# Fetch the file from GitHub
response = requests.get(url, verify=False)
response.raise_for_status()  # Check if the request was successful

# Read the Excel file into a DataFrame
df = pd.read_excel(BytesIO(response.content))




#Check the number of rows in the DataFrame
if df.shape[0] == 8760:
     a=365 #Non-leap year
else:
     a=366 #leap year

#Creting a matrix with zeros
V=np.zeros((24,a))
watt_new=np.zeros((24,365))

for i in range(a):
    for j in range(24):
         V[j,i]=df.iloc[i*24+j,4]


#If a value is greater than 12 it will be changed to 12	
for i in range(24):
    for j in range(a):
        if V[i, j] > 13:
            V[i, j] = 0

for i in range(24):
    for j in range(a):
        if V[i, j] < 2.8:
            V[i, j] = 0

watt=np.array([0,0,0.1,0.2,0.35,0.5,0.8,1.3,2,2.7,3.7,5,6,6])
m_s=np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13])
f = interp1d(m_s, watt)

def wind(n):
    watt_new=f(V)*n
    return watt_new

watt_new=wind(1)

print(watt_new)

total_sum=ceil(np.sum(watt_new))
print(f"The yearly production of wind power is {total_sum}kWh")

# Creating the plot
plt.figure(figsize=(10, 5))
plt.plot(m_s, watt, marker='o', linestyle='-', label='Power Output')
plt.xlabel('Wind Speed (m/s)')
plt.ylabel('Power Output (kW)')
plt.title('Wind turbine power curve')
plt.legend()
plt.grid(True)
plt.show()
