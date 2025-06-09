#region
from numpy import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt 
import windpower
import el_price
from Frequency import frequency_price

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
