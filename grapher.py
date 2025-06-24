import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


merged_time = pd.read_csv("merged_time.csv")
merged_memory = pd.read_csv("merged_memory.csv")

# Ensure the 'plots' directory exists
os.makedirs('plots', exist_ok=True)

# List of valid prefixes for plotting
plotting_prefixes = [
    "rounding_s", "rounding_m", "rounding_l",
    "clustered_s", "clustered_m", "clustered_l", "clustered_xl", "clustered_xxl", "clustered_xxxl", "clustered_xxxxl", "clustered_xxxxxl",
    "clustered_xxxxxxl", "clustered_xxxxxxxl", "clustered_xxxxxxxxl",
    "clustered_xxxxxxxxxl", "clustered_xxxxxxxxxxl", "clustered_xxxxxxxxxxxl", "clustered_xxxxxxxxxxxxl", "clustered_xxxxxxxxxxxxxl", "clustered_xxxxxxxxxxxxxxl",
    "clustered_xxxxxxxxxxxxxxxl", "clustered_xxxxxxxxxxxxxxxxl", "clustered_xxxxxxxxxxxxxxxxxl", "clustered_xxxxxxxxxxxxxxxxxxl", "clustered_xxxxxxxxxxxxxxxxxxxl",
    "random_s", "random_m", "random_l", "star_intersections_4", "star_intersections_6", "star_intersections_7", "star_intersections_8"
]

# Replace these with actual DataFrames
dfs = [merged_time, merged_memory]
df_names = ['time', 'memory']

# Iterate over each DataFrame
for df, df_name in zip(dfs, df_names):
    df = df.copy()  # Avoid modifying the original DataFrame
    df["Prefix"] = df["File"].apply(lambda x: "_".join(x.split('_')[1:-1]))  # Extract prefix
    df = df[df["Prefix"].isin(plotting_prefixes)]

    def extract_x_value(filename):
        match = re.search(r'(\d+)(?=\.csv$)', filename)
        return int(match.group(1)) if match else None

    df.loc[:, "X_Value"] = df["File"].apply(extract_x_value)

    for prefix in plotting_prefixes:
        df_prefix = df[df["Prefix"] == prefix]
        if df_prefix.empty:
            continue

        df_prefix = df_prefix.sort_values(by="X_Value")
        columns_to_plot = [col for col in df_prefix.columns if col not in ['File', 'Prefix', 'X_Value']]

        for column in columns_to_plot:
            df_prefix[column] = pd.to_numeric(df_prefix[column], errors='coerce')

            n_values = df_prefix["X_Value"]
            y_values = df_prefix[column]

            plt.figure(figsize=(10, 6))

            if 'clustered' not in prefix:
                valid_indices = ~(np.isnan(y_values) | np.isinf(y_values))
                n_values_clean = n_values[valid_indices]
                y_values_clean = y_values[valid_indices]

            plt.plot(n_values, y_values, marker='o', label=column)

            plt.title(f'{prefix} Data - {df_name} - {column}')
            plt.xlabel('Number of segments' if 'clustered' not in prefix else 'Number of clusters')
            plt.ylabel('Time in ms' if df_name == 'time' else 'Memory usage in bytes')
            plt.legend(title='Columns')
            plt.grid(True)

            plt.savefig(f'plots/{df_name}_{column}_{prefix}.png')
            plt.close()