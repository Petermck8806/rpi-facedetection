import numpy as np
import cv2
import datetime, os, time
import RPi.GPIO as GPIO


filename = "" #used to track generated image file name by opencv
GPIO.setmode(GPIO.BCM) #bcm numbering system
PIR_PIN = 23 #motion sensor GPIO PIN
GPIO.setup(PIR_PIN,GPIO.IN) #input on PIR_PIN - 23


#returns rectangle coords for faces found in the image located at the path
def detectFaces(path):
	img = cv2.imread(path)
	cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

	print("Detecting faces...")
	rects = cascade.detectMultiScale(img,1.1,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))

	if len(rects) == 0:
		print("No faces detected...")
		return [], img

	rects[:, 2:] += rects[:, :2]
	return rects,img


#draws rectangles around the faces in the image
def addFaceRectangles(rects, img):
	for x1,y1,x2,y2 in rects:
		print("face detected!")
		cv2.rectangle(img,(x1,y1),(x2,y2),(127,255,0),2)
	cv2.imwrite('images/detected.jpg',img)


#adds the PI day text to the image.
def addPIDay(img):
        cv2.putText(img,"Happy PI Day!",(10,500),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255))
	

#uses the raspberry pi camera module to take a still picture
def captureImage():
        global filename
        filename = "./images/imgsample_" + time.strftime('%Y-%m-%d-%H-%M-%S') + ".jpg"
        os.system("raspistill -w 800 -h 600 -o " + filename)
        

def onMotion(PIR_PIN):
        print("Motion sensed...Starting camera...")
        
        captureImage()
        rects, img = detectFaces(filename)
            
        addFaceRectangles(rects, img)
        addPIDay(img)
               
        cv2.imshow('img',img)
        cv2.moveWindow('img',0,0)
        cv2.waitKey(5000)
        cv2.destroyWindow('img')
        cv2.waitKey(1)

        
try:
        #interrupt - add callback method
        GPIO.add_event_detect(PIR_PIN,GPIO.RISING,callback=onMotion,bouncetime=9000)
        print "waiting for motion..."
        
        #this is silly but whatever.
        while True:
                time.sleep(100)
                
                
#catch keyboard interrupt
except KeyboardInterrupt:
        print "\nCleaning up GPIO"
        GPIO.cleanup()



