#include<Wire.h>


void setup() {
  // put your setup code here, to run once:
  Wire.begin(1); //슬레이브 주소
  Wire.onRequest(requestEvent); //요청시 requestEvent함수 호출
  Wire.onReceive(receiveEvent); //데이터 전송 받을 때 receiveEvent 함수 호출
  Serial.begin(9600);
  pinMode(6,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(500);
}

void receiveEvajgjent(int howMany){//전송 데이터 읽기
  while(Wire.available()>1){
    char ch =Wire.read();
    Serial.print(ch);
  }
  int x=Wire.read();
  Serial.println(x);
}

void requestEvent(){//요청 시 수행 함
  Wire.write("ok!\n");
  digitalWrite(6,HIGH);
  delay(3000);
  digitalWrite(6,LOW);
}
