# Import necessary modules
import subprocess

# List of Python script files to run
script_files = ["generate_results.py", "analyze_results.py", "final_results.py", "population_average.py", "cluster_centroids_graph.py"]

# Function to run each script
def run_script(script):
    subprocess.run(["python", script])

# Run scripts in series
for script in script_files:
    run_script(script)