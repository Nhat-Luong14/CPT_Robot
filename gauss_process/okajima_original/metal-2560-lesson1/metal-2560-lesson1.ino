/*  ___   ___  ___  _   _  ___   ___   ____ ___  ____
   / _ \ /___)/ _ \| | | |/ _ \ / _ \ / ___) _ \|    \
  | |_| |___ | |_| | |_| | |_| | |_| ( (__| |_| | | | |
   \___/(___/ \___/ \__  |\___/ \___(_)____)___/|_|_|_|
                    (____/
   Arduino Mecanum Omni Direction Wheel Robot Car
   Tutorial URL http://osoyoo.com/?p=30022
   CopyRight www.osoyoo.com

   After running the code, smart car will
   go forward and go backward for 2 seconds,
   left turn and right turn for 2 seconds,
   right shift and left shift for 2 seconds,
   left diagonal back and right diagonal forward for 2 seconds,
   left diagonal forward and right diagonal back for 2 seconds,
   then stop.

*/
///////////////#define SPEED 75
///////////////#define TURN_SPEED 90
float SPEED = 90;

#define speedPinR 9   //  Front Wheel PWM pin connect Right MODEL-X ENA 
#define RightMotorDirPin1  22    //Front Right Motor direction pin 1 to Right MODEL-X IN1  (K1)
#define RightMotorDirPin2  24   //Front Right Motor direction pin 2 to Right MODEL-X IN2   (K1)                                 
#define LeftMotorDirPin1  26    //Front Left Motor direction pin 1 to Right MODEL-X IN3 (K3)
#define LeftMotorDirPin2  28   //Front Left Motor direction pin 2 to Right MODEL-X IN4 (K3)
#define speedPinL 10   //  Front Wheel PWM pin connect Right MODEL-X ENB

#define speedPinRB 11   //  Rear Wheel PWM pin connect Left MODEL-X ENA 
#define RightMotorDirPin1B  5    //Rear Right Motor direction pin 1 to Left  MODEL-X IN1 ( K1)
#define RightMotorDirPin2B 6    //Rear Right Motor direction pin 2 to Left  MODEL-X IN2 ( K1) 
#define LeftMotorDirPin1B 7    //Rear Left Motor direction pin 1 to Left  MODEL-X IN3  (K3)
#define LeftMotorDirPin2B 8  //Rear Left Motor direction pin 2 to Left  MODEL-X IN4 (K3)
#define speedPinLB 12    //  Rear Wheel PWM pin connect Left MODEL-X ENB

//float kkk;
int i = 0;
#define GasSensor A0
float Gsens = 0.0;
char *p;
String Pos;
String data_array[10];
String data_string;
int data_len;
String p_string;
float x, y, v1, v2, v3, v4;
int kk, oo, pp, qq;

/*motor control*/
void go_advance(int speed) {
  RL_fwd(speed);
  RR_fwd(speed);
  FR_fwd(speed);
  FL_fwd(speed);
}
void go_back(int speed) {
  RL_bck(speed);
  RR_bck(speed);
  FR_bck(speed);
  FL_bck(speed);
}
void right_shift(int speed_fl_fwd, int speed_rl_bck , int speed_rr_fwd, int speed_fr_bck) {
  FL_fwd(speed_fl_fwd);
  RL_bck(speed_rl_bck);
  RR_fwd(speed_rr_fwd);
  FR_bck(speed_fr_bck);
}
void left_shift(int speed_fl_bck, int speed_rl_fwd , int speed_rr_bck, int speed_fr_fwd) {
  FL_bck(speed_fl_bck);
  RL_fwd(speed_rl_fwd);
  RR_bck(speed_rr_bck);
  FR_fwd(speed_fr_fwd);
}

