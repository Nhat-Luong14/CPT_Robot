import csv
import math 
import config
import sys

# First is convert meter to millimeter. Then offset the y-coordinate value to non negative
def rounding(data):
    minimum = get_extrema(data, column_index=1)[0]
    offset = (-1)*math.floor(minimum * 1000)
    for row in data:
        x = round(float(row[0]) * 1000)
        y = round(float(row[1]) * 1000) + offset
        row[0] = roundPartial(x, config.resolution)
        row[1] = roundPartial(y, config.resolution) 
    return data
    

def roundPartial (value, resolution):
    return round (value / resolution) * resolution


# Normalize the gas sensor reading value. The range is [0,1]
def nomalize(data):
    minimum, maximum = get_extrema(data, column_index=2)
    for row in data:
        row[2] = round((float(row[2]) - minimum)/(maximum-minimum),2)
    return data

# Get the maximum and minimum number in a column
def get_extrema(data, column_index):
    list_value = []
    for row in data:
        list_value.append(float(row[column_index]))
    maximum = max(list_value)
    minimum = min(list_value)
    return minimum, maximum

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


def save_csv(modified_data, csv_name):
    with open(csv_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x(mm)", "y(mm)", "sensor_value"])
        for row in modified_data:
            writer.writerow(row)


def check_exist(x,y,data):
    for row in data:
        if int(row[0]) == x and int(row[1]) == y:
            return True
    return False 

# Insert default gas values (0) for uncovered position when taking gas measurement
def insert_blank(file_name):
    append_data = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        modified_data = list(reader)
        del modified_data[0]   
        for x in range(0, config.x_dim+1, config.resolution):
            for y in range(0, config.y_dim+1, config.resolution):
                check = check_exist(x,y,modified_data)
                if check is False:
                    append_data.append((x,y,0))
                else:
                    pass
        
        completed_data = modified_data + append_data
        inserted_file_name = file_name.replace('.', "_grid_map.")
        with open(inserted_file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["x(mm)", "y(mm)", "sensor_value"])
            for row in completed_data:
                writer.writerow(row)

def data_makeup(data):
    for row in data:  
        sensor_reading = row[2] 
        value = get_avarage(sensor_reading)
        row[2] = value
    data = nomalize(data)
    data = rounding(data)
    return data


if __name__ == "__main__":
    # Get csv file name of experiment data in command line
    try:
        csv_name = sys.argv[1]
    except Exception as e:
        print("missing csv file name as an argument")
        sys.exit()

    with open(csv_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        del data[0]             # delete csv header (row 1)
        new_data = data_makeup(data)
        save_csv(new_data, csv_name)
        insert_blank(csv_name)
        print("Done processing!!")