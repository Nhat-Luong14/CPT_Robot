import time
import threading
import numpy as np
import socket
from getkey import getkey
from scipy import stats
import collections
import config
import learning 

def e_stop():
    key = getkey()
    if key == 'q':
        connection.send(b'stop')
        connection.close()

def scheduler(interval):
    sens = collections.deque(maxlen=4)
    count = 0
    Mx, My = learning.training(gen_new=False) 
    new_thread = threading.Thread(target=e_stop)
    new_thread.start()
    connection.send(b'searching')
    while True: 
        try: 
            gas_val = str(connection.recv(1024), 'utf-8')
            sens.append(float(gas_val)) #sensorValue格納
            count += 1					

            if count != 4: #arduinoに適当なデータを送る(available()を有効にしてsensorValue取得のため)
                connection.send(b'searching')
            
            elif count == 4: #read.line()の前にデータを送る(ガウス移動指示)
                input = np.array([sens[3], sens[2], sens[1], sens[0]])
                print(input)
                x_mean, x_std = Mx.predict(input.reshape(1, -1), return_std=True) #crosswind
                y_mean, y_std = My.predict(input.reshape(1, -1), return_std=True) #upwind
                x_pred = stats.truncnorm.rvs(-0.5, 0.5, loc=x_mean, scale=x_std, size=1)[0]
                y_pred = stats.truncnorm.rvs(-0.5, 0.5, loc=y_mean, scale=y_std, size=1)[0]

                msg = str(x_pred) + "," + str(y_pred)
                connection.send(msg.encode('utf-8'))
                count = 0
            time.sleep(interval)	
        except Exception as e:
            connection.close()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config.server_ip, 10002))
    s.listen()
    connection, addr = s.accept()
    with connection:
        while True:
            key = getkey()
            if key == 'g':
                print("start")
                scheduler(interval=0.1)