# -*- coding: utf-8 -*-g

import neopixel
from PIL import Image
from PIL import ImageEnhance
import time
import os
import threading
import sys
import board

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

Main_port_num=5557  # Window 포트번호
Server1_port_num=4206  #라즈베리파이 포트번호

# LED 설정
pixel_pin = board.D18  # GPIO 18에 연결된 LED
num_pixels = 1280+1024#256 픽셀 LED 5개 +floor = 2304
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
    if address == "/SILOKSH":
        print(f"Received OSC message from {address}: {args}")#수신한 메세지를 출력. 
        #OSC신호 1을 수신하면 콘텐츠 재생
        if args[0]==1:
            start_time=time.time()
            for i in range(num_iterations):#출력할 이미지 개수
                index = i % len(image_pixels_list)  # 이미지 배열을 순환
                show_image(*image_pixels_list[index]) #이미지를 출력.
            end_time=time.time()
            execution_time=end_time-start_time
            print("TIME    :",execution_time,"sec")
            pixels.fill((0, 0, 0))
            pixels.show()
            osc_client.send_message("/Rasp1", 3)
            print("Sent OSC message: /Rasp1 3")  # 전송한 메시지 출력
        #OSC신호 0을 수신하면 LED OFF
        elif args[0]==0:
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
directory_path = "/home/silolab_ksh/Desktop/11/"

# 이미지 파일들의 경로를 저장할 배열
image_paths = []

# 이미지경로에 있는 png파일 가져오기
for filename in os.listdir(directory_path):
    if filename.endswith(".png"):  # png 파일인 경우에만 처리
        image_paths.append(filename)

# 파일 이름들의 숫자 순서대로 정렬
image_paths.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# image_paths = ["image1.png", "image2.png", "image3.png"] 이런식으로 저장됨.

# 정렬된 파일 이름들에 디렉토리 경로를 추가하여 완전한 파일 경로를 생성
# 폴더의 경로가 아닌 각 이미지마다 자기 경로가 지정이됨. 
image_paths = [os.path.join(directory_path, filename) for filename in image_paths]
# iamge_paths= ['/home/user/images/image1.png', '/home/user/images/image2.png', '/home/user/images/image3.png', ...]


'''---------------------------------------------------------------------------'''

# 이미지각각 마다 이미지 영역을 자르고 픽셀 배열로 변환하는 함수
def image_to_pixels(image_path):
    image=Image.open(image_path).convert("RGB") #이미지를 RGB색상모드로 변환
    enhancer=ImageEnhance.Contrast(image) 
    image=enhancer.enhance(1.7) #이미지의 채도를 강하게.

    image1 = image.crop((0, 0, 16, 16)) 
    image2 = image.crop((16, 0, 32, 16)) 
    image3 = image.crop((32, 0, 48, 16))  
    image4 = image.crop((48, 0, 64, 16))  
    image5 = image.crop((64, 0, 80, 16)) 
    
    # 이미지를 상하로 반전
    image1 = image1.transpose(Image.FLIP_TOP_BOTTOM)
    image2 = image2.transpose(Image.FLIP_TOP_BOTTOM)
    image3 = image3.transpose(Image.FLIP_TOP_BOTTOM)
    image4 = image4.transpose(Image.FLIP_TOP_BOTTOM)
    image5 = image5.transpose(Image.FLIP_TOP_BOTTOM)
    
    #get Image pixel
    image1_pixels = list(image1.getdata())
    image2_pixels = list(image2.getdata())
    image3_pixels = list(image3.getdata())
    image4_pixels = list(image4.getdata())
    image5_pixels = list(image5.getdata())
    
    #이미지들의 RGB색상들의 리스트가 배열로 저장됨.
    image_pixel_lists = [image1_pixels, image2_pixels, image3_pixels, image4_pixels, image5_pixels]
    
    # 'ㄹ' 모양의 패턴에 맞게 이미지 배열을 재구성
    for image_pixels in image_pixel_lists:
        for y in range(16): # 0부터 15까지
            #이미지는 x가 작은 순부터 읽기 때문에 네오픽셀 특성상
            #홀수번째 행일때만 이미지를 반대로 뒤집음.
            if y % 2 == 1:
                start_index = y * 16
                end_index = (y + 1) * 16
                image_pixels[start_index:end_index] = reversed(image_pixels[start_index:end_index])
                
    return image1_pixels,image2_pixels,image3_pixels,image4_pixels,image5_pixels

#########################################################################
# 이미지 출력 함수
def show_image(image1_pixels, image2_pixels, image3_pixels, image4_pixels, image5_pixels):
    combined_pixels = image1_pixels + image2_pixels + image3_pixels + image4_pixels + image5_pixels
    for i, pixel_value in enumerate(combined_pixels):
        if i < 1280:
            pixels[i] = (int(pixel_value[0] * 1), int(pixel_value[1] * 0.9), int(pixel_value[2] * 0.5))
        else:
            pixels[i] = (60, 60, 30)
    pixels.show()


# 이게 최종 image_pixelx_list !!
image_pixels_list = [image_to_pixels(image_path) for image_path in image_paths]

# 이미지를 1/30초 간격으로 송출s
interval = 1 / 30  # 1/30초 간격
total_time =  12 # 10초
num_iterations = int(total_time / interval) #이미지 출력 개수

#########################################################################
# OSC 메시지 수신 대기
try:
    while True:
        server.handle_request()
except KeyboardInterrupt:
    server.server_close()
    
