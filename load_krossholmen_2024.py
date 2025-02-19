# To run script both pandas and openpyxl must be installed. If not, install them by running the following commands:
# pip install pandas
# pip install openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path_to_file = "/Users/a518244/Python/measurePointConsumption.xlsx"

df = pd.read_excel(path_to_file)

# Extract values from the fourth column third row-2185th row (index 3)
load_values = df.iloc[6:8791, 4].values

# Create a matrix (reshape if needed, here assuming a 1D array)
load_matrix = np.array(load_values)

print(load_matrix)

# Initialize an empty 2D array with appropriate dimensions
rows = 24
cols = -(-len(load_matrix) // rows)  # Calculate number of columns needed, rounding up
load = np.zeros((rows, cols))

# Fill the matrix "load" with values
for i, value in enumerate(load_matrix):
    row = i % rows
    col = i // rows
    load[row, col] = value

load_df = pd.DataFrame(load)
print(load_df)

# Correct slicing syntax
load_jan = load[:, 0:30]
load_feb = load[:, 30:59]
load_mar = load[:, 59:90]
load_apr = load[:, 90:120]
load_may = load[:, 120:151]
load_jun = load[:, 151:181]
load_jul = load[:, 181:212]
load_aug = load[:, 212:243]
load_sep = load[:, 243:273]
load_oct = load[:, 273:304]
load_nov = load[:, 304:334]
load_dec = load[:, 334:365]

# Calculate the sum of all values in each row of load_jan
load_jan_sums = load_jan.sum(axis=1)

print(load_jan_sums)

# Create a boxplot for the sum of all values in each row of load_jan
plt.boxplot(load_jan_sums)
plt.title('Boxplot for Sum of Load in January')
plt.xlabel('Row')
plt.ylabel('Sum of Load')
plt.grid(True)
plt.show()