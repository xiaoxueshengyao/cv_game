import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

face_detector = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml") 
#get video
camera= PiCamera()
camera.resolution = (320,240)
raw_cap = PiRGBArray(camera,size=(320,240))
sample_num = 0
#id = raw_input('enter ur id:')
#1--YJJ, 2--lzy
id =2
for frame in camera.capture_continuous(raw_cap,format="bgr",use_video_port=True):
    # Capture frame-by-frame
    raw_cap.truncate()
    raw_cap.seek(0)
    image = frame.array

    # Our operations on the frame come here
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #cv2.imshow('frame',gray)
    faces = face_detector.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5)
    for (x,y,w,h) in faces:
        cv2.rectangle(gray,(x,y),(x+w,y+h),(0,255,0),2)
        sample_num = sample_num+1
        cv2.imwrite("data/user."+str(id)+'.'+str(sample_num)+".jpg",gray[y:y+h,x:x+w])
        cv2.imshow('frame',gray)
    if cv2.waitKey(100) & 0xFF == 27:
        # When everything done, release the capture
        raw_cap.truncate(0)
        break
    elif sample_num>=50:
        break

print("\n[INFO] Exiting program ,I got it")
raw_cap.truncate(0)
