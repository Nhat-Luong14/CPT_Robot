/*
  Motor.h - Library for controlling motors of cpt robot.
  Created by Duc-Nhat Luong, March 10, 2021.
*/

#include "Arduino.h"
#ifndef Motor_h
#define Motor_h

class Motor
{
  public:
    Motor(byte enc_pin, byte fwd_pin, byte bwd_pin, byte pwm_pin, double kp, double ki, double kd);
    void detect_a();
    void set_direction(int dir);
    void set_speed(int pwm);
    void update_count();

    double get_speed();
    double get_kp();
    double get_ki();
    double get_kd();
    byte get_enc_pin();

  private:
    byte _enc_pin;
    byte _fwd_pin;
    byte _bwd_pin;
    byte _pwm_pin;
    double _kp;
    double _ki;
    double _kd;
    int _enc_count;
};

#endif
