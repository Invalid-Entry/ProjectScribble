#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>

// Define some steppers and the pins the will use\

#define X_STEP_PIN 54
#define X_DIR_PIN 55
#define X_ENABLE_PIN 38

#define Y_STEP_PIN 60
#define Y_DIR_PIN 61
#define Y_ENABLE_PIN 56

#define SERVO_0 11
#define SERVO_1 6
#define SERVO_2 5
#define SERVO_3 4


AccelStepper stepperA(1, X_STEP_PIN, X_DIR_PIN); // 1 = Driver
AccelStepper stepperB(1, Y_STEP_PIN, Y_DIR_PIN); // 1 = Driver
MultiStepper steppers;
Servo myservo; 

long positions[2];

// variabbles used by my program

char incomingByte = ' ';

long a_target = 0;
long b_target = 0;

long temp_value = 0;

bool runrun = false;

int servo_pos = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  stepperA.setMaxSpeed(4000);
  stepperA.setAcceleration(500);
  stepperA.setEnablePin(X_ENABLE_PIN);
 

  stepperB.setMaxSpeed(4000);
  stepperB.setAcceleration(500);
  stepperB.setEnablePin(Y_ENABLE_PIN);

  stepperA.setPinsInverted(false, false, true); //invert logic of enable pin
  stepperA.enableOutputs();

  stepperB.setPinsInverted(false, false, true); //invert logic of enable pin
  stepperB.enableOutputs();

  steppers.addStepper(stepperA);
  steppers.addStepper(stepperB);

  myservo.attach(SERVO_0);
  myservo.write(servo_pos);              
  
}

void loop() {
  // put your main code here, to run repeatedly:

  if (Serial.available() > 0) {
    readSerial();
  }

  if (runrun) {
   /* if (steppers.run()) {
       
    } else {
      runrun = false;
      Serial.println("!-- Reached move-end ---");
    }*/
    /*if (stepperA.distanceToGo() == 0 and stepperB.distanceToGo() == 0){
      runrun = false;
      Serial.println("!-- Reached move-end ---");
    } else{
      if (stepperA.distanceToGo() != 0) {
        stepperA.run();
      }
      if (stepperB.distanceToGo() != 0) {
        stepperB.run();
      }
    }*/
  }
}

void readSerial(){
  incomingByte = char(Serial.read());
  if( incomingByte == 10 ){
      // do nothing - enter on the keyboard
  } else {
    Serial.print("!-- I received: ");
    Serial.println(incomingByte);

    if (incomingByte== 'A' or incomingByte == 'B') {
      delay(25);
      
      // now read 4 Bytes
      temp_value = Serial.read();
      //Serial.print(temp_value); Serial.print(" ");
      //delay(25);
      
      temp_value = temp_value << 8;
      temp_value += Serial.read();
      //Serial.print(temp_value); Serial.print(" ");
      //delay(25);
      temp_value = temp_value << 8;
      temp_value += Serial.read();
      //Serial.print(temp_value); Serial.print(" ");
      //delay(25);
      temp_value = temp_value << 8;
      temp_value += Serial.read();
      //Serial.print(temp_value); Serial.print(" ");
      
      if(incomingByte == 'A') {
        a_target = temp_value;
        Serial.print("!--- A target length = ");
        Serial.println(a_target);
        
      } else {
        b_target = temp_value;
        Serial.print("!--- B target length = ");
        Serial.println(b_target);
      }
    } else if (incomingByte== 'D') {
      Serial.println("!--- Debug ---");
      Serial.print("!--- A length = ");
      Serial.println(stepperA.currentPosition());
      Serial.print("!--- B length = ");
      Serial.println(stepperB.currentPosition());
      Serial.print("!--- A target length = ");
      Serial.println(a_target);
      Serial.print("!--- B target length = ");
      Serial.println(b_target);
    } else if (incomingByte== 'G') {
      Serial.println("!--- Running ---");
      positions[0] = a_target;
      positions[1] = b_target;
      
      steppers.moveTo(positions);
      //stepperA.moveTo(a_target);
      //stepperB.moveTo(b_target);
      steppers.runSpeedToPosition();
      Serial.println("!-- Reached move-end ---");
      runrun = true;
    } else if (incomingByte== 'S') {
      Serial.println("!--- Stopping ---");
      runrun = false;
    } else if (incomingByte == 'R') {
      stepperA.setCurrentPosition(0);
      stepperB.setCurrentPosition(0);
    } else if (incomingByte == 'C') {
         for(; servo_pos <= 90; servo_pos += 1){
            myservo.write(servo_pos);             
            delay(5);
          }
     // myservo.write(90);              

    } else if (incomingByte == 'X') {
      for(; servo_pos >= 0; servo_pos -= 1){
            myservo.write(servo_pos);             
            delay(5);
          }
      //myservo.write(0);              
  
    }
    
  }

}
