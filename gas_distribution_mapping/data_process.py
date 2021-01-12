# data processing for gas mapping
import csv
import math 
import config

def rounding(data):
    for row in data:
        x = round(float(row[0]) * 1000)
        y = round(float(row[1]) * 1000)
        row[0] = roundPartial(x, config.resolution)
        row[1] = roundPartial(y, config.resolution) + 1450 #offset
    return data

def roundPartial (value, resolution):
    return round (value / resolution) * resolution

# Normalize the gas sensor reading value. The range is [0,1]
def nomalize_sensing(data):
    list_value = []
    for row in data:
        list_value.append(float(row[2]))
    maximum = max(list_value)
    minimum = min(list_value)
    for row in data:
        row[2] = round((float(row[2]) - minimum)/(maximum-minimum),2)
    return data

def save_new(modified_data):
    with open('new_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x(mm)", "y(mm)", "sensor_value"])
        for row in modified_data:
            writer.writerow(row)


if __name__ == "__main__":
    with open('test_4.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        del data[0]     
        for row in data:
            list_sensor_val = row[2].replace('\'', '')
            list_val = list_sensor_val.replace('[', '')
            list_val = list_val.replace(']', '')
            list_val = [float(idx) for idx in list_val.split(', ')]
            average_val = sum(list_val)/len(list_val)
            row[2] = average_val
        data = rounding(data)
        new_data = nomalize_sensing(data)
        save_new(new_data)