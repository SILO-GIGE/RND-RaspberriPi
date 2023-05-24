#include <AccelStepper.h>
#include <SoftwareSerial.h>
#define FULLSTEP 8  //Half-step mode (8 step control signal sequence)
#define HALFSTEP 4  //하프와 풀의 차이는 전류또는 속도와관련, 풀이더빠름
//모터 핀 번호 정의(1번모터: 8~11, 2번모터: 3~6)
#define mtrPin1  8     // IN1 on the ULN2003 driver 1
#define mtrPin2  9     // IN2 on the ULN2003 driver 1
#define mtrPin3  10     // IN3 on the ULN2003 driver 1
#define mtrPin4  11     // IN4 on the ULN2003 driver 1
#define mtrPin_1  4     // IN1 on the ULN2003 driver 2
#define mtrPin_2  5     // IN2 on the ULN2003 driver 2
#define mtrPin_3  6     // IN3 on the ULN2003 driver 2
#define mtrPin_4  7     // IN4 on the ULN2003 driver 2

unsigned long steps = 2048;//한바퀴 스텝수
unsigned long rotation_number_1=steps;//원하는 모터 회전수
unsigned long rotation_number_2=steps;//원하는 모터 회전수


AccelStepper stepper1(HALFSTEP, mtrPin1, mtrPin3, mtrPin2, mtrPin4); //모터1정의
AccelStepper stepper2(HALFSTEP, mtrPin_1, mtrPin_3, mtrPin_2, mtrPin_4); //모터2정의

void setup() {
  Serial.begin(9600);
  stepper1.setMaxSpeed(2000.0);
  stepper2.setMaxSpeed(2000.0);
}
char state;

void loop(){
  //모터정지상태
  stepper1.stop();
  stepper2.stop();
  stepper1.disableOutputs(); //motor power disconnect, so motor led will turn off
  stepper2.disableOutputs();
  Serial.println("NO");delay(500);//모터정지상태(전원x)일때 STOP보내기
  
  if(Serial.available()){  //데이터가 들어오면
    state=Serial.read();  //state에 읽은 데이터 입력
    if (state=='c'){  //'o'가 입력되면 창문열기
      Serial.println(state);
      _CW();  //창문열기
    }
    else if (state== 'w'){  //'c'가 입력되면 창문닫기
      Serial.println(state);
      _CCW();  //창문닫기
    }
  }
}
void _CCW() { 
  for (;;) {
    stepper1.moveTo(rotation_number_1);
    stepper2.moveTo(rotation_number_2);
    stepper1.setSpeed(500);
    stepper2.setSpeed(500);
    stepper1.runSpeedToPosition();//가속없이 현재속도로 실행하는 함수
    stepper2.runSpeedToPosition();
    if ((stepper1.distanceToGo()==0) and (stepper2.distanceToGo()==0)){//모터2개 회전수같으면||써도됨
      stepper1.setCurrentPosition(0);
      stepper2.setCurrentPosition(0);
      Serial.println("'The Window Is Open'");
      return;
    }
  }
}

void _CW(){ 
  for(;;){
    stepper1.moveTo(-rotation_number_1);
    stepper2.moveTo(-rotation_number_2);
    stepper1.setSpeed(500);
    stepper2.setSpeed(500);
    stepper1.runSpeedToPosition();//가속없이 현재속도로 실행하는 함수
    stepper2.runSpeedToPosition();
    if ((stepper1.distanceToGo()==0)and(stepper2.distanceToGo()==0)){
      stepper1.setCurrentPosition(0);
      stepper2.setCurrentPosition(0);
      Serial.println("'The Window Is Closed'");
      return;
    }
  }
}
