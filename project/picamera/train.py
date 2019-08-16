import cv2
import os
import numpy as np
from PIL import Image

#initialize face recognizer
#recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer = cv2.createLBPHFaceRecognizer()
detector = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml")

def get_image_and_labels(path):
    image_paths = [os.path.join(path,f) for f in os.listdir(path)]
    face_samples = []
    ids = []
    
    for image_path in image_paths:
        image = Image.open(image_path).convert('L')
        image_np = np.array(image,'uint8')
        if os.path.split(image_path)[-1].split(".")[-1] != 'jpg':
            continue
        image_id = int(os.path.split(image_path)[-1].split(".")[1])
        faces= detector.detectMultiScale(image_np)
        for (x,y,w,h) in faces:
            face_samples.append(image_np[y:y+h,x:x+w])
            ids.append(image_id)
    return face_samples,ids
    
faces,ids = get_image_and_labels('data')
recognizer.train(faces,np.array(ids))
#recognizer.save('train/trainner_yjj.yml')
#recognizer.write('train/trainner_yjj.yml')
recognizer.save('train/trainner.yml')
print("\n [INFO]{0} faces trained. Exiting Program".format(len(np.unique(ids))))

