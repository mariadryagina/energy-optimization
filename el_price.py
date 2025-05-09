import pandas as pd
import numpy as np
import requests
from io import BytesIO

# URL to the Excel file on GitHub
url23 = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Spotpriser/price_2023.csv"
url24 = "https://raw.githubusercontent.com/mariadryagina/energy-optimization/main/Spotpriser/price_2024.csv"

# Fetch the file from GitHub
response23 = requests.get(url23, verify=False)
response24 = requests.get(url24, verify=False)
response23.raise_for_status()  # Check if the request was successful
response24.raise_for_status()  # Check if the request was successful

# Read the Excel file into a DataFrame
df23 = pd.read_csv(BytesIO(response23.content))
df24 = pd.read_csv(BytesIO(response24.content))

# Extract values from the second column (index 1)
values_2023 = df23.iloc[0:8761, 1].values
values_2024 = df24.iloc[0:8785, 1].values

# Create a matrix (reshape if needed, here assuming a 1D array)
spotprice_matrix_2023 = np.array(values_2023)
spotprice_matrix_2024 = np.array(values_2024)

# Initialize an empty 2D array with appropriate dimensions
rows = 24
cols_2023 = -(-len(spotprice_matrix_2023) // rows)  # Calculate number of columns needed, rounding up
spotprice_2023 = np.zeros((rows, cols_2023))

# Fill the matrix "spotprice_matrix_2023" with values
for i, value in enumerate(spotprice_matrix_2023):
    row = i % rows
    col = i // rows
    spotprice_2023[row, col] = value

rows = 24
cols_2024 = -(-len(spotprice_matrix_2024) // rows)  # Calculate number of columns needed, rounding up
spotprice_2024 = np.zeros((rows, cols_2024))

# Fill the matrix "spotprice_matrix_2024" with values
for i, value in enumerate(spotprice_matrix_2024):
    row = i % rows
    col = i // rows
    spotprice_2024[row, col] = value

spotprice_2023_winter = spotprice_2023[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
spotprice_2023_spring = spotprice_2023[:, 59:151]
spotprice_2023_summer = spotprice_2023[:, 151:243]
sptorprice_2023_autumn = spotprice_2023[:, 243:334]

spotprice_2024_winter = spotprice_2024[:, np.concatenate((np.arange(334, 365), np.arange(0, 59)))]
spotprice_2024_spring = spotprice_2024[:, 59:151]
spotprice_2024_summer = spotprice_2024[:, 151:243]
sptorprice_2024_autumn = spotprice_2024[:, 243:334]


# # Printing the spotprice
# spotprice_df_2023 = pd.DataFrame(spotprice_matrix_2023)
# spotprice_df_2024 = pd.DataFrame(spotprice_matrix_2024)
# print(np.size(spotprice_2023))
# print(spotprice_df_2024)


