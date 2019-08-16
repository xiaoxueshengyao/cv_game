import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from functools import partial
import multiprocessing as mp# multithreading
from socket import *

camera= PiCamera()
camera.resolution = (320,240)

raw_cap = PiRGBArray(camera,size=(320,240))
#load face detector
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

#recognizer
recognizer = cv2.createLBPHFaceRecognizer()
#recognizer = cv2.face.LBPHFaceRecognizer_create()
#recognizer.read('trainner/trainner.yml')
recognizer.load('trainner/trainner.yml')

for frame in camera.capture_continuous(raw_cap,format="bgr",use_video_port=True):
	raw_cap.truncate(0)
	raw_cap.seek(0)
	image = frame.array
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray)
	
	for (x,y,w,h) in faces:
		cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),2)
		img_id,conf = recognizer.predict(gray[y:y+h,x:x+w])
		if conf>50:		
			if img_id ==1:
				img_id = "YJJ"
		else:
			img_id = "unknown"
		cv2.putText(gray,str(img_id),(x,y+h),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),1)
		
		cv2.imshow("frame",gray)
		if cv2.waitKey(20) & 0xFF == 27:
				break
		
		raw_cap.truncate(0)
			
