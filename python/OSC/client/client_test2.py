'''
라즈베리파이 python 코드에서 윈도우 터디로 osc신호 보내기 예제
'''
from pythonosc.udp_client import SimpleUDPClient

ip = "192.168.0.54"
port = 5000

client = SimpleUDPClient(ip, port)  # Create client

client.send_message("/some/address", 123)   # Send float message
client.send_message("/some/address", [1, 2, "hello"])  # Send message with int, float and string
