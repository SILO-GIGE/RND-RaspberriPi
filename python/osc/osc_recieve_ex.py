'''from pythonosc import osc_server

def handle_osc_message(address, *args):
    # OSC 메시지 처리 로직을 여기에 작성합니다.
    print(f"Received OSC message from {address}: {args}")

# OSC 서버 설정
ip = '0.0.0.0'  # 모든 IP 주소에서 들어오는 OSC 메시지를 수신합니다.
port = 7000    # OSC 메시지를 수신할 포트 번호를 지정합니다.

# OSC 서버 생성 및 실행
server = osc_server.ThreadingOSCUDPServer((ip, port), handle_osc_message)
print(f"OSC server is listening on {ip}:{port}")
server.serve_forever() # OSC 신호 수신 대기
print(f"OSC server is listening on {ip}:{port}")
'''

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

# OSC 메시지 처리를 위한 콜백 함수
def receive_osc_message(address, *args):
    print(f"Received OSC message from {address}: {args}")

# OSC 서버 설정
ip = '0.0.0.0'  # 모든 IP 주소에서 들으려면 '0.0.0.0'을 사용합니다.
port = 7000  # TouchDesigner에서 설정한 포트 번호로 변경해야 합니다.

# OSC 디스패처 설정
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(receive_osc_message)  # 모든 메시지를 동일한 핸들러로 전달합니다.

# OSC 서버 시작
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"OSC server listening on {ip}:{port}")
# OSC 메시지 수신 대기
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()