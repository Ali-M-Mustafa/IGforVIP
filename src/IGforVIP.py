'''
*********************************************************************************************************************
                                    Sudan University of Science and Technology
                                        Department of ELectrical Engineering
                                                Graduation Project
                                                __________________
                                                ------------------


*Name      :     "Intelligent GLasses For Visually Impaired People (IG for VIP)"

*Supervisor:     @ Jalal Abdulrahman

*Authors   :     @ Ahmed Abdulatif
                 @ Ali Motasim
                 @ Mohammed Abdalazeem
                 @ Ogba Majdi
            
*Date      :     18/1/2022
*********************************************************************************************************************  
'''
#Import Libraries 
import picamera
import cv2
import numpy as np
import RPi.GPIO as GPIO

#Import CODE files
import Face
import detect
import Vibration
from play import play
from speech import listen

#GPIO setting
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)

#______________________________________________________________________

#set pin 31 as output
button_pin     = 31
GPIO.setup(button_pin,GPIO.IN)
GPIO.setup(button_pin,GPIO.IN , pull_up_down = GPIO.PUD_DOWN)

#camera preparation 
camera     = picamera.PiCamera()
camera.resolution = (640,480)

#image pre-processing
image      = np.empty((480,640, 3), dtype=np.uint8)
image_center = tuple(np.array(image.shape[1::-1])/2)
rot_mat    = cv2.getRotationMatrix2D(image_center, -90, 1)

button_stat  = 0 #describe the status of button

orders = [ 'vibration', 'face', 'object'] #list of three different moods
order_indx = 0 

#a callback function for interuption via button 
def B_pressed(p):
    global button_stat
    button_stat = 1    
GPIO.add_event_detect(button_pin, GPIO.BOTH, callback = B_pressed, bouncetime = 100)

#---------------------------------------------------------------------------------
#main loop for differnet moods
#---------------------------------------------------------------------------------

while True :
                         #if button pressed, ask the user to say the mood name or quit
    if button_stat == 1 :
        spoken_word = listen()
        order_indx = orders.index(spoken_word)
        button_stat = 0
#___________________________________________________________________________________
                        #Enter the 'vibration' mood
    if button_stat < 1 and orders[order_indx] == 'vibration':
        button_stat = 0
        play ('mario')
        print ('Vibration')
        while GPIO.input(button_pin) == 0 :
            Vibration.Run(50)
#____________________________________________________________________________________
                        #Enter the 'face' mood
    if button_stat < 1 and orders[order_indx] == 'face':
        button_stat = 0
        play ('mario')
        print ('Face Recognition Mood')
        while GPIO.input(button_pin) == 0 :
            camera.capture(image, format="bgr")
            image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
            Face.Run(image)
            if cv2.waitKey(1) == 27: 
                break
#_________________________________________________________________________________
                       #Enter the 'object' mood
    if button_stat < 1 and orders[order_indx] == 'object':
        button_stat = 0 
        play ('mario')
        print("Object Detection Mood")
        while GPIO.input(button_pin) == 0 :
             camera.capture(image, format="bgr")
             image = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
             detect.Run(image)
             cv2.imshow('object_detector', image)
             if cv2.waitKey(1) == 27: 
                 break
        cv2.destroyAllWindows()

#___________________________________________________________________________________
    
play ('exit')
