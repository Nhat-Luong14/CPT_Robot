# Learning process
# from util import plot_gp

import pandas as pd
import numpy as np
from sklearn.gaussian_process.kernels import ConstantKernel, RBF, WhiteKernel
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt 
import seaborn as sns

def plot_covriance_matrix(cov_matrix):
    plt.figure(figsize=(10,10))
    sns.set(font_scale=1.5)
    hm = sns.heatmap(cov_matrix, cbar=True, square=True, annot=True)
    plt.title('Covariance matrix showing correlation coefficients')
    plt.tight_layout()
    plt.show()

def define_kernel():
    l = 1.0
    sigma_f = 1.0
    kernel = ConstantKernel(constant_value=sigma_f,constant_value_bounds=(1e-5, 1e5)) \
            * RBF(length_scale=l, length_scale_bounds=(1e-5, 1e5))
    return kernel

def get_gp_model(kernel, sigma_n):
    kernel = RBF(length_scale=.5) + WhiteKernel()
    Mx = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
    My = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
    return Mx,My

def plot_gp_model(x, f_x, x_star, y_pred):
    
    x = [item for sublist in x for item in sublist]
    f_x = [item for sublist in f_x for item in sublist]
    x_star = [item for sublist in x_star for item in sublist]
    y_pred = [item for sublist in y_pred for item in sublist]
    fig, ax = plt.subplots()
    # Plot "true" linear fit.
    sns.lineplot(x=x, y=f_x, color='red', label='f(x)', ax=ax, marker="o")
    # Plot prediction. 
    sns.lineplot(x=x_star, y=y_pred, color='green', label='pred', ax=ax, marker="o")
    ax.set(title='Prediction GaussianProcessRegressor')
    ax.legend(loc='upper right')
    plt.show()





if __name__ == "__main__":
    file_name = 'data/Study_gaussian_new_new.csv'
    data = pd.read_csv(file_name)
    DATA_LEN = 4000
    # Study_output:displacement of position (4step - 1step)
    # Study_input:current voltage, voltage after 1,2,3 step
    # The voltage values are estimated from the gas distribution map using Gauss Process
    delta_x = np.array(data["delta_x"][:DATA_LEN])
    delta_y = np.array(data["delta_y"][:DATA_LEN])

    vol_0 = data["step_0_voltage"][:DATA_LEN]
    vol_1 = data["step_1_voltage"][:DATA_LEN]
    vol_2 = data["step_2_voltage"][:DATA_LEN]
    vol_3 = data["step_3_voltage"][:DATA_LEN]

    training_input = np.array([vol_0, vol_1, vol_2, vol_3]).transpose()
    training_output_x = delta_x.reshape(DATA_LEN,1)
    training_output_y = delta_y.reshape(DATA_LEN,1)

    # Split sample set into test set and training set
    # I stand for Input, o stand for output. Capital I means this is a high dimensional input
    Ix_train, Ix_test, ox_train, ox_test = train_test_split(training_input, training_output_x, 
        random_state=12, test_size=0.25)
    Iy_train, Iy_test, oy_train, oy_test = train_test_split(training_input, training_output_y, 
        random_state=12, test_size=0.25)

    kernel = RBF(length_scale=.5) + WhiteKernel(noise_level_bounds=(1e-20, 1e20))
    Mx = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
    My = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
    Mx.fit(Ix_train, ox_train)
    My.fit(Iy_train, oy_train)

    # # Compute posterior mean and covariance
    # mu_x, cov_x = My.predict(Iy_test, return_cov=True)
    # mu_y, cov_y = Mx.predict(Ix_test, return_cov=True)
    # print(mu_s.shape)
    # print(cov_s.shape)

    delta_x_pred = Mx.predict(Ix_test)
    delta_y_pred = My.predict(Ix_test)

    print("Training set score: {:.2f}".format(Mx.score(Ix_train, ox_train)))
    print("Test set score: {:.2f}".format(Mx.score(Ix_test, ox_test)))

    print("Training set score: {:.2f}".format(My.score(Iy_train, oy_train)))
    print("Test set score: {:.2f}".format(My.score(Iy_test, oy_test)))

    # plot_gp_model(Ix_test, ox_test, Ix_test, y_pred)
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