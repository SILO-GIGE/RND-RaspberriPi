'''
터디에서 button입력으로 주는 0/1값 osc신호로 받아오기
들어온 osc신호값이 1이면 아두이노로 LED ON명령
들어온 osc신호값이 0이면 아두이노로 LED OFF명령
'''

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import time
import serial

# OSC 메시지 처리를 위한 콜백 함수
def receive_osc_message(address, *args):
    print(f"Received OSC message from {address}: {args}")
    if args and args[0] == 1:
        ser.write(b'1')  # Arduino로 '1'을 보냅니다.
    elif args and args[0] == 0:
        ser.write(b'0')  # Arduino로 '1'을 보냅니다.


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

# 시리얼 포트와 속도 설정 (시리얼 포트 이름은 자신의 환경에 따라 변경해야 합니다)
ser = serial.Serial('/dev/ttyACM0', 9600)
ser2= serial.Serial('/dev/ttyACM1',9600)

# OSC 서버의 IP 주소와 포트 번호를 설정합니다.
ip_win= '192.168.0.54'  # OSC 서버의 IP 주소를 입력합니다.
port_win = 6000  # OSC 서버가 수신 대기하는 포트 번호를 입력합니다.
# OSC 서버 설정
ip_raspi= '0.0.0.0'  # 모든 IP 주소에서 들으려면 '0.0.0.0'을 사용합니다.
port_raspi= 8000  # TouchDesigner에서 설정한 포트 번호로 변경해야 합니다.

# OSC 디스패처 설정
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(receive_osc_message)  # 모든 메시지를 동일한 핸들러로 전달합니다.

# OSC 서버 시작
server = osc_server.ThreadingOSCUDPServer((ip_raspi, port_raspi), dispatcher)
print(f"OSC server listening on {ip_raspi}:{port_raspi}")

# OSC 클라이언트 생성
client = udp_client.SimpleUDPClient(ip_win, port_win)

# OSC 메시지 보내기
address = '/Raspi->windowTD'  # OSC 주소를 입력합니다.

num_messages = 100  # 보내고자 하는 횟수를 지정합니다.
current_value = 0  # 현재 보내고 있는 값의 초기값을 0으로 설정합니다.
# OSC 메시지 수신 대기
try:
    while True:
        server.handle_request()
        client.send_message(address, [str(current_value)])  # 현재 값을 문자열로 변환하여 보냅니다.
        current_value += 1  # 현재 값을 1씩 증가시킵니다.

        
except KeyboardInterrupt:
    server.server_close()
    ser.close()
    ser2.close()
