# data processing for gas mapping
import csv
import math 
import config
import sys

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


# Get average from a list of float numbers
def get_avarage(list_val):
    average_val = sum(list_val)/len(list_val)
    return average_val


# Convert a string in th form "['0','1']" into a list of float
def str2list_float(str_val):
    new_str = str_val.replace('\'', '').replace('[', '').replace(']', '')
    list_val = [float(idx) for idx in new_str.split(', ')]
    return list_val


def save_new(modified_data):
    with open('new_data.csv', 'w', newline='') as file:
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
def insert_blank():
    append_data = []
    with open('new_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        modified_data = list(reader)
        del modified_data[0]   
        for x in range(0,2400,50):
            for y in range(0,1800,50):
                check = check_exist(x,y,modified_data)
                if check is False:
                    append_data.append((x,y,0))
                else:
                    pass
    
    with open('new_data.csv','a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(append_data)


if __name__ == "__main__":
    # Get csv file name of experiment data in command line
    try:
        csv_name = sys.argv[1]
    except Exception as e:
        print("missing csv file name as argument")
        sys.exit()

    with open(csv_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        del data[0]             # delete csv header (row 1)
        for row in data:        # convert string to array of float (sensor readings)
            list_val = str2list_float(row[2])
            row[2] = get_avarage(list_val)  
        
        rounded_data = rounding(data)
        new_data = nomalize_sensing(rounded_data)
        save_new(new_data)
        insert_blank()