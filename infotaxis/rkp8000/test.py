import numpy as np

arr1 = np.array([
    [True, True, True],
    [True, True, True],
    [True, False, False],
    [False, False, False]])


arr2 = np.array([
    [60, 77, 88],
    [23, 35, 48],
    [33, 44, 55],
    [99, 9, 202]])

b = np.ma.MaskedArray(arr2, arr1)
print(np.ma.argmin(b))