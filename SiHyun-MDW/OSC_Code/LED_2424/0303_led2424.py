'''
[03/03]
주석 달았음.
라즈베리파이 서버를 윈도우에서 테스트 하는중. 

24*24 pixels
_______________________
 front2|front3 |      | 
       |       |      | 
---------------|      |
               |      |
               |fornt4|
    front1     |      |
               |      |
               |      |
_______________|______|
               |   X  |
               |______|

[코드 실행 순서]
1. image_pixels_list 배열 생성. 
    - image_to_pixels함수 실행되어 이미지 각각 배열로 저장됨.
2. OSC신호 '1'을 수신하면.
3. show_image()함수 실행.
    - pixels[]마다 RGB 값이 하나씩 저장됨.
    - pixel.show()를 통해 한번에 출력.


    
'''
# -*- coding: utf-8 -*-g

import neopixel
from PIL import Image
from PIL import ImageEnhance
import time
import os
import threading
import sys

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

Main_port_num=5557  # Window 포트번호
Server1_port_num=4206  #라즈베리파이 포트번호

# LED 설정
pixel_pin = board.D18  # GPIO 18에 연결된 LED
num_pixels = 1728 + 192 #24*24 픽셀 3면, 8*8 픽셀 빈부분 3면
ORDER = neopixel.GRB

# OSC 클라이언트 설정
client_ip = '192.168.0.7'  # Window IP 주소
client_port = Main_port_num
osc_client = udp_client.SimpleUDPClient(client_ip, client_port)

# OSC 서버 설정
ip = '0.0.0.0'  # 모든 IP 주소에서 수신
port = Server1_port_num

#이미지 채도를 강하게 만드는 함수
def enhance_image(image):
    enhancer=ImageEnhance.Brightness(image)
    enhanced_image=enhancer.enhance(2.0)
    return enhanced_image

# OSC 메시지 처리를 위한 콜백 함수
def receive_osc_message(address, *args):
    if address == "/SILOKSH":
        print(f"Received OSC message from {address}: {args}")#수신한 메세지를 출력. 
        #OSC신호 1을 수신하면 콘텐츠 재생
        if args[0]==1:
            for i in range(num_iterations):#출력할 이미지 개수
                index = i % len(image_pixels_list)  # 이미지 배열을 순환
                show_image(*image_pixels_list[index]) #이미지를 출력.
                time.sleep(interval)

            # 이미지가 모두 재생된 후 LED를 끄고 OSC 메시지 전송
            time.sleep(0.5)
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
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)

# 이미지 파일이 있는 디렉토리 경로
directory_path = "/home/silolab_ksh/Desktop/blackwhite/"

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
    image=enhancer.enhance(1) #이미지의 채도를 강하게.

##원본이미지=40*72 픽셀

    #앞면 이미지 영역
    front1=image.crop((0,16,16,32))
    front2=image.crop((0,8,8,16))
    front3=image.crop((8,8,16,16))
    front4=image.crop((16,8,24,40))

    #오른쪽면 이미지 영역
    right1=image.crop((24,16,40,32))
    right2=image.crop((24,8,32,16))
    right3=image.crop((32,8,40,16))
    right4=image.crop((40,8,48,40))

    #오른쪽면 이미지 영역
    top1=image.crop((48,16,64,32))
    top2=image.crop((48,8,56,16))
    top3=image.crop((56,8,64,16))
    top4=image.crop((64,0,72,32))
    
## front 이미지들을 상하로 반전
    front1 = front1.transpose(Image.FLIP_TOP_BOTTOM)
    front2 = front2.transpose(Image.FLIP_TOP_BOTTOM)
    front3 = front3.transpose(Image.FLIP_TOP_BOTTOM)
    front4 = front4.transpose(Image.FLIP_TOP_BOTTOM)

    # right 이미지들을 상하로 반전
    right1 = right1.transpose(Image.FLIP_TOP_BOTTOM)
    right2 = right2.transpose(Image.FLIP_TOP_BOTTOM)
    right3 = right3.transpose(Image.FLIP_TOP_BOTTOM)
    right4 = right4.transpose(Image.FLIP_TOP_BOTTOM)

    # top 이미지들을 상하로 반전
    top1 = top1.transpose(Image.FLIP_TOP_BOTTOM)
    top2 = top2.transpose(Image.FLIP_TOP_BOTTOM)
    top3 = top3.transpose(Image.FLIP_TOP_BOTTOM)
    top4 = top4.transpose(Image.FLIP_TOP_BOTTOM)

    
