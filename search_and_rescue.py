import sys
import socket
import time
import math

#from numpy import true_divide
import numpy as np
from NatNetClient import NatNetClient
from util import quaternion_to_euler_angle_vectorized1

IP_ADDRESS = '192.168.0.202'
clientAddress = "192.168.0.48"
optitrackServerAddress = "192.168.0.4"
robot_id = 2
positions = {}
rotations = {}

FAST = 'CMD_MOTOR#1500#1500#1500#1500\n'
SLOW = 'CMD_MOTOR#1200#1200#1200#1200\n'
RIGHT = 'CMD_MOTOR#1500#1500#-1500#-1500\n'
LEFT = 'CMD_MOTOR#-1500#-1500#1500#1500\n'
BACKWARD = 'CMD_MOTOR#-1500#-1500#-1500#-1500\n'
STOP = 'CMD_MOTOR#00#00#00#00\n'

# format [x, y, rotation to rotate to (if applicable)]
RESCUE_CIRCLE = [0, 0, 0]

# Connect to the robot
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP_ADDRESS, 5000))
print('Connected')

# This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
def receive_rigid_body_frame(robot_id, position, rotation_quaternion):
    # Position and rotation received
    positions[robot_id] = position
    # The rotation is in quaternion. We need to convert it to euler angles

    rotx, roty, rotz = quaternion_to_euler_angle_vectorized1(rotation_quaternion)

    rotations[robot_id] = rotz

def control_robot(currentPos, currentRot):
    
    # Send control input to the motors
    command = 'CMD_MOTOR#%d#%d#%d#%d\n'%(u[0], u[0], u[1], u[1])
    s.send(command.encode('utf-8'))
    print(command)


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
    
    while robot_id not in positions:
        print("Looking for robot")
        continue
    print('Starting\n')
    try:
        while is_running:
            if robot_id in positions:
                currentPos = positions[robot_id]
                currentRot = rotations[robot_id]
                print('Last position', currentPos, ' rotation', currentRot)
                control_robot(currentPos, currentRot)

                time.sleep(1)
    except KeyboardInterrupt:
        # STOP
        print("Stopping\n")
        command = STOP
        s.send(command.encode('utf-8'))
        # Close the connection
        s.shutdown(2)
        s.close()
