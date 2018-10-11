#!/usr/bin/env python

import socket


TCP_IP = '192.168.43.12'
TCP_PORT = 2345
BUFFER_SIZE = 100  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

s.close()