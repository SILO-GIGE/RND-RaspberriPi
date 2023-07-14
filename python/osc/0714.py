
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

def messege_handler(unused_addr, *p):
    try:
        print(p)
        client.send_message("/message_echo", "Hello")
    except ValueError: pass

dispatcher = dispatcher.Dispatcher()
dispatcher.map("/message", messege_handler)
server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 5005), dispatcher)
print("Serving on {}".format(server.server_address))

client = udp_client.SimpleUDPClient("192.168.0.54", 5006)
client.send_message("/message_echo", "Hello")

server.serve_forever()