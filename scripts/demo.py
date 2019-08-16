import cv2
import numpy as np
import os
import multiprocessing as mp

resX = 320
resY = 240

cx = resX / 2
cy = resY / 2

os.system( "echo 0=150 > /dev/servoblaster" )
os.system( "echo 1=150 > /dev/servoblaster" )
 
xdeg = 150
ydeg = 150

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainner/trainner.yml')
#setup the camera
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
cascade_path = "haarcascade_frontalface_alt.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

def get_faces( img ):
 
    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    faces = face_cascade.detectMultiScale( gray )
 
    return faces, img




if __name__ == '__main__':
 
    pool = mp.Pool( processes=4 )
    fcount = 0
 
    camera.capture( rawCapture, format="bgr" )  
 
    r1 = pool.apply_async( get_faces, [ rawCapture.array ] )    
    r2 = pool.apply_async( get_faces, [ rawCapture.array ] )    
    r3 = pool.apply_async( get_faces, [ rawCapture.array ] )    
    r4 = pool.apply_async( get_faces, [ rawCapture.array ] )    
 
    f1, i1 = r1.get()
    f2, i2 = r2.get()
    f3, i3 = r3.get()
    f4, i4 = r4.get()
 
    rawCapture.truncate( 0 )    
 
    for frame in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):
        image = frame.array
 
        if   fcount == 1:
            r1 = pool.apply_async( get_faces, [ image ] )
            f2, i2 = r2.get()
            cv2.rectangle(frame,(x-50,y-50),(x+w+50,y+h+50),(0,255,),2)
		
 
        elif fcount == 2:
            r2 = pool.apply_async( get_faces, [ image ] )
            f3, i3 = r3.get()
            cv2.rectangle(frame,(x-50,y-50),(x+w+50,y+h+50),(0,255,),2)
 
        elif fcount == 3:
            r3 = pool.apply_async( get_faces, [ image ] )
            f4, i4 = r4.get()
            cv2.rectangle(frame,(x-50,y-50),(x+w+50,y+h+50),(0,255,),2)
 
        elif fcount == 4:
            r4 = pool.apply_async( get_faces, [ image ] )
            f1, i1 = r1.get()
            cv2.rectangle(frame,(x-50,y-50),(x+w+50,y+h+50),(0,255,),2)
 
            fcount = 0
 
        fcount += 1
        img_id,conf = recognizer.predict(gray[y:y+h,x:x+w])
        if conf>50:		
            if img_id ==1:
                img_id = "YJJ"
            else:
                img_id = "unknown"
        cv2.putText(frame,str(img_id),(x,y+h),font,1.5,(0,0,255),1)
        rawCapture.truncate( 0 )

