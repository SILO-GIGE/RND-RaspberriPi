'''
python 에서 on 또는 off를 입력하면 값에 따라 아두이노로 시리얼 값을 전송한다.
'''
import serial
import time

# 시리얼 포트와 속도 설정 (시리얼 포트 이름은 자신의 환경에 따라 변경해야 합니다)
ser = serial.Serial('/dev/ttyACM0', 9600)

# LED 제어 함수
def control_led(arduino, status):
    if status == 'on':
        arduino.write(b'1')  # 아두이노로 1을 보내서 LED를 켭니다.
        print("motor1 on")
    elif status == 'off':
        arduino.write(b'0')  # 아두이노로 0을 보내서 LED를 끕니다.
        print("motor 2 on")
    else:
        print("잘못된 입력입니다. 'on' 또는 'off'를 입력하세요.")

try:
    while True:
        # 사용자로부터 LED 상태 입력 받기
        user_input = input("Input the motor number (on/off/exit): ").lower()

        if user_input == 'exit':
            break  # 프로그램 종료

        # LED 상태 제어
        control_led(ser, user_input)

except KeyboardInterrupt:
    print("\n프로그램을 종료합니다.")
    ser.close()
