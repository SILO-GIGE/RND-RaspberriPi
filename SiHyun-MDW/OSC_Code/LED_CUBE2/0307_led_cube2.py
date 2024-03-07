import neopixel
from PIL import Image, ImageEnhance
import time
import os
import board
from pythonosc import dispatcher, osc_server, udp_client

Main_port_num = 5557  # Window 포트번호
Server1_port_num = 4208  # 라즈베리파이 포트번호

# LED 설정
pixel_pin = board.D18  # GPIO 18에 연결된 LED
num_pixels = 1280  # 1280 + 1024 픽셀
ORDER = neopixel.GRB

# OSC 클라이언트 설정
client_ip = '192.168.50.191'  # Window IP 주소
client_port = Main_port_num
osc_client = udp_client.SimpleUDPClient(client_ip, client_port)

# OSC 서버 설정
ip = '0.0.0.0'  # 모든 IP 주소에서 수신
port = Server1_port_num

# OSC 메시지 처리를 위한 콜백 함수
def receive_osc_message(address, *args):
    if address == "/SILOKSH" and args[0] == 1:
        print(f"Received OSC message from {address}: {args}")#수신한 메세지를 출력. 
        start_time = time.time()
        for i in range(num_iterations):
            show_image(*image_pixels_list[i % len(image_pixels_list)])
            time.sleep(1/25)
        end_time = time.time()
        execution_time = end_time - start_time
        print("TIME    :", execution_time, "sec")
        pixels.fill((0, 0, 0))
        pixels.show()
        osc_client.send_message("/Rasp1", 3)
        print("Sent OSC message: /Rasp1 3")
    elif address == "/SILOKSH" and args[0] == 0:
        print(f"Received OSC message from {address}: {args}")#수신한 메세지를 출력. 
        pixels.fill((0, 0, 0))
        pixels.show()

# OSC 디스패처 설정
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(receive_osc_message)

# OSC 서버 시작
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"OSC server listening on {ip}:{port}")

# LED 초기화 및 밝기 설정
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.7, auto_write=False, pixel_order=ORDER)

# 이미지 파일이 있는 디렉토리 경로
directory_path = "/home/silolab_ksh/Desktop/o14-2/"

# 이미지 파일들의 경로를 저장할 배열
image_paths = [os.path.join(directory_path, filename) for filename in sorted(os.listdir(directory_path)) if filename.endswith(".png")]

# 이미지각각 마다 이미지 영역을 자르고 픽셀 배열로 변환하는 함수
def image_to_pixels(image_path):
    image = Image.open(image_path).convert("RGB")  # 이미지를 RGB색상모드로 변환
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.7)  # 이미지의 채도를 강하게.
    image_pixel_lists = []
    for x in range(0, 80, 16):
        image_piece = image.crop((x, 0, x + 16, 16))
        image_piece = image_piece.transpose(Image.FLIP_TOP_BOTTOM)
        image_pixel_lists.append(list(image_piece.getdata()))
    for image_pixels in image_pixel_lists:
        for y in range(16):
            if y % 2 == 1:
                start_index = y * 16
                end_index = (y + 1) * 16
                image_pixels[start_index:end_index] = reversed(image_pixels[start_index:end_index])
    return image_pixel_lists

# 최종 image_pixelx_list
image_pixels_list = [image_to_pixels(image_path) for image_path in image_paths]

# 이미지를 1/30초 간격으로 송출
interval = 1 / 30  # 1/30초 간격
total_time = 12  # 10초
num_iterations = int(total_time / interval)  # 이미지 출력 개수

# 이미지 출력 함수
def show_image(image1_pixels, image2_pixels, image3_pixels, image4_pixels, image5_pixels):
    combined_pixels = image1_pixels + image2_pixels + image3_pixels + image4_pixels + image5_pixels
    for i, pixel_value in enumerate(combined_pixels):
        pixels[i] = (int(pixel_value[0] * 1), int(pixel_value[1] * 0.9), int(pixel_value[2] * 0.5))
    pixels.show()

# OSC 메시지 수신 대기
try:
    while True:
        server.handle_request()
except KeyboardInterrupt:
    server.server_close()
