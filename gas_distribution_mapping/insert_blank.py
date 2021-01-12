import csv

append_data = []

def check_exist(x,y,data):
    for row in data:
        if int(row[0]) == x and int(row[1]) == y:
            return True
    return False 
    
with open('new_data.csv', newline='') as csvfile:
    exist = True
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