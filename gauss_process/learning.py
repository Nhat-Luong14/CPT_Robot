# Learning process
import pandas as pd
import numpy as np
from sklearn.gaussian_process import kernels as sk_kern

file_name = 'okajima_original/Study_gaussian_new_new_try.csv'
csv_input = pd.read_csv(file_name)

#study_output:displacement of position (4step - 1step)
study_delta_x = np.array(csv_input["x"])
study_delta_y = np.array(csv_input["y"])

# study_input:current voltage, voltage after 1,2,3 step
study_conc1 = csv_input["current_voltage"]
study_conc2 = csv_input["step_1_voltage"]
study_conc3 = csv_input["step_2_voltage"]
study_conc4 = csv_input["step_3_voltage"]

# #四次元入力、一次元出力_study用
study_input_list = np.array([study_conc1, study_conc2, study_conc3, study_conc4]).T
study_output_list_x = study_delta_x.reshape(len(csv_input),1)
study_output_list_y = study_delta_y.reshape(len(csv_input),1)

print('Bujidesu')

#gaussianのモデル作成
kernel = sk_kern.RBF(length_scale=.5) + sk_kern.WhiteKernel()
# #alphaは発散しないように対角行列に加える値
# Mx = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
# My = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
# Mx.fit(study_input_list, study_output_list_x)
# My.fit(study_input_list, study_output_list_y)
# kkk = Mx.log_marginal_likelihood()
# kkkk = My.log_marginal_likelihood()
# params_x = Mx.kernel_.get_params()
# params_y = My.kernel_.get_params()
# print(kkk)
# print(kkkk)
# print(params_x)
# print(params_y)

# with open('param.txt', 'w') as f:
# 	print('Mx : log_marginal_likelihood', file=f)
# 	print(kkk,params_x, file=f)
# 	print('My : log_marginal_likelihood', file=f)
# 	print(kkkk,params_y, file=f)
# #-------------------------------------------------------------------

# print('bujide')