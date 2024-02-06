#%%
from pathlib import Path
import pandas as pd
import glob
import matplotlib.pyplot as plt
#%%
def analyze_clusters(data_folder="analyzed_results"):
    # Set the data path
    data_path = Path(data_folder)

    # Get a list of all CSV files in the data path
    csv_files = glob.glob(str(data_path / '*.csv'))

    # Initialize counters for clusters won by Biden and Trump
    biden_wins = []
    trump_wins = []

    # Iterate through each CSV file
    for csv_file in csv_files:
        # Read the CSV file into a DataFrame
        analyzed_result = pd.read_csv(csv_file)

        # Initialize counters for clusters won by Biden and Trump in this file
        biden_wins_file = 0
        trump_wins_file = 0

        # Iterate through each cluster in the file
        for cluster in analyzed_result['Cluster'].unique():
            cluster_data = analyzed_result[analyzed_result['Cluster'] == cluster]

            # Determine the winner for the current cluster
            cluster_winner = 'Biden' if cluster_data['Biden Votes Weighted'].sum() > cluster_data['Trump Votes Weighted'].sum() else 'Trump'

            # Update counters for clusters won by Biden and Trump in this file
            if cluster_winner == 'Biden':
                biden_wins_file += 1
            else:
                trump_wins_file += 1

        # Update total counters
        biden_wins.append(biden_wins_file)
        trump_wins.append(trump_wins_file)
    return biden_wins,trump_wins
#%%
def plot_distribution(data):
    plt.hist(data, bins=4, alpha=0.7, color='blue', edgecolor='black')
    plt.title('Distribution of Numbers')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
#%%
# Call the function
biden_wins, trump_wins = analyze_clusters()
# %%
plot_distribution(biden_wins)
# %%
plot_distribution(trump_wins)
# %%
