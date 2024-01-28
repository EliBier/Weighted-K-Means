#%%
from __future__ import division, print_function
from datetime import datetime
import numpy as np
import wkmeans as wkm
import pandas as pd
import math
import cProfile
import pstats
import random
#%%
Blocks = pd.read_csv("Blocks.csv", index_col="GEOID")
my_data = Blocks[["Longitude","Latitude"]].to_numpy()
my_counts = Blocks["Population"].to_numpy()
#%%
def iterative_run(num_clusters,data,weights,a=3,b=0.5):
    profiler = cProfile.Profile()
    profiler.enable()
    startTime = datetime.now()
    while True:
        print("Current alpha:", a)
        print("Current beta", b)
        try:
            # If you have your own data use:
            wkmeans = wkm.KPlusPlus(num_clusters, X=data, c=weights, alpha=a, beta=b)

            # Initialise centroids using k-means++...
            wkmeans.init_centers()
            # and run to find clusters:
            wkmeans.find_centers(method='++')

            # Break out of the loop if successful
            break

        except ValueError as ve:
            # Catching ValueError and applying the specified conditions
            if math.isclose(b + 0.1, 1.0):
                a += 0.1
                b = 0.5
            else:
                b += 0.1
            print("alpha:",a)
            print("beta:",b)

    # Now plot the result:
    wkmeans.plot_clusters(wkmeans.plot_clusters.calls)

    profiler.disable()
    profiler.print_stats(sort='cumulative')

    # We're done so print some useful info:
    print('The End!')
    print('\tRun time: ', datetime.now() - startTime)
    print('\tTotal runs: ', wkmeans._cluster_points.calls)
    print('\tNumber of unique items per cluster: ', [len(x) for x in wkmeans.clusters])
    print('\tNumber of items per cluster: ', wkmeans.counts_per_cluster)
# %%
def single_run(num_clusters,data,weights,a=3,b=0.5):
    profiler = cProfile.Profile()
    profiler.enable()
    startTime = datetime.now()
    try:
        # If you have your own data use:
        wkmeans = wkm.KPlusPlus(num_clusters, X=data, c=weights, alpha=a, beta=b)

        # Initialise centroids using k-means++...
        wkmeans.init_centers()
        # and run to find clusters:
        wkmeans.find_centers(method='++')
    
        # Now plot the result:
        wkmeans.plot_clusters(wkmeans.plot_clusters.calls)
    except ValueError as ve:
        t=1
    finally:
        profiler.disable()
        profiler.print_stats(sort='cumulative')

        # We're done so print some useful info:
        print('The End!')
        print('\tRun time: ', datetime.now() - startTime)
        print('\tTotal runs: ', wkmeans._cluster_points.calls)
        print('\tNumber of unique items per cluster: ', [len(x) for x in wkmeans.clusters])
        print('\tNumber of items per cluster: ', wkmeans.counts_per_cluster)
# %%
single_run(14,my_data,my_counts, a=3.1, b=0.5)
# %%
