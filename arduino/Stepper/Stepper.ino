/*
 * 스텝모터 시계방향으로 한바퀴, 반시계방향으로 한바퀴
 * <Stepper.h라이브러리 설명>
 * -Stepper stepper(STEPS,IN1,IN2,IN3,IN4):사용하는 Stepper Motor스템수, 각 4핀을 세팅.
 * -stepper.setSpeed(값): Stepper Motor의 속도 설정.
 * -stepper.step(스텝수):스텝 수로 회전각을 표현한다.
 * 스텝모터 한바퀴 스텝각 2048일때 속도 10~14정도가 적당
 * 
 */


//라이브러리
#include <Stepper.h>
#define STEPS 2048//한바퀴 스텝각

#define STEP_IN1 8
#define STEP_IN2 9
#define STEP_IN3 10
#define STEP_IN4 11

//스텝모터 선언
Stepper stepper(STEPS, STEP_IN4, STEP_IN2, STEP_IN3, STEP_IN1);           

void setup() {
  //스텝 모터 동작 속도 14RPM
  stepper.setSpeed(14); 
}
void loop() {
  // 시계 방향으로 이동
  stepper.step(STEPS);
  delay(1000);
  // 반시계 방향으로 이동
  stepper.step(-STEPS);
  delay(1000);
}
