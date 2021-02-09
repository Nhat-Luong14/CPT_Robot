import pandas as pd
import numpy as np
from sklearn.gaussian_process.kernels import ConstantKernel, RBF, WhiteKernel
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt 
import seaborn as sns
from joblib import dump, load
import config
import time

def plot_covriance_matrix(cov_matrix):
    plt.figure(figsize=(10,10))
    sns.set(font_scale=1.5)
    hm = sns.heatmap(cov_matrix, cbar=True, square=True, annot=True)
    plt.title('Covariance matrix showing correlation coefficients')
    plt.tight_layout()
    plt.show()


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
    return Mx, My


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


def validating(gen_new):
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

    # Split sample set into test set and training set
    # I stand for Input, o stand for output. Capital I means this is a high dimensional input
    Ix_train, Ix_test, ox_train, ox_test = train_test_split(training_input, training_output_x, 
        random_state=12, test_size=0.25)
    Iy_train, Iy_test, oy_train, oy_test = train_test_split(training_input, training_output_y, 
        random_state=12, test_size=0.25)

    Mx, My = get_gp_model(Ix_train, ox_train, oy_train, gen_new=gen_new)
    return Mx, My, Ix_test, Iy_test, ox_test, oy_test, Ix_train, Iy_train, ox_train, oy_train


def rmsd(var1, var2):
    sum = 0
    for i in range(len(var1)):
        temp = var1[i][0] - var2[i][0]
        sum += temp**2
    return sum/len(var1)


if __name__ == "__main__":
    start = time.time()
    Mx, My, Ix_test, Iy_test, ox_test, oy_test, Ix_train, Iy_train, ox_train, oy_train = validating(gen_new=True)
    # # Compute posterior mean and covariance
    # mu_x, cov_x = My.predict(Iy_test, return_cov=True)
    # mu_y, cov_y = Mx.predict(Ix_test, return_cov=True)
    # print(mu_s.shape)
    # print(cov_s.shape)

    delta_x_pred = Mx.predict(Ix_test)
    delta_y_pred = My.predict(Ix_test)

    result1 = rmsd(Mx.predict(Ix_train), ox_train)
    result2 = rmsd(Mx.predict(Ix_test), ox_test)
    result3 = rmsd(My.predict(Iy_train), oy_train)
    result4 = rmsd(My.predict(Iy_test), oy_test)

    print("Training set X score:", result1)
    print("Test set X score:", result2)
    print("Training set Y score:", result3)
    print("Test set Y score:", result4)
    print("Running time is:", (time.time() - start)/60)