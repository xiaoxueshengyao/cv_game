import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import multiprocessing as mp# multithreading
from socket import *
import os
import struct
import base64
from threading import Thread
import threading

camera= PiCamera()
camera.resolution = (320,240)

raw_cap = PiRGBArray(camera,size=(320,240))
#load face detector
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

#recognizer
recognizer = cv2.createLBPHFaceRecognizer()
#recognizer = cv2.face.LBPHFaceRecognizer_create()
#recognizer.load('trainner/trainner.yml')
recognizer.load('train/trainner.yml')


t_start = time.time()
fps = 0
#socket setting 
host = '192.168.1.110'
server_port = 6699

server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
server_socket.bind((host,server_port))
server_socket.listen(5)

#html_yjj = 'HTTP/1.1 200 ok\nContent-type: text/html\n\r\n<div>Hello world!\r\nJerry is comming\r\n</div>'

html_yjj_img = "HTTP/1.1 200 ok\n\n<html><head><meta charset=\"utf-8\"/><title>web_serve</title></head><body><center><h1>YJJ</h1></center><hr color=\"green\"><div><img src=\"data:image/jpg;base64,"
end_html = '\"</body></img>'

#html_lzy = '''HTTP/1.1 200 ok\nContent-type: text/html\r\n<div>Zhaoyang is comming\r\n</div>'''
html_lzy_img = "HTTP/1.1 200 ok\n\n<html><head><meta charset=\"utf-8\"/><title>web_serve</title></head><body><center><h1>LZY</h1></center><hr color=\"green\"><div><img src=\"data:image/jpg;base64,"

def load_img(path):
	imgpath=path
	f1 = open(imgpath,'rb')
	data=f1.read(os.path.getsize(imgpath))
	print(os.path.getsize(imgpath))
	data=base64.b64encode(data)
	f1.close()
	return data

def get_faces(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray)
	print ('we got'+str(len(faces))+' face(s)')
	
	return faces, gray
	
def draw_frame(gray,faces):
	global fps
	img_id=0
	#draw a rectangle around every face
	for (x,y,w,h) in faces:
		cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),2)
		img_id,conf = recognizer.predict(gray[y:y+h,x:x+w])
		if conf<100:		
			if img_id ==1:
				img_id = "YJJ"
				
			elif img_id ==2:
				img_id="lzy"	
				
		else:
			img_id = "unknown"
		cv2.putText(gray,str(img_id),(x,y+h),cv2.FONT_HERSHEY_SIMPLEX,1.25,(0,0,255),1)
	
	fps = fps+1
	sfps = fps/(time.time()-t_start)
	cv2.putText(gray,"fps: "+str(int(sfps)),(10,10),
		cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
	cv2.imshow("frame",gray)
	return img_id

def sb(raw_cap):
	for frame in camera.capture_continuous(raw_cap,format="bgr",use_video_port=True):
		raw_cap.truncate()
		raw_cap.seek(0)
		image = frame.array
		f1,i1 =get_faces(image)
		name_id=draw_frame(i1,f1)
		if name_id=="YJJ":
			camera.capture("YJJ.jpg")	
		elif name_id=="lzy":
			camera.capture("lzy.jpg")
		raw_cap.truncate(0)
con=0		
def accept_hd(server_socket):
	con,add = server_socket.accept()
	sentence = con.recv(1024)
	print(str(sentence))
			 
		
name_id =0
if __name__=="__main__":
	pool = mp.Pool(processes =4)
	fcount = 0
	
	last_id =0
	camera.capture(raw_cap,format="bgr")

	raw_cap.truncate(0)
	
	thread1=threading.Thread(target=sb,args=(raw_cap,))
	thread1.start()
	
	while True:

		thread2=threading.Thread(target=accept_hd,args=(server_socket,))
		thread2.start()
		thread2.join()
		thread1=threading.Thread(target=sb,args=(raw_cap,))
		thread1.start()
		
		if name_id!=last_id:
			if name_id=="YJJ":
				data = load_img("YJJ.jpg")
				html_yjj_img+=data
				html_yjj_img+=end_html	
					#con.sendall(html_yjj)
				con.sendall(html_yjj_img)
					#print(str("lalalalal"))
				last_id =name_id
			elif name_id=="lzy":
					#camera.capture("lzy.jpg")
				data2=load_img("lzy.jpg")
				html_lzy_img+=data2
				html_lzy_img+=end_html
					#con.sendall(html_lzy)
				con.sendall(html_lzy_img)
				last_id=name_id
				
		if cv2.waitKey(20) & 0xFF == 27:
			break
		

		
	
	
