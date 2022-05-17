'''
    This file is for testing the search algorithm
'''

import sys
import socket
import time
import math
from tkinter import LAST

#from numpy import true_divide
import numpy as np
from NatNetClient import NatNetClient

# +- limit for robotics lab grid & important points
global X_LIMIT
X_LIMIT = 5
global Y_LIMIT
Y_LIMIT = 5
global RESCUE_CIRCLE
RESCUE_CIRCLE = [0, -5]
global LAST_POS
LAST_POS = [-5, -5]
FINAL_POS = [5, 5]

# Globals for states of moving around the lab
global UP
UP = 0
global DOWN
DOWN = 1
global LEFT
LEFT = 2
global RIGHT
RIGHT = 3
global STATE
STATE = UP

# dividing lab into grid and marking off
global EXPLORED    # number of squares in grid explored
EXPLORED = 0
global OPEN
OPEN = 0
global SEARCHED
SEARCHED = 1
global OBSTACLE
OBSTACLE = 2
global GRID
GRID = [[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN], 
[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN], 
[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN], 
[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN], 
[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN], 
[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN], 
[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN], 
[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN], 
[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN], 
[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN], 
[OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN, OPEN]]
GRID[LAST_POS[0] + 5][LAST_POS[1] + 5] = SEARCHED
global SQUARES
SQUARES = len(GRID) * len(GRID[0])  # total # of squares in the lab
#SQUARES = 5

# fake data for testing
global DUCKS
DUCKS = [[0, 0], [4, 3]]
global OBSTACLES
OBSTACLES = [[-4, 3], [1, 1]]

def print_grid():
    for row in GRID:
        print(row)

def direction_check():
    global STATE
    global LAST_POS
    global Y_LIMIT
    global X_LIMIT

    if STATE == UP:
        if (LAST_POS[1]) == Y_LIMIT:
            return False
        return True
    if STATE == DOWN:
        if (LAST_POS[1]) == -Y_LIMIT:
            return False
        return True
    if STATE == LEFT:
        if (LAST_POS[0]) == -X_LIMIT:
            return False
        return True
    if STATE == RIGHT:
        if (LAST_POS[0]) == X_LIMIT:
            return False
        return True

# function that actually sends the move commands to the robot
def go_to_coords(coords):
    print("Going to coords: " + str(coords))
    return True

def move():
    global STATE
    global LAST_POS
    global Y_LIMIT

    if STATE == UP:
        LAST_POS[1] += 1
    if STATE == DOWN:
        LAST_POS[1] -= 1
    if STATE == RIGHT:
        LAST_POS[0] += 1
        if LAST_POS[1] == -Y_LIMIT:
            STATE = UP
        if LAST_POS[1] == Y_LIMIT:
            STATE = DOWN
    if STATE == LEFT:
        LAST_POS[0] -= 1
    go_to_coords(LAST_POS)
    print("New Position: " + str(LAST_POS))
    mark_grid([LAST_POS[0] + 5, LAST_POS[1] + 5], SEARCHED)
    global EXPLORED
    EXPLORED += 1

def get_direction():
    if STATE == UP:
        return "UP"
    if STATE == DOWN:
        return "DOWN"
    if STATE == LEFT:
        return "LEFT"
    if STATE == RIGHT:
        return "RIGHT"

def mark_grid(POS, status):
    global GRID
    GRID[POS[0]][POS[1]] = status

