import serial
import time
import threading
import struct
import msvcrt
#-------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import pandas as pd
import GPy
import math
import os
# import cv2
import matplotlib.patches as pat
import csv
import time
from time import sleep
import random
from statistics import mean
from sklearn.gaussian_process import kernels as sk_kern
from sklearn.gaussian_process import GaussianProcessRegressor

#-------------------------------------------------
def worker():
	# print(time.time())
	time.sleep(5)

def scheduler(interval, f, wait = True):
	base_time = time.time()
	next_time = 0
	i=5
	sens = []
	global Mx, My
	try:
		with serial.Serial('COM7', 115200, timeout=1) as ser:
			while True:
				print(time.time()) #check time
				t = threading.Thread(target = f)
				t.start()
				if wait:
					t.join()
				next_time = ((base_time - time.time()) % interval) or interval



				c = ser.readline()#\nまで受信
				print(c)
				if i == 5:  #最初だけ
					# print(i)
					i = 0
					sens = [] #Initialize
				else:
					if c != b'':
						# print(i)
						val_decoded = c.decode().strip() #str型
						try:
							d = float(val_decoded) #float型
							sens.append([d]) #sensorValue格納
							print(sens)
							i = i + 1
							# print(i)
							# print('-------------')
						except ValueError:
							# 必要におうじエラー処理を行う
							print('bu----')
							pass						
	
		#---------------------------------------------------------
				ee = 1000
				fff = 111
				if i != 4: #arduinoに適当なデータを送る(available()を有効にしてsensorValue取得のため)
					ser.write((str(ee)+ "," + str(ee) + "&").encode('utf-8'))
				elif i == 4: #read.line()の前にデータを送る(ガウス移動指示)
					conc = np.array([sens[3], sens[2], sens[1], sens[0]])
					x_mean, x_std = Mx.predict(conc.reshape(1, -1), return_std=True) #crosswind
					y_mean, y_std = My.predict(conc.reshape(1, -1), return_std=True) #upwind
					x_pred = x_mean + (x_std * random.uniform(-1,1))
					y_pred = y_mean + (y_std * random.uniform(-1,1))
					with open('CPTexp.csv', 'a', newline='') as f:
						writer = csv.writer(f)	
						writer.writerow([sens[0][0],sens[1][0],sens[2][0],sens[3][0],x_pred[0][0],y_pred[0][0]])	
					ser.write((str(x_pred[0][0])+ "," + str(y_pred[0][0]) + "&").encode('utf-8'))		
					i = 0
					sens = [] #Initialize
				time.sleep(next_time)				
				print(i)
		#----------------------------------------------------------
				if msvcrt.kbhit(): # キーが押されているか
					lb = msvcrt.getch() # 押されていれば、キーを取得する
					lb_rev = lb.decode() # byte→str型に
					if lb_rev == 'q':
						print('interrupt now')
						c = ser.readline()#\nまで受信
						ser.write((str(fff)+ "," + str(fff) + "&").encode('utf-8'))
						sleep(0.2)
						break
	except OSError:
		#接続エラー時の回避
		print('connect error')
		pass
#-------------------------------------------------

#study_model
#-------------------------------------------------------------------
CSV = 'Study_gaussian_new_new_try.csv'
#-------------------------------------------------------------------
csv_input = pd.read_csv(CSV,header=None)
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

#四次元入力、一次元出力_study用
study_input_list = np.array([study_conc1.ravel(), study_conc2.ravel(), study_conc3.ravel(), study_conc4.ravel()]).T

study_output_list_x = study_delta_x.reshape(len(csv_input),1)
study_output_list_y = study_delta_y.reshape(len(csv_input),1)

print('bujidesu')

#gaussianのモデル作成
#-------------------------------------------------------------------
kernel = sk_kern.RBF(length_scale=.5)+sk_kern.WhiteKernel()
#alphaは発散しないように対角行列に加える値
Mx = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
My = GaussianProcessRegressor(kernel=kernel, alpha = 1e-5, optimizer = "fmin_l_bfgs_b", n_restarts_optimizer = 100, normalize_y=True)
Mx.fit(study_input_list, study_output_list_x)
My.fit(study_input_list, study_output_list_y)
kkk = Mx.log_marginal_likelihood()
kkkk = My.log_marginal_likelihood()
params_x = Mx.kernel_.get_params()
params_y = My.kernel_.get_params()
print(kkk)
print(kkkk)
print(params_x)
print(params_y)

with open('param.txt', 'w') as f:
	print('Mx : log_marginal_likelihood', file=f)
	print(kkk,params_x, file=f)
	print('My : log_marginal_likelihood', file=f)
	print(kkkk,params_y, file=f)
#-------------------------------------------------------------------

print('bujide')

#main
while True:
	if msvcrt.kbhit(): # キーが押されているか
		kb = msvcrt.getch() # 押されていれば、キーを取得する
		kb_rev = kb.decode() # byte→str型に
		if kb_rev == 'g':
			print('start')
			scheduler(0.1, worker, False)
		elif kb_rev == 'q':
			print('halt now')
			pass