##get Image pixel
    # front 이미지들의 픽셀 데이터 리스트
    front1_pixels = list(front1.getdata())
    front2_pixels = list(front2.getdata())
    front3_pixels = list(front3.getdata())
    front4_pixels = list(front4.getdata())

    # right 이미지들의 픽셀 데이터 리스트
    right1_pixels = list(right1.getdata())
    right2_pixels = list(right2.getdata())
    right3_pixels = list(right3.getdata())
    right4_pixels = list(right4.getdata())

    # top 이미지들의 픽셀 데이터 리스트
    top1_pixels = list(top1.getdata())
    top2_pixels = list(top2.getdata())
    top3_pixels = list(top3.getdata())
    top4_pixels = list(top4.getdata())

    ''' 
    image1_pixels 형식
    [ (R,G,B), # 첫번째 픽셀의 색상
      (R,G,B), # 두번째 픽셀의 색상
      ...
    ]
    '''
    #이미지들의 RGB색상들의 리스트가 배열로 저장됨.
    image_pixel_lists = [
        front1_pixels, front2_pixels, front3_pixels, front4_pixels,
        right1_pixels, right2_pixels, right3_pixels, right4_pixels,
        top1_pixels, top2_pixels, top3_pixels, top4_pixels
    ]
    '''
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
    '''
    # 'ㄹ' 모양의 패턴에 맞게 이미지 배열을 재구성
    for i,image_pixels in enumerate(image_pixel_lists):
        # 16*16 픽셀 'ㄹ' 모양 읽기
        if i in [0,4,8]:# front1, right1, top1에 대해서만 전체 패턴을 적용
            for y in range(16): # 16픽셀씩 'ㄹ'자로 16행까지
                if y % 2 == 1:
                    start_index = y * 16
                    end_index = (y + 1) * 16
                    image_pixels[start_index:end_index] = reversed(image_pixels[start_index:end_index])
        # 8*8 픽셀 'ㄹ' 모양 읽기
        elif i in [1,2,5,6,9,10]: 
            for y in range(8):# 8*8픽셀 8행까지
                if y % 2 == 1:
                    start_index= y* 8
                    end_index = ( y+1 ) * 8
                    image_pixels[start_index:end_index] = reversed(image_pixels[start_index:end_index])
        # 8*32 픽셀 'ㄹ' 모양 읽기
        elif i in [3,7,11]:
            for y in range(32): # 8픽셀씩 'ㄹ'자로 32행까지
                if y % 2 == 1:
                    start_index= y * 8
                    end_index = ( y+1 ) * 8
                    image_pixels[start_index:end_index] = reversed(image_pixels[start_index:end_index])

    return front1_pixels, front2_pixels, front3_pixels, front4_pixels,right1_pixels, right2_pixels, right3_pixels, right4_pixels,top1_pixels, top2_pixels, top3_pixels, top4_pixels

#########################################################################
# 이미지 출력 함수
def show_image(front1_pixels, front2_pixels, front3_pixels, front4_pixels,right1_pixels, right2_pixels, right3_pixels, right4_pixels,top1_pixels, top2_pixels, top3_pixels, top4_pixels):
    image_pixel_lists = [front1_pixels, front2_pixels, front3_pixels, front4_pixels,right1_pixels, right2_pixels, right3_pixels, right4_pixels,top1_pixels, top2_pixels, top3_pixels, top4_pixels]
    
    pixel_index = 0
    for image_pixels in image_pixel_lists:
        for pixel_value in image_pixels:
            pixels[pixel_index] = pixel_value #pixel_value는 픽셀마다 색상값을 나타냄.
            pixel_index += 1
    
    '''
    픽셀 1개 마다 이미지의 RGB값이 저장되어 LED 행렬이 설정된다.
    pixels[0] = (255, 255, 255)  # 첫 번째 픽셀의 RGB 색상 값 (흰색)
    pixels[1] = (0, 0, 0)        # 두 번째 픽셀의 RGB 색상 값 (검은색)
    pixels[2] = (255, 0, 0)      # 세 번째 픽셀의 RGB 색상 값 (빨강)
    pixels[3] = (0, 255, 0)      # 네 번째 픽셀의 RGB 색상 값 (녹색)
    ...
    '''

    # 1부터 1280까지의 LED에 대해 밝기 0.1 설정
    #
    for i in range(1280):
        pixels[i] = (int(pixels[i][0] * 1), int(pixels[i][1] * 1), int(pixels[i][2] * 1))
    
    # 1280부터 1792까지의 LED에 대해 밝기 1로 설정
    for i in range(1280, num_pixels):
        pixels[i] = (int(255 * 0.7), int(255 * 0.6), int(255 * 0.4))  # 밝기 조절
    pixels.show() # LED ON

    
# 각 이미지를 픽셀 배열로 변환하여 배열에 저장 !! 제일 중요한 부분.
# LED행렬을 만들어 낸다.
# 이게 최종 image_pixelx_list !!
image_pixels_list = [image_to_pixels(image_path) for image_path in image_paths]

# 이미지를 1/30초 간격으로 송출
interval = 1 / 30  # 1/30초 간격
total_time = 10  # 10초
num_iterations = int(total_time / interval) #이미지 출력 개수

#########################################################################
# OSC 메시지 수신 대기
try:
    while True:
        server.handle_request()
except KeyboardInterrupt:
    server.server_close()
    
