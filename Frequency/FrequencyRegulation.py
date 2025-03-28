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
#___Calculating the fraction______________________________________________________________________________________________________
#region
frequency_data1=zeros((8760,5))
#1 FCR_d_upp
#2 FCR_d_ned
#3 FCR_n_low
#4 FCR_n_high
#5 Correct 50.0

for i in range(len(frequency_data) // 20):
    for j in(range(20)): 
        value = frequency_data[i*20+j]
        if 49.5 <= value < 49.9:
            frequency_data1[i,0] += 1
        elif 50.1 < value <= 50.5:
            frequency_data1[i,1] += 1
        elif 49.0 <= value < 50.0:
            frequency_data1[i,2] += 1
        elif 50.0 < value <= 50.1:
            frequency_data1[i,3] += 1
        elif value == 50.0:
            frequency_data1[i,4] += 1 

frequency_data1=frequency_data1/20

print(f"the fraction")
print(frequency_data1)


#endregion
#__Calculating mean value__________________________________________________________________________________________________
#region
frequency_data2=zeros((8760,5))

# Initialize lists to store values for each span within each hour
fcr_d_upp_values = [[] for _ in range(8760)]
fcr_d_ned_values = [[] for _ in range(8760)]
fcr_n_low_values = [[] for _ in range(8760)]
fcr_n_high_values = [[] for _ in range(8760)]
correct_values = [[] for _ in range(8760)]

# Process 20 values at a time and store the counts in the corresponding row of frequency_data1
for i in range(8760):
    for j in range(20):
        value = frequency_data[i * 20 + j]
        if 49.5 <= value < 49.9:
            fcr_d_upp_values[i].append(value)
        elif 50.1 <= value <= 50.5:
            fcr_d_ned_values[i].append(value)
        elif 49.0 <= value < 50.0:
            fcr_n_low_values[i].append(value)
        elif 50.0 < value <= 50.1:
            fcr_n_high_values[i].append(value)
        elif value == 50.0:
            correct_values[i].append(value)

# Calculate the mean frequency for each span within each hour and store in the matrix
for i in range(8760):
    frequency_data2[i, 0] = mean(fcr_d_upp_values[i]) if fcr_d_upp_values[i] else 0
    frequency_data2[i, 1] = mean(fcr_d_ned_values[i]) if fcr_d_ned_values[i] else 0
    frequency_data2[i, 2] = mean(fcr_n_low_values[i]) if fcr_n_low_values[i] else 0
    frequency_data2[i, 3] = mean(fcr_n_high_values[i]) if fcr_n_high_values[i] else 0
    frequency_data2[i, 4] = mean(correct_values[i]) if correct_values[i] else 0

# Print the frequency_data1 matrix
print(f"The mean")
print(frequency_data2)
#endregion
#__Caluclating the activation rate___________________________________________________________________________________________
#region
# Define the target values and interval bounds for each category
target_values = [49.9, 50.1, 50.0, 50.0, 50.0]
interval_bounds = [
    (49.5, 49.9),  # FCR-D upp
    (50.1, 50.5),  # FCR-D ned
    (49.9, 50.0),  # FCR-N low
    (50.0, 50.1),  # FCR-N high
    (50.0, 50.0)   # Correct (no activation, always 0%)
]

# Initialize the activation_rate matrix
activation_rate = zeros((8760, 5))

# Calculate the activation rate for each row in frequency_data2
for i in range(8760):
    for j in range(5):
        mean_value = frequency_data2[i, j]
        target = target_values[j]
        lower_bound, upper_bound = interval_bounds[j]
        
        # Calculate activation rate only if the value is within the interval
        if lower_bound <= mean_value <= upper_bound:
            if mean_value < target:  # Below the target
                activation_rate[i, j] = (target - mean_value) / (target - lower_bound)
            elif mean_value > target:  # Above the target
                activation_rate[i, j] = (mean_value - target) / (upper_bound - target)
        else:
            activation_rate[i, j] = 0  # No activation if outside the interval

# Print the activation_rate matrix
print(f"The activation rate")
print(activation_rate)
#endregion

#___Calculating the potential revenue________________________________________________________________________________
#region
#First, decied a bid size. 0,1MW because that is the minimum bid size

P_bid=full((8760,5), 0.1) #[MW]
P_bid_scaled=zeros((8760,5))

#How much of the bid size is used?
for i in range(8760):
    for j in range(5):
        P_bid_scaled[i,j]=P_bid[i,j]*activation_rate[i,j]


# Initialize revenue matrices
FCR_revenue = zeros((8760, 5))


# Calculate FCR-N revenue
for i in range(8760):
    FCR_revenue[i, 0] = P_bid_scaled[i, 0] * FCR_D_up_price[i]
    FCR_revenue[i, 1] = P_bid_scaled[i, 1] * FCR_D_down_price[i]
    FCR_revenue[i, 2] = P_bid_scaled[i, 2] * FCR_N_price[i]  # Explicitly extract scalar
    FCR_revenue[i, 3] = P_bid_scaled[i, 3] * FCR_N_price[i]  # Explicitly extract scalar
    FCR_revenue[i, 4] = P_bid_scaled[i, 4]

# Print the FCR-N revenue matrix
print("FCR Revenue:")
print(FCR_revenue)

# Convert the NumPy array to a DataFrame
FCR_revenue_pd = pd.DataFrame(FCR_revenue)

# Save the frequency data to a CSV file for further analysis
FCR_revenue_pd.to_csv('FCR_revenue.csv', index=False)


#endregion