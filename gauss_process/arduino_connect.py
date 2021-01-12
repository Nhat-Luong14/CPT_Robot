import time
from getkey import getkey

import numpy as np
import pandas as pd
import math
import os

import csv
from time import sleep
import random
from statistics import mean
from sklearn.gaussian_process import kernels as sk_kern
from sklearn.gaussian_process import GaussianProcessRegressor

import socket
import config
#-------------------------------------------------
def scheduler(interval, wait=True):
	base_time = time.time()
	count=0
	sens = []
	global Mx, My
	fff = 111
	try:
		while True:
			print(time.time()) #check time
			next_time = ((base_time - time.time()) % interval) or interval

			print("hello")
			data, addr = pi_communication.recvfrom(1024)
			data = data.decode('utf-8')
			sensor_val = float(data)
			sens.append([sensor_val]) 
			count = count + 1

			if count != 4: #arduinoに適当なデータを送る(available()を有効にしてsensorValue取得のため)
				feed_back = "1000,1000&"
				pi_communication.sendto(feed_back.encode('utf-8'), addr)

			elif count == 4: #read.line()の前にデータを送る(ガウス移動指示)
				conc = np.array([sens[3], sens[2], sens[1], sens[0]])
				x_mean, x_std = Mx.predict(conc.reshape(1, -1), return_std=True) #crosswind
				y_mean, y_std = My.predict(conc.reshape(1, -1), return_std=True) #upwind
				x_pred = x_mean + (x_std * random.uniform(-1,1))
				y_pred = y_mean + (y_std * random.uniform(-1,1))

				with open('CPTexp.csv', 'a', newline='') as f:
					writer = csv.writer(f)	
					writer.writerow([sens[0][0],sens[1][0],sens[2][0],sens[3][0],x_pred[0][0],y_pred[0][0]])

				feed_back = str(x_pred[0][0])+ "," + str(y_pred[0][0]) + "&"
				pi_communication.sendto(feed_back.encode('utf-8'), addr)

				count = 0
				sens.clear()
				
			time.sleep(next_time)				
			print(count)
		
		key = getkey(blocking=False)
		if key == 'g':
			print('interrupt now')
			feed_back = str(fff)+ "," + str(fff) + "&"
			pi_communication.sendto(feed_back.encode('utf-8'), addr)
			#break
	except Exception as e:
		prinr(str(e))

def learning_process():
	data_csv = config.training_data_csv
	csv_input = pd.read_csv(data_csv, header=None)
	#study_output:displacement of position (4step - 1step)
	study_delta_x=csv_input.values[:, 9]
	study_delta_y=csv_input.values[:, 10]
	
	#study_input:current voltage
	study_conc1=csv_input.values[:,3]
	#study_input:voltage after 1 step
	study_conc2=csv_input.values[:,6]
	#study_input:voltage after 2 step
	study_conc3=csv_input.values[:,7]
	#study_input:voltage after 3 step
	study_conc4=csv_input.values[:,8]

	study_input_list = np.array([study_conc1.ravel(), study_conc2.ravel(), 
		study_conc3.ravel(), study_conc4.ravel()]).transpose()

	study_output_list_x = study_delta_x.reshape(len(csv_input),1)
	study_output_list_y = study_delta_y.reshape(len(csv_input),1)

	print('Bujidesu')
	create_gaussian_model(study_input_list, study_output_list_x, study_output_list_y)

def create_gaussian_model(study_input_list, study_output_list_x, study_output_list_y)
	kernel = sk_kern.RBF(length_scale=.5) + sk_kern.WhiteKernel()

	#alphaは発散しないように対角行列に加える値
	Mx = GaussianProcessRegressor(
		kernel=kernel, 
		alpha = 1e-5, 
		optimizer = "fmin_l_bfgs_b", 
		n_restarts_optimizer = 100, 
		normalize_y=True)

	My = GaussianProcessRegressor(
		kernel=kernel, 
		alpha = 1e-5, 
		optimizer = "fmin_l_bfgs_b", 
		n_restarts_optimizer = 100, 
		normalize_y=True)

	Mx.fit(study_input_list, study_output_list_x)
	My.fit(study_input_list, study_output_list_y)
	kkk = Mx.log_marginal_likelihood()
	kkkk = My.log_marginal_likelihood()
	params_x = Mx.kernel_.get_params()
	params_y = My.kernel_.get_params()
	# print(kkk)
	# print(kkkk)
	# print(params_x)
	# print(params_y)

	save_param(kkk, kkkk, params_x, params_y)
	print('bujide')

def save_param(kkk, kkkk, params_x, params_y):
	with open('param.txt', 'w') as f:
		f.write('Mx : log_marginal_likelihood')
		f.write(kkk, params_x)
		f.write('My : log_marginal_likelihood')
		f.write(kkkk,params_y)
        
if __name__ == "__main__": 
	host = config.server_ip
	port = config.server_port
	pi_communication = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	pi_communication.bind((host, port))
	print("Server Started")

	#traing AI
	learning_process()
	
	while True:
		key = getkey()
		if key == 'g':
			print("start")
			scheduler(0.1, False)
		if key == 's': #stop
            sys.exit()
		except KeyboardInterrupt:
			print('halt now')
			pass