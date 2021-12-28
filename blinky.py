#!/usr/bin/env python

import pigpio
from time import sleep
import math


class options:
    gpio = 16
    rate = 200 #Hz

pi = pigpio.pi() # Connect to local Pi.
inc = 0
duty = 0
while True:
    inc = inc + float(options.rate)/float(255)
    if inc >= float(3.1415) or duty < 0:
        inc = float(0)
        duty = 255*math.sin(inc)
    else:
        duty = 255*math.sin(inc)
    pi.set_PWM_dutycycle(options.gpio,duty) # PWM off
    sleep(1/options.rate)
    
    

    

#pi.set_PWM_frequency(options.gpio,options.rate) #setup frequency for PWM
#pi.set_servo_pulsewidth(options.gpio,)
#pi.set_servo_pulsewidth(options.gpsGpio,options.ledPWM)


#while True:
#    GPIO.setmode(GPIO.BCM)
#    GPIO.setwarnings(False)
#    GPIO.setup(options.gpsGpio,GPIO.OUT)
#    GPIO.output(options.gpsGpio,GPIO.HIGH)
#    sleep(options.delay)
#    GPIO.output(options.gpsGpio,GPIO.LOW)
#    sleep(options.delay)