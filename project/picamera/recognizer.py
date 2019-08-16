import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from functools import partial
import multiprocessing as mp# multithreading


camera= PiCamera()
camera.resolution = (320,240)

raw_cap = PiRGBArray(camera,size=(320,240))
#load face detector
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

#recognizer
recognizer = cv2.createLBPHFaceRecognizer()
#recognizer = cv2.face.LBPHFaceRecognizer_create()
#recognizer.read('train/trainner_yjj.yml')
recognizer.load('train/trainner')


t_start = time.time()
fps = 0

def sendmsg(name):
    url="http://sc.ftqq.com/SCU52481T8fed00fc62b26c7d97b14fd560310b525cee445745ec3.send?"
    urllib.request.urlopen(url+"text="+name)
    
#jian ce lian 
def get_faces(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray)
	print ('we got'+str(len(faces))+' face(s)')
	
	return faces, gray


#biao zhu lian hua kuang 	
def draw_frame(gray,faces):
	global fps
	
	#draw a rectangle around every face
	for (x,y,w,h) in faces:
		cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),2)
		img_id,conf = recognizer.predict(gray[y:y+h,x:x+w])#shi bie 
		if conf>50:		
			if img_id ==1:
		            img_id = "YJJ"
		            print(img_id+" is comming")
		            #sendmsg(img_id)
		    elif img_id==2:
				img_id='lzy'
				print(img_id+" is comming")
		else:
			img_id = "unknown"
			#sendmsg(img_id)
		cv2.putText(gray,str(img_id),(x,y+h),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,255),1)
	
	fps = fps+1
	sfps = fps/(time.time()-t_start)
	cv2.putText(gray,"fps: "+str(int(sfps)),(10,10),
		cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
	cv2.imshow("frame",gray)
	

if __name__=="__main__":
	pool = mp.Pool(processes =3)
	fcount = 0
	
	camera.capture(raw_cap,format="bgr")
	
	r1 = pool.apply_async(get_faces,[raw_cap.array])
	r2 = pool.apply_async(get_faces,[raw_cap.array])
	r3 = pool.apply_async(get_faces,[raw_cap.array])
	
	
	f1,i1 = r1.get()
	f2,i2 = r2.get()
	f3,i3 = r3.get()
	
	
	raw_cap.truncate(0)
	
	for frame in camera.capture_continuous(raw_cap,format="bgr",use_video_port=True):
		image = frame.array
		
		if fcount==1:
			r1 = pool.apply_async(get_faces,[image])
			f2,i2 = r2.get()
			draw_frame(i2,f2)
		elif fcount==2:
			r2 = pool.apply_async(get_faces,[image])
			f3,i3 = r3.get()
			draw_frame(i3,f3)
		elif fcount==3:
			r3 = pool.apply_async(get_faces,[image])
			f1,i1 = r1.get()
			draw_frame(i1,f1)
		
			
			fcount = 0
		fcount+=1
		if cv2.waitKey(20) & 0xFF == 27:
			break
		raw_cap.truncate(0)
