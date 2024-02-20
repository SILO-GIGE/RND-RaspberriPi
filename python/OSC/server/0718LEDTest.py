"""
 윈도우 터디에서 보낸 버튼 0/1상태 OSC신호로 받아서 LED ON/OFF
"""

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
import RPi.GPIO as GPIO
import time

LED_pin=17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_pin,GPIO.OUT,initial=GPIO.LOW)

# OSC 메시지 처리를 위한 콜백 함수
def receive_osc_message(address, *args):
    if address == "/button1":
        print(f"Received OSC message from {address}: {args}")
        if args[0]==1:
            GPIO.output(LED_pin,True)#led on (GPIO.HIGH)
        elif args[0]==0:
            GPIO.output(LED_pin,False)#led off


            

# OSC 서버 설정
ip = '0.0.0.0'  # 모든 IP 주소에서 들으려면 '0.0.0.0'을 사용합니다.
port = 8000  # TouchDesigner에서 설정한 포트 번호로 변경해야 합니다.

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
    GPIO.cleanup()# Cleanup GPIO on program exit
