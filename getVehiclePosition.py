#!/usr/bin/env python

from pymavlink import mavutil
import os
import time

simulation = False

if not simulation:
    #check for cable plugged in
    while not os.path.exists("/dev/ttyACM0"):
        time.sleep(1)
        print "Waiting for Serial Connection..."
    
    print "Serial connected!"
    
    the_connection = mavutil.mavlink_connection('/dev/ttyACM0', baud=57600)
    print the_connection
    
       
    #check for good data coming from telemetry before pointing antenna
    telem_data=False
    msg=False
    print "Waiting for Vehicle Telemetry..." 
    while not telem_data:
        msg = the_connection.recv_match()
        if msg:
            if msg.get_type() == 'GPS_RAW_INT':
                telem_data=True
                print "Got Vehicle Telemetry Data!"
                print msg

else:    

    #add some stuff to connect to bluetooth serial connection or whatever
    #the_connection = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
    the_connection = mavutil.mavlink_connection('udpin:192.168.2.132:14550')





class options:
    debug = False
    printMessages = False

def parseRawGpsMav(msg):
    vehicle_pos = {
            'Time':     float(msg.time_usec)*10**-6,
            'Num_Sats': int(msg.satellites_visible),        
            'Lat':      float(msg.lat)*10**-7,
            'Lon':      float(msg.lon)*10**-7,
            'MSL_Alt':  float(msg.alt)*10**-3,
            'GndTrk':   float(msg.cog)*10**-2,
            'GndSpd':   float(msg.vel)*10**-2,
                }
    return vehicle_pos

def getVehiclePosition():
    if not options.printMessages:    
        no_gps=True #init for looking for GPS from vehicle
        while no_gps:
            msg = the_connection.recv_match()
            if not msg:
                no_gps=True
                continue
#            if msg.get_type() == "BAD_DATA":
#                print('bad data!')
#                if mavutil.all_printable(msg.data):
#                   no_gps=True
#                   continue
            else:
        
                if msg.get_type() == 'GPS_RAW_INT':
                    
                #if msg.get_type() == 'ALTITUDE':
                #if msg.get_type() == 'HEARTBEAT':
                #if msg.get_type() == 'AUTOPILOT_VERSION':
                    #print(msg.fieldnames)
                    #if we know the HDOP to less than 5m, and have at least 5 sats visible, return the position
                    if float(msg.fix_type)>=3 and int(msg.satellites_visible) > 5 : 
                        if options.printMessages:                        
                            print "Time: %9.1f -- Lat: %3.6f -- Lon: %3.6f -- AltMSL: %3.2f -- GndTrk: %3.1f -- GndSpd: %3.2f -- NSats: %2.0f " % (float(msg.time_usec)*10**-6,float(msg.lat)*10**-7,float(msg.lon)*10**-7,float(msg.alt)*10**-3,float(msg.cog)*10**-2,float(msg.vel)*10**-2,int(msg.satellites_visible))
                        
                        vehicle_pos=parseRawGpsMav(msg)
                        no_gps=False
                       
                    else: 
                        no_gps=True
                        #print "Need better vehicle position fix, only have %s sats, > 5 required" % msg.satellites_visible
                        
                        continue
        return vehicle_pos
    else:
        msg = the_connection.recv_match(blocking=True)
        print msg.type
        
        
if options.debug:        
    while True:        
        getVehiclePosition()


getVehiclePosition()
