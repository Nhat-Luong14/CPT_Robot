import math
import numpy
import config
import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd
import sys

# Indicates the likelihood that the measurement represents the concentration at
# a given distance from the point of measurement.
# The readings were convolved using the two dimensional normalised Gaussian.
# [Paper: Gas source localisation by constructing concentration gridmaps 
# with a mobile robot] (equation 1)
def weight_cal(displacement):
    x = displacement[0]
    y = displacement[1]
    sigma = config.sigma
    exp_term =  math.exp(-0.5*(x*x + y*y)/(sigma*sigma))
    weight = (0.5*exp_term)/(math.pi*sigma*sigma)
    return weight 

def displacement_cal(point1_x, point1_y, point2_x, point2_y):
    displacement = (point2_x-point1_x, point2_y-point1_y)
    return displacement

def check_weight(displacement):
    sum = displacement[0]**2 + displacement[1]**2
    if math.sqrt(sum) <= config.cutoff_radius:
        return weight_cal(displacement)
    else:
        return 0

def plot_heat_map():
    sns.set_theme()
    data = pd.read_csv('new_data.csv')
    data = data.pivot("y(mm)", "x(mm)", "sensor_value")
    ax = sns.heatmap(data, vmin=0, vmax=1)
    plt.show()

if __name__ == '__main__':
    plot_heat_map()