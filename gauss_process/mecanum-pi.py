#  ___   ___  ___  _   _  ___   ___   ____ ___  ____  
# / _ \ /___)/ _ \| | | |/ _ \ / _ \ / ___) _ \|    \ 
#| |_| |___ | |_| | |_| | |_| | |_| ( (__| |_| | | | |
# \___/(___/ \___/ \__  |\___/ \___(_)____)___/|_|_|_|
#                  (____/ 
# Osoyoo Model-Pi L298N DC motor driver programming guide
# tutorial url: https:#osoyoo.com/2020/03/01/python-programming-tutorial-model-pi-l298n-motor-driver-for-raspberry-pi/

import RPi.GPIO as GPIO #control motor board through GPIO pins
import time #set delay time to control moving distance
import math 
import socket
import config

SPEED = 90

#If IN1Rear=True and IN2Rear=False right motor move forward, If IN1Rear=False,IN2Rear=True right motor move backward,in other cases right motor stop
IN1Rear = 16 #GPIO23 to IN1 Rear-right wheel direction 
IN2Rear = 18 #GPIO24 to IN2 Rear-right wheel direction

#If IN3Rear=True and IN3Rear=False left motor move forward, If IN3Rear=False,IN4Rear=True left motor move backward,in other cases left motor stop
IN3Rear = 13 #GPIO27 to IN3 Rear-left wheel direction
IN4Rear = 15 #GPIO22 to IN4 Rear-left wheel direction

#ENA/ENB are PWM(analog) signal pin which control the speed of right/left motor through GPIO ChangeDutyCycle(speed) function
ENA = 12 #GPIO18 to ENA PWM SPEED of rear left motor
ENB = 33 #GPIO13 to ENB PWM SPEED of rear right motor

#If IN1Front=True and IN2Front=False right motor move forward, If IN1Front=False,IN2Front=True right motor move backward,in other cases right motor stop
IN1Front = 40 #GPIO21 to IN1 Front Model X right wheel direction 
IN2Front = 38 #GPIO20 to IN2 Front Model X right wheel direction

#If IN3Front=True and IN3Front=False left motor move forward, If IN3Front=False,IN4Front=True left motor move backward,in other cases left motor stop
IN3Front = 36 #GPIO16 to IN3 Front Model X left wheel direction
IN4Front = 32 #GPIO12 to IN4 Front Model X left wheel direction

#============ initialize GPIO pins ============#
#tell OS which pins will be used to control Model-Pi L298N board
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IN1Rear, GPIO.OUT) 
GPIO.setup(IN2Rear, GPIO.OUT)
GPIO.setup(IN3Rear, GPIO.OUT)
GPIO.setup(IN4Rear, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN1Front, GPIO.OUT) 
GPIO.setup(IN2Front, GPIO.OUT)
GPIO.setup(IN3Front, GPIO.OUT)
GPIO.setup(IN4Front, GPIO.OUT)
GPIO.output(ENA,True)
GPIO.output(ENB,True)

#================ Wheel contorl ================#
#make rear right motor moving forward
def rr_ahead(speed):
    GPIO.output(IN1Rear,True)
    GPIO.output(IN2Rear,False)

#make rear left motor moving forward    
def rl_ahead(speed):  
    GPIO.output(IN3Rear,True)
    GPIO.output(IN4Rear,False)
    
#make rear right motor moving backward
def rr_back(speed):
    GPIO.output(IN2Rear,True)
    GPIO.output(IN1Rear,False)

#make rear left motor moving backward    
def rl_back(speed):  
    GPIO.output(IN4Rear,True)
    GPIO.output(IN3Rear,False)
    
#make front right motor moving forward
def fr_ahead(speed):
    GPIO.output(IN1Front,True)
    GPIO.output(IN2Front,False)

#make Front left motor moving forward    
def fl_ahead(speed):  
    GPIO.output(IN3Front,True)
    GPIO.output(IN4Front,False)
 
#make Front right motor moving backward
def fr_back(speed):
    GPIO.output(IN2Front,True)
    GPIO.output(IN1Front,False)

#make Front left motor moving backward    
def fl_back(speed):  
    GPIO.output(IN4Front,True)
    GPIO.output(IN3Front,False)

