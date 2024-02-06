#%%
import pandas as pd
import math
import numpy as np 
from pathlib import Path
import glob
#%%
data_path = Path("raw-results")
cluster_path = Path("cluster-populations")
#%%
Blocks = pd.read_csv("Blocks.csv")
County_Results_2020 = pd.read_csv("2020-County-Results.csv")
#%%
# Create the output folder if it doesn't exist
output_folder = Path("analyzed_results")
output_folder.mkdir(exist_ok=True)

# Get a list of all CSV files in the data path
csv_files = glob.glob(str(data_path / '*.csv'))

# Iterate through each CSV file
for csv_file in csv_files:
    # Read the CSV file into a DataFrame
    Cluster_Results = pd.read_csv(csv_file)

    # Merge with 'Blocks' DataFrame
    merged_df = pd.merge(Cluster_Results, Blocks, on=["Latitude", "Longitude"])

    # Merge with 'County_Results_2020' DataFrame
    merged_df = pd.merge(merged_df, County_Results_2020, on="County")

    # Calculate weighted votes
    merged_df['Biden Votes Weighted'] = merged_df['Population'] * merged_df['Biden Votes per Capita']
    merged_df['Trump Votes Weighted'] = merged_df['Population'] * merged_df['Trump Votes per Capita']

    # Sum the weighted votes based on the 'Cluster' column
    result_sum = merged_df.groupby('Cluster')[['Biden Votes Weighted', 'Trump Votes Weighted']].sum().reset_index()

    # Sum the cluster populations and save them to the county-population folder
    cluster_populations = merged_df.groupby('Cluster')['Population'].sum().reset_index()
    cluster_filename = cluster_path / f"population_{Path(csv_file).stem}.csv"
    cluster_populations.to_csv(cluster_filename,index = False)
    # Create the output filename with "analyzed_" prefix
    output_filename = output_folder / f"analyzed_{Path(csv_file).stem}.csv"

    # Save the result to the output folder
    result_sum.to_csv(output_filename, index=False)

    print(f"Analysis completed for {csv_file}. Results saved to {output_filename}")
# %%
