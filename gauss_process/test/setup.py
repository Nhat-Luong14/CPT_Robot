import RPi.GPIO as GPIO #control motor board through GPIO pins

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

def gpio_init():
    #initialize GPIO pins, tell OS which pins will be used to control Model-Pi L298N board
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

def gpio_clean():
    GPIO.cleanup()    