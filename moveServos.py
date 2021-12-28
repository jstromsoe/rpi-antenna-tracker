#!/usr/bin/env python

import time
import pigpio
import csv
import os
#import vectorToVehicle

#options setup
class options:
    testMode=False
    debug=False #use this if you don't have a GPS signal, will just point to some predetermined angles
    verbose=True
    testPause=10 #s at each position
    looprate=10 #Hz
    logfile=True

class pan:
    gpio=21  #GPIOxx number currently on rpi that is being used by the tilt servo, 
    offset=0 #trim offset in degrees
    rot=[]   #placeholder for total amount of rotation desired 
    curr=[]  #placeholder for Current pulse in microseconds
    step=5  #steps for each movement in microseconds
    time=.0001  #time to wait between step commands
    rng=360   #degrees of range on the pan axis (MUST be less than servo capability)
    minpwm = 735 #us
    maxpwm = 2435 #us
    flip = True #flips direction of servo movement in pan 

class tilt:
    gpio=20  #GPIOxx number currently on rpi that is being used by the tilt servo, 
    offset=0 #trim offset in degrees
    rot=[]   #placeholder for total amount of rotation desired 
    curr=[]  #placeholder for Current pulse in microseconds
    step=5   #steps for each movement in microseconds
    time=.0001  #time to wait between step commands
    rng=90   #degrees of range on the tilt axis (MUST be less than servo capability) 
    minpwm = 780 #us
    maxpwm = 1525 #us
    flip = True #flips direction of servo movement in tilt

pi = pigpio.pi() # Connect to local Pi.
pi.set_PWM_frequency(pan.gpio, 50) #setup frequency for PWM
pi.set_PWM_frequency(tilt.gpio, 50) #setup frequency for PWM

tilt.curr=(tilt.minpwm+tilt.maxpwm)/2 #set to neutral first
pan.curr=(pan.minpwm+pan.maxpwm)/2 #set to neutral first

if options.debug:
    tilt.curr=(tilt.maxpwm-tilt.minpwm)/2+tilt.minpwm
    pan.curr =(pan.maxpwm-pan.minpwm)/2+pan.minpwm
    pi.set_servo_pulsewidth(pan.gpio, pan.curr) #move servos to the neutral 
    time.sleep(1)
    pi.set_servo_pulsewidth(tilt.gpio, tilt.curr) #move servos to the neutral
    time.sleep(1)

if options.logfile:
    if not os.path.exists("/home/stroms/rpi-antenna-tracker/logs"):
        os.makedirs("/home/stroms/rpi-antenna-tracker/logs")

    
    class log:
        logdir = '/home/stroms/rpi-antenna-tracker/logs'
        num_files=len([name for name in os.listdir(logdir) if os.path.isfile(os.path.join(logdir, name))])
        log_num=num_files+1
        print "Recording logs to file number: %s" % log_num
        filename=('/home/stroms/rpi-antenna-tracker/logs/'+
        'AT-log_'+
        str('%1.0f' % log_num)+        
        '.csv'
        )
        
