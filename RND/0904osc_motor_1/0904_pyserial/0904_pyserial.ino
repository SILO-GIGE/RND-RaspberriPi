// '/dev/tty/ACM0'
// 스텝모터제어
// python에서 보낸 시리얼 신호받아서 모터제어.
/*
스텝모터 2개 압출기용 제어코드

속도단위 steps/seconds
Full Step (LLL): 1바퀴=200스텝
Half Step (HLL): 1바퀴=400스텝
Quarter step (LHL):1바퀴=800스텝
Eighth step (HHL):1바퀴 1600스텝
Sixteenth step (HHH): 1바퀴 3200스텝

*/
#include <AccelStepper.h>
#define dirPin1 2
#define stepPin1 3
#define dirPin2 4
#define stepPin2 5
 
AccelStepper stepper1(AccelStepper::DRIVER, stepPin1, dirPin1);
AccelStepper stepper2(AccelStepper::DRIVER, stepPin2, dirPin2);
 
int button = 8;
int Control1=A1;//가변저항 아날로그 핀설정

void setup() {
  pinMode(button, INPUT);
  stepper1.setMaxSpeed(6400);
  stepper2.setMaxSpeed(6400);
  Serial.begin(9600);
}

void loop() 
{ 

  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar == '1') {
      stepper1.setCurrentPosition(0);//위치 초기화
      Serial.println("1  in ");
      while(stepper1.currentPosition()!=3200){ //Siteeth step일때 10도 움직임.
        Control1= analogRead(A1);
        int motorSpeed1=map(Control1,0,1023,0,3200);
        stepper1.setSpeed(motorSpeed1);
        stepper1.run();
      }
      Serial.print("receive 1!!!" );
      delay(1000);
    }
    else if (receivedChar =='0'){
      stepper2.setCurrentPosition(0);//위치 초기화
      stepper1.setCurrentPosition(0);//위치 초기화
      Serial.println("2  in ");
      while(stepper2.currentPosition()!=3200 and stepper1.currentPosition()!=3200){
        stepper2.setSpeed(6400); //steps/seconds
        stepper2.run();
        stepper1.setSpeed(5000);
        stepper1.run();
      }
      Serial.print("receive 1!!!" );
      
    }
  }
    else{
      stepper1.stop();
      stepper2.stop();
      stepper1.disableOutputs();
      stepper2.disableOutputs();
      
    }
  
}
