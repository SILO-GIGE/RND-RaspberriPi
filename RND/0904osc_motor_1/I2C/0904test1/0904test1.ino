
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
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  Wire.begin();//Master 설정. 주소 안적음.
}
byte x=0;
void loop() 
{ 
      Wire.beginTransmission(1);// 슬레이브주소 1번 전송시작
      Wire.write("good   !!!! ");//문자열전송
      Wire.endTransmission();//전송중단
      delay(5000);

      Wire.requestFrom(1,4); //슬레이브 (1)dp 4byte요청
      while(Wire.available()){
        char c =Wire.read();
        Serial.print(c);
      }
      x++;
      if(x==6) x=0;
}
