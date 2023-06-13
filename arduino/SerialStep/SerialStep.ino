#include <Stepper.h>
#include <SoftwareSerial.h>
#define STEPS 2048//한바퀴 스텝각
#define STEPS_PER_MOTOR_REVOLUTION 32
#define STEP_IN1 8
#define STEP_IN2 9
#define STEP_IN3 10
#define STEP_IN4 11

//스텝모터 선언
Stepper stepper(STEPS, STEP_IN4, STEP_IN2, STEP_IN3, STEP_IN1);           

void setup(){
    Serial.begin(9600);
    //stepper.
    Serial.println("Ready");
}

void loop(){

    float degree;
    if(Serial.available()){
        degree=Serial.parseInt();
       
        //float revol=64.0*degree/360.0;

        degree=map(degree,0,360,0,2048);//회전각 스템수
        
        //Serial.print("Revol");Serial.println(revol)
        stepper.step(degree);
        Serial.print("degree: "); Serial.println(degree);
        delay(10);
        
    }


}
