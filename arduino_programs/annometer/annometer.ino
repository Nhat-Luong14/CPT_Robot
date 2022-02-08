/* 
This code is created by Duc-Nhat Luong 

This code demonstrate communication between Arduino and Wind sensor 
using software serial. Wind data is read and published to ROS network
*/

#include <SoftwareSerial.h>
#include <ros.h>
#include <olfaction_msgs/anemometer.h>

SoftwareSerial windSerial(10,11);

ros::NodeHandle nh;
olfaction_msgs::anemometer wind_msg;
ros::Publisher chatter("chatter", &wind_msg);

void setup() {
    nh.initNode();
    nh.advertise(chatter);
    
    windSerial.begin(19200);    //Default is 9600. windSerial.write("$01BR1*//\r\n"); to change to 119200
    Serial.begin(9600);
    delay(6000);

    //SET communication interface of the sensor to UART
    windSerial.write("$01CIU*//\r\n");
    delay(2000);
    
    //QUERY to check if the communicaiton protocol is set or not
    windSerial.write("$01CI?*//\r\n");
    delay(1000);

    //Disable compass
    windSerial.write("$01CFD*//\r\n");
    delay(1000);
}

void loop() {
    String storedData = "";
    //send query for WIND speed and direction
    windSerial.write("$//WV?*//\r\n");
    while (windSerial.available()) {
        char inChar = windSerial.read();
        storedData += inChar;
    }
    
    double spd, dir;
    char str1 [10], str2 [10];
    sscanf(storedData.c_str(),"%[^=]= %lf, %lf, %[^,],", str1, &spd, &dir, str2);
    
    if (dir <= 180.0 ) {
        dir = dir * M_PI / 180.0; // convert rad to degrees
    }
    else {
        dir = (dir - 360.0)* M_PI / 180.0; // convert rad to degrees
    }
    wind_msg.header.stamp = nh.now();  
    wind_msg.header.frame_id = "/anemometer_frame";
    wind_msg.sensor_label = "1";
    wind_msg.wind_speed = spd;
    wind_msg.wind_direction = dir;
    
    chatter.publish( &wind_msg );
    nh.spinOnce();
    delay(200);
}

double getSpeed(const char *str) {
  while (!(*str >= '0' && *str <= '9') && (*str != '-') && (*str != '+')) str++;
  int number;
  if (sscanf(str, "%d", &number) == 1) {
    return number;
  }
  return -1; 
}