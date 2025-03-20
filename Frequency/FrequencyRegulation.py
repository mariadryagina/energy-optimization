from numpy import *
import pandas as pd
from datetime import datetime
from math import *
import matplotlib.pyplot as plt 

#Reading excel file 
path_to_file = "/Users/a517469/Python/energy-optimization/Frequency/frequencydata_2023.xlsx"
df = pd.read_excel(path_to_file)


F=zeros((20,8760))

# Define the valid intervals
valid_intervals = list(range(1, 60, 3))  # 1, 4, 7, ..., 58
valid_intervals1=valid_intervals*8760


frequency_data=[]
excluded_values =[]

for i in range(len(df)):
    minute = df.iloc[i,2]
    if minute in valid_intervals:
        frequency_data.append([df.iloc[i,2], df.iloc[i,5], df.iloc[i,1]])
    else:
        excluded_values.append((i, df.iloc[i, 2], df.iloc[i, 5], df.iloc[i, 1]))


# Convert the list to a NumPy array
frequency_data=array(frequency_data)
excluded_values=array(excluded_values)
print(len(frequency_data))

# Convert the NumPy array to a DataFrame
excluded_df = pd.DataFrame(excluded_values)

# Save the frequency data to a CSV file for further analysis
excluded_df.to_csv('Excluded_values.csv', index=False)


#____________________round 1__________________________________________________________
#Checking if there are any values missing and finding their position
while True:
    missing_values = []
    for i in range(len(frequency_data)-1):
        b=abs(int(frequency_data[i+1,0])-int(frequency_data[i,0]))
        if b!=3 and b!=57: 
            missing_values.append(i)
        
    missing_values=array(missing_values)

    if len(missing_values) == 0:
        break

    # Print the missing values
    print("Missing Values:")
    print(missing_values)
    print(len(missing_values))

    # Add the values at the specified positions
    for pos in reversed(missing_values):
        if int(frequency_data[pos,0]) == 58:
            value_to_add = [1,50,0]
        else:
            value_to_add = [int(frequency_data[pos,0])+3,50, 0]
        
        frequency_data = insert(frequency_data, pos+1, value_to_add, axis=0)

    print("Length of Frequency Array:")
    a = len(frequency_data)
    print(a)


#_____________Creating a CSV file_______________________________________________________
# Convert the NumPy array to a DataFrame
frequency_df = pd.DataFrame(frequency_data)

# Save the frequency data to a CSV file for further analysis
frequency_df.to_csv('frequency_data2.csv', index=False)

#The different frequency disturbance spans
#FCR-D upp 49,9-49,5
#FCR-D ned 50,1-50,5
#FCR-N 50,0-49,9 50,0-50,1



