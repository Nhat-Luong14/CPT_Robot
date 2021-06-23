import numpy as np
import matplotlib.pyplot as plt
from tests.test_infotaxis import show_infotaxis_demo

for i in range(8,30):
    result = show_infotaxis_demo(seed=i)
    if result is True:
        break
plt.show()