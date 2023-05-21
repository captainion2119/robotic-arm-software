#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <math.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Servo motor parameters
const int numServos = 12;  // Total number of servos
const int servoPins[numServos] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};  // PWM pins connected to the servo motors
const int servoAngles[numServos] = {90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90};  // Initial angles for each servo

// Arm parameters
const int arm1ServoStartIndex = 0;  // Starting index of arm 1 servos
const int arm2ServoStartIndex = 6;  // Starting index of arm 2 servos
const float L1 = 10.0;  // Length of arm segment 1
const float L2 = 10.0;  // Length of arm segment 2
const float L3 = 10.0;  // Length of arm segment 3
// int updtx, updty, updtz;
float arm1X, arm1Y, arm1Z;
float arm2X, arm2Y, arm2Z;

void setup() {
  Serial.begin(115200);

  pwm.begin();
  pwm.setPWMFreq(60);

  for (int i = 0; i < numServos; i++) {
    setServoAngle(i, servoAngles[i]);
  }
}

void loop() {
  if (Serial.available()) {
    String ReadData = Serial.readStringUntil('\n');
    ReadData.trim();
    if (ReadData == "Ping") {
      Serial.print("Pong");
    } else if (ReadData == "1curpos") {
      Serial.print("001002003");
    } else if (ReadData == "2curpos") {
      Serial.print("004005006");
    }else if (ReadData.toInt() >= 10) {
      // 1001002003
      int arm = ReadData.substring(0, 1).toInt();
      int x = ReadData.substring(1, 4).toInt();
      int y = ReadData.substring(4, 7).toInt();
      int z = ReadData.substring(7).toInt();
      moveToPosition(arm, x, y, z);
    } else if (ReadData == "end") {
      Serial.print("End");
    }
  }
}

void setServoAngle(int servoNum, int angle) {
  int pulseWidth = map(angle, 0, 180, 150, 600);  // Convert angle to pulse width
  pwm.setPWM(servoPins[servoNum], 0, pulseWidth);
}

void moveToPosition(int armNum, float x, float y, float z) {
  int servoStartIndex;
  float L;

  if (armNum == 1) {
    servoStartIndex = arm1ServoStartIndex;
    L = L1;
    arm1X = x;
    arm1Y = y;
    arm1Z = z;
  } else if (armNum == 2) {
    servoStartIndex = arm2ServoStartIndex;
    L = L2;
    arm2X = x;
    arm2Y = y;
    arm2Z = z;
  }

  // Calculate the inverse kinematics angles
  float theta1 = atan2(y, x) * 180.0 / PI;
  float r = sqrt(x * x + y * y);
  float D = (z * z + r * r - L * L - L3 * L3) / (2 * L * L3);
  float theta2 = acos(D) * 180.0 / PI;
  float D1 = (L3 * sin(theta2 * PI / 180.0)) / (sqrt(L * L + L3 * L3 + 2 * L * L3 * cos(theta2 * PI / 180.0)));
  float theta3 = atan2(z, D1) * 180.0 / PI;

  // Move the servos to the calculated angles
  setServoAngle(servoStartIndex, theta1);
  setServoAngle(servoStartIndex + 1, theta2);
  setServoAngle(servoStartIndex + 2, theta3);

  // updtx = x;
  // updty = y;
  // updtz = z;
}

void getCurPos(int arm) {
  // Convert the current (x, y, z) coordinates of the specified arm to strings with leading zeros if necessary
  String xStr, yStr, zStr;
  if (arm == 1) {
    xStr = String(arm1X, 10);
    while (xStr.length() < 3) {
      xStr = "0" + xStr;
    }
    yStr = String(arm1Y, 10);
    while (yStr.length() < 3) {
      yStr = "0" + yStr;
    }
    zStr = String(arm1Z, 10);
    while (zStr.length() < 3) {
      zStr = "0" + zStr;
    }
  } else if (arm == 2) {
    xStr = String(arm2X, 10);
    while (xStr.length() < 3) {
      xStr = "0" + xStr;
    }
    yStr = String(arm2Y, 10);
    while (yStr.length() < 3) {
      yStr = "0" + yStr;
    }
    zStr = String(arm2Z, 10);
    while (zStr.length() < 3) {
      zStr = "0" + zStr;
    }
  } else {
    // Invalid arm number
    Serial.println("Invalid arm number");
    return;
  }

  // DEBUG CODE:
  // xStr = "020";
  // yStr = "007";
  // zStr = "100";

  // Print the current position of the specified arm in the format "XXXYYYZZZ"
  Serial.print(xStr);
  Serial.print(yStr);
  Serial.print(zStr);
  Serial.print("\n");
}