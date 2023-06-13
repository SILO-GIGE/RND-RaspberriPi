from pythonosc import udp_client

# OSC 서버의 IP 주소와 포트 번호를 설정합니다.
ip = '192.168.0.54'  # OSC 서버의 IP 주소를 입력합니다.
port = 5000  # OSC 서버가 수신 대기하는 포트 번호를 입력합니다.

# OSC 클라이언트 생성
client = udp_client.SimpleUDPClient(ip, port)

# OSC 메시지 보내기
address = '/example'  # OSC 주소를 입력합니다.
message = 42  # 보낼 데이터를 입력합니다. (여기에서는 예시로 정수형 데이터인 42를 보냅니다.)
client.send_message(address, message)
 
