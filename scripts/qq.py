import cv2
import numpy

cap = cv2.VideoCapture(1)
#fps=30
#size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

while 1:
    ret, frame = cap.read()
    cv2.imshow("capture", frame)
    if cv2.waitKey(10) & 0xff == ord('q'):
        break
"""
video_write = cv2.VideoWriter("test.avi",cv2.VideoWriter_fourcc('I','4','2','0'),fps,size)
num = 10*fps-1
ret, frame = cap.read()
while ret and num>0:
	video_write.write(frame)
	ret, frame = cap.read()
	num-=1
"""
cap.release()
cv2.destroyAllWindows()
