#include <PID_v1.h>
#include <Motor.h>

int timer1_counter; //for timer

// param(enc_pin, fwd_pin, bwd_pin, pwm_pin, kp, ki, kd)
Motor motor_fl(18,3,4,2, 1.0, 1.2, 0.02);
Motor motor_fr(19,5,6,7, 1.0, 1.2, 0.02);
Motor motor_bl(20,9,10,8, 1.0, 1.2, 0.02);
Motor motor_br(21,11,13,12, 1.0, 1.2,0.02);

double out_speed1 = 0, set_speed1 = 0, output1 = 0;
double out_speed2 = 0, set_speed2 = 0, output2 = 0;
double out_speed3 = 0, set_speed3 = 0, output3 = 0;
double out_speed4 = 0, set_speed4 = 0, output4 = 0;

PID pid_fl(&out_speed1, &output1, &set_speed1, motor_fl.get_kp(), motor_fl.get_ki(), motor_fl.get_kd(), DIRECT);  
PID pid_fr(&out_speed2, &output2, &set_speed2, motor_fr.get_kp(), motor_fr.get_ki(), motor_fr.get_kd(), DIRECT); 
PID pid_bl(&out_speed3, &output3, &set_speed3, motor_bl.get_kp(), motor_bl.get_ki(), motor_bl.get_kd(), DIRECT); 
PID pid_br(&out_speed4, &output4, &set_speed4, motor_br.get_kp(), motor_br.get_ki(), motor_br.get_kd(), DIRECT); 

void setup() {  
  attachInterrupt(digitalPinToInterrupt(motor_fl.get_enc_pin()), update_enc1, RISING);
  attachInterrupt(digitalPinToInterrupt(motor_fr.get_enc_pin()), update_enc2, RISING);
  attachInterrupt(digitalPinToInterrupt(motor_bl.get_enc_pin()), update_enc3, RISING);
  attachInterrupt(digitalPinToInterrupt(motor_br.get_enc_pin()), update_enc4, RISING);
  
  //--------------------------timer setup
  noInterrupts();           // disable all interrupts
  TCCR5A = 0;
  TCCR5B = TCCR5B & 0b11111000 | 1; // set 31KHz PWM to prevent motor noise
  timer1_counter = 59286;           // preload timer 65536-16MHz/256/2Hz (34286 for 0.5sec) (59286 for 0.1sec)

  TCNT5 = timer1_counter;   // preload timer
  TCCR5B |= (1 << CS12);    // 256 prescaler 
  TIMSK5 |= (1 << TOIE1);   // enable  timer overflow interrupt
  interrupts();             // enable all interrupts
  //--------------------------timer setup

  pid_fl.SetMode(AUTOMATIC);  //set PID in Auto mode
  pid_fr.SetMode(AUTOMATIC);
  pid_bl.SetMode(AUTOMATIC);
  pid_br.SetMode(AUTOMATIC);
  pid_fl.SetSampleTime(20);   // refresh rate of PID controller in ms
  pid_fr.SetSampleTime(20);       
  pid_bl.SetSampleTime(20);
  pid_br.SetSampleTime(20);
  pid_fl.SetOutputLimits(0, 255); // this is the MAX PWM value to move motor, here change in value reflect change in speed of motor.
  pid_fr.SetOutputLimits(0, 255);
  pid_bl.SetOutputLimits(0, 255);
  pid_br.SetOutputLimits(0, 255);
  Serial.begin(115200);
}

void loop() {
  set_speed1 = 50;
  set_speed2 = 50;
  set_speed3 = 50;
  set_speed4 = 50;
  motor_fl.set_direction(-1);  //1:forward, -1: backward
  motor_fr.set_direction(1);
  motor_bl.set_direction(1);
  motor_br.set_direction(-1);
  pid_fl.Compute();
  pid_fr.Compute();
  pid_bl.Compute();
  pid_br.Compute();
  motor_fl.set_speed(output1);
  motor_fr.set_speed(output2);
  motor_bl.set_speed(output3);
  motor_br.set_speed(output4);
}

// interrupt service routine - tick every 0.1sec
ISR(TIMER5_OVF_vect) {        
  TCNT5 = timer1_counter;     
  out_speed1 = motor_fl.get_speed();
  out_speed2 = motor_fr.get_speed();
  out_speed3 = motor_bl.get_speed();
  out_speed4 = motor_br.get_speed();
  Serial.println(out_speed1);  
}

void update_enc1(){
  motor_fl.update_count();}

void update_enc2(){
  motor_fr.update_count();}

void update_enc3(){
    motor_bl.update_count();}

void update_enc4(){
    motor_br.update_count();}
