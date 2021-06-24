//------------------------------------------------------------------
// This code peform ethanol hit detection using ARX model
// This code is written and modified by Luong Duc Nhat form the CPT Drone 
// project of Cesar Hernandez-Reyes 
//
// Japan, Tokyo Institute of Technology, 2021 June.
// 
// Please referred authors if you reused the code.
//------------------------------------------------------------------
#define GSL_PIN A0    // Gas Sensor Left
#define LED_PIN 12   // LED Indicator

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
double a1 = -0.981;
double a2 = 0.01653;
double b0 = 0.2833;
double b1 = -0.2706;
  
void setup() {
    // put your setup code here, to run once:
    pinMode(LED_PIN, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    getArxValues();
    getStimuli();
    delay(100);
}


/* Shift the array to the right for 1 unit step
param num: size of the array
param val_array: array of value */
void shift_array(double* val_array, int num) {
    for(int i = num-2; i >= 0; i--) {
        val_array[i+1] = val_array[i];
    }
}


/* Calcualte the average of all value in the array
param num: size of the array
param val_array: array of value */
double cal_average(double* val_array, int num) {
    double sum = 0.0;
    for(int i = 0; i < num; i++) {
        sum += val_array[i];
    }
    return sum/num;
}

/* Compute ARX model output for the raw data of gas sensors
param gasSensValL Raw value of left sensor
param gasSensValR Raw value of right sensor */
void getArxValues() {
    //Update moving average gas sensing
    shift_array(yL, yNUM);
    yL[0] = analogRead(GSL_PIN) * (5.0/1023.0); //voltage

    shift_array(ma_yL, ma_yNUM);
    ma_yL[0] = cal_average(yL, yNUM);

    for(int i = ma_yNUM-2; i >= 0; i--){
      dyL[i] = (ma_yL[i] - ma_yL[i+1])/(TS*0.001);
    }

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
    for(int i=0; i<5; i++){
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
