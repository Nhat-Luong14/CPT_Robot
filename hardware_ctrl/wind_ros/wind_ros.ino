/* 
This code is created by Duc-Nhat Luong 

This code demonstrate communication between Arduino and Wind sensor 
using software serial. Wind data is read and published to ROS network
*/

#include <SoftwareSerial.h>
#include <ros.h>
#include <std_msgs/String.h>

SoftwareSerial windSerial(10,11);

ros::NodeHandle nh;
std_msgs::String str_msg;
ros::Publisher chatter("chatter", &str_msg);

void setup() {
    nh.initNode();
    nh.advertise(chatter);
    
    windSerial.begin(9600);
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
    str_msg.data = storedData.c_str();
    chatter.publish( &str_msg );
    nh.spinOnce();
    delay(200);
}