def ultrasound_check():
    global OBSTACLES
    global LAST_POS
    limit = 30  # limit for how close robot can get
    detected_distance = 40
    check = []

    if STATE == UP:
        check = [LAST_POS[0], LAST_POS[1] + 1]

    if STATE == DOWN:
        check = [LAST_POS[0], LAST_POS[1] - 1]

    if STATE == LEFT:
        check = [LAST_POS[0] - 1, LAST_POS[1]]

    if STATE == RIGHT:
        check = [LAST_POS[0] + 1, LAST_POS[1]]
    
    if check in OBSTACLES:
        print("OBASTACLE DETECTED")
        detected_distance = limit - 1
    
    if detected_distance <= limit:
        print("Obstacle detected, going around")
        if STATE == UP:
            mark_grid([LAST_POS[0] + 5, LAST_POS[1] + 6], OBSTACLE)
            go_to_coords([LAST_POS[0] - 1, LAST_POS[1]])
            go_to_coords([LAST_POS[0] - 1, LAST_POS[1] + 2])
            go_to_coords([LAST_POS[0], LAST_POS[1] + 2])
            LAST_POS = [LAST_POS[0], LAST_POS[1] + 2]

        if STATE == DOWN:
            mark_grid([LAST_POS[0] + 5, LAST_POS[1] + 4], OBSTACLE)
            go_to_coords([LAST_POS[0] - 1, LAST_POS[1]])
            go_to_coords([LAST_POS[0] - 1, LAST_POS[1] - 2])
            go_to_coords([LAST_POS[0], LAST_POS[1] - 2])
            LAST_POS = [LAST_POS[0], LAST_POS[1] - 2]

        if STATE == LEFT:
            mark_grid([LAST_POS[0] + 4, LAST_POS[1] + 5], OBSTACLE)
            go_to_coords([LAST_POS[0], LAST_POS[1] - 1])
            go_to_coords([LAST_POS[0] - 2, LAST_POS[1] - 1])
            go_to_coords([LAST_POS[0] - 2, LAST_POS[1]])
            LAST_POS = [LAST_POS[0] - 2, LAST_POS[1]]

        if STATE == RIGHT:
            mark_grid([LAST_POS[0] + 6, LAST_POS[1] + 5], OBSTACLE)
            go_to_coords([LAST_POS[0], LAST_POS[1] - 1])
            go_to_coords([LAST_POS[0] + 2, LAST_POS[1] - 1])
            go_to_coords([LAST_POS[0] + 2, LAST_POS[1]])
            LAST_POS = [LAST_POS[0] + 2, LAST_POS[1]]

    return True

def duck_check():
    global LAST_POS
    global DUCKS

    if LAST_POS in DUCKS:
        print("Duck found!")
        return True

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
    go_to_coords(LAST_POS)
    print("Starting Search at: " + str(LAST_POS))
    global STATE
    SPOTTED = False

    wait_time = 1

    # Big search loop that checks for several limits, like ultrasound and # of squares checked
    while not SPOTTED and EXPLORED < SQUARES:
        if duck_check():
            return True

        # worked way to other end of lab
        if LAST_POS[0] == FINAL_POS[0] and LAST_POS[1] == FINAL_POS[1]:
            return False

        # continue moving
        #print("Making move number " + str(EXPLORED))

        # check the ultrasound distance
        distance = ultrasound_check()

        # checks if next movement will move out of bounds
        bounds = direction_check()
        if bounds:
            #print("Continuing movement in " + get_direction())
            move()
            print_grid()
            time.sleep(wait_time)
        if not bounds:
            if STATE == UP:
                STATE = RIGHT
            if STATE == RIGHT:
                STATE = DOWN
            if STATE == DOWN:
                STATE = RIGHT
            #print("Changing movement to direction " + get_direction())
            print_grid()
            time.sleep(wait_time)
            continue
            
    return False

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
    global LAST_POS

    print("Capturing ducky")
    if STATE == UP:
        LAST_POS = [LAST_POS[0], LAST_POS[1] + 1]
    if STATE == DOWN:
        LAST_POS = [LAST_POS[0], LAST_POS[1] - 1]
    if STATE == LEFT:
        LAST_POS = [LAST_POS[0] - 1, LAST_POS[1]]
    if STATE == UP:
        LAST_POS = [LAST_POS[0] + 1, LAST_POS[1]]

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
    print("Returning to rescue circle at: " + str(RESCUE_CIRCLE))
    go_to_coords(RESCUE_CIRCLE)

if __name__ == "__main__":
    continue_search = True
    while continue_search:
        continue_search = search()
        capture()
        return_target()
    print_grid()