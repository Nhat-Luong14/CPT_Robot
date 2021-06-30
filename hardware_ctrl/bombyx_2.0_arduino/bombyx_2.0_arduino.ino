//------------------------------------------------------------------
// This code is the main file of controlling the bombyx 2.0 robot
// This code is written by Luong Duc Nhat 
//
// Japan, Tokyo Institute of Technology, 2021 June.
// 
// Please referred author if you reused the code.
//------------------------------------------------------------------

#include <PID_v1.h>
#include <Motor.h>

//=========Pins and variables for gas detection=================//
#define GSL_PIN A0    // Gas Sensor Left
#define LED_PIN A15   // LED Indicator
#define TC 100      // 100 ms timestep
#define SAMP_NUM 5  // Number of sampling cycles during TC
#define TS TC/SAMP_NUM  // Sampling frequency 20ms

// Thresholds
#define THRESHOLD 0.04
#define SP_THRESHOLD 0 //未使用

// Settings of average movement filter
#define yNUM 7
#define ma_yNUM 3
#define dyNUM 2
#define uNUM 7
#define ma_uNUM 5

// Global variables for ARX computations
double yL[yNUM] = {0};  //Sensor value history
double uL[uNUM] = {0};
double dyL[dyNUM] = {0};
double ma_yL[ma_yNUM] = {0};  //Moving average gas sensing
double ma_uL[ma_uNUM] = {0};

//iG_ma 140113 c4 7 5, 高橋修論モデル
const double a1 = -0.981;
const double a2 = 0.01653;
const double b0 = 0.2833;
const double b1 = -0.2706;

//=========Pins and variables for motors control=================//
int timer1_counter; //for timer
// param: enc_pin, fwd_pin, bwd_pin, pwm_pin, kp, ki, kd
Motor motor_fl(18, 3, 4, 2, 1.0, 1.2, 0.02);
Motor motor_fr(19, 5, 6, 7, 1.0, 1.2, 0.02);
Motor motor_bl(20, 9, 10, 8, 1.0, 1.2, 0.02);
Motor motor_br(21, 11, 13, 12, 1.0, 1.2,0.02);

double out_speed1 = 0; double set_speed1 = 0; double output1 = 0;
double out_speed2 = 0; double set_speed2 = 0; double output2 = 0;
double out_speed3 = 0; double set_speed3 = 0; double output3 = 0;
double out_speed4 = 0; double set_speed4 = 0; double output4 = 0;

PID pid_fl(&out_speed1, &output1, &set_speed1, motor_fl.get_kp(), motor_fl.get_ki(), motor_fl.get_kd(), DIRECT);  
PID pid_fr(&out_speed2, &output2, &set_speed2, motor_fr.get_kp(), motor_fr.get_ki(), motor_fr.get_kd(), DIRECT); 
PID pid_bl(&out_speed3, &output3, &set_speed3, motor_bl.get_kp(), motor_bl.get_ki(), motor_bl.get_kd(), DIRECT); 
PID pid_br(&out_speed4, &output4, &set_speed4, motor_br.get_kp(), motor_br.get_ki(), motor_br.get_kd(), DIRECT); 

void setup() {  
	pinMode(LED_PIN, OUTPUT);
	attachInterrupt(digitalPinToInterrupt(motor_fl.get_enc_pin()), update_enc1, RISING);
	attachInterrupt(digitalPinToInterrupt(motor_fr.get_enc_pin()), update_enc2, RISING);
	attachInterrupt(digitalPinToInterrupt(motor_bl.get_enc_pin()), update_enc3, RISING);
	attachInterrupt(digitalPinToInterrupt(motor_br.get_enc_pin()), update_enc4, RISING);

	//--------------------------timer setup-------------------------//
	noInterrupts();           // disable all interrupts
	TCCR5A = 0;
	TCCR5B = TCCR5B & 0b11111000 | 1; // set 31KHz PWM to prevent motor noise
	timer1_counter = 59286;           // preload timer 65536-16MHz/256/2Hz (34286 for 0.5sec) (59286 for 0.1sec)

	TCNT5 = timer1_counter;   // preload timer
	TCCR5B |= (1 << CS12);    // 256 prescaler 
	TIMSK5 |= (1 << TOIE1);   // enable  timer overflow interrupt
	interrupts();             // enable all interrupts

	//--------------------------PID setup---------------------------//
	pid_fl.SetMode(AUTOMATIC);  //set PID in Auto mode
	pid_fr.SetMode(AUTOMATIC);
	pid_bl.SetMode(AUTOMATIC);
	pid_br.SetMode(AUTOMATIC);
	pid_fl.SetSampleTime(20);   // refresh rate of PID controller in ms
	pid_fr.SetSampleTime(20);       
	pid_bl.SetSampleTime(20);
	pid_br.SetSampleTime(20);
	pid_fl.SetOutputLimits(0, 255); // this is the MAX PWM value to move motor
	pid_fr.SetOutputLimits(0, 255);
	pid_bl.SetOutputLimits(0, 255);
	pid_br.SetOutputLimits(0, 255);
	Serial.begin(115200);
}

