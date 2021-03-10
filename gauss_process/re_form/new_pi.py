import RPi.GPIO as GPIO #control motor board through GPIO pins
import time
import socket
import config
import sys
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class Driver:
    def __init__(self):
        self.IN1Rear = 16 #GPIO23 to IN1 Rear-right wheel direction 
        self.IN2Rear = 18 #GPIO24 to IN2 Rear-right wheel direction
        self.IN3Rear = 13 #GPIO27 to IN3 Rear-left wheel direction
        self.IN4Rear = 15 #GPIO22 to IN4 Rear-left wheel direction

        self.IN1Front = 40 #GPIO21 to IN1 Front Model X right wheel direction 
        self.IN2Front = 38 #GPIO20 to IN2 Front Model X right wheel direction
        self.IN3Front = 36 #GPIO16 to IN3 Front Model X left wheel direction
        self.IN4Front = 32 #GPIO12 to IN4 Front Model X left wheel direction

        self.ENA = 12 #GPIO18 to ENA PWM SPEED of rear left motor
        self.ENB = 33 #GPIO13 to ENB PWM SPEED of rear right motor
        self.ENA1 = 35
        self.ENB1 = 37
        
        self.rightSpeed = 0
        self.leftSpeed = 0
        self.rightSpeed1 = 0 
        self.leftSpeed1 = 0


    def gpio_init(self):
        #initialize GPIO pins, tell OS which pins will be used
        #GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.IN1Rear, GPIO.OUT) 
        GPIO.setup(self.IN2Rear, GPIO.OUT)
        GPIO.setup(self.IN3Rear, GPIO.OUT)
        GPIO.setup(self.IN4Rear, GPIO.OUT)
        
        GPIO.setup(self.IN1Front, GPIO.OUT) 
        GPIO.setup(self.IN2Front, GPIO.OUT)
        GPIO.setup(self.IN3Front, GPIO.OUT)
        GPIO.setup(self.IN4Front, GPIO.OUT)

        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        GPIO.setup(self.ENA1, GPIO.OUT)
        GPIO.setup(self.ENB1, GPIO.OUT)

        GPIO.output(self.ENA,True)
        GPIO.output(self.ENB,True)
        GPIO.output(self.ENA1,True)
        GPIO.output(self.ENB1,True)

        self.rightSpeed = GPIO.PWM(self.ENA,1000)	
        self.leftSpeed = GPIO.PWM(self.ENB,1000)
        self.rightSpeed1 = GPIO.PWM(self.ENA1,1000)    
        self.leftSpeed1 = GPIO.PWM(self.ENB1,1000) 
	
        self.rightSpeed.start(0)
        self.leftSpeed.start(0)
        self.rightSpeed1.start(0)
        self.leftSpeed1.start(0)


    def gpio_clean(self):
        GPIO.cleanup()    
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        GPIO.output(self.ENA,True)
        GPIO.output(self.ENB,True)


    def rr_ahead(self, speed):
        GPIO.output(self.IN1Rear,True)
        GPIO.output(self.IN2Rear,False)
        self.rightSpeed.ChangeDutyCycle(speed)


    def rl_ahead(self, speed):  
        GPIO.output(self.IN3Rear,True)
        GPIO.output(self.IN4Rear,False)
        self.leftSpeed.ChangeDutyCycle(speed)


    def rr_back(self, speed):
        GPIO.output(self.IN2Rear,True)
        GPIO.output(self.IN1Rear,False)
        self.rightSpeed.ChangeDutyCycle(speed)


    def rl_back(self, speed):  
        GPIO.output(self.IN4Rear,True)
        GPIO.output(self.IN3Rear,False)
        self.leftSpeed.ChangeDutyCycle(speed)


    def fr_ahead(self, speed):
        GPIO.output(self.IN1Front,True)
        GPIO.output(self.IN2Front,False)
        self.rightSpeed1.ChangeDutyCycle(speed)


    def fl_ahead(self, speed):  
        GPIO.output(self.IN3Front,True)
        GPIO.output(self.IN4Front,False)
        self.leftSpeed1.ChangeDutyCycle(speed)


    def fr_back(self, speed):
        GPIO.output(self.IN2Front,True)
        GPIO.output(self.IN1Front,False)
        self.rightSpeed1.ChangeDutyCycle(speed)
 

    def fl_back(self, speed):  
        GPIO.output(self.IN4Front,True)
        GPIO.output(self.IN3Front,False)
        self.leftSpeed1.ChangeDutyCycle(speed)


    def go_ahead(self, speed):
        self.rl_ahead(speed)
        self.rr_ahead(speed)
        self.fl_ahead(speed)
        self.fr_ahead(speed)


    def go_back(self, speed):
        self.rr_back(speed)
        self.rl_back(speed)
        self.fr_back(speed)
        self.fl_back(speed)
  

    def turn_right(self, speed):
        self.rl_ahead(speed)
        self.rr_back(speed)
        self.fl_ahead(speed)
        self.fr_back(speed)
        

    def turn_left(self, speed):
        self.rr_ahead(speed)
        self.rl_back(speed)
        self.fr_ahead(speed)
        self.fl_back(speed)


    def shift_left(self, speed):
        self.fr_ahead(speed)
        self.rr_back(speed)
        self.rl_ahead(speed)
        self.fl_back(speed)


    def shift_right(self, speed):
        self.fr_back(speed)
        self.rr_ahead(speed)
        self.rl_back(speed)
        self.fl_ahead(speed)


    def upper_right(self, speed):
        self.rr_ahead(speed)
        self.fl_ahead(speed)


    def lower_left(self, speed):
        self.rr_back(speed)
        self.fl_back(speed)


    def upper_left(self, speed):
        self.fr_ahead(speed)
        self.rl_ahead(speed)


    def lower_right(self, speed):
        self.fr_back(speed)
        self.rl_back(speed)


    #make both motor stop
    def stop_car(self):
        GPIO.output(self.IN1Rear,False)
        GPIO.output(self.IN2Rear,False)
        GPIO.output(self.IN3Rear,False)
        GPIO.output(self.IN4Rear,False)
        GPIO.output(self.IN1Front,False)
        GPIO.output(self.IN2Front,False)
        GPIO.output(self.IN3Front,False)
        GPIO.output(self.IN4Front,False)
        self.leftSpeed.ChangeDutyCycle(0)
        self.rightSpeed.ChangeDutyCycle(0)
        self.leftSpeed1.ChangeDutyCycle(0)
        self.rightSpeed1.ChangeDutyCycle(0)
        time.sleep(0.3)

