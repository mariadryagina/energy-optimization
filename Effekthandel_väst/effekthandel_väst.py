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
response = requests.get(url,verify=False)
response.raise_for_status()  # Check if the request was successful

# Read the Excel file into a DataFrame
df = pd.read_excel(BytesIO(response.content))


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


# Randomly select 13% of these blocks for activation
#region
num_blocks_to_activate = int(len(blocks_with_bids) * 0.13)  # 13% of the blocks
activated_blocks = random.choice(len(blocks_with_bids), size=num_blocks_to_activate, replace=False)

# Activate the selected blocks
for block_index in activated_blocks:
    day, block = blocks_with_bids[block_index]  # Get the day and block
    for hour in block:
        I_activated[hour, day] = 1  # Activate the entire block

# #endregion


