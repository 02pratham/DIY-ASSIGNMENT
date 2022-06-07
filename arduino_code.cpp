// C++ code
//
#include <Servo.h>

int face_recognition = 0;

int var = 0;

int unnamed = 0;

int i = 0;

int j = 0;

int k = 0;

Servo servo_9;

void setup()
{
  servo_9.attach(9, 500, 2500);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  face_recognition = 1;
  servo_9.write(0);
  if (face_recognition == 1) {
    servo_9.write(90);
    delay(5000); // Wait for 5000 millisecond(s)
    servo_9.write(0);
    delay(5000); // Wait for 5000 millisecond(s)
    j = 0;
  }
}

void loop()
{
  if (face_recognition == 1) {
    var = (j % 6);
    j = (j + 1);
    if (var == 0) {
      digitalWrite(10, LOW);
    }
    if (var == 1) {
      digitalWrite(11, HIGH);
      digitalWrite(12, LOW);
      digitalWrite(13, LOW);
    }
    if (var == 2) {
      digitalWrite(12, HIGH);
      digitalWrite(11, LOW);
      digitalWrite(13, LOW);
    }
    if (var == 3) {
      digitalWrite(12, LOW);
      digitalWrite(11, LOW);
      digitalWrite(13, HIGH);
    }
    if (var == 4) {
      digitalWrite(12, LOW);
      digitalWrite(11, LOW);
      digitalWrite(13, LOW);
    }
    if (var == 5) {
      digitalWrite(10, HIGH);
    }
    if (var == 5) {
      digitalWrite(10, HIGH);
    }
  }
  delay(5000); // Wait for 5000 millisecond(s)
}