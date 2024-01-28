#%%
import numpy as np
from scipy.spatial.distance import cdist
import pandas as pd
#%%
centroids = np.array([[1,1],
               [1,2],
               [2,2],
               [3,2]])

point = np.array([[1.5, 1.5],
                  [2.0, 2.0]])
# %%
cdist(point,centroids,'euclidean')
# %%
Blocks = pd.read_csv("Blocks.csv", index_col="GEOID")
my_data = Blocks[["Longitude","Latitude"]].to_numpy()
#%%
test = cdist(my_data,centroids,'euclidean')
# %%
# Example 2D numpy array
array_2d = np.array([[1, 5, 3],
                     [4, 2, 9],
                     [7, 8, 6]])

# Get the indices of the minimum values in each row
min_indices_per_row = np.argmin(array_2d, axis=1)

print("Indices of minimum values in each row:", min_indices_per_row)

# %%
min_indices_per_row = np.argmin(array_2d, axis=1)

print("Indices of minimum values in each row:", min_indices_per_row)
# %%
# Example 2D numpy array (matrix)
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Example numpy array with the same length as the rows of the matrix
array2 = np.array([2, 3, 4])

# Perform element-wise multiplication using broadcasting
result = np.multiply(matrix, array2[:, np.newaxis])

print("Result of element-wise multiplication with broadcasting:")
print(result)
# %%
arr = np.array([1, 2, 3, 1, 2, 1, 3, 4, 5, 4])

# Use numpy.unique to get unique values and their counts
unique_values, counts = np.unique(arr, return_counts=True)

# Print the results
for value, count in zip(unique_values, counts):
    print(f"{value}: {count} times")
# %%

# Example NumPy array containing a list of indices
numpy_array = np.array([0, 4, 2, 3,4])

# Example list containing data points
data_points = [10, 20, 30, 40, 50]

result_list = [[] for i in range(len(data_points))]
for i in range(len(numpy_array)):
    result_list[numpy_array[i]].append(data_points[i])
# %%
result_list = np.empty(max(numpy_array) + 1, dtype=object)
result_list[:] = [[] for _ in range(len(result_list))]
result_list[numpy_array].append([data_point for data_point in data_points])
# %%
