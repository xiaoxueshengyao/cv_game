from time import sleep
from picamera import PiCamera

def open_preview():
	with PiCamera() as camera:
		camera.resolution = (320,240)
		camera.start_preview()
		sleep(5)
		camera.capture("a_test.jpg")#,resize=(80,60))
		
if __name__=="__main__":
	open_preview()
