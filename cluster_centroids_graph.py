#%%
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
#%%
def plot_cluster_centroids_scatter(folder_path):
    # Initialize empty lists to store latitudes and longitudes
    all_latitudes = []
    all_longitudes = []

    # Loop through all CSV files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)

            # Read CSV file using pandas
            df = pd.read_csv(file_path)

            # Extract Latitude and Longitude columns
            latitudes = df['Latitude'].tolist()
            longitudes = df['Longitude'].tolist()

            # Append to the overall lists
            all_latitudes.extend(latitudes)
            all_longitudes.extend(longitudes)

    # Plot the latitudes and longitudes on a scatter plot
    plt.scatter(all_longitudes, all_latitudes, marker='o', color='blue')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Cluster Centroids - Scatter Plot')
    plt.grid(True)
    plt.show()

def plot_cluster_centroids_heatmap(folder_path):
    # Initialize an empty DataFrame
    combined_df = pd.DataFrame()

    # Loop through all CSV files in the folder and concatenate them
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)

            # Read CSV file using pandas
            df = pd.read_csv(file_path)

            # Concatenate the DataFrame
            combined_df = pd.concat([combined_df, df])

    # Generate a heatmap using seaborn
    plt.figure(figsize=(10, 8))
    sns.heatmap(combined_df[['Latitude', 'Longitude']], cmap='viridis', annot=False)
    plt.title('Cluster Centroids - Heatmap')
    plt.show()

# Provide the path to the "cluster-centroids" folder
folder_path = Path('cluster-centroids')
#%%
# Plot scatter plot
plot_cluster_centroids_scatter(folder_path)
