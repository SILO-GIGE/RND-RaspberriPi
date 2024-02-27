// '/dev/tty/ACM1'
const int ledPin = 2; // LED가 연결된 핀 번호

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600); // 라즈베리 파이와 같은 속도로 시리얼 통신 시작
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar == '1') {
      digitalWrite(ledPin, HIGH); // LED 켜기
    } else if (receivedChar == '0') {
      digitalWrite(ledPin, LOW); // LED 끄기
    }
  }
}
