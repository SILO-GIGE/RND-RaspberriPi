#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
라즈베리파이에서 터디로 osc신호 랜덤값 0.1초에 한번씩 보내기
'''

#OSC신호를 보내는 모든것을 client라고한다.
import argparse
import random
import time

from pythonosc import udp_client

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="192.168.0.54",#시현 윈도우 IP주소
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=6001,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  for x in range(1000):
    client.send_message("/filter", random.random()) #설정된 주소, 포트로 osc신호를 보낸다.
    time.sleep(0.1)
