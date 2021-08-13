void mpu_init() {
  
  mpu.begin();
  mpu.calibrateGyro();
  
}

void gyro_read(){
  
  digitalWrite(15,HIGH);
  
  timer = millis();
  Vector norm = mpu.readNormalizeGyro();
  
  P_ROTATE = P_ROTATE + norm.YAxis * timeStep;
  Firebase.pushFloat(path + "/Rotation_Roll", R_ROTATE);
  Serial.print("Roll = ");
  Serial.print(P_ROTATE);
  
  R_ROTATE = R_ROTATE + norm.XAxis * timeStep;
  Firebase.pushFloat(path + "/Rotation_Pitch",P_ROTATE);
  Serial.print(" Pitch = ");
  Serial.print(R_ROTATE);
  
  Y_ROTATE = Y_ROTATE + norm.ZAxis * timeStep;
  Firebase.pushFloat(path + "/Rotation_Yaw", Y_ROTATE);
  Serial.print(" Yaw = ");
  Serial.println(Y_ROTATE);
}

void mpu_read() {
  
  Vector normAccel = mpu.readNormalizeAccel();

  float X_ACCEL = normAccel.XAxis;
  Firebase.pushFloat(path + "/Acceleration_X", X_ACCEL);
  Serial.print("X = ");
  Serial.print(X_ACCEL);
  
  float Y_ACCEL = normAccel.YAxis;
  Firebase.pushFloat(path + "/Acceleration_Y", Y_ACCEL);
  Serial.print(" Y = ");
  Serial.print(normAccel.YAxis);
  
  float Z_ACCEL = normAccel.ZAxis;
  Firebase.pushFloat(path + "/Acceleration_Z", Z_ACCEL);
  Serial.print(" Z = ");
  Serial.println(normAccel.ZAxis);

  /*
  //Vector normAccel = mpu.readNormalizeAccel();
  Serial.print(" Xnorm = ");
  Serial.print(normAccel.XAxis);
  Serial.print(" Ynorm = ");
  Serial.print(normAccel.YAxis);
  Serial.print(" Znorm = ");
  Serial.println(normAccel.ZAxis);
  */
  
}
