import config
import socket
import sys

SPEED = 90

def analogRead():
	return 5

def stop():
	  print("stop")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((config.server_ip, config.server_port))
	while True:
		data = str(s.recv(1024), 'utf-8')   # pythonからの信号受信
		gas_reading = analogRead()
		  
		if (data == 'searching'):
			s.send(str(gas_reading).encode('utf-8'))    # Pythonへsensor値を送信

		elif (data == 'stop'):
			sys.exit()

		elif (data == ''):
			pass

		else:
			x = float(data.split(", ")[0])      # x移動量=横方向
			y = -1*float(data.split(", ")[1])   # y移動量=前進方向
			print(x,y)
			s.send(str(gas_reading).encode('utf-8'))