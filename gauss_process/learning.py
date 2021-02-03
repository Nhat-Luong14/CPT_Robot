# Learning process
import pandas as pd
import numpy as np
from sklearn.gaussian_process import kernels as sk_kern
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import train_test_split
import time

start_t = time.time()

file_name = 'data/Study_gaussian_new_new_simple.csv'
data = pd.read_csv(file_name)

#study_output:displacement of position (4step - 1step)
study_delta_x = np.array(data["delta_x"])
study_delta_y = np.array(data["delta_y"])

# study_input:current voltage, voltage after 1,2,3 step
study_conc1 = data["estimated_voltage"]
study_conc2 = data["step_1_voltage"]
study_conc3 = data["step_2_voltage"]
study_conc4 = data["step_3_voltage"]

# #四次元入力、一次元出力_study用
study_input_list = np.array([study_conc1, study_conc2, study_conc3, study_conc4]).T
study_output_list_x = study_delta_x.reshape(len(data),1)
study_output_list_y = study_delta_y.reshape(len(data),1)

print('Bujidesu')

Ix_train, Ix_test, ox_train, ox_test = train_test_split(study_input_list, study_output_list_x, random_state=0)
Iy_train, Iy_test, oy_train, oy_test = train_test_split(study_input_list, study_output_list_y, random_state=0)

#gaussianのモデル作成
kernel = sk_kern.RBF(length_scale=.5) + sk_kern.WhiteKernel()
# #alphaは発散しないように対角行列に加える値
Mx = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
My = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)

Mx.fit(Ix_train, ox_train)
My.fit(Iy_train, oy_train)

print("Training set score: {:.2f}".format(Mx.score(Ix_train, ox_train)))
print("Test set score: {:.2f}".format(Mx.score(Ix_test, ox_test)))

print("Training set score: {:.2f}".format(My.score(Iy_train, oy_train)))
print("Test set score: {:.2f}".format(My.score(Iy_test, oy_test)))


# kkk = Mx.log_marginal_likelihood()
# kkkk = My.log_marginal_likelihood()
# params_x = Mx.kernel_.get_params()
# params_y = My.kernel_.get_params()

# with open('param.txt', 'w') as f:
# 	print('Mx : log_marginal_likelihood', file=f)
# 	print(kkk,params_x, file=f)
# 	print('My : log_marginal_likelihood', file=f)
# 	print(kkkk,params_y, file=f)
# #-------------------------------------------------------------------

# print('bujide')


end_t = time.time()
print((end_t-start_t)/60)