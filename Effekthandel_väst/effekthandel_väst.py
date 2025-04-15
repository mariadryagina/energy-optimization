#___Importing stuff_____________________________________________________________________________
#region
from numpy import *
import pandas as pd
from math import *
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# URL to the Excel file on GitHub
url = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Effekthandel_väst/Effekthandelväst_aktivering.xlsx"

# Fetch the file from GitHub
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Read the Excel file into a DataFrame
df = pd.read_excel(BytesIO(response.content))

# Ensure the date column is in datetime format
df['Date'] = pd.to_datetime(df['Date'])  # Replace 'Date' with the actual column name in your DataFrame

# Filter data for each year
df_2022 = df[df['Date'].dt.year == 2022]
df_2023 = df[df['Date'].dt.year == 2023]
df_2024 = df[df['Date'].dt.year == 2024]


#endregion

#____Creating Matrix_____________________________________________________________________________
#region
#We assume that the bids are placed every second week in Januari, Februari, Mars, November, December
#7-9 and 17-19
#Boat: 100kWh/150kW
#BESS: 533kWh/352kW

#Creating a matrix for when bids are place
# Initialize the bid matrix (24 hours x 365 days)
I_bid = zeros((24, 365))

# Define the months for bidding (1-based indexing for months)
bidding_months = [1, 2, 3, 11, 12]  # January, February, March, November, December

# Loop through all days of the year
for day in range(365):
    # Get the current date
    current_date = pd.Timestamp('2023-01-01') + pd.Timedelta(days=day)
    
    # Check if the current month is in the bidding months
    if current_date.month in bidding_months:
        # Check if the current day is a Monday and belongs to every second week
        if current_date.weekday() == 0 and (day // 7) % 2 == 0:  # Monday and every second week
            # Place bids for the entire week (7 days)
            for offset in range(7):  # Loop through the next 7 days
                if day + offset < 365:  # Ensure we don't go out of bounds
                    # Set bids for hours 7-9
                    I_bid[7:9, day + offset] = 1
                    # Set bids for hours 17-19
                    I_bid[17:19, day + offset] = 1

# Print the bid matrix to verify
print(I_bid)
# Count the total number of 1s in the I_bid matrix
total_bids = I_bid.sum()

# Print the result
print(f"Total number of bids (1s) in I_bid: {total_bids}")

#Creating a matrix for when the bids are activated
# Initialize the activation matrix (same shape as I_bid)
I_activated = zeros_like(I_bid)

# Identify all blocks (7-9 and 17-19) where bids are placed
blocks_with_bids = []
for day in range(365):
    if any(I_bid[7:10, day] == 1):  # Check if 7-9 block has bids
        blocks_with_bids.append((day, range(7, 9)))  # Add the 7-9 block
    if any(I_bid[17:20, day] == 1):  # Check if 17-19 block has bids
        blocks_with_bids.append((day, range(17, 19)))  # Add the 17-19 block



# Define specific positions to activate (indices of blocks_with_bids)
specific_positions = [10,40, 50,60, 90, 100,120]  # Replace with the specific indices you want to activate
print(f"Total number of blocks with bids: {len(blocks_with_bids)}")

# Ensure the number of positions matches 5% of the total blocks
num_blocks_to_activate = int(len(blocks_with_bids) * 0.05)
if len(specific_positions) != num_blocks_to_activate:
    raise ValueError("The number of specific positions must match 5 the total blocks.")



# Activate the selected blocks
for block_index in specific_positions:
    day, block = blocks_with_bids[block_index]  # Get the day and block
    for hour in block:
        I_activated[hour, day] = 1  # Activate the entire block

# Print the activation matrix to verify
print(I_activated)



# Randomly select 13% of these blocks for activation
#region
# num_blocks_to_activate = int(len(blocks_with_bids) * 0.13)  # 13% of the blocks
# activated_blocks = random.choice(len(blocks_with_bids), size=num_blocks_to_activate, replace=False)

# # Activate the selected blocks
# for block_index in activated_blocks:
#     day, block = blocks_with_bids[block_index]  # Get the day and block
#     for hour in block:
#         I_activated[hour, day] = 1  # Activate the entire block

# # Print the activation matrix to verify
# print(I_activated)

# print(f"Total activated bids: {I_activated.sum()}")  # Each block has 3 hours
# print(f"Activated blocks: {len(activated_blocks)}")
#endregion
#endregion




#____Function_______________________________________________________________________________________
#region

R_cap= 200/1000 #0,2 SEK/kWh
R_energy = 3500/1000 #3,5 SEK/kWh
boat_capacity=100 
bess_capacity=533
number_boats=3
range=0.8 

def flexibility_market(R_cap, R_energy, boat_capacity, bess_capacity, number_boats, range):
    P_bid=(((number_boats*boat_capacity)+bess_capacity)*range)/2
    R_LFM_cap=I_bid*R_cap*P_bid
    R_LFM_activated=I_activated*R_energy*P_bid
    R_LFM=R_LFM_cap+R_LFM_activated
    
    return R_LFM, P_bid

R_LFM, P_bid =flexibility_market(R_cap, R_energy, boat_capacity, bess_capacity, number_boats, range)

print(R_LFM)
print(P_bid)

total_revenue=R_LFM.sum()

# # Print the result
# print(f"Total revenue generated: {total_revenue}")

#endregion

#____CSV files____________________________________________________________________________________
#region

# # Optionally, save the activation matrix to a CSV file
# I_activated_df = pd.DataFrame(I_activated)
# I_activated_df.to_csv('I_activated.csv', index=False)


# # Convert the NumPy array to a DataFrame
# I_bid_df = pd.DataFrame(I_bid)
# # Save the bid matrix to a CSV file for further analysis
# I_bid_df.to_csv('I_bid.csv', index=False)

# # Optionally, save the activation matrix to a CSV file
# R_LFM_df = pd.DataFrame(R_LFM)
# R_LFM_df.to_csv('R_LFM.csv', index=False)

#endregion