#================ Robot contorl ================#
def go_ahead(speed):
    rl_ahead(speed)
    rr_ahead(speed)
    fl_ahead(speed)
    fr_ahead(speed)
    
def go_back(speed):
    rr_back(speed)
    rl_back(speed)
    fr_back(speed)
    fl_back(speed)

def turn_right(speed):
    rl_ahead(speed)
    rr_back(speed)
    fl_ahead(speed)
    fr_back(speed)
      
def turn_left(speed):
    rr_ahead(speed)
    rl_back(speed)
    fr_ahead(speed)
    fl_back(speed)

# parallel left shift 
def shift_left(speed):
    fr_ahead(speed)
    rr_back(speed)
    rl_ahead(speed)
    fl_back(speed)

# parallel right shift 
def shift_right(speed):
    fr_back(speed)
    rr_ahead(speed)
    rl_back(speed)
    fl_ahead(speed)

def upper_right(speed):
    rr_ahead(speed)
    fl_ahead(speed)

def lower_left(speed):
    rr_back(speed)
    fl_back(speed)
    
def upper_left(speed):
    fr_ahead(speed)
    rl_ahead(speed)

def lower_right(speed):
    fr_back(speed)
    rl_back(speed)

def stop_car():
    GPIO.output(IN1Rear,False)
    GPIO.output(IN2Rear,False)
    GPIO.output(IN3Rear,False)
    GPIO.output(IN4Rear,False)
    GPIO.output(IN1Front,False)
    GPIO.output(IN2Front,False)
    GPIO.output(IN3Front,False)
    GPIO.output(IN4Front,False)