void FR_fwd(int speed)  //front-right wheel forward turn
{
  digitalWrite(RightMotorDirPin1, HIGH);
  digitalWrite(RightMotorDirPin2, LOW);
  analogWrite(speedPinR, speed);
}
void FR_bck(int speed) // front-right wheel backward turn
{
  digitalWrite(RightMotorDirPin1, LOW);
  digitalWrite(RightMotorDirPin2, HIGH);
  analogWrite(speedPinR, speed);
}
void FL_fwd(int speed) // front-left wheel forward turn
{
  digitalWrite(LeftMotorDirPin1, HIGH);
  digitalWrite(LeftMotorDirPin2, LOW);
  analogWrite(speedPinL, speed);
}
void FL_bck(int speed) // front-left wheel backward turn
{
  digitalWrite(LeftMotorDirPin1, LOW);
  digitalWrite(LeftMotorDirPin2, HIGH);
  analogWrite(speedPinL, speed);
}

void RR_fwd(int speed)  //rear-right wheel forward turn
{
  digitalWrite(RightMotorDirPin1B, HIGH);
  digitalWrite(RightMotorDirPin2B, LOW);
  analogWrite(speedPinRB, speed);
}
void RR_bck(int speed)  //rear-right wheel backward turn
{
  digitalWrite(RightMotorDirPin1B, LOW);
  digitalWrite(RightMotorDirPin2B, HIGH);
  analogWrite(speedPinRB, speed);
}
void RL_fwd(int speed)  //rear-left wheel forward turn
{
  digitalWrite(LeftMotorDirPin1B, HIGH);
  digitalWrite(LeftMotorDirPin2B, LOW);
  analogWrite(speedPinLB, speed);
}
void RL_bck(int speed)    //rear-left wheel backward turn
{
  digitalWrite(LeftMotorDirPin1B, LOW);
  digitalWrite(LeftMotorDirPin2B, HIGH);
  analogWrite(speedPinLB, speed);
}

void stop_Stop()    //Stop
{
  analogWrite(speedPinLB, 0);
  analogWrite(speedPinRB, 0);
  analogWrite(speedPinL, 0);
  analogWrite(speedPinR, 0);
}




//Pins initialize
void init_GPIO()
{
  pinMode(RightMotorDirPin1, OUTPUT);
  pinMode(RightMotorDirPin2, OUTPUT);
  pinMode(speedPinL, OUTPUT);

  pinMode(LeftMotorDirPin1, OUTPUT);
  pinMode(LeftMotorDirPin2, OUTPUT);
  pinMode(speedPinR, OUTPUT);
  pinMode(RightMotorDirPin1B, OUTPUT);
  pinMode(RightMotorDirPin2B, OUTPUT);
  pinMode(speedPinLB, OUTPUT);

  pinMode(LeftMotorDirPin1B, OUTPUT);
  pinMode(LeftMotorDirPin2B, OUTPUT);
  pinMode(speedPinRB, OUTPUT);

  stop_Stop();
}

void setup()
{
  pinMode(13, OUTPUT);
  Serial1.begin(115200);
  init_GPIO();

  //---------------------------------------------------
//     go_advance(SPEED);
//     delay(1000);
//     stop_Stop();
//     digitalWrite( 13, HIGH );
//     delay(1000);
//  
//     go_back(SPEED);
//     delay(1000);
//     stop_Stop();
//     digitalWrite( 13, LOW );
//     delay(1000);
  //
  //   left_turn(TURN_SPEED);
  //   delay(1000);
  //   stop_Stop();
  //   digitalWrite( 13, HIGH );
  //   delay(1000);
  //
  //   right_turn(TURN_SPEED);
  //   delay(1000);
  //   stop_Stop();
  //   digitalWrite( 13, LOW );
  //   delay(1000);
  //
  //   right_shift(200,200,200,200); //right shift
  //   delay(1000);
  //   stop_Stop();
  //   digitalWrite( 13, HIGH );
  //   delay(1000);
  //
  //   left_shift(200,200,200,200); //left shift
  //   delay(1000);
  //   stop_Stop();
  //   digitalWrite( 13, LOW );
  //   delay(1000);
  //
  //   left_shift(200,0,200,0); //left diagonal back
  //   delay(1000);
  //   stop_Stop();
  //   digitalWrite( 13, HIGH );
  //   delay(1000);
  //
  //   right_shift(200,0,200,0); //right diagonal ahead
  //   delay(1000);
  //   stop_Stop();
  //   digitalWrite( 13, LOW );
  //   delay(1000);
  //
  //   left_shift(0,200,0,200); //left diagonal ahead
  //   delay(1000);
  //   stop_Stop();
  //   digitalWrite( 13, HIGH );
  //   delay(1000);
  //
  //   right_shift(0,200,0,200); //right diagonal back
  //   delay(1000);
  //   stop_Stop();
  //   digitalWrite( 13, LOW );
  //   delay(1000);
  //---------------------------------------------------

}

