import csv
import numpy as np
import pandas as pd

FILE_NAME = "spambase.data"

# load with csv file
with open(FILE_NAME, 'r') as f:
    data = list(csv.reader(f, delimiter=','))
data = np.array(data, dtype=np.float32)
print(data.shape)

# load with np.loadtxt()
data = np.loadtxt(FILE_NAME, delimiter=',', dtype=np.float32)
print(data.shape, data.dtype)

# load from np.genfromtxt()
data = np.genfromtxt(FILE_NAME, delimiter=',', dtype=np.float32)
print(data.shape)

n_samples, n_features = data.shape
n_features -= 1
X = data[:, 0:n_features]
y = data[:, n_features]
print(X.shape, y.shape)
print(X[0,0:5])

