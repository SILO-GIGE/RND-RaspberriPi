'''
라즈베리파이 python 코드에서 윈도우 터디로 osc신호
동시에, 터디에서 button입력으로 주는 0/1값 osc신호로 받아오기
'''

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import time

# OSC 메시지 처리를 위한 콜백 함수
def receive_osc_message(address, *args):
    print(f"Received OSC message from {address}: {args}")

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
address = '/example'  # OSC 주소를 입력합니다.

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
