#!/usr/bin/env python
#coding=utf-8

from socket import *
import os
import re


host = ''
server_port = 6699

server_socket = socket(AF_INET,SOCK_STREAM)#build socket
server_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)#reuse the address
server_socket.bind((host,server_port))#bind
server_socket.listen(5)#listen max 
"""
while True:
	con,add = server_socket.accept()
	print("server connected by",add)
	while True:
		data = con.recv(1024)#read next line
		if not data: break
		con.send("Echo>-"+data)
	con.close()
"""


print('Serving port',server_port)

html = '''HTTP/1.1 200 ok\nContent-type: text/html\n\r\nHello world!\n\r\nJerry is comming'''

while True:
	#build TCP connect
	con,add = server_socket.accept()
	sentence = con.recv(1024)#receive data,1k max

	con.sendall(html)
	
	con.close()
	
	
