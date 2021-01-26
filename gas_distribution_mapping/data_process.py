import csv
import math 
import config
import sys
import pandas as pd 
import mapping

# First is convert meter to millimeter. Then offset the y-coordinate value to non negative
def rounding(data):
    column = data["y"]
    min_val = column.min()
    offset = (-1)*math.floor(min_val * config.scale)
    for i in range(len(data.index)):
        x = round(data.at[i,"x"] * config.scale)
        y = round(data.at[i,"y"] * config.scale) + offset
        data.at[i,"x"] = roundPartial(x, config.resolution)
        data.at[i,"y"] = roundPartial(y, config.resolution) 
    return data
    

# Round to a nearest number in a set of number with fixed interval
# This action likes assigning the coordinate of a point in a cell 
# to that cell's center coordination.
def roundPartial (value, resolution):
    val = round(value / resolution) * resolution
    return val


# Normalize the gas sensor reading value. The range is [0,1]
def nomalize(data):
    column = data["sensor_value"]
    max_val = column.max()
    min_val = column.min()
    for i in range(len(data.index)):
        val = data.at[i,'sensor_value']
        average_val = round((val - min_val)/(max_val - min_val),2)
        data.at[i,'sensor_value'] = average_val
    return data


# Convert string to array of float (sensor readings)
# Get average from a list of float numbers
def get_avarage(sensor_readings):    
    list_val = str2list_float(sensor_readings)
    average_val = sum(list_val)/len(list_val)
    return average_val


# Convert a string in th form "['0','1']" into a list of float
def str2list_float(str_val):
    new_str = str_val.replace('\'', '').replace('[', '').replace(']', '')
    list_val = [float(idx) for idx in new_str.split(', ')]
    return list_val


# To check whether a place in a blank map has measurement value
def check_exist(x,y,data):
    for i in range(len(data.index)):
        x_data = data.at[i,'x']
        y_data = data.at[i,'y']
        if x_data == x and y_data == y:
            return True
    return False 


# Insert default gas values (0) for uncovered position when taking gas measurement
def insert_blank(data):
    append_data = []
    for x in range(0, config.x_dim+1, config.resolution):
        for y in range(0, config.y_dim+1, config.resolution):
            check = check_exist(x,y,data)
            if check is False:
                append_data.append((x,y,0))
    append_rows = pd.DataFrame(append_data,columns=['x','y','sensor_value'])
    data_grid = pd.concat([data, append_rows], ignore_index=True)
    return data_grid


# Do convert string to list of float, average, normalize, rounding
def data_makeup(data):
    for i in range(len(data.index)):
        sensor_val_str = data.at[i,'sensor_value']
        data.at[i,'sensor_value'] = get_avarage(sensor_val_str)
    data = nomalize(data)
    data = rounding(data)
    return data


if __name__ == "__main__":
    # Get csv file name of data in command line
    try:
        csv_name = sys.argv[1]
    except Exception as e:
        print("missing csv file name as an argument")
        sys.exit()
    data = pd.read_csv(csv_name) 
    new_data = data_makeup(data)
    data_grid = insert_blank(new_data)
    mapping.update_cell(new_data, data_grid)
    mapping.plot_heat_map('output.csv')
    print("Done!!")