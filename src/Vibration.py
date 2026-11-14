#Import necessary Libraries
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
#set GPIO Pins
GPIO_TRIGGER  = 37
GPIO_ECHO     = 35
vib           = 33
button        = 31
GPIO.setup(button,GPIO.IN)
GPIO.setup(button,GPIO.IN , pull_up_down = GPIO.PUD_DOWN)

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(vib, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#this function calculate the distance and compare with a a given value D; if less activate the vibrator
def vibrate(d):
    d = int(d)
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0 and TimeElapsed < (1/343):
        StartTime = time.time()
        TimeElapsed = StopTime - StartTime
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1 :#and TimeElapsed < (1/343):
        StopTime = time.time()
        TimeElapsed = StopTime - StartTime
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    vibtime = .1*(1-(distance/d)) + .05
    sleeptime = .1*(distance/d)
    #print ("getting distance")
    t= 0 
    while distance <= d and t <3 :#and TimeElapsed != (1/343) :
        #print("low")
        GPIO.output(vib, True)
        time.sleep(0.1)
        GPIO.output(vib, False)
        time.sleep(0.1)
        t+= 1
    return int(distance)
def Run(D):
    while GPIO.input(button) is  not 1  :
        while GPIO.input(button) is not 1  :
            dist = vibrate(D)
            print ("Measured Distance = %.1f cm" % dist,'\t button state is' ,GPIO.input(button))
            dist = 0
        GPIO.output(vib,False)
        GPIO.cleanup
    GPIO.output(vib,False)
    GPIO.cleanup
#Run (50)
# GPIO.output(vib,False)
# print ('pressed botton')