#we can use this if we actually know the system time, future development needed to update the system time via GPS.  Details: the ublox GPS needs to be updated to put out the $GPZDA message                
#        local=time.localtime() 
#        filename=('./logs/'+             
#        str(local.tm_year)+
#        str('%02d' % local.tm_mon)+
#        str('%02d' % local.tm_mday)+
#        '_'+
#        str('%02d' % local.tm_hour)+
#        str('%02d' % local.tm_min)+
#        str('%02d' % local.tm_sec)+
#        'AT-log.csv'
#        )
        
    
    #make a header row in the logfile    
    row = [
    'Time(s)',
    'Trkr_Lat(dd)',
    'Trkr_Lon(dd)',
    'Trkr_Hgt(m)',
    'Trkr_Hdg(deg)',
    'Vcl_Lat(dd)',
    'Vcl_Lon(dd)',
    'Vcl_Hgt(m)',
    'Meas_El(deg)',
    'Srvo_El(deg)',
    'Meas_Az(deg)',
    'Adj_Az(deg)',
    'Srvo_Az(deg)',
    'Dsrd_Tilt(us)',
    'Curr_Tilt(us)',
    'Dsrd_Pan(us)',
    'Curr_Pan(us)',
    ]
    
    with open(log.filename,'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
   
   



#enter a test mode that moves the servo to discrete full left, mid, and full right positions, with selectable pause between
if options.testMode:
    #full left (770us for Hitec HS5035HD)
#    pi.set_servo_pulsewidth(tilt.gpio, tilt.minpwm)
#    time.sleep(options.testPause)   
    
    print("Testing Pan")
    #first test pan
#    print("moving to min pan pwm")
#    pi.set_servo_pulsewidth(pan.gpio, pan.minpwm)
#    time.sleep(options.testPause)
    print("moving to mid pwm ")
    pi.set_servo_pulsewidth(pan.gpio, ((pan.maxpwm-pan.minpwm)/2)+pan.minpwm)
    time.sleep(options.testPause)
#    print("moving to min pan pwm")
#    pi.set_servo_pulsewidth(pan.gpio, pan.minpwm)
#    time.sleep(options.testPause)
#    print("moving to max pan pwm")
#    pi.set_servo_pulsewidth(pan.gpio, pan.maxpwm)
#    time.sleep(options.testPause)


#    print("Testing Tilt")
#     #then same for tilt
#    pi.set_servo_pulsewidth(tilt.gpio, tilt.minpwm)
#    time.sleep(options.testPause)
#    pi.set_servo_pulsewidth(tilt.gpio, (tilt.minpwm+tilt.maxpwm)/2)
#    time.sleep(options.testPause)
#    pi.set_servo_pulsewidth(tilt.gpio, tilt.maxpwm)
#    time.sleep(options.testPause)
    
    print("Moving Back to neutral")
#    pi.set_servo_pulsewidth(tilt.gpio, (tilt.minpwm+tilt.maxpwm)/2)
#    pi.set_servo_pulsewidth(pan.gpio, (pan.minpwm+pan.maxpwm)/2)



if not options.debug:
    import vectorToVehicle

if not options.testMode:

    tracker_home=False
    #start main loop
    
    print "now in the main antenna pointing control loop at %3.0f Hz" % (options.looprate) 
    while True:
        #get vector to vehicle
        if not options.debug:
            if not tracker_home:
                    vehicle_vector, tracker_home = vectorToVehicle.vectorToVehicle(False,True) #gets all the angles we need to get position
            else:   
                    
                    vehicle_vector, tracker_home = vectorToVehicle.vectorToVehicle(tracker_home,False)  
                    time.sleep(1/options.looprate)
               
        else:
            vehicle_vector = {
                        'Range':      float(100),
                        'AdjAzimuth': float(59.5),
                        'Elevation':  float(90),
                         }
                         
                         
            tracker_home = {
                        'Time'    :float(1),
                        'Num_Sats':float(12),    
                        'HDOP'    :float(0.67),    
                        'Lat'     :float(32.7529218389),
                        'Lon'     :float(-117.2471762500),
                        'MSL_Alt' :float(-3.19),
                        'Hdg'     :float(0),
                         } 
        #tilt, based on elevation angle

        tilt.angle=vehicle_vector['Elevation']
        pan.angle=vehicle_vector['AdjAzimuth']
        
        
         
        #correctly interpret the pan angle for the servos such that we center the servo about north, arbitrary but easy to remember
        if pan.angle > 180:
            pan.angle = (pan.rng/2)-360+pan.angle

        else:
            pan.angle = pan.rng/2+pan.angle

        #check for bad data
        if tilt.angle>tilt.rng:
            tilt.angle=tilt.rng
        if tilt.angle<0:
            tilt.angle=0
        
        if pan.angle>pan.rng:
            pan.angle=pan.rng
        if pan.angle<0:
            pan.angle=0
            
        #tilt the opposite direction, if desired
        if tilt.flip:
            tilt.angle = tilt.rng-tilt.angle
        
        #pan the opposite direction, if desired
        if pan.flip:
            pan.angle = pan.rng-pan.angle
        
        #flip the pan angle if we are between 0 and 180
#        if tracker_home['Hdg'] > 0 and tracker_home['Hdg'] < 180:
#            pan.angle = pan.rng-pan.angle
         
        
        #convert angles to pwms
        tilt.pwm = ((tilt.angle+tilt.offset)/tilt.rng)*(tilt.maxpwm-tilt.minpwm)+tilt.minpwm
        pan.pwm =  ((pan.angle+pan.offset)/pan.rng)*(pan.maxpwm-pan.minpwm)+pan.minpwm 

        if options.verbose:
            print "Desired Tilt PWM is: %3.2f microseconds" % (tilt.pwm)
            print "Current Tilt PWM is: %3.2f microseconds" % (tilt.curr)
            print "Desired Pan PWM is: %3.2f microseconds" % (pan.pwm)
            print "Current Pan PWM is: %3.2f microseconds" % (pan.curr)
            print "Elevation Angle is: %3.2f deg"  % (vehicle_vector['Elevation'])
            print "Azimuth Angle is: %3.2f deg"  % (vehicle_vector['AdjAzimuth'])
            print "Servo Tilt Angle is: %3.2f deg" % (tilt.angle)
            print "Servo Pan Angle is: %3.2f deg" % (pan.angle)
            
        if options.logfile:
            
            row = [
            vehicle_vector['Time'],
            tracker_home['Lat'],
            tracker_home['Lon'],
            tracker_home['MSL_Alt'],
            tracker_home['Hdg'],
            vehicle_vector['Lat'],
            vehicle_vector['Lon'],
            vehicle_vector['Hgt'],
            vehicle_vector['Elevation'],
            90-tilt.angle,
            vehicle_vector['Azimuth'],
            vehicle_vector['AdjAzimuth'],
            pan.angle,
            tilt.pwm,
            tilt.curr,
            pan.pwm,
            pan.curr
            ]
            with open(log.filename,'a') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()

        
        #move to the tilt or pan .pwm position at a controlled rate
        while abs(tilt.curr-tilt.pwm)>0 or abs(pan.curr-pan.pwm)>0:
            tilt.rot = tilt.curr-tilt.pwm
            pan.rot  = pan.curr-pan.pwm
            #print " %3.2f microseconds to move til desired position reached" % (tilt.rot)
            if tilt.rot > 0 : #need to move -
                pi.set_servo_pulsewidth(tilt.gpio,tilt.curr-tilt.step)
                #print "moving -"
                time.sleep(tilt.time)
                tilt.curr=tilt.curr-tilt.step #update the current value
            else: #need to move +
                pi.set_servo_pulsewidth(tilt.gpio,tilt.curr+tilt.step)
                #print "moving +"
                time.sleep(tilt.time)
                tilt.curr=tilt.curr+tilt.step #update the current value
            
            if abs(tilt.rot)<tilt.step : #then move the last little bit
                pi.set_servo_pulsewidth(tilt.gpio,tilt.pwm)
                time.sleep(tilt.time)
                tilt.curr=tilt.pwm
                
            if pan.rot > 0 : #need to move -
                pi.set_servo_pulsewidth(pan.gpio,pan.curr-pan.step)
                #print "moving -"
                time.sleep(pan.time)
                pan.curr=pan.curr-pan.step #update the current value
            else: #need to move +
                pi.set_servo_pulsewidth(pan.gpio,pan.curr+pan.step)
                #print "moving +"
                time.sleep(pan.time)
                pan.curr=pan.curr+pan.step #update the current value
            
            if abs(pan.rot)<pan.step : #then move the last little bit
                pi.set_servo_pulsewidth(pan.gpio,pan.pwm)
                time.sleep(pan.time)
                pan.curr=pan.pwm
        if options.debug:
            print("debug run finished")
            break
        
          
    
     



   
   
   
   
   
   
   
   
   
   
   
   
   
# switch servos off
#pi.set_servo_pulsewidth(pan.gpio, 0);
#pi.set_servo_pulsewidth(tilt.gpio, 0);
#pi.stop()
