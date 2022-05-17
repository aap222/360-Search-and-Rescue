import socket
import time
import numpy as np

from NatNetClient import NatNetClient
from util import quaternion_to_euler_angle_vectorized1

positions = {}
rotations = {}

# This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
def receive_rigid_body_frame(robot_id, position, rotation_quaternion):
    # Position and rotation received
    positions[robot_id] = position
    # The rotation is in quaternion. We need to convert it to euler angles

    rotx, roty, rotz = quaternion_to_euler_angle_vectorized1(rotation_quaternion)

    rotations[robot_id] = rotz
        
if __name__ == "__main__":

    IP_ADDRESS = '192.168.0.202'
    clientAddress = "192.168.0.2"
    optitrackServerAddress = "192.168.0.4"
    robot_id = 2

    streaming_client = NatNetClient()
    streaming_client.set_client_address(clientAddress)
    streaming_client.set_server_address(optitrackServerAddress)
    streaming_client.set_use_multicast(True)
    
    streaming_client.rigid_body_listener = receive_rigid_body_frame
    
    is_running = streaming_client.run()


    # Connect to the robot
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP_ADDRESS, 5000))
    print('Connected')

    waypoint_state = 0
    kω = 15
    kd = 650
    r = .5

    try:
        while is_running:
            if robot_id in positions:
                print("seen")
                if(waypoint_state == 0):
                    p_d = [5.5,-3.2]
                elif(waypoint_state == 1):
                    p_d = [0.,-3.]
                elif(waypoint_state == 2):
                    p_d = [5.5,-3.]
                elif(waypoint_state == 3):
                    p_d = [5.5, 0.] # end of first path
                elif(waypoint_state == 4):
                    p_d = [5.5, 3.5]
                elif(waypoint_state == 5):
                    p_d = [.75, 3.5]
                elif(waypoint_state == 6):
                    p_d = [5.5, 3.5]
                elif(waypoint_state == 7):
                    p_d = [5.5, 0.] # end of second path
                elif(waypoint_state == 8):
                    p_d = [1., 0.]
                elif(waypoint_state == 9):
                    p_d = [5.5, 0.] # end of third path

                print(p_d)
                p_r = [positions[robot_id][0], positions[robot_id][1]]
                α = np.arctan2((p_d[1]-p_r[1]), (p_d[0]-p_r[0]))
                q = (p_d[0] - p_r[0] , p_d[1] - p_r[1])
                distance = np.sqrt(q[0]**2+q[1]**2)
                theta_r = np.radians(rotations[robot_id])

                ω = kω *np.degrees(np.arctan2((α-theta_r),(α-theta_r)) + 1.57)
                #ω = 0
                v = kd*(distance)
                
                u = np.array([v-ω,v+ ω])
                u[u > 1500] = 1500
                u[u < -1500] = -1500
                

                if(distance <= r):
                    wait_time = 1.3
                    if waypoint_state == 0:
                        command = 'CMD_MOTOR#1500#1500#-1500#-1500\n'
                        s.send(command.encode('utf-8'))
                        time.sleep(wait_time * .7)
                        command = 'CMD_MOTOR#00#00#00#00\n'
                        s.send(command.encode('utf-8'))
                        time.sleep(wait_time)
                    if waypoint_state == 6:
                        command = 'CMD_MOTOR#-1500#-1500#1500#1500\n'
                        s.send(command.encode('utf-8'))
                        time.sleep(wait_time)
                        command = 'CMD_MOTOR#00#00#00#00\n'
                        s.send(command.encode('utf-8'))
                        time.sleep(wait_time)
                    if waypoint_state == 1 or waypoint_state == 5 or waypoint_state == 8:
                        command = 'CMD_MOTOR#1500#1500#-1500#-1500\n'
                        s.send(command.encode('utf-8'))
                        time.sleep(wait_time * 2.5)
                        command = 'CMD_MOTOR#00#00#00#00\n'
                        s.send(command.encode('utf-8'))
                        time.sleep(wait_time)
                    waypoint_state += 1
                    #command = 'CMD_MOTOR#0000#0000#-1500#-1500\n'
                    #s.send(command.encode('utf-8'))
                    #time.sleep(1)'''

                # Send control input to the motors
                command = 'CMD_MOTOR#%d#%d#%d#%d\n'%(u[0], u[0], u[1], u[1])
                s.send(command.encode('utf-8'))
                #print("Robot: ", p_r,  "\nDestination: ", p_d, "\nDistance: ", distance)
                print("ω: ", ω, "\tv: ", v, "\tu: ", u, "\np_r: ", p_r, "\ttheta_r: ", theta_r, "\ttheta_d: ", α, "\ndistance: ", distance)

                print(waypoint_state)
                # Wait for 1 second
                time.sleep(.1)


    except KeyboardInterrupt:
        # STOP
        command = 'CMD_MOTOR#00#00#00#00\n'
        s.send(command.encode('utf-8'))
        s.shutdown(2)
        s.close()

    # Close the connection