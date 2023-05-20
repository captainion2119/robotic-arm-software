// #include <Wire.h>
// #include <Adafruit_PWMServoDriver.h>
// #include <math.h>

// Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// // Servo motor parameters
// const int numServos = 12;  // Total number of servos
// const int servoPins[numServos] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};  // PWM pins connected to the servo motors
// const int servoAngles[numServos] = {90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90};  // Initial angles for each servo

// // Arm parameters
// const int arm1ServoStartIndex = 0;  // Starting index of arm 1 servos
// const int arm2ServoStartIndex = 6;  // Starting index of arm 2 servos
// const float L1 = 10.0;  // Length of arm segment 1
// const float L2 = 10.0;  // Length of arm segment 2
// const float L3 = 10.0;  // Length of arm segment 3
// int updtx, updty, updtz;

// void setup() {
//   Serial.begin(115200);

//   pwm.begin();
//   pwm.setPWMFreq(60);

//   for (int i = 0; i < numServos; i++) {
//     setServoAngle(i, servoAngles[i]);
//   }
// }

// void loop() {
//   if (Serial.available()) {
//     String ReadData = Serial.readStringUntil('\n');
//     ReadData.trim();
//     if (ReadData == "Ping") {
//       Serial.print("Pong");
//     } else if (ReadData.toInt() >= 10) {
//       // 1001002003
//       int arm = ReadData.substring(0, 1).toInt();
//       int x = ReadData.substring(1, 4).toInt();
//       int y = ReadData.substring(4, 7).toInt();
//       int z = ReadData.substring(7).toInt();
//       moveToPosition(arm, x, y, z);
//     } else if (ReadData == "end") {
//       Serial.print("End");
//     } else if (ReadData.toInt() >= 7) {
//       int arm = ReadData.substring(0, 1).toInt();
//       if (arm == 1) {
//         //Serial.print(getArmPos(arm))
//       } else {
//         //Serial.print(getArmPos(arm))
//       }
//     }
//   }
// }

// void setServoAngle(int servoNum, int angle) {
//   int pulseWidth = map(angle, 0, 180, 150, 600);  // Convert angle to pulse width
//   pwm.setPWM(servoPins[servoNum], 0, pulseWidth);
// }

// void moveToPosition(int armNum, float x, float y, float z) {
//   int servoStartIndex;
//   float L;

//   if (armNum == 1) {
//     servoStartIndex = arm1ServoStartIndex;
//     L = L1;
//   } else if (armNum == 2) {
//     servoStartIndex = arm2ServoStartIndex;
//     L = L2;
//   }

//   // Calculate the inverse kinematics angles
//   float theta1 = atan2(y, x) * 180.0 / PI;
//   float r = sqrt(x * x + y * y);
//   float D = (z * z + r * r - L * L - L3 * L3) / (2 * L * L3);
//   float theta2 = acos(D) * 180.0 / PI;
//   float D1 = (L3 * sin(theta2 * PI / 180.0)) / (sqrt(L * L + L3 * L3 + 2 * L * L3 * cos(theta2 * PI / 180.0)));
//   float theta3 = atan2(z, D1) * 180.0 / PI;

//   // Move the servos to the calculated angles
//   setServoAngle(servoStartIndex, theta1);
//   setServoAngle(servoStartIndex + 1, theta2);
//   setServoAngle(servoStartIndex + 2, theta3);

//   updtx = x;
//   updty = y;
//   updtz = z;
// }