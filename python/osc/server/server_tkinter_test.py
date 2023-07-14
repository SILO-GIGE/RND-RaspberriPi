"""
라즈베리파이 서버 테스트 코드.
TD에서 보낸 osc신호를 Tkinter창에 출력한다.
"""

from pythonosc import dispatcher, osc_server
import tkinter as tk

# OSC 메시지를 처리하는 함수
def print_osc_message(address, *args):
    message = f"OSC 메시지 수신 - 주소: {address}, 값: {args}"
    label.config(text=message)

# OSC 서버 설정
ip = "0.0.0.0"  # 모든 IP 주소에서의 연결 허용
port = 8000     # 사용할 포트 번호

# Dispatcher 객체 생성 및 OSC 메시지 핸들러 등록
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(print_osc_message)  # 모든 OSC 메시지를 처리하는 함수 등록

# OSC 서버 생성 및 시작
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"OSC 서버 시작 - IP: {ip}, 포트: {port}")

# Tkinter 창 생성
window = tk.Tk()
window.title("OSC 메시지 출력")
label = tk.Label(window, text="")
label.pack()

# OSC 메시지 처리 및 Tkinter 창 업데이트
def process_osc_messages():
    server.handle_request()
    window.after(10, process_osc_messages)  # 100ms마다 메시지 처리 및 창 업데이트

process_osc_messages()
window.mainloop()
