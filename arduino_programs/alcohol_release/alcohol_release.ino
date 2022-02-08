/**
 * @file alcohol_release.ino
 *
 * @brief Program to open and close the solenoid valve at regular intervals.
 * Triggered to start cyclic operation of solenoid valve.
 * Physical switch: Located on digital pin 12
 * Serial command: 'g' for ON, 'q' for OFF
 *
 * @author Luong Duc Nhat
 * Contact: luong.d.aa@m.titech.ac.jp
 * 
 * @copyright Copyright 2021, The Chemical Plume Tracing (CPT) Robot Project"
 * credits ["Luong Duc Nhat"]
 * license GPL
 * 
 * @version    = "1.0.0"
 * maintainer  = "Luong Duc Nhat"
 * status      = "Release"
 */

int period = 1000;	// ms ~ 1Hz
int pulse_width = 200; //ms
bool flag = false;
char cmd = ' ';

void setup() {
  	pinMode(8, OUTPUT); 	//HIGH : Denjiben is open 
  	pinMode(9, OUTPUT); 	//HIGH : LED bright
	digitalWrite(8, LOW);
    digitalWrite(9, LOW);
  	
	Serial.begin(115200);
  	Serial.println("Program Started");
}

void loop() {
 	if (Serial.available() > 0) {
		char cmd = Serial.read();

		if(cmd == 'g'){	
			Serial.print("Running");
			flag = true;
		}
		else if (cmd == 'q') {
			Serial.println("Stopped");
			flag = false;
		}
		else {
			Serial.println("Wrong command");
		}
  	}
  
	if (flag == true) {
		digitalWrite(8, HIGH);
		digitalWrite(9, HIGH);
		delay(pulse_width);

		digitalWrite(8, LOW);
		digitalWrite(9, LOW);
		delay(period-pulse_width);
	}
	else {
		digitalWrite(8, LOW);
		digitalWrite(9, LOW);
		delay(period);
	}
}