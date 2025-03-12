from numpy import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt 

import requests
from io import BytesIO

# URL to the Excel file on GitHub
url = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/solardata_2023.xlsx"

# Fetch the file from GitHub
response = requests.get(url)
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

#_Function begins_______________________________________________________________#
#I - irradiation in W/m^2
#A - amount of panels in m^2
#eta - efficency of PV farm
def solar(A, eta):
    P_s = (I * A * eta) / (1000*1000)
    P_s1 = zeros(a)  # Initialize P_s1 as an array
    for i in range(a):
        P_s1[i] = sum(P_s[:, i])
    
    return P_s1
#_______________________________________________________________________________#

#Calling on function
# P_s2=solar(167,0.20)

# #Calculating the sum of the array
# total_sum=round(sum(P_s2)*10)/10
# print(f"The yearly production of solar power is {total_sum}MWh")

# #______________________________________________________________________________#
# #Validation
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

#______________________________________________________________________________#

