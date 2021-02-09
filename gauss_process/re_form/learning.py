import pandas as pd
import numpy as np
from sklearn.gaussian_process.kernels import RBF, WhiteKernel
from sklearn.gaussian_process import GaussianProcessRegressor
import config
from joblib import dump, load

def get_gp_model(training_input, training_output_x, training_output_y, gen_new):
    if gen_new is True:
        kernel = RBF(length_scale=.5) + WhiteKernel()
        Mx = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
        My = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
        Mx = Mx.fit(training_input, training_output_x)
        My = My.fit(training_input, training_output_y)
        dump(Mx, 'data/Mx.joblib') 
        dump(My, 'data/My.joblib') 
    else:
        Mx = load('Mx.joblib') 
        My = load('My.joblib') 

    kkk = Mx.log_marginal_likelihood()
    kkkk = My.log_marginal_likelihood()
    params_x = Mx.kernel_.get_params()
    params_y = My.kernel_.get_params()
    # print(kkk)
    # print(kkkk)
    # print(params_x)
    # print(params_y)

    # with open('param.txt', 'w') as f:
    #     print('Mx : log_marginal_likelihood', file=f)
    #     print(kkk,params_x, file=f)
    #     print('My : log_marginal_likelihood', file=f)
    #     print(kkkk,params_y, file=f)
    # print('bujide')
    return Mx,My


# Study_output:displacement of position (4step - 1step)
# Study_input:current voltage, voltage after 1,2,3 step
# The voltage values are estimated from the gas distribution map using Gauss Process
def training(gen_new):
    file_name = config.data_file_name
    data = pd.read_csv(file_name)
    delta_x = np.array(data["delta_x"][:config.data_len])
    delta_y = np.array(data["delta_y"][:config.data_len])
    vol_0 = data["step_0_voltage"][:config.data_len]
    vol_1 = data["step_1_voltage"][:config.data_len]
    vol_2 = data["step_2_voltage"][:config.data_len]
    vol_3 = data["step_3_voltage"][:config.data_len]

    training_input = np.array([vol_0, vol_1, vol_2, vol_3]).transpose()
    training_output_x = delta_x.reshape(config.data_len,1)
    training_output_y = delta_y.reshape(config.data_len,1)
    # print('bujidesu')
    Mx, My = get_gp_model(training_input, training_output_x, training_output_y, gen_new=gen_new)
    return Mx, My
