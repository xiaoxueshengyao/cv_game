import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

#setup the camera
camera = PiCamera()
camera.resolution = (320,240)
#camera.framerate=60# fuck u off
raw_cap = PiRGBArray(camera,size=(320,240))
#load face detector
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

#calculate the fps
t_start = time.time()
fps = 0


for frame in camera.capture_continuous(raw_cap,format="bgr",use_video_port=True):
	image = frame.array
	
	#detect faces
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray)
	print ('we got'+str(len(faces))+' face(s)')
	
	#draw rectangle around every face
	
	for (x,y,w,h) in faces:
		cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
	
	fps = fps+1
	sfps = fps/(time.time()-t_start)
	cv2.putText(image,"fps: "+str(int(sfps)),(10,10),
		cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
	
	cv2.imshow("frame",image)
	
	#cv2.waitKey(1)
	if cv2.waitKey(20) & 0xFF == 27:
		break
	#clear stream in preparation for the next time
	raw_cap.truncate(0)

