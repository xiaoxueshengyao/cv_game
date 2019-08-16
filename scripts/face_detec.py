#图片人脸检测
import cv2
import sys
import matplotlib.pyplot as plt

# Get user supplied values
imagePath = "./me2.jpg"
# Create the haar cascade
faceCascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml") 
# Read the image
image = cv2.imread(imagePath)#2
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#3
# Detect faces in the image
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.15,
    minNeighbors=5,
    minSize=(5,5),
    flags = cv2.CASCADE_SCALE_IMAGE
) #4
print("Found {0} faces!".format(len(faces)))#5

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2) #6
crop = gray[x:x+w,y:y+h,]
crop = cv2.resize(crop,(96,96),interpolation=cv2.INTER_CUBIC)
cv2.imshow("Faces found", image)#7

 
plt.imshow(crop)
plt.show()

cv2.waitKey(0) #8

