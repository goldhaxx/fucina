#include <Arduino.h>
#include <Wire.h>

// I2C address — 0x68 default, 0x69 if AD0 pin is HIGH
constexpr int MPU_ADDR = 0x68;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Wake up MPU-6050 (exits sleep mode)
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // Set to 0 = wake up
  Wire.endTransmission(true);

  Serial.println("MPU-6050 Accelerometer/Gyroscope Test");
}

void loop() {
  // Request 14 bytes starting from register 0x3B
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 14, true);

  int16_t accel_x = Wire.read() << 8 | Wire.read();
  int16_t accel_y = Wire.read() << 8 | Wire.read();
  int16_t accel_z = Wire.read() << 8 | Wire.read();
  int16_t temp    = Wire.read() << 8 | Wire.read();
  int16_t gyro_x  = Wire.read() << 8 | Wire.read();
  int16_t gyro_y  = Wire.read() << 8 | Wire.read();
  int16_t gyro_z  = Wire.read() << 8 | Wire.read();

  Serial.print("aX="); Serial.print(accel_x);
  Serial.print(" aY="); Serial.print(accel_y);
  Serial.print(" aZ="); Serial.print(accel_z);
  Serial.print(" tmp="); Serial.print(temp / 340.00 + 36.53);
  Serial.print(" gX="); Serial.print(gyro_x);
  Serial.print(" gY="); Serial.print(gyro_y);
  Serial.print(" gZ="); Serial.println(gyro_z);
  delay(1000);
}
