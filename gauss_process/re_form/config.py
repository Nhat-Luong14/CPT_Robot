<<<<<<< HEAD
import pandas as pd
import numpy as np

server_ip       = "192.168.1.31"
server_port     = 10002

data = pd.read_csv("data/ex6.csv")
data_len = len(np.array(data["delta_x"]))
print(data_len)

# data_len        = 600
data_file_name  = "data/Study_gaussian_new_new.csv"
=======
server_ip       = "192.168.2.214"
server_port     = 10002
data_len        = 7000
data_file_name  = "data/Study_gaussian_new_new.csv"
>>>>>>> 55d64d9cc63b93dd1b2e70f2eeddbd6573f659e4
