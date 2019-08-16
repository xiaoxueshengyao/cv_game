import cv2
import numpy as np

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner/trainner.yml")

cascade_path = "./haarcascade_frontalface_alt.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)
#get camera
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
	ret,frame = cap.read()
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray,1.2,5)
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x-50,y-50),(x+w+50,y+h+50),(0,255,),2)
		img_id,conf = recognizer.predict(gray[y:y+h,x:x+w])
		if conf>50:		
			if img_id ==1:
				img_id = "YJJ"
		else:
			img_id = "unknown"
		cv2.putText(frame,str(img_id),(x,y+h),font,1.5,(0,0,255),1)
	cv2.imshow("frame",frame)
	if cv2.waitKey(10) &0xFF == 27:
		break
cap.release()
cv2.destroyAllWindows()
