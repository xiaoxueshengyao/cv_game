import numpy as np
import cv2


face_detector = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml") 
cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    #cv2.imshow('frame',gray)
    faces = face_detector.detectMultiScale(gray,
    scaleFactor=1.15,
    minNeighbors=5,
    minSize=(5,5),
    flags = cv2.CASCADE_SCALE_IMAGE
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('frame',frame)
    if cv2.waitKey(10) & 0xFF == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
