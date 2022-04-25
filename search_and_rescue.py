import sys
import socket
import time
import math

#from numpy import true_divide
import numpy as np
from NatNetClient import NatNetClient
from util import quaternion_to_euler_angle_vectorized1

positions = {}
rotations = {}

# easy ways to give robot static movement commands
FAST = 'CMD_MOTOR#1500#1500#1500#1500\n'
SLOW = 'CMD_MOTOR#1200#1200#1200#1200\n'
RIGHT = 'CMD_MOTOR#1500#1500#-1500#-1500\n'
LEFT = 'CMD_MOTOR#-1500#-1500#1500#1500\n'
BACKWARD = 'CMD_MOTOR#-1500#-1500#-1500#-1500\n'
STOP = 'CMD_MOTOR#0#0#0#0\n'

# format [x, y, rotation to rotate to (if applicable)]
RESCUE_CIRCLE = [0, 0, 0]

# Connect to the robot
IP_ADDRESS = '192.168.0.202' #robot's IP address
clientAddress = "192.168.0.48" # user's computer's IP address
optitrackServerAddress = "192.168.0.4" # IP address of camera system
robot_id = 2
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_ADDRESS, 5000))
print('Connected to robot ' + str(robot_id))

# This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
def receive_rigid_body_frame(robot_id, position, rotation_quaternion):
    # Position and rotation received
    positions[robot_id] = position
    # The rotation is in quaternion. We need to convert it to euler angles

    rotx, roty, rotz = quaternion_to_euler_angle_vectorized1(rotation_quaternion)

    rotations[robot_id] = rotz

"""
    Navigates around lab while using on-board camera with color filter to search for unique target
    colors.  Also tracks if robot is within view of lab's camera system.  SHould the robot be out 
    of it too long, the robot will switch to searching while only relying on on-board sensors until
    it is back in camera's view.  When a target has been identified, the robot stops moving and the 
    function returns.

    Inputs:
        x
        y
    Returns:
        type - number indicating which type of target has been identified
"""
def search():
    print("searching")

"""
    With the type of target having been identified, this function centers the target within its camera
    frame and moves forward rapidly, scooping up the target.

    Inputs:
        type - the type of target that has been identified while searching; the type indicates which 
        color filter the function should use on the camera
    Returns:
        null - returning indicates the target has been captured
"""
def capture():
    print("capturing")

"""
    Move robot with target in scoop back to the rescue circle.  After arriving at the rescue circle,
    the robot waits a certain number of seconds for the operator to remove the target from the scoop
    then returns.

    Inputs:
        x - 
        y - 
    Return:
        null - returning indicates the robot has stayed in the rescue circle for the required 
        amount of time
"""
def return_target():
    print("returning")

if __name__ == "__main__":
    # This will create a new NatNet client
    streaming_client = NatNetClient()
    streaming_client.set_client_address(clientAddress)
    streaming_client.set_server_address(optitrackServerAddress)
    streaming_client.set_use_multicast(True)
    # Configure the streaming client to call our rigid body handler on the emulator to send data out.
    streaming_client.rigid_body_listener = receive_rigid_body_frame

    # Start up the streaming client now that the callbacks are set up.
    # This will run perpetually, and operate on a separate thread.
    is_running = streaming_client.run()

    print("Connected to OptiTrack System")
    
    print("Looking for robot")
    while robot_id not in positions:
        continue
    print('Robot Found!  Starting Search and Recue Operations.\n')
    try:
        sleep_time = 1 # in seconds
        while is_running:
            type = search()
            capture(type)
            return_target()
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        # STOP
        print("Stopping\n")
        command = STOP
        s.send(command.encode('utf-8'))
        # Close the connection
        s.shutdown(2)
        s.close()
