import math
import config
import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd

# Indicates the likelihood that the measurement represents the concentration at
# a given distance from the point of measurement.
# The readings were convolved using the two dimensional normalised Gaussian.
# [Paper: Gas source localisation by constructing concentration gridmaps 
# with a mobile robot] (equation 1)
def weight_cal(distance):
    sigma = config.sigma
    exp_term =  math.exp(-0.5*distance*distance/(sigma*sigma))
    weight = (0.5*exp_term)/(math.pi*sigma*sigma)
    return weight 


# calculate the distance between the measument point and a cell
def cal_distance(x1,x2,y1,y2):
    distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return distance


# build the confidence map
def confidence_map(data):
    data['confidence'] = 0.0
    scaling_param = weight_cal(0)
    for i in range(len(data.index)):
        acc_weight = data.at[i,'acc_weight']
        exp_term = (acc_weight/scaling_param)**2
        confidence = 1 - math.exp(-1*exp_term)
        data.at[i,'confidence'] = confidence
    return data


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
    estimate_mean_sensor_val = data['sensor_value'].mean()  # Check again if it counts all cell or not?
    # Adding accumulated weight and accumulated reading
    for i in range(len(data.index)):
        for j in range(len(grid_data.index)):
            measure_x = data.at[i,'x']
            measure_y = data.at[i,'y']
            neighbor_x = grid_data.at[j,'x']
            neighbor_y = grid_data.at[j,'y']
            dis = cal_distance(measure_x, neighbor_x, measure_y, neighbor_y)
            weight = weight_cal(dis)
            grid_data.at[j,'acc_weight'] += weight
            grid_data.at[j,'acc_weight_reading'] += data.at[i,'sensor_value']*weight
    grid_data = confidence_map(grid_data)
    grid_data = cal_mean_estimate(grid_data, estimate_mean_sensor_val)
    grid_data.to_csv('output.csv', index=False)


def cal_mean_estimate(grid_data, val):
    for i in range(len(grid_data.index)):
        confidence = grid_data.at[i,'confidence']
        acc_weight = grid_data.at[i,'acc_weight']
        acc_reading = grid_data.at[i,'acc_weight_reading']
        mean_estimate = confidence*(acc_reading/acc_weight) + (1-confidence)*val
        grid_data.at[i,'sensor_value'] = mean_estimate
    return grid_data