void loop() {
  if (Serial1.available()) {
    String str = Serial1.readStringUntil('&');  //pythonからの信号受信

    int check = (str.indexOf(",")); //str.indexOf( )　 関数でカンマの位置が判りました
    String data = (str.substring(0, check)); //x移動量=横方向
    String data2 = (str.substring(check + 1)); //y移動量=前進方向
    x = data.toDouble();
    y = -1 * (data2.toDouble());

    v1 = 1 / sqrt(2) * (-x/0.4 + y/0.4); //各ホイールの回転速度  ::/0.4はコントロール周期
    v2 = -1 / sqrt(2) * (x/0.4 + y/0.4);
    v3 = 1 / sqrt(2) * (x/0.4 - y/0.4);
    v4 = 1 / sqrt(2) * (x/0.4 + y/0.4);


    //-------------------------------------------------------------------
    if (data.toFloat() == 1000) {

      Gsens = analogRead(GasSensor); // sensor値を取得
      Gsens = 5.0 * Gsens / 1023;  //voltage
      Serial1.println(Gsens);  //pythonへsensor値を送信
    }
    else if (data.toFloat() == 111) {
      stop_Stop();
    }
    else {
      //---------------------------
      //motor movement order. write down here
      //-------------------------------------------------------------------
      if (v1 > 0) {
        kk = 1;
      }
      else if (v1 < 0) {
        kk = 2;
      }

      if (v2 > 0) {
        oo = 1;
      }
      else if (v2 < 0) {
        oo = 2;
      }

      if (v3 > 0) {
        pp = 1;
      }
      else if (v3 < 0) {
        pp = 2;
      }

      if (v4 > 0) {
        qq = 1;
      }
      else if (v4 < 0) {
        qq = 2;
      }
      //-------------------------------------------------------------------
      if ((kk == 1) && (oo == 1) && (pp == 1) && (qq == 1)) {
        FR_fwd(abs(v1)+SPEED);
        FL_bck(abs(v2)+SPEED);
        RL_bck(abs(v3)+SPEED);
        RR_fwd(abs(v4)+SPEED);
      }
      else if ((kk == 1) && (oo == 1) && (pp == 1) && (qq == 2)) {
        FR_fwd(abs(v1)+SPEED);
        FL_bck(abs(v2)+SPEED);
        RL_bck(abs(v3)+SPEED);
        RR_bck(abs(v4)+SPEED);
      }
      else if ((kk == 1) && (oo == 1) && (pp == 2) && (qq == 1)) {
        FR_fwd(abs(v1)+SPEED);
        FL_bck(abs(v2)+SPEED);
        RL_fwd(abs(v3)+SPEED);
        RR_fwd(abs(v4)+SPEED);
      }
      else if ((kk == 1) && (oo == 1) && (pp == 2) && (qq == 2)) {
        FR_fwd(abs(v1)+SPEED);
        FL_bck(abs(v2)+SPEED);
        RL_fwd(abs(v3)+SPEED);
        RR_bck(abs(v4)+SPEED);
      }
      else if ((kk == 1) && (oo == 2) && (pp == 1) && (qq == 1)) {
        FR_fwd(abs(v1)+SPEED);
        FL_fwd(abs(v2)+SPEED);
        RL_bck(abs(v3)+SPEED);
        RR_fwd(abs(v4)+SPEED);
      }
      else if ((kk == 1) && (oo == 2) && (pp == 1) && (qq == 2)) {
        FR_fwd(abs(v1)+SPEED);
        FL_fwd(abs(v2)+SPEED);
        RL_bck(abs(v3)+SPEED);
        RR_bck(abs(v4)+SPEED);
      }
      else if ((kk == 1) && (oo == 2) && (pp == 2) && (qq == 1)) {
        FR_fwd(abs(v1)+SPEED);
        FL_fwd(abs(v2)+SPEED);
        RL_fwd(abs(v3)+SPEED);
        RR_fwd(abs(v4)+SPEED);
      }
      else if ((kk == 1) && (oo == 2) && (pp == 2) && (qq == 2)) {
        FR_fwd(abs(v1)+SPEED);
        FL_fwd(abs(v2)+SPEED);
        RL_fwd(abs(v3)+SPEED);
        RR_bck(abs(v4)+SPEED);
      }
      else if ((kk == 2) && (oo == 1) && (pp == 1) && (qq == 1)) {
        FR_bck(abs(v1)+SPEED);
        FL_bck(abs(v2)+SPEED);
        RL_bck(abs(v3)+SPEED);
        RR_fwd(abs(v4)+SPEED);
      }
      else if ((kk == 2) && (oo == 1) && (pp == 1) && (qq == 2)) {
        FR_bck(abs(v1)+SPEED);
        FL_bck(abs(v2)+SPEED);
        RL_bck(abs(v3)+SPEED);
        RR_bck(abs(v4)+SPEED);
      }
      else if ((kk == 2) && (oo == 1) && (pp == 2) && (qq == 1)) {
        FR_bck(abs(v1)+SPEED);
        FL_bck(abs(v2)+SPEED);
        RL_fwd(abs(v3)+SPEED);
        RR_fwd(abs(v4)+SPEED);
      }
      else if ((kk == 2) && (oo == 1) && (pp == 2) && (qq == 2)) {
        FR_bck(abs(v1)+SPEED);
        FL_bck(abs(v2)+SPEED);
        RL_fwd(abs(v3)+SPEED);
        RR_bck(abs(v4)+SPEED);
      }
      else if ((kk == 2) && (oo == 2) && (pp == 1) && (qq == 1)) {
        FR_bck(abs(v1)+SPEED);
        FL_fwd(abs(v2)+SPEED);
        RL_bck(abs(v3)+SPEED);
        RR_fwd(abs(v4)+SPEED);
      }
      else if ((kk == 2) && (oo == 2) && (pp == 1) && (qq == 2)) {
        FR_bck(abs(v1)+SPEED);
        FL_fwd(abs(v2)+SPEED);
        RL_bck(abs(v3)+SPEED);
        RR_bck(abs(v4)+SPEED);
      }
      else if ((kk == 2) && (oo == 2) && (pp == 2) && (qq == 1)) {
        FR_bck(abs(v1)+SPEED);
        FL_fwd(abs(v2)+SPEED);
        RL_fwd(abs(v3)+SPEED);
        RR_fwd(abs(v4)+SPEED);
      }
      else if ((kk == 2) && (oo == 2) && (pp == 2) && (qq == 2)) {
        FR_bck(abs(v1)+SPEED);
        FL_fwd(abs(v2)+SPEED);
        RL_fwd(abs(v3)+SPEED);
        RR_bck(abs(v4)+SPEED);
      }
      //---------------------------
      //      go_advance(SPEED);

      Gsens = analogRead(GasSensor); // sensor値を取得
      Gsens = 5.0 * Gsens / 1023;  //voltage
      Serial1.println(Gsens);  //pythonへsensor値を送信
    }
    //-------------------------------------------------------------------



    //------------------------------------------------
    //    Serial1.print(data.toFloat());
    //    Serial1.print(',');
    //    Serial1.println(data2.toFloat());  //pythonへsensor値を送信
    //------------------------------------------------


    //    Serial1.println(str.toFloat());


    //    Gsens = analogRead(GasSensor);  // sensor値を取得
    //    Gsens = 5.0 * Gsens / 1023; //voltage
    //    Serial1.println(Gsens+10.2);  //pythonへsensor値を送信


    //     float c = Serial1.parseFloat();
    //     Serial1.println(c);
  }

  //      Serial1.print(2.5321);
  //      Serial1.write(2);
}
