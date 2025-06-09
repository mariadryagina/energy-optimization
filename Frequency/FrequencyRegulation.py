#___Importing stuff_____________________________________________________________________________
#region
from numpy import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import frequency_price

# URL to the Excel file on GitHub
url = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Frequency/frequency_data_fixed.xlsx"

# Fetch the file from GitHub
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Read the Excel file into a DataFrame
df = pd.read_excel(BytesIO(response.content))

frequency_data= array(df.iloc[:,1])

#Imported variables from frequency_price
FCR_N_price=frequency_price.FCR_N_1
FCR_N_up_price=frequency_price.FCR_N_upp
FCR_N_down_price=frequency_price.FCR_N_ned
FCR_D_up_price=frequency_price.FCR_D_up_1
FCR_D_down_price=frequency_price.FCR_D_down_1


#endregion
#The different frequency disturbance spans
#FCR-D upp 49,9-49,5
#FCR-D ned 50,1-50,5
#FCR-N 50,0-49,9 50,0-50,1

#__Calculating for how many hours the frequency deviates_________________________________________________________________________________________
#region
fcr_d_upp = []
fcr_d_ned = []
fcr_n_low = []
fcr_n_high = []
correct = []


# Categorize the frequency data
for value in frequency_data:
    if 49.5 <= value < 49.9:
        fcr_d_upp.append(value)
    elif 50.1 < value <= 50.5:
        fcr_d_ned.append(value)
    elif 49.0 <= value < 50.0:
        fcr_n_low.append(value)
    elif 50.0 < value <= 50.1:
        fcr_n_high.append(value)
    elif value == 50.0:
        correct.append(value)

# Print the lengths of each category
print(f"FCR-D upp (49.5-49.9): {len(fcr_d_upp)/20} h")
print(f"FCR-D ned (50.1-50.5): {len(fcr_d_ned)/20} h")
print(f"FCR-N low (49.0-50.0): {len(fcr_n_low)/20} h")
print(f"FCR-N high (50.0-50.1): {len(fcr_n_high)/20} h")
print(f"Correct 50.0: {len(correct)/20} h")

fcr_d_upp = array(fcr_d_upp)
fcr_d_ned = array(fcr_d_ned)
fcr_n_low = array(fcr_n_low)
fcr_n_high = array(fcr_n_high)

#endregion
