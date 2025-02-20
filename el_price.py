import pandas as pd
import numpy as np

path_to_file = "/Users/a518244/Python/energy-optimization/measurePointConsumptionPrice.xlsx"

df = pd.read_excel(path_to_file)

# Extract values from the fourth column third row-2185th row (index 3)
spotprice_values = df.iloc[1:2184, 3].values

# Create a matrix (reshape if needed, here assuming a 1D array)
spotprice_matrix = np.array(spotprice_values)

print(spotprice_matrix)

# Initialize an empty 2D array with appropriate dimensions
rows = 24
cols = -(-len(spotprice_matrix) // rows)  # Calculate number of columns needed, rounding up
spotprice = np.zeros((rows, cols))

# Fill the matrix "spotprice" with values
for i, value in enumerate(spotprice_matrix):
    row = i % rows
    col = i // rows
    spotprice[row, col] = value

#print(spotprice)

spotprice_df = pd.DataFrame(spotprice)
print(spotprice_df)

