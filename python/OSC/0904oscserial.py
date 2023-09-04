"""
라즈베리파이 서버 테스트 코드.
TD에서 보낸 osc신호를 print로 출력한다.

"""

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import serial
import time

# 시리얼 포트와 속도 설정 (시리얼 포트 이름은 자신의 환경에 따라 변경해야 합니다)
ser = serial.Serial('/dev/ttyACM0', 9600)
ser2= serial.Serial('/dev/ttyACM1',9600)

# OSC 메시지 처리를 위한 콜백 함수
def receive_osc_message(address, *args):
    print(f"Received OSC message from {address}: {args}")
    

# OSC 서버 설정
ip = '0.0.0.0'  # 모든 IP 주소에서 들으려면 '0.0.0.0'을 사용합니다.
port = 8000  # TouchDesigner에서 설정한 포트 번호로 변경해야 합니다.

# OSC 디스패처 설정
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(receive_osc_message)  # 모든 메시지를 동일한 핸들러로 전달합니다.

# OSC 서버 시작
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"OSC server listening on {ip}:{port}")


# LED 제어 함수
def control_led(arduino, status):
    if status == 'on':
        arduino.write(b'1')  # 아두이노로 1을 보내서 LED를 켭니다.
        print("LED를 켭니다.")
    elif status == 'off':
        arduino.write(b'0')  # 아두이노로 0을 보내서 LED를 끕니다.
        print("LED를 끕니다.")
    else:
        print("잘못된 입력입니다. 'on' 또는 'off'를 입력하세요.")

# OSC 메시지 수신 대기
try:
    server.serve_forever()
    while True:
        # LED 상태 제어
        control_led(ser, user_input)
        control_led(ser2,user_input)
except KeyboardInterrupt:
    server.server_close()
    ser.close()
