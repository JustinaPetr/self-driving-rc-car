#include<AFMotor.h>
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
byte input;

void setup()
{
 motor1.setSpeed(255);
 motor2.setSpeed(255);
 Serial.begin(9600);
}

void forward()
{
 motor1.run(FORWARD);
 motor2.run(RELEASE);
}
void backward()//
{
 motor1.run(BACKWARD);
 motor2.run(RELEASE);
}
void left()//
{
 motor1.run(FORWARD);
 motor2.run(BACKWARD);
}
void right()//
{
 motor1.run(FORWARD);
 motor2.run(FORWARD);
}
void my_stop()//
{
 motor1.run(RELEASE);
 motor2.run(RELEASE);

}

void loop()
{
 input = Serial.read();

 if (input == 'F') 
 {
     forward(); 
 }
 if (input == 'B')
 {
     backward();
 }
 if (input == 'L') 
 {
     left();
 }
 if (input == 'R')
 {
     right();
 }
 if (input == 'S')
   my_stop();
}