if __name__ == "__main__":
    host = config.client_ip
    port = config.port
    
    server = (config.server_ip, config.server_port)
    
    pc_communication = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pc_communication.bind((host,port))

    run_cmd = input("-> ")

    while True:
        sensor_val = "10000000000000000000000000000000"
        pc_communication.sendto(sensor_val.encode('utf-8'), server)
        data, addr = pc_communication.recvfrom(1024)
        data = data.decode('utf-8')
        msg_str = data.split('&')[0]     # PCからの信号受信

        x = float(msg_str.split(',')[0])         #Delta X
        y = -1 * float(msg_str.split(',')[1])    #Delta Y

        sqrt_2 = math.sqrt(2)
        v1 = (1/sqrt_2) * (-x/0.4 + y/0.4) #各ホイールの回転速度  ::/0.4はコントロール周期
        v2 = (-1/sqrt_2) * (x/0.4 + y/0.4)
        v3 = (1/sqrt_2) * (x/0.4 - y/0.4)
        v4 = (1/sqrt_2) * (x/0.4 + y/0.4)

        #-------------------------------------------------------------------
        if (x == 1000):
            Gsens = analogRead(GasSensor)   # sensor値を取得
            Gsens = 5.0 * Gsens / 1023      #voltage
            Serial1.println(Gsens)          #pythonへsensor値を送信
        elif (x == 111):
            stop_Stop()
        else:
            pass

        #---------------------------
        #motor movement order. write down here
        #---------------------------
        if (v1 > 0):
            kk = 1
        if (v1 < 0):
            kk = 2
        if (v2 > 0):
            oo = 1
        if (v2 < 0):
            oo = 2
        if (v3 > 0):
            pp = 1
        if (v3 < 0):
            pp = 2
        if (v4 > 0):
            qq = 1
        if (v4 < 0): 
            qq = 2
        #-------------------------------------------------------------------
        if ((kk == 1) and (oo == 1) and (pp == 1) and (qq == 1)):
            fr_ahead(abs(v1)+SPEED)
            fl_back(abs(v2)+SPEED)
            rl_back(abs(v3)+SPEED)
            rr_ahead(abs(v4)+SPEED)
            
        elif ((kk == 1) and (oo == 1) and (pp == 1) and (qq == 2)):
            fr_ahead(abs(v1)+SPEED)
            fl_back(abs(v2)+SPEED)
            rl_back(abs(v3)+SPEED)
            rr_back(abs(v4)+SPEED)

        elif ((kk == 1) and (oo == 1) and (pp == 2) and (qq == 1)):
            fr_ahead(abs(v1)+SPEED)
            fl_back(abs(v2)+SPEED)
            rl_ahead(abs(v3)+SPEED)
            rr_ahead(abs(v4)+SPEED)
        
        elif ((kk == 1) and (oo == 1) and (pp == 2) and (qq == 2)):
            fr_ahead(abs(v1)+SPEED)
            fl_back(abs(v2)+SPEED)
            rl_ahead(abs(v3)+SPEED)
            rr_back(abs(v4)+SPEED)
        
        elif ((kk == 1) and (oo == 2) and (pp == 1) and (qq == 1)):
            fr_ahead(abs(v1)+SPEED)
            fl_ahead(abs(v2)+SPEED)
            rl_back(abs(v3)+SPEED)
            rr_ahead(abs(v4)+SPEED)
        
        elif ((kk == 1) and (oo == 2) and (pp == 1) and (qq == 2)):
            fr_ahead(abs(v1)+SPEED)
            fl_ahead(abs(v2)+SPEED)
            rl_back(abs(v3)+SPEED)
            rr_back(abs(v4)+SPEED)
        
        elif ((kk == 1) and (oo == 2) and (pp == 2) and (qq == 1)):
            fr_ahead(abs(v1)+SPEED)
            fl_ahead(abs(v2)+SPEED)
            rl_ahead(abs(v3)+SPEED)
            rr_ahead(abs(v4)+SPEED)
        
        elif ((kk == 1) and (oo == 2) and (pp == 2) and (qq == 2)):
            fr_ahead(abs(v1)+SPEED)
            fl_ahead(abs(v2)+SPEED)
            rl_ahead(abs(v3)+SPEED)
            rr_back(abs(v4)+SPEED)
        
        elif ((kk == 2) and (oo == 1) and (pp == 1) and (qq == 1)):
            fr_back(abs(v1)+SPEED)
            fl_back(abs(v2)+SPEED)
            rl_back(abs(v3)+SPEED)
            rr_ahead(abs(v4)+SPEED)
        
        elif ((kk == 2) and (oo == 1) and (pp == 1) and (qq == 2)):
            fr_back(abs(v1)+SPEED)
            fl_back(abs(v2)+SPEED)
            rl_back(abs(v3)+SPEED)
            rr_back(abs(v4)+SPEED)
        
        elif ((kk == 2) and (oo == 1) and (pp == 2) and (qq == 1)):
            fr_back(abs(v1)+SPEED)
            fl_back(abs(v2)+SPEED)
            rl_ahead(abs(v3)+SPEED)
            rr_ahead(abs(v4)+SPEED)
        
        elif ((kk == 2) and (oo == 1) and (pp == 2) and (qq == 2)):
            fr_back(abs(v1)+SPEED)
            fl_back(abs(v2)+SPEED)
            rl_ahead(abs(v3)+SPEED)
            rr_back(abs(v4)+SPEED)
        
        elif ((kk == 2) and (oo == 2) and (pp == 1) and (qq == 1)):
            fr_back(abs(v1)+SPEED)
            fl_ahead(abs(v2)+SPEED)
            rl_back(abs(v3)+SPEED)
            rr_ahead(abs(v4)+SPEED)
        
        elif ((kk == 2) and (oo == 2) and (pp == 1) and (qq == 2)):
            fr_back(abs(v1)+SPEED)
            fl_ahead(abs(v2)+SPEED)
            rl_back(abs(v3)+SPEED)
            rr_back(abs(v4)+SPEED)
        
        elif ((kk == 2) and (oo == 2) and (pp == 2) and (qq == 1)):
            fr_back(abs(v1)+SPEED)
            fl_ahead(abs(v2)+SPEED)
            rl_ahead(abs(v3)+SPEED)
            rr_ahead(abs(v4)+SPEED)
        
        elif ((kk == 2) and (oo == 2) and (pp == 2) and (qq == 2)):
            fr_back(abs(v1)+SPEED)
            fl_ahead(abs(v2)+SPEED)
            rl_ahead(abs(v3)+SPEED)
            rr_back(abs(v4)+SPEED)

        Gsens = analogRead(GasSensor); # sensor値を取得
        Gsens = 5.0 * Gsens / 1023;  #voltage
        Serial1.println(Gsens);  #pythonへsensor値を送信

    GPIO.cleanup()  