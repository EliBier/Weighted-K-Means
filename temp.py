#%%
from pathlib import Path
import pandas as pd
import glob
import matplotlib.pyplot as plt
#%%
DISTRICT_COLORS = {
    -1: "#000000",
    0: "#e6194B",
    1: "#3cb44b",
    2: "#ffe119",
    3: "#4363d8",
    4: "#f58231",
    5: "#911eb4",
    6: "#42d4f4",
    7: "#f032e6",
    8: "#bfef45",
    9: "#fabed4",
    10: "#469990",
    11: "#dcbeff",
    12: "#9A6324",
    13: "#fffac8",
}
#%%
Blocks = pd.read_csv("raw-results/result_1_a_3.0_b_0.7_accept_1.01_temp.csv")
Blocks2 = pd.read_csv("raw-results/result_1136_a_3.1_b_0.7_accept_1.01.csv")
#%%
def plot_blocks_clusters_no_pop(Blocks):
    # Scatter plot of latitude and longitude colored by clusters using DISTRICT_COLORS
    plt.figure(figsize=(16, 8))
    total_points = Blocks.groupby("Cluster").size().sum()

    for cluster in set(Blocks["Cluster"]):
        cluster_data = Blocks[Blocks["Cluster"] == cluster]
        color = DISTRICT_COLORS.get(
            cluster, "#808080"
        )  # Default to gray if color not defined
        plt.scatter(
            cluster_data["Longitude"],
            cluster_data["Latitude"],
            label=f"Cluster {cluster}",
            c=color,
            s=0.1
        )

    # Set labels and title
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("K-Means Clustering of Blocks")
    plt.legend()
    plt.show()
# %%
plot_blocks_clusters_no_pop(Blocks)
# %%
plot_blocks_clusters_no_pop(Blocks2)
# %%
