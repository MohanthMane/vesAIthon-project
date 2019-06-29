import os
import RPi.GPIO as GPIO
import time
import sys

p1=12
p2=18

GPIO.setmode(GPIO.BCM)

GPIO.setup(p1, GPIO.OUT)
GPIO.setup(p2, GPIO.OUT)

p1 = GPIO.PWM(p1, 50)
p2 = GPIO.PWM(p2, 50)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)



p1.start(7.5)
p2.start(7.5)


def get_distance(ax,ay):

        vy=ay/18+2.5
        vx=ax/18+2.5
        p1.ChangeDutyCycle(vy)  # turn towards 90 degree
        p2.ChangeDutyCycle(vx)  # turn towards 90 degree
        time.sleep(0.21) # sleep 1 second
        #p.ChangeDutyCycle(2.5)  # turn towards 0 degree
        #time.sleep(1) # sleep 1 second
        #p.ChangeDutyCycle(12.5) # turn towards 180 degree
        #time.sleep(1) # sleep 1 secon 
        p1.ChangeDutyCycle(vy)  # turn towards 90 degree
        p2.ChangeDutyCycle(vx)  # turn towards 90 degree
        time.sleep(0.2)
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.000001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()
        print("before")
        while GPIO.input(GPIO_ECHO)==0:
            start = time.time()
        while GPIO.input(GPIO_ECHO)==1:
            stop = time.time()
        print("after")
        elapsed = stop-start
        distancet = elapsed * 34300
        distance = distancet / 2
        print ("Distance :{}", distance)
        vy=7.5
        vx=7.5
        p1.ChangeDutyCycle(vy)  # turn towards 90 degree
        p2.ChangeDutyCycle(vx)
        p1.stop()
        p2.stop()
        GPIO.cleanup()
        return round(distance)

#print(get_distance(0,0)
x,y = int(sys.argv[1]),int(sys.argv[2])
os.system('say ' + str(get_distance(x,y)) + ' centimeters away')
