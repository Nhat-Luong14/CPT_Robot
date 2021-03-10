/*
  Motor.cpp - Library for controlling motors of cpt robot.
  Created by Duc-Nhat Luong, March 10, 2021.
*/

#include "Arduino.h"
#include "Motor.h"

Motor::Motor(byte enc_pin, byte fwd_pin, byte bwd_pin, byte pwm_pin, double kp, double ki, double kd)
{
  pinMode(enc_pin, INPUT_PULLUP);
  pinMode(fwd_pin, OUTPUT);
  pinMode(bwd_pin, OUTPUT);
  pinMode(pwm_pin, OUTPUT);

  digitalWrite(enc_pin, HIGH); //turn pullup resistor on
  digitalWrite(fwd_pin,0);  //stop motor
  digitalWrite(bwd_pin,0);  //stop motor
  analogWrite(pwm_pin,0);   //stop motor

  _enc_pin = enc_pin;
  _fwd_pin = fwd_pin;
  _bwd_pin = bwd_pin;
  _pwm_pin = pwm_pin;
  _enc_count = 0;
  _kp = kp;
  _ki = ki;
  _kd = kd;
}

void Motor::set_direction(int dir)
{ 
  switch(dir) {
  case 1:
    digitalWrite(_fwd_pin,1);      //run motor run forward ỏ backward I don't know
    digitalWrite(_bwd_pin,0);
    break;
  case -1:
    digitalWrite(_fwd_pin,0);      //run motor run forward ỏ backward I don't know
    digitalWrite(_bwd_pin,1);
    break;
  default:
    break;
  }
}

void Motor::set_speed(int pwm)
{
  analogWrite(_pwm_pin, pwm);
}

void Motor::update_count()
{
  _enc_count += 1;
  // Serial.println(_enc_count);
}

double Motor::get_speed()
{
  double spd; 
  spd = 0.213*_enc_count; //60/562/0.5
  _enc_count = 0;
  return spd;
}

byte Motor::get_enc_pin()
{
  return _enc_pin;
}

double Motor::get_kp()
{
  return _kp;
}

double Motor::get_ki()
{
  return _ki;
}

double Motor::get_kd()
{
  return _kd;
}
