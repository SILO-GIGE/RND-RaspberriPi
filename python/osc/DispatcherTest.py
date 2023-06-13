#dispatcher

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

def handle_osc_address1(address, *args):
    print("Received OSC message for address1:", address, args)

def handle_osc_address2(address, *args):
    print("Received OSC message for address2:", address, args)

# Dispatcher 생성 및 핸들러 등록
dispatcher = Dispatcher()
#/adress1로 시작하는 OSC메시지에 대해 핸들러함수를 호출한다.
dispatcher.map("/address1", handle_osc_address1)
dispatcher.map("/address2", handle_osc_address2)

# OSC 서버 생성 및 Dispatcher와 연결
server = BlockingOSCUDPServer(("192.168.0.54", 9000), dispatcher)
server.serve_forever()
