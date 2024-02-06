#%%
from __future__ import division, print_function
from datetime import datetime
import numpy as np
import wkmeans as wkm
import pandas as pd
import math
import os
from tqdm import tqdm
from wkmeans import NonConvergenceError

# Load Data
Blocks = pd.read_csv("Blocks.csv", index_col="GEOID")
my_data = Blocks[["Longitude", "Latitude"]].to_numpy()
my_counts = Blocks["Population"].to_numpy()
# Functions
def run_until_100_successful_results(data, weights, max_results=1000):
    result_count = 0
    total_attempts = 0  # New counter for total attempts
    current_run_attempts = 0
    accept_ratio = 1.01
    successful_results = []

    results_folder = "raw-results"
    non_convergence_folder = "non-convergence-results"
    centroids_folder = "cluster-centroids"

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    if not os.path.exists(non_convergence_folder):
        os.makedirs(non_convergence_folder)

    with tqdm(total=max_results, desc="Runs", unit="run") as pbar:
        while result_count < max_results:
            total_attempts += 1  # Increment total attempts
            current_run_attempts += 1
            if current_run_attempts == 1:
                a, b = 3.0, 0.7
            try:
                wkmeans = wkm.KPlusPlus(14, X=data, c=weights, alpha=a, beta=b)
                wkmeans.init_centers()
                wkmeans.find_centers(method='++')

                # Save successful alpha and beta values
                successful_results.append({'Alpha': a, 'Beta': b})

                # Save cluster information to CSV
                points_clusters = []
                points_latitude = []
                points_longitude = []

                for i, cluster in enumerate(wkmeans.clusters):
                    for point in cluster:
                        points_clusters.append(i)
                        points_longitude.append(point[0])
                        points_latitude.append(point[1])
                
                cluster_latitude = []
                cluster_longitude = []

                for i in wkmeans.mu:
                    cluster_longitude.append(i[0])
                    cluster_latitude.append(i[1])

                df_combined = pd.DataFrame({'Cluster': points_clusters,
                                            'Latitude': points_latitude,
                                            'Longitude': points_longitude})
                
                df_cluster_centroids = pd.DataFrame({'Latitude' : cluster_latitude, 'Longitude': cluster_longitude})
                
                result_filename = os.path.join(results_folder, f'result_{result_count + 1}_a_{a}_b_{b}_accept_{accept_ratio}.csv')
                centroid_filename = os.path.join(centroids_folder, f'result_{result_count + 1}_a_{a}_b_{b}_accept_{accept_ratio}.csv')


                df_combined.to_csv(result_filename, index=False)
                df_cluster_centroids.to_csv(centroid_filename, index=False)


                result_count += 1
                pbar.update(1)
            except ValueError as ve:
                # Handle convergence issues or exceptions
                print(f"Run {result_count + 1} (Attempt {total_attempts}): lost districts. Trying again.")
                if math.isclose(b + 0.1, 1.0):
                    a += 0.1
                    b = 0.5
                else:
                    b += 0.1
            except NonConvergenceError:
                print(f"Run {result_count + 1} (Attempt {total_attempts}): run did not converge. Trying again.")
                if math.isclose(b + 0.1, 1.0):
                    a += 0.1
                    b = 0.5
                else:
                    b += 0.1
                # Save non-convergent cluster information to CSV
                clusters = []
                latitude = []
                longitude = []

                for i, cluster in enumerate(wkmeans.clusters):
                    for point in cluster:
                        clusters.append(i)
                        longitude.append(point[0])
                        latitude.append(point[1])

                df_combined = pd.DataFrame({'cluster': clusters,
                                            'latitude': latitude,
                                            'longitude': longitude})
                
                non_convergence_filename = os.path.join(non_convergence_folder, f'non_convergence_result_{result_count + 1}_attempt_{total_attempts}_a_{a}_b{b}.csv')
                pd.DataFrame(df_combined).to_csv(non_convergence_filename, index=False)

    # # Save successful alpha and beta values to a CSV file
    # successful_filename = os.path.join(results_folder, 'successful_runs_temp.csv')
    # pd.DataFrame(successful_results).to_csv(successful_filename, index=False)
    current_run_attempts = 0

    print(f"\nGenerated {result_count} successful results out of {total_attempts} total attempts.")

# Run Example
run_until_100_successful_results(my_data, my_counts)

# %%
