import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


merged_time = pd.read_csv("merged_time.csv")
merged_memory = pd.read_csv("merged_memory.csv")

dfs = [merged_time, merged_memory]
df_names = ['time', 'memory']

# Configurations for prefix mappings and column restrictions
prefix_mapping = {
    # Merging configurations
    #"star_intersections_9_combined_cgal": ["star_intersections_9"],
    #"star_intersections_9_combined_boost": ["star_intersections_9"],
    #"star_intersections_9_combined_leda": ["star_intersections_9"],
    #"star_intersections_9_combined_cpp": ["star_intersections_9"],
    #"star_intersections_9_combined_python_1": ["star_intersections_9"],
    #"star_intersections_9_combined_python_2": ["star_intersections_9"],
    #"star_intersections_9_combined_x": ["star_intersections_9"],
    #"star_intersections_10_combined_cgal": ["star_intersections_10"],
    #"star_intersections_10_combined_boost": ["star_intersections_10"],
    #"star_intersections_10_combined_leda": ["star_intersections_10"],
    #"star_intersections_10_combined_cpp": ["star_intersections_10"],
    #"star_intersections_10_combined_python_1": ["star_intersections_10"],
    #"star_intersections_10_combined_python_2": ["star_intersections_10"],
    #"star_intersections_10_combined_x": ["star_intersections_10"],
    #"star_intersections_9_10_combined_cgal": ["star_intersections_9", "star_intersections_10"],
    #"star_intersections_9_10_combined_boost": ["star_intersections_9"],
    "star_intersections_9_10_combined_leda": ["star_intersections_9", "star_intersections_10"],
    #"star_intersections_9_10_combined_cpp": ["star_intersections_10"],
    #"star_intersections_9_10_combined_python_1": ["star_intersections_9"],
    #"star_intersections_9_10_combined_python_2": ["star_intersections_9"],
    #"star_intersections_9_10_combined_x": ["star_intersections_9"],
}

columns_to_restrict = {
    #"star_intersections_9_10_combined_cgal": ["Cgal_intersector_ud", "Cgal_arrangement_ud", "Cgal_intersector_ur", "Cgal_arrangement_ur"],
    #"star_intersections_9_10_combined_boost": ["Boost_d", "Boost_r"],
    "star_intersections_9_10_combined_leda": ["Leda_ud", "Leda_ur"],
    #"star_intersections_9_10_combined_cpp": ["Cgal_intersector_ud", "Cgal_arrangement_ud", "Cgal_intersector_ur", "Leda_ur", "Ogdf_ud"],
    #"star_intersections_9_10_combined_python_1": ["Double_d", "Decimal5_r", "Decimal25_r", "Decimal50_r", "Decimal75_r", "Decimal100_r"],
    #"star_intersections_9_10_combined_python_2": ["Double_d", "Decimal100_r", "Tofraction_r"],
    #"star_intersections_9_10_combined_x": ["Geo_d", "Leda_ud"],
    #"star_intersections_10_combined_cgal": ["Cgal_intersector_ud", "Cgal_arrangement_ud", "Cgal_intersector_ur", "Cgal_arrangement_ur"],
    #"star_intersections_10_combined_boost": ["Boost_d", "Boost_r"],
    #"star_intersections_10_combined_leda": ["Leda_ud", "Leda_ur"],
    #"star_intersections_10_combined_cpp": ["Cgal_intersector_ud", "Cgal_arrangement_ud", "Cgal_intersector_ur", "Cgal_arrangement_ur", "Leda_ud", "Leda_ur"],
    #"star_intersections_10_combined_python_1": ["Double_d", "Decimal5_r", "Decimal25_r", "Decimal50_r", "Decimal75_r", "Decimal100_r"],
    #"star_intersections_10_combined_python_2": ["Double_d", "Decimal100_r", "Tofraction_r"],
    #"star_intersections_10_combined_x": ["Geo_d", "Leda_ud", "Leda_ur"],
}

exclude_prefixes = ['clustered', 'star_intersections_combined_cgal']

os.makedirs('plots_merged', exist_ok=True)

# Iterate over each DataFrame
for df, df_name in zip(dfs, df_names):
    # Extract and map prefixes
    df["Prefix"] = df["File"].apply(lambda x: "_".join(x.split('_')[1:-1]))  # Extract prefix (e.g., "rounding_l")


    # Flatten the prefix_mapping so that each prefix gets assigned to a single unified prefix
    def get_unified_prefix(prefix):
        for unified_prefix, prefixes in prefix_mapping.items():
            if prefix in prefixes:
                return unified_prefix
        return prefix  # If not found, return the prefix itself


    df["Unified_Prefix"] = df["Prefix"].apply(get_unified_prefix)


    # Extract x-values
    def extract_x_value(filename):
        match = re.search(r'(\d+)(?=\.csv$)', filename)  # Match any number before ".csv"
        if match:
            return int(match.group(1))  # Return the matched number as an integer
        return None  # Return None if no number was found


    df.loc[:, "X_Value"] = df["File"].apply(extract_x_value)

    # Process each unified prefix
    for unified_prefix, original_prefixes in prefix_mapping.items():
        unified_data = df[df["Unified_Prefix"] == unified_prefix]
        if unified_data.empty:
            continue  # Skip if no data for this prefix

        # Sort by X_Value
        unified_data = unified_data.sort_values(by="X_Value")

        legend_entries = []

        # Plot separate lines for each original prefix within the unified group
        for original_prefix in original_prefixes:
            prefix_data = unified_data[unified_data["Prefix"] == original_prefix]
            if prefix_data.empty:
                continue  # Skip if no data for this prefix

            # Restrict columns based on configuration
            columns_to_plot = [col for col in prefix_data.columns if col in columns_to_restrict.get(unified_prefix, [])]

            # Plot each column for this prefix
            for column in columns_to_plot:
                prefix_data[column] = pd.to_numeric(prefix_data[column], errors='coerce')

                line, = plt.plot(
                    prefix_data["X_Value"],
                    prefix_data[column],  # Keep y-values specific to this prefix
                    marker='o',
                    label=f"{'si9' if original_prefix == 'star_intersections_9' else 'si10'} - {column}"
                )

                final_y_value = prefix_data[column].iloc[-1]  # Last value in the series
                legend_entries.append((line, final_y_value))

        # Order the legend entries based on final Y-values
        legend_entries.sort(key=lambda x: x[1], reverse=True)  # Sort by final Y-values in descending order

        # Extract sorted lines and labels
        sorted_lines = [entry[0] for entry in legend_entries]
        sorted_labels = [entry[0].get_label() for entry in legend_entries]

        # Set ordered legend
        #plt.legend('')
        plt.legend(sorted_lines, sorted_labels, loc='best')

        # plt.title(f"{df_name} - {unified_prefix}")
        plt.xlabel('Number of Segments')
        # Remove y-axis labels and grid
        # plt.yticks([])  # Remove y-axis tick labels
        plt.ylabel('Runtime in ms' if df_name == 'time' else 'Memory in bytes')  # Remove y-axis label
        plt.grid(True)

        # Save the plot
        plt.savefig(f'plots_merged/{df_name}_{unified_prefix}_combined.png')
        plt.close()


