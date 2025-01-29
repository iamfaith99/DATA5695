import pandas as pd
import numpy as np
import math

# Create the data
data = [
    ['7/7/2010', 1060.27, np.nan, 127.00, np.nan],
    ['7/14/2010', 1095.17, 0.03239, 130.72, 0.02887],
    ['7/21/2010', 1069.59, -0.02363, 125.27, -0.04259],
    ['7/28/2010', 1106.13, 0.03359, 128.43, 0.02491],
    ['8/4/2010', 1127.24, 0.01890, 131.27, 0.02187],
    ['8/11/2010', 1089.47, -0.03408, 129.83, -0.01103],
    ['8/18/2010', 1094.16, 0.00430, 129.39, -0.00338],
    ['8/25/2010', 1055.33, -0.03613, 125.27, -0.03238],
    ['9/1/2010', 1080.29, 0.02338, 125.77, 0.00398],
    ['9/8/2010', 1098.87, 0.01705, 126.08, 0.00246],
]

columns = ['Date', 'S&P 500 Price', 'S&P 500 Return', 'IBM Price', 'IBM Return']

df = pd.DataFrame(data, columns=columns)

# Calculate standard deviations and annualize
std_sp = round(df['S&P 500 Return'].std(), 5)
std_ibm = round(df['IBM Return'].std(), 5)

annualized_sp = round(std_sp * math.sqrt(52), 5)
annualized_ibm = round(std_ibm * math.sqrt(52), 5)

# Add summary rows with np.nan for Price columns
df.loc[len(df)] = ['Standard deviation', np.nan, std_sp, np.nan, std_ibm]
df.loc[len(df)] = ['Standard deviation × √52', np.nan, annualized_sp, np.nan, annualized_ibm]

# Replace NaN with empty strings for cleaner output
df.fillna('', inplace=True)

# Print the table with NaN replaced by empty strings
print(df.to_string(index=False))