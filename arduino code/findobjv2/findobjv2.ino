#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <MeMCore.h>
byte number = 0;
double angle_rad = PI/180.0;
double angle_deg = 180.0/PI;
MeRGBLed rgbled_7(7, 7==7?2:4);
MeDCMotor motor_9(9);
MeDCMotor motor_10(10);
unsigned char table[5] = {0};

int dir = 0;

void move(int direction)
{
      int leftSpeed = 0;
      int rightSpeed = 0;
      if(direction == 1){
          leftSpeed = 150;
          rightSpeed = 150;
      }else if(direction == 2){
          leftSpeed = -100;
          rightSpeed = -100;
      }else if(direction == 3){
          leftSpeed = 100;
          rightSpeed = 150;
      }else if (direction == 4){
          leftSpeed = 150;
          rightSpeed = 100;
      }else if (direction == 0){
          leftSpeed = 0;
          rightSpeed = 0;
      }
      motor_9.run((9)==M1?-(leftSpeed):(leftSpeed));
      motor_10.run((10)==M1?-(rightSpeed):(rightSpeed));
}
 

  void setup()
  {
     Serial.begin(57600);
     //move(1,0); //程式開始mbot直行
  }


void loop(){
  int readdata = 0, count = 0;
  if (Serial.available()>0)  
  {
    while((readdata = Serial.read()) != (int)-1)
    {
      table[count] = readdata;
      count++;
      delay(5);
    }
    //Procotol: FF 55 data
    if((table[0] == 255) && (table[1] == 85))
    {      
      dir = table[2];
      if(dir == 0){
      move(0);
      }
      if(dir == 1){
        move(1);
      }
      if(dir == 2){
        move(2);
      }
      if(dir == 3){
        move(3);
      }
      if(dir == 4){
        move(4);
      }
     }
     
   }
  
  
}
