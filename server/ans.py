#!/usr/bin/env python

import socket
import random
import time

TCP_IP = '172.30.44.243'
TCP_PORT = 1500
BUFFER_SIZE = 1024
MESSAGE = '{"answer":"A", "user_id":"104659413"}'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
for i in range(104659413, 104659513):
    answer = random.choice(['"A"', '"B"', '"C"', '"D"', '"E"', '"F"'])
    MESSAGE = '{"answer":' + answer + ', "user_id":"' + str(i) + '"}'
    s.send(MESSAGE.encode('utf-8'))
    time.sleep(0.05)