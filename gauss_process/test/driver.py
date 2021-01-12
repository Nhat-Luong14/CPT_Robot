#following code only works when using Model-Pi instead of Model X motor driver board which can give raspberry Pi USB 5V power
#Initialize Rear model X board ENA and ENB pins, tell OS that ENA,ENB will output analog PWM signal with 1000 frequency
#rightSpeed = GPIO.PWM(ENA,1000)	
#leftSpeed = GPIO.PWM(ENB,1000)	
#rightSpeed.start(0)
#leftSpeed.start(0)

#make rear right motor moving forward
from setup import IN1Front, IN1Rear, IN2Front, IN2Rear, IN3Front, IN3Rear, IN4Front, IN4Rear
from setup import GPIO
import time

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

#making right turn   
def turn_right(speed):
    rl_ahead(speed)
    rr_back(speed)
    fl_ahead(speed)
    fr_back(speed)
      
#make left turn
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

#make both motor stop
def stop_car():
    GPIO.output(IN1Rear,False)
    GPIO.output(IN2Rear,False)
    GPIO.output(IN3Rear,False)
    GPIO.output(IN4Rear,False)
    GPIO.output(IN1Front,False)
    GPIO.output(IN2Front,False)
    GPIO.output(IN3Front,False)
    GPIO.output(IN4Front,False)
    time.sleep(0.5)