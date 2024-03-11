#import neopixel
from PIL import Image,ImageEnhance
import time
import os
# import board
from pythonosc import dispatcher, osc_server, udp_client

import cv2
import numpy as np

Main_port_num = 5557  # Window 포트번호
Server1_port_num = 4206  # 라즈베리파이 포트번호

# LED 설정
# pixel_pin = 18  # GPIO 18에 연결된 LED
num_pixels = 2304  # 1280 + 1024 픽셀
#ORDER = neopixel.GRB

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
        print(f"Received OSC message from {address}: {args}")  # 수신한 메세지를 출력.
        print("HIHIHI")
        start_time = time.time()
        for i in range(num_iterations):
            show_image(*image_pixels_list[i % len(image_pixels_list)])
            time.sleep(interval)
        end_time = time.time()
        execution_time = end_time - start_time
        print("TIME    :", execution_time, "sec")
        #pixels.fill((0, 0, 0))
        #pixels.show()
        osc_client.send_message("/Rasp1", 3)
        print("Sent OSC message: /Rasp1 3")
    elif address == "/SILOKSH" and args[0] == 0:
        print(f"Received OSC message from {address}: {args}")  # 수신한 메세지를 출력.
        #pixels.fill((0, 0, 0))
        #pixels.show()

# OSC 디스패처 설정
dispatcher = dispatcher.Dispatcher()
dispatcher.set_default_handler(receive_osc_message)

# OSC 서버 시작
server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
print(f"OSC server listening on {ip}:{port}")

# LED 초기화 및 밝기 설정
pixels = [(0, 0, 0)] * num_pixels
# 이미지 파일이 있는 디렉토리 경로
directory_path = "C:/Users/sihyu/Desktop/Composition1/"

# 이미지 파일들의 경로를 저장할 배열
image_paths = [os.path.join(directory_path, filename) for filename in sorted(os.listdir(directory_path)) if
               filename.endswith(".png")]

# OpenCV를 사용하여 이미지를 처리하는 함수
def image_to_pixels_opencv(image_path):
    image = cv2.imread(image_path)  # 이미지 읽기
    #image_name = os.path.splitext(os.path.basename(image_path))[0]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # BGR -> RGB로 변환
    image_pixel_lists = []
    image_index = 0 
    # 이미지를 80x16 크기의 조각으로 잘라서 픽셀 배열로 변환
    for x in range(0, 80, 16):
        image_piece = image[:, x:x+16, :]  # 이미지 조각 선택
        #cv2.imwrite(os.path.join("C:/Users/sihyu/Desktop/crop/",f"{image_name}_piece_{x}_{image_index}.png"), image_piece)  # 이미지 저장
        image_piece = cv2.flip(image_piece, 0)  # 이미지 뒤집
        #for i in range(16):
        #    if i % 2 == 1:
        #        image_piece[i] = np.flipud(image_piece[i])  # 홀수 행 좌우 반전
        image_pixel_lists.append(image_piece.reshape(-1, 3).tolist())  # 2차원 배열을 1차원으로 변환 후 리스트로 변환
        image_index += 1  # 이미지 순서 증가
    #with open("C:/Users/sihyu/Desktop/combined_pixels.txt", "w") as file:           
    #    file.write(f"{image_pixel_lists}\n")
    return image_pixel_lists

# 최종 image_pixel_list 생성
image_pixels_list = [image_to_pixels_opencv(image_path) for image_path in image_paths]


# 이미지를 1/30초 간격으로 송출
interval = 1 / 30  # 1/30초 간격
total_time = 10  # 10초
num_iterations = int(total_time / interval)  # 이미지 출력 개수

def show_image_opencv(image1_pixels, image2_pixels, image3_pixels, image4_pixels, image5_pixels):
    # 이미지를 합치기 위해 각 이미지 크기 조정
    image1 = np.array(image1_pixels).reshape(16, 16, 3).astype(np.uint8)
    image2 = np.array(image2_pixels).reshape(16, 16, 3).astype(np.uint8)
    image3 = np.array(image3_pixels).reshape(16, 16, 3).astype(np.uint8)
    image4 = np.array(image4_pixels).reshape(16, 16, 3).astype(np.uint8)
    image5 = np.array(image5_pixels).reshape(16, 16, 3).astype(np.uint8)

    # 이미지를 이어붙임
    combined_image = np.concatenate((image1, image2, image3, image4, image5), axis=1)

    # 이미지를 화면에 표시
    cv2.imshow('Combined Image', combined_image)
    cv2.waitKey(1)  # 화면 업데이트를 위해 잠시 대기
    
show_image = show_image_opencv
# OSC 메시지 수신 대기
try:
    while True:
        for i in range(1280, num_pixels):
            pixels[i] = (150, 140, 90)  # 화이트 설정
        print("OSC 대기중!!")
        server.handle_request()
except KeyboardInterrupt:
    server.server_close()
