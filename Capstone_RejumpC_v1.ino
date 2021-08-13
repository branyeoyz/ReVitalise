#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include <MPU6050.h>
#include <Wire.h>
#include <SPI.h>

#define FIREBASE_HOST "rvcapstone-default-rtdb.asia-southeast1.firebasedatabase.app"   // the project name address from firebase id
#define FIREBASE_AUTH "QVmgxFX86Tc6rN4a7TY5O9v0M5dUVMeqlgWLzH6Y"       // the secret key generated from firebase
#define WIFI_SSID "SUTD_LAB"    
#define CLEAR 0                            
// #define WIFI_PASSWORD "20112008"

MPU6050 mpu;

// Gyroscope rotation variables:
unsigned long timer = 0;
float timeStep = 0.01;
float P_ROTATE = 0;
float R_ROTATE = 0;
float Y_ROTATE = 0;

int time1 = 0;


String path = "Data"; //subject to change


void setup() {
  
/* 
   * Initialise RTC module.
   * Take in a date and time.
   * Initialise Firebase.
   * Create an address in Firebase.
   * EEPROM used to store profile instances.
   * time1 = millis();
   * ----------------------
   * Read MPU value 
   * Upload MPU Values into database
*/

  Serial.begin(9600);
  Wire.begin();

  // Insert initialisations here
  firebase_init();
  firebase_value_reset();
  delay(5000);
  mpu_init();

  
  int time1 = millis();
  pinMode(15,OUTPUT);

  
}

void loop() {
    
    int time2 = millis();
    int time_elapsed = time2 - time1;
    Firebase.pushInt(path + "/Timing", time_elapsed);
    //Serial.println("Time(ms): ");
    //Serial.print(time_elapsed);
    
    mpu_read();
    gyro_read();
    firebase_read(); 
  
    delay(100);
    digitalWrite(15,LOW);
}