def move(delta_x, delta_y):
    print("Moving delta_x:", delta_x)
    print("Moving delta_y:", delta_y)

    if delta_y > 0: 
        driver.go_ahead(50)
        time.sleep(0.7)
        driver.stop_car()

    elif delta_y < 0:
        driver.go_back(50)
        time.sleep(0.7)
        driver.stop_car()

    if delta_x > 0: 
        driver.shift_left(50)
        time.sleep(0.7)
        driver.stop_car()

    elif delta_x < 0:
        driver.shift_right(50)
        time.sleep(0.7)
        driver.stop_car()


def sensing():
    chan = AnalogIn(mcp, MCP.P0)
    sensor_data = str(round(chan.voltage,2))
    return sensor_data 
 
if __name__ == "__main__":   
    #driver = Driver()
    #driver.gpio_init()
    print("step 1")
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D25)
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs, ref_voltage=5)
    print("step2")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("step3")
        s.connect((config.server_ip, config.server_port))
        while True:
            data = str(s.recv(1024), 'utf-8')   # pythonからの信号受信
            gas_reading = sensing()        
            if (data == 'searching'):
                s.send(str(gas_reading).encode('utf-8'))    # Pythonへsensor値を送信
 
            elif (data == 'stop'):
    #            driver.stop_car()
                sys.exit()
    
            elif (data == ''):
                print("vl")
                pass
    #
            else:
                delta_x = float(data.split(",")[0])      # x移動量=横方向
                delta_y = -1*float(data.split(",")[1])   # y移動量=前進方向 
    #            # move(delta_x, delta_y)
                print(delta_x, delta_y)
                s.send(str(gas_reading).encode('utf-8'))

