import socket
import sys
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#build conneection
s.connect(('127.0.0.1',9999))

print(s.recv(1024))
for data in ['Michael', 'Tracy', 'Sarah']:
    # 发送数据:
    s.send(data)
    print(s.recv(1024)) 
s.send('exit')
s.close()

