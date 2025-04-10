from numpy import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt
import requests
from io import BytesIO

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
V=zeros((24,a))

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


#_Function begins_______________________________________________________________#
#V - wind speed in m/s
#n - amount of turbines
#The formula for wind power is P_w=0,0116*V^2,4721 and it is in kW

def wind(n):
     
     P_wind=(0.0146*V**2.3654*n)
     

     return P_wind
#_______________________________________________________________________________#

#Calling on function
#P_wind1=wind(1)

#Calculating the sum of the array
# total_sum=ceil(sum(P_wind2)*10)/10
# print(f"The yearly production of wind power is {total_sum}MWh")

#_______________________________________________________________________________#
# # Creating a plot
# plt.figure(figsize=(10, 5))
# plt.plot(range(0, a), P_wind1*1000, label='Daily Wind Power Production')
# plt.xlabel('Day of the Year')
# plt.ylabel('Wind Power Production (kWh)')
# plt.title('Daily Wind Power Production')
# plt.legend()
# plt.grid(True)
# plt.show()