void loop() {
	getArxValues();
	getStimuli(); 
	delay(100);
	if (Serial.available() > 0) {
		delay(1);   //delay to allow byte to arrive in input buffer
		int cmd = Serial.read();

		// direction: 1=forward, -1=backward 
		// speed: 0~255 
		switch(cmd) { 
			case '1':
				// forward
				set4wheel_dir(1,1,1,1);
				set4wheel_spd(100,112,112,112);	
				break;
			case '2':
				// backward
				set4wheel_dir(-1,-1,-1,-1);
				set4wheel_spd(90,102,102,102);
				break;
			case '3':
				// left
				set4wheel_dir(-1,1,1,-1);
				set4wheel_spd(170,184,182,180);
				break;
			case '4':
				// right
				set4wheel_dir(1,-1,-1,1);
				set4wheel_spd(177,186,186,180);
				break;
			default:
				output1 = output2 = output3 = output4 = 0;
				// getArxValues();
				// getStimuli();
   		}
		motor_fl.set_speed(output1);
		motor_fr.set_speed(output2);
		motor_bl.set_speed(output3);
		motor_br.set_speed(output4);
		delay(1400);
		stop();
	}
}

// interrupt service routine - tick every 0.1sec
ISR(TIMER5_OVF_vect) {        
	TCNT5 = timer1_counter;     
	out_speed1 = motor_fl.get_speed();
	out_speed2 = motor_fr.get_speed();
	out_speed3 = motor_bl.get_speed();
	out_speed4 = motor_br.get_speed();
}

/* 
Shift the array to the right for 1 unit step
param num: size of the array
param val_array: array of value 
*/
void shift_array(double* val_array, int num) {
    for(int i = num-2; i >= 0; i--) {
        val_array[i+1] = val_array[i];
    }
}

/* 
Calcualte the average of all value in the array
param num: size of the array
param val_array: array of value 
*/
double cal_average(double* val_array, int num) {
    double sum = 0.0;
    for(int i = 0; i < num; i++) {
        sum += val_array[i];
    }
    return sum/num;
}


/* 
Compute ARX model output for the raw data of gas sensors
param gasSensValL : Raw value of left sensor
param gasSensValR : Raw value of right sensor 
*/
void getArxValues() {
    //Update moving average gas sensing
    shift_array(yL, yNUM);
    yL[0] = analogRead(GSL_PIN) * (5.0/1023.0); //voltage

    shift_array(ma_yL, ma_yNUM);
    ma_yL[0] = cal_average(yL, yNUM);

    for(int i = ma_yNUM-2; i >= 0; i--){
      	dyL[i] = (ma_yL[i] - ma_yL[i+1])/(TS*0.001);
    }

	shift_array(uL, uNUM);
    uL[0] = -a1*uL[1] - a2*uL[2] + b0*dyL[0] + b1*dyL[1];
    shift_array(ma_uL, ma_uNUM);
    ma_uL[0] = cal_average(uL, uNUM);
}


/*
Get a binary output to indicate if there was a detection in either sensor (for MothT) or in general (for InfoT)
param spikeL : Spikes counter for left detection
param spikeR : Spikes counter for right detection
param stimuL : Binary output for left detection
param stimuR : Binary output for right detection
*/
void getStimuli(){
  	int spikeL = 0;
  	int stimuL = 0; // Sensor binary flags 
    // Take 5 samples of the ARX model output and update the spike counters
    for(int i=0; i<ma_uNUM; i++){
        if(ma_uL[i] > THRESHOLD){
            spikeL++;
        }
    }
    // Update stimuli outputs and directions
    if(spikeL > SP_THRESHOLD) {
        digitalWrite(LED_PIN, HIGH);
    }
	else {
    	digitalWrite(LED_PIN, LOW);
  	}
}

/*
Set rotating direction for each wheels. 1 is forward, -1 is backward 
param fl : Front left wheel
param fr : Front right wheel
param bl : Back left wheel
param br : Back right wheel
*/
void set4wheel_dir(int fl, int fr, int bl, int br) {
	motor_fl.set_direction(fl);  
	motor_fr.set_direction(fr);
	motor_bl.set_direction(bl);
	motor_br.set_direction(br);
}

/*
Set speed (pmw value) for each wheels
param fl : PWM of front left wheel
param fr : PWM of front right wheel
param bl : PWM of back left wheel
param br : PWM of back right wheel
*/
void set4wheel_spd(int fl, int fr, int bl, int br) {
	set_speed1 = fl;
	set_speed2 = fr;
	set_speed3 = bl;
	set_speed4 = br;
	pid_fl.Compute();
	pid_fr.Compute();
	pid_bl.Compute();
	pid_br.Compute();
}

/*
Stop all the wheels by setting speed = 0
*/
void stop(){
	motor_fl.set_speed(0);
	motor_fr.set_speed(0);
	motor_bl.set_speed(0);
	motor_br.set_speed(0);
}

/*
Pulse counting event called by the interupts
*/
void update_enc1(){
	motor_fl.update_count();}

void update_enc2(){
	motor_fr.update_count();}

void update_enc3(){
	motor_bl.update_count();}

void update_enc4(){
	motor_br.update_count();}