/**
 * @file wind_sensor.ino
 *
 * @brief This code demonstrate communication between Arduino and Wind sensor (FT205EV)
 * using software serial. Wind data is read and published to ROS network
 *
 * @author Luong Duc Nhat
 * Contact: luong.d.aa@m.titech.ac.jp
 * 
 * @copyright Copyright 2021, The Chemical Plume Tracing (CPT) Robot Project"
 * credits ["Luong Duc Nhat"]
 */


#include <SoftwareSerial.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <olfaction_msgs/anemometer.h>

SoftwareSerial windSerial(10,11);

ros::NodeHandle nh;
std_msgs::String msg;
ros::Publisher chatter("chatter", &msg);

void setup() {
    nh.initNode();
    nh.advertise(chatter);
    
    windSerial.begin(9600);     //baud rate of 9600 baud is Factory Default Setting
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

    //SET baud rate to 19200
    //The new baud rate will be only valid in next powered-up or after a Reset command (RSU) 
    windSerial.write("$01BR1*//\r\n");  
    delay(2000);
}

void loop() {
    String storedData = "";
    //send query for WIND speed and direction
    windSerial.write("$//WV?*//\r\n");
    while (windSerial.available()) {
        char inChar = windSerial.read();
        storedData += inChar;
    }
    msg.data = storedData.c_str();
    chatter.publish( &msg );
    nh.spinOnce();
    delay(200);
}