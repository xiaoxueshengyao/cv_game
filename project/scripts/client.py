#!/usr/bin/env python
#coding= utf-8

from socket import *
import sys

server_host = 'localhost'
server_port = 6699

msg = ['hello network world']
num=3
while bool(num):
	if len(sys.argv)>1:
		server_host=sys.argv[1]
	if len(sys.argv)>2:
		msg = sys.argv[2]
		
	socket_obj = socket(AF_INET,SOCK_STREAM)
	socket_obj.connect((server_host,server_port))
	
	for line in msg:
		socket_obj.send(line)
		data = socket_obj.recv(1024)
		print("client received:",repr(data))
	num=num-1
	socket_obj.close()


