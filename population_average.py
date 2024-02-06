#%%
import os
import pandas as pd
import matplotlib.pyplot as plt
#%%
folder_path = "cluster-populations"
#%%
def calculate_average_deviation(csv_path):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_path)
    
    # Calculate the mean of the 'Population' column
    mean_population = df['Population'].mean()
    
    # Calculate the absolute deviation of each population from the mean
    deviations = abs(df['Population'] - mean_population)
    
    # Calculate the average deviation
    average_deviation = deviations.mean()
    
    return average_deviation
#%%
def process_folder(folder_path):
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    # Accumulate deviations across all files
    all_deviations = []
    
    for csv_file in csv_files:
        # Construct the full path to the CSV file
        csv_path = os.path.join(folder_path, csv_file)
        
        # Calculate average deviation and append to the list
        avg_deviation = calculate_average_deviation(csv_path)
        all_deviations.append(avg_deviation)
        
        # Print individual results
        print(f"CSV file: {csv_file}, Average Deviation: {avg_deviation}")
    
    # Calculate the average deviation across all files
    average_deviation_across_all = sum(all_deviations) / len(all_deviations) if all_deviations else 0
    
    # Print the result
    print(f"Average Deviation Across All CSVs: {average_deviation_across_all}")
    
    # Plot histogram
    plt.hist(all_deviations, bins=20, color='blue', edgecolor='black')
    plt.title('Histogram of Average Deviations')
    plt.xlabel('Average Deviation')
    plt.ylabel('Frequency')
    plt.show()

#%%
# Process the folder and generate histogram
process_folder(folder_path)
# %%
