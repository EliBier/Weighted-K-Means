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
def run_until_100_successful_results(data, weights, max_results=10):
    result_count = 0
    total_attempts = 0  # New counter for total attempts
    successful_results = []

    results_folder = "results"
    non_convergence_folder = "non-convergence-results"

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    if not os.path.exists(non_convergence_folder):
        os.makedirs(non_convergence_folder)

    with tqdm(total=max_results, desc="Runs", unit="run") as pbar:
        while result_count < max_results:
            total_attempts += 1  # Increment total attempts

            try:
                # Use current alpha and beta for the run
                alpha, beta = 3.0, 0.5

                wkmeans = wkm.KPlusPlus(14, X=data, c=weights, alpha=alpha, beta=beta)
                wkmeans.init_centers()
                wkmeans.find_centers(method='++')

                # Save successful alpha and beta values
                successful_results.append({'Alpha': alpha, 'Beta': beta})

                # Save cluster information to CSV
                result_filename = os.path.join(results_folder, f'result_{result_count + 1}.csv')
                pd.DataFrame(wkmeans.clusters).to_csv(result_filename, index=False)

                result_count += 1
                pbar.update(1)
            except ValueError as ve:
                # Handle convergence issues or exceptions
                print(f"Run {result_count + 1} (Attempt {total_attempts}): lost districts. Trying again.")
                if math.isclose(beta + 0.1, 1.0):
                    alpha += 0.1
                    beta = 0.5
                else:
                    beta += 0.1
            except NonConvergenceError:
                print(f"Run {result_count + 1} (Attempt {total_attempts}): run did not converge. Trying again.")
                if math.isclose(beta + 0.1, 1.0):
                    alpha += 0.1
                    beta = 0.5
                else:
                    beta += 0.1

                # Save non-convergent cluster information to CSV
                non_convergence_filename = os.path.join(non_convergence_folder, f'non_convergence_result_{result_count + 1}.csv')
                pd.DataFrame(wkmeans.clusters).to_csv(non_convergence_filename, index=False)

    # Save successful alpha and beta values to a CSV file
    successful_filename = os.path.join(results_folder, 'successful_runs.csv')
    pd.DataFrame(successful_results).to_csv(successful_filename, index=False)

    print(f"\nGenerated {result_count} successful results out of {total_attempts} total attempts.")

# Run Example
run_until_100_successful_results(my_data, my_counts)
