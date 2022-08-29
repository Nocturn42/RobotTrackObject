#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>

#include <MeMCore.h>

MeDCMotor motor_9(9);
MeDCMotor motor_10(10);
unsigned char table[5] = {0};
int velocity = 0;
int dir = 0;
void move(int direction, int speed)
{     
      int leftSpeed = 0;
      int rightSpeed = 0;
      if(direction == 0){
        leftSpeed = 0;
        rightSpeed = 0;
      }
      else if(direction == 1){
          leftSpeed = 150+speed;
          rightSpeed = 150-speed;
      }else if(direction == 2){
          leftSpeed = -150+speed;
          rightSpeed = -150-speed;
      }
      
      motor_9.run((9)==M1?-(leftSpeed):(leftSpeed));
      motor_10.run((10)==M1?-(rightSpeed):(rightSpeed));
}

void setup()
{
   Serial.begin(57600);

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
      
      velocity = table[2];
      sign = table[3];
      dir = table[4];
     if(sign==1){
       velocity = -velocity;
     }
     
   }
  }
  move(dir, velocity);   
}
