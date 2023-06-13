from pythonosc import osc_server

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
