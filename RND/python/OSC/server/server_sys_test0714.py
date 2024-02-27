"""
라즈베리파이 서버 테스트 코드.
TD에서 보낸 osc신호를 sys로 출력한다.
"""

from pythonosc import dispatcher, osc_server
import sys

# OSC 메시지를 처리하는 함수
def print_osc_message(address, *args):
    message = f"OSC 메시지 수신 - 주소: {address}, 값: {args}"
    sys.stdout.write(f"{message}\n")
    sys.stdout.flush()

# OSC 서버 설정
ip = "0.0.0.0"  # 모든 IP 주소에서의 연결 허용
port = 8000     # 사용할 포트 번호

# Dispatcher 객체 생성 및 OSC 메시지 핸들러 등록
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(print_osc_message)  # 모든 OSC 메시지를 처리하는 함수 등록

# OSC 서버 생성 및 시작
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"OSC 서버 시작 - IP: {ip}, 포트: {port}")

# OSC 메시지 처리
server.serve_forever()



  
