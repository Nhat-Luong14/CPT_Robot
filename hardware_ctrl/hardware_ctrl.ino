#include <PID_v1.h>

const byte enc_fr = 18 ; //for encoder pulse 
const byte fwd_fr = 3;    //for H-bridge: run motor forward
const byte bwd_fr = 2;    //for H-bridge: run motor backward
const byte pwm_fr = 10;   //for H-bridge: motor speed

const byte enc_fl = 19 ; //for encoder pulse A
const byte fwd_fl = 4;    //for H-bridge: run motor forward
const byte bwd_fl = 5;    //for H-bridge: run motor backward
const byte pwm_fl = 11;   //for H-bridge: motor speed

const byte enc_rr = 20 ; //for encoder pulse A
const byte fwd_rr = 6;    //for H-bridge: run motor forward
const byte bwd_rr = 7;    //for H-bridge: run motor backward
const byte pwm_rr = 12;   //for H-bridge: motor speed

const byte enc_rl = 21 ; //for encoder pulse A
const byte fwd_rl = 9;    //for H-bridge: run motor forward
const byte bwd_rl = 8;    //for H-bridge: run motor backward
const byte pwm_rl = 13;   //for H-bridge: motor speed

int encoder = 0;
double out_speed = 0, set_speed = 0, output = 0;
int timer1_counter; //for timer

//Specify the links and initial tuning parameters
//double kp=0.6, ki=2.5, kd=0; //for FR
double kp=0.6, ki=2.5, kd=0; //for FL
//double kp=4, ki=0, kd=0;    //for RR
PID myPID(&out_speed, &output, &set_speed, kp, ki, kd, DIRECT);  


void setup() {  
  pinMode(enc_fr,INPUT_PULLUP);
  pinMode(fwd_fr,OUTPUT);
  pinMode(bwd_fr,OUTPUT);
  pinMode(pwm_fr,OUTPUT);

  pinMode(enc_fl,INPUT_PULLUP);
  pinMode(fwd_fl,OUTPUT);
  pinMode(bwd_fl,OUTPUT);
  pinMode(pwm_fl,OUTPUT);

  pinMode(enc_rr,INPUT_PULLUP);
  pinMode(fwd_rr,OUTPUT);
  pinMode(bwd_rr,OUTPUT);
  pinMode(pwm_rr,OUTPUT);

  pinMode(enc_rl,INPUT_PULLUP);
  pinMode(fwd_rl,OUTPUT);
  pinMode(bwd_rl,OUTPUT);
  pinMode(pwm_rl,OUTPUT);
  
  digitalWrite(enc_fr, HIGH); //turn pullup resistor on
  digitalWrite(fwd_fr,0);  //stop motor
  digitalWrite(bwd_fr,0);  //stop motor
  analogWrite(pwm_fr,0);   //stop motor
  
  digitalWrite(enc_fl, HIGH); //turn pullup resistor on
  digitalWrite(fwd_fl,0);  //stop motor
  digitalWrite(bwd_fl,0);  //stop motor
  analogWrite(pwm_fl,0);   //stop motor
  
  digitalWrite(enc_rr, HIGH); //turn pullup resistor on
  digitalWrite(fwd_rr,0);  //stop motor
  digitalWrite(bwd_rr,0);  //stop motor
  analogWrite(pwm_rr,0);   //stop motor
  
  digitalWrite(enc_rl, HIGH); //turn pullup resistor on
  digitalWrite(fwd_rl,0);  //stop motor
  digitalWrite(bwd_rl,0);  //stop motor
  analogWrite(pwm_rl,0);   //stop motor
  
  attachInterrupt(digitalPinToInterrupt(enc_fr), detect_a, RISING);
//  attachInterrupt(digitalPinToInterrupt(enc_fr), detect_a, RISING);
//  attachInterrupt(digitalPinToInterrupt(enc_rr), detect_a, RISING);
//  attachInterrupt(digitalPinToInterrupt(enc_rl), detect_a, RISING);
  
  // start serial port at 9600 bps:
  Serial.begin(9600);
  
  //--------------------------timer setup
  noInterrupts();           // disable all interrupts
  TCCR1A = 0;
  // TCCR1B = 0;
  TCCR1B = TCCR1B & 0b11111000 | 1; // set 31KHz PWM to prevent motor noise
  timer1_counter = 59286;           // preload timer 65536-16MHz/256/2Hz (34286 for 0.5sec) (59286 for 0.1sec)

  TCNT1 = timer1_counter;   // preload timer
  TCCR1B |= (1 << CS12);    // 256 prescaler 
  TIMSK1 |= (1 << TOIE1);   // enable timer overflow interrupt
  interrupts();             // enable all interrupts
  //--------------------------timer setup

  myPID.SetMode(AUTOMATIC);   //set PID in Auto mode
  myPID.SetSampleTime(100);  // refresh rate of PID controller in ms
  myPID.SetOutputLimits(0, 255); // this is the MAX PWM value to move motor, here change in value reflect change in speed of motor.
}


void loop() {
  set_speed = 65;
  digitalWrite(fwd_rr,0);      //run motor run forward ỏ backward I don't know
  digitalWrite(bwd_rr,1);
  
  digitalWrite(fwd_fr,0);      //run motor run forward ỏ backward I don't know
  digitalWrite(bwd_fr,1);
  
  digitalWrite(fwd_rl,0);      //run motor run forward ỏ backward I don't know
  digitalWrite(bwd_rl,1);
  
  digitalWrite(fwd_fl,0);      //run motor run forward ỏ backward I don't know
  digitalWrite(bwd_fl,1);
  myPID.Compute();
  analogWrite(pwm_fr, 180);
}


//increasing encoder at new pulse
void detect_a() {
  encoder+=1;
}


ISR(TIMER1_OVF_vect) {        // interrupt service routine - tick every 0.1sec
  TCNT1 = timer1_counter;     // set timer
  out_speed = 1.6*encoder;     //calculate motor speed, unit is rpm (60/75/0.5) This increase the speed
  encoder=0;
  Serial.print("speed: ");
  Serial.println(out_speed );  
  Serial.println(output ); 
}
