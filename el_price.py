import pandas as pd
import numpy as np

path_to_file4 = "/Users/a518244/Python/energy-optimization/Spotpriser/price_2024.csv"
path_to_file3 = "/Users/a518244/Python/energy-optimization/Spotpriser/price_2023.csv"

# Read the CSV file
df4 = pd.read_csv(path_to_file4)
df3 = pd.read_csv(path_to_file3)

# Extract values from the second column (index 1)
values_2023 = df3.iloc[0:8761, 1].values
values_2024 = df4.iloc[0:8785, 1].values

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

# Printing the spotprice
# spotprice_df_2023 = pd.DataFrame(spotprice_matrix_2023)
# spotprice_df_2024 = pd.DataFrame(spotprice_matrix_2024)
# print(spotprice_df_2023)
# print(spotprice_df_2024)

