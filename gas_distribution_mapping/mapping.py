import math
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
    weight = (0.5*exp_term)*1000000/(math.pi*sigma*sigma)
    return weight 


# Calculate the weigth of the measurment point to neighbor cells
def check_weight(displacement):
    sum = displacement[0]**2 + displacement[1]**2
    if math.sqrt(sum) <= config.cutoff_radius:
        return weight_cal(displacement)
    else:
        return 0


# Plot Gas Distribution mapping
def plot_heat_map(csv_name):
    sns.set_theme()
    data = pd.read_csv(csv_name)
    data = data.pivot("y", "x", "sensor_value")
    ax = sns.heatmap(data, vmin=0, vmax=1)
    plt.show()


# Update value of cell reading using extrapolate
def update_cell(data, grid_data):
    grid_data['acc_weight'] = 0.0
    grid_data['acc_weight_reading'] = 0.0     
    # Adding accumulated weight and accumulated reading
    for i in range(len(data.index)):
        for j in range(len(grid_data.index)):
            measure_x = data.at[i,'x']
            measure_y = data.at[i,'y']
            neighbor_x = grid_data.at[j,'x']
            neighbor_y = grid_data.at[j,'y']
            displacement = (measure_x-neighbor_x, measure_y-neighbor_y)
            weight = check_weight(displacement)
            grid_data.at[j,'acc_weight'] += weight
            grid_data.at[j,'acc_weight_reading'] += data.at[i,'sensor_value']*weight

    for j in range(len(grid_data.index)):
        acc_weight = grid_data.at[j,'acc_weight']
        acc_reading = grid_data.at[j,'acc_weight_reading']

        if(acc_weight != 0):
            grid_data.at[j,'sensor_value'] = acc_reading/acc_weight
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    grid_data.to_csv('output.csv', index=False)
    