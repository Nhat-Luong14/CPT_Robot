import math
import config
import seaborn as sns 
import matplotlib.pyplot as plt
import pandas as pd
import sys
import csv

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


# Calculate the distance between the point of measument to surounding neighbor cells
def displacement_cal(point1_x, point1_y, point2_x, point2_y):
    displacement = (point2_x-point1_x, point2_y-point1_y)
    return displacement


# Calculate the weigth of the measurment point to neighbor cells
def check_weight(displacement):
    sum = displacement[0]**2 + displacement[1]**2
    if math.sqrt(sum) <= config.cutoff_radius:
        return weight_cal(displacement)
    else:
        return 0


def plot_heat_map(csv_name):
    sns.set_theme()
    data = pd.read_csv(csv_name)
    data = data.pivot("y(mm)", "x(mm)", "sensor_value")
    ax = sns.heatmap(data, vmin=0, vmax=1)
    plt.show()


# Update value of cell reading using extrapolate
def update_cell(csv_name):
    blank_grid = pd.read_csv(csv_name)
    blank_grid['acc_weight'] = 0
    blank_grid['acc_weight_reading'] = 0
    blank_grid.to_csv(csv_name, index=False)

    before_insert_file = csv_name.replace("_grid_map.", '.')
    with open(before_insert_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        del data[0]   

        with open(csv_name, newline='') as csvfile_2:
            reader_2 = csv.reader(csvfile_2)
            blank_data = list(reader_2)
            del blank_data[0]   
            
            # Adding accumulated weight and accumulated reading
            for row in data:
                for blank_row in blank_data:
                    measurement_x = int(row[0])
                    measurement_y = int(row[1])
                    neighbor_x = int(blank_row[0])
                    neighbor_y = int(blank_row[1])
                    displacement = displacement_cal(measurement_x, measurement_y, neighbor_x, neighbor_y)
                    weight = check_weight(displacement)
                    blank_row[3] = float(blank_row[3]) + weight
                    blank_row[4] = float(blank_row[4]) + float(row[2])*weight

            for blank_row in blank_data:
                if(float(blank_row[3]) != 0 and float(blank_row[2]) == 0):
                    blank_row[2] = float(blank_row[4]) / float(blank_row[3])

            with open('output.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["x(mm)", "y(mm)", "sensor_value","acc_weight","acc_weight_reading"])
                for row in blank_data:
                    writer.writerow(row)

if __name__ == '__main__':
    # Get csv file name of experiment data in command line
    try:
        csv_name = sys.argv[1]
    except Exception as e:
        print("Missing csv file name as argument")
        print("Please input the csv file has the gridmap value!")
        sys.exit()

    update_cell(csv_name)
    plot_heat_map("output.csv")