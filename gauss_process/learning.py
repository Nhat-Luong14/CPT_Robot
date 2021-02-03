# Learning process
import pandas as pd
import numpy as np
from sklearn.gaussian_process import kernels as sk_kern
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import train_test_split
import time
import matplotlib.pyplot as plt 
import seaborn as sns
from util import plot_gp

start_t = time.time()

file_name = 'data/Study_gaussian_new_new_simple.csv'
data = pd.read_csv(file_name)

# Study_output:displacement of position (4step - 1step)
delta_x = np.array(data["delta_x"])
delta_y = np.array(data["delta_y"])
training_output_x = delta_x.reshape(len(data),1)
training_output_y = delta_y.reshape(len(data),1)

# study_input:current voltage, voltage after 1,2,3 step
# the voltage values are estimated from the gas distribution map using Gauss Process
vol_0 = data["step_0_voltage"]
vol_1 = data["step_1_voltage"]
vol_2 = data["step_2_voltage"]
vol_3 = data["step_3_voltage"]
#training_input = np.array([vol_0, vol_1, vol_2, vol_3]).T
training_input = np.array([vol_0]).T

# Split sample set into test set and training set
# I stand for Input, o stand for output. 
# Capital I means this is a high dimensional input
# 4D input and 1D output
Ix_train, Ix_test, ox_train, ox_test = train_test_split(training_input, training_output_x, 
    random_state=0, test_size=0.46)
Iy_train, Iy_test, oy_train, oy_test = train_test_split(training_input, training_output_y, 
    random_state=0, test_size=0.55)

Ix_train = np.array([0,2,4,6],).reshape(-1,1)
ox_train = np.array([0,4,16,36]).reshape(-1,1)
Ix_test = np.array([0,1,2,3,6]).reshape(-1,1)
ox_test = np.array([0,1,5,8,46]).reshape(-1,1)

#gaussianのモデル作成
# kernel = sk_kern.RBF(length_scale=1) + sk_kern.WhiteKernel()
kernel = sk_kern.RBF(length_scale=1) + sk_kern.WhiteKernel()
# #alphaは発散しないように対角行列に加える値
# Mx = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", 
#     n_restarts_optimizer = 100, normalize_y=False)
# My = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", 
#     n_restarts_optimizer = 100, normalize_y=True)

Mx = GaussianProcessRegressor(kernel=kernel, normalize_y=True)
# My = GaussianProcessRegressor(kernel=kernel, normalize_y=False)

Mx.fit(Ix_train, ox_train)
# My.fit(Iy_train, oy_train)

# Compute posterior mean and covariance
# mu_s, cov_s = My.predict(Iy_test, return_cov=True)
mu_s, cov_s = Mx.predict(Ix_test, return_cov=True)
print(mu_s.shape)
print(cov_s.shape)




print("Training set score: {:.2f}".format(Mx.score(Ix_train, ox_train)))
print("Test set score: {:.2f}".format(Mx.score(Ix_test, ox_test)))

# print("Training set score: {:.2f}".format(My.score(Iy_train, oy_train)))
# print("Test set score: {:.2f}".format(My.score(Iy_test, oy_test)))


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
# plot_gp(mu_s, cov_s, Iy_test, X_train=Iy_train, Y_train=oy_train)
plot_gp(mu_s, cov_s, Ix_test, X_train=Ix_train, Y_train=ox_train)

plt.figure(figsize=(10,10))
sns.set(font_scale=1.5)
hm = sns.heatmap(cov_s, cbar=True, square=True, annot=True)
plt.title('Covariance matrix showing correlation coefficients')
plt.tight_layout()
plt.show()

end_t = time.time()
print((end_t-start_t)/60)