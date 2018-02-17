
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
import Tkinter as tk


def set_velocity_body(vehicle, vx, vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()


#This part of the code is to ensure that the drone is ready to take off#
def arm_and_takeoff(TargetAltitude):
#### your code here #####
    print ("Excecuting Takeoff")

    while not drone.is_armable:
        print("Vehicle is not armable, waiting....")
        time.sleep(1)
    print("ready to arm")
    drone.mode = VehicleMode("GUIDED")
    drone.armed = True

    while not drone.armed:
        print("Waiting for arming")
        time.sleep(1)

    print("Ready for takeoff, taking off")
    drone.simple_takeoff(TargetAltitude)

    while True:
        Altitude = drone.location.global_relative_frame.alt
        print("Altitude: ", Altitude)
        time.sleep(1)

        if Altitude >= TargetAltitude * 0.95:
            print("Altitude reached")
            break
#The first part of the code lets you open tk to use arrows to use, the next part is to tell the drone that every time the key is pressed the drone will advance 5 m to that direction#

def key(event):
    if event.char == event.keysym: #-- standard keys
        if event.keysym == 'r':
            drone.mode = VehicleMode("RTL")            
    else: #-- non standard keys
        if event.keysym == 'Up':
            set_velocity_body(drone,5,0,0)
        elif event.keysym == 'Down':
            set_velocity_body(drone,-5,0,0)

        elif event.keysym == 'Left':
            set_velocity_body(drone,0,-5,0)

        elif event.keysym == 'Right':
            set_velocity_body(drone,0,5,0)



#This command lets us connect to any device we want#
drone = connect ('127.0.0.1:14551', wait_ready=True)

# Take off to 10 m altitude#
arm_and_takeoff(10)
 
# The code starts to run the tk program to habilitate the arrow keys#
root = tk.Tk()
print(">> Control the drone with the arrow keys. Press r for RTL mode")
root.bind_all('<Key>', key)
root.mainloop()