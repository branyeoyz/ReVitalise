//Firebase functions need to update the values the MPU values
void firebase_init() {

  // connect to wifi.
  WiFi.begin(WIFI_SSID); //WTFI_PASSWORD if needed
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
    }
    
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void firebase_value_reset()  {
  Firebase.setFloat(path + "/Acceleration_X",0);
  Firebase.setFloat(path + "/Acceleration_Y",0);
  Firebase.setFloat(path + "/Acceleration_Z",0);
  Firebase.setFloat(path + "/Rotation_Pitch",0);
  Firebase.setFloat(path + "/Rotation_Yaw",0);
  Firebase.setFloat(path + "/Rotation_Roll",0);
  Firebase.setFloat(path + "/Timing",0);
  Serial.println("Data cleared");
}

void firebase_read()  {

  #if CLEAR == 1
  Firebase.remove("Data");
  #endif

  if (Firebase.failed()) {
      Serial.print("setting /number failed:");
      digitalWrite(13,HIGH);
      Serial.println(Firebase.error());  
      return;
  }
}

      
