import math
import config
import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd
import data_process

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
    data_cme = data.pivot("y", "x", "sensor_value")
    data_vme = data.pivot("y", "x", "variance")
    #ax = sns.heatmap(data, vmin=0, vmax=1)

    fig, (ax1, ax2) = plt.subplots(1,2)
    sns.heatmap(data_cme, ax=ax1, vmin=0, vmax=1, cbar_kws={"orientation": "horizontal"}, xticklabels=4, yticklabels=4)
    sns.heatmap(data_vme, ax=ax2, vmin=0, vmax=1, cbar_kws={"orientation": "horizontal"}, xticklabels=4, yticklabels=4)
    plt.show()


def cal_mean_estimate(grid_data, val):
    for i in range(len(grid_data.index)):
        confidence = grid_data.at[i,'confidence']
        acc_weight = grid_data.at[i,'acc_weight']
        acc_reading = grid_data.at[i,'acc_weight_reading']
        mean_estimate = confidence*(acc_reading/acc_weight) + (1-confidence)*val
        grid_data.at[i,'sensor_value'] = mean_estimate
    return grid_data


def cal_variance_estimate(data, grid_data):
    grid_data['acc_variance'] = 0.0
    grid_data['variance'] = 0.0
    mean_val = cal_mean_variance(data)

    for i in range(len(data.index)):
        for j in range(len(grid_data.index)):
            #mean_predict = grid_data.at[j,'sensor_value']
            nearest_x = data.at[i,'x']
            nearest_y = data.at[i,'y'] + config.resolution
            mean_predict = grid_data.loc[(grid_data.x == nearest_x) & (grid_data.y == nearest_y),'sensor_value'].tolist()[0]


            sens_reading = data.at[i,'sensor_value']
            measure_x = data.at[i,'x']
            measure_y = data.at[i,'y']
            neighbor_x = grid_data.at[j,'x']
            neighbor_y = grid_data.at[j,'y']
            dis = cal_distance(measure_x, neighbor_x, measure_y, neighbor_y)
            weight = weight_cal(dis)
            grid_data.at[j,'acc_variance'] += weight*(sens_reading-mean_predict)**2

    for i in range(len(grid_data.index)):
        confidence = grid_data.at[i,'confidence']
        acc_weight = grid_data.at[i,'acc_weight']
        acc_variance = grid_data.at[i,'acc_variance']
        variance_estimate = confidence*(acc_variance/acc_weight) + (1-confidence)*mean_val
        grid_data.at[i,'variance'] = variance_estimate
    return grid_data


# To calculate thr estimate v0 of the distribution variance
def cal_mean_variance(data):
    mean_val = data['sensor_value'].mean()
    sum = 0
    for i in range(len(data.index)):
        sensor_reading = data.at[i,'sensor_value']
        sum += (sensor_reading-mean_val)**2
    mean_variance = sum/(len(data.index)-1)
    return mean_variance


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
    grid_data = cal_variance_estimate(data, grid_data)
    grid_data = data_process.nomalize(grid_data, 'variance')
    grid_data = data_process.nomalize(grid_data, 'sensor_value')
    grid_data.to_csv('output.csv', index=False)