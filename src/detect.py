#Import Necessary Libraries
import sys
import time
import cv2
import numpy as np
import picamera
import RPi.GPIO as GPIO

#Import Code Files
from object_detector import ObjectDetector
from object_detector import ObjectDetectorOptions
import utils
from play import play
from Vibration import vibrate

#set GPIO
GPIO.setmode(GPIO.BOARD)

#____________________________________________________________________

model     = 'efficientdet_lite0.tflite'    #path for tensor flow lite object detection model
# Visualization parameters
camera_id           = 0
width               = 640
height              = 480
row_size            = 20  # pixels
left_margin         = 24  # pixels
text_color          = (255, 255, 255)  # red
font_size           = 1
font_thickness      = 1
fps_avg_frame_count = 10
button              = 31

#set button oin as GPIO input
GPIO.setup(button,GPIO.IN)
GPIO.setup(button,GPIO.IN , pull_up_down = GPIO.PUD_DOWN)

# Initialize the object detection model
options            = ObjectDetectorOptions(
  num_threads      = 5,
  score_threshold  = 0.4,
  max_results      = 2,
  enable_edgetpu   = False)

detector = ObjectDetector(model_path=model, options=options)
#set a parameters to keep track mentioning the same object 
global t # as a counter
t     = 1
seen  = [] # seen objects
objct = 0
last  = None

# camera = picamera.PiCamera()
# camera.resolution = (640,480)
# image = np.empty((480,640, 3), dtype=np.uint8)
  
# Continuously capture images from the camera and run inference
def Run (image):
    global last
    global objct
    global seen 
    global t
    # Run object detection estimation using the model.
    detections = detector.detect(image)
    try :
        objct = detections[0][1][0][0]
        
        if (objct not in seen or t > 20 )  and objct is not last:
            t = 0
            play(objct)
            seen.append (objct)
            if len (seen ) > 2 : seen.pop(0)
        else :
            t += 1
        last = objct
#         print (seen , last   , t)
    except : pass
#     image = utils.visualize(image, detections)
#     cv2.imshow('object_detector', image)
    if cv2.waitKey(1) == 27: pass
    
#________________________________________________________
    
# image_center = tuple(np.array(image.shape[1::-1])/2)
# rot_mat = cv2.getRotationMatrix2D(image_center, -90, 1)
# while True :
#     camera.capture(image, format="bgr")
#     image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
#     Run(image)
#     if cv2.waitKey(1) == 27: 
#         break
# cv2.destroyAllWindows()
