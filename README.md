# 360-Search-and-Rescue
Authors: Andrew Principato
         Daniel Lin

There are several test files used in this project.  The first test file is color_test.py, which we used to test detecting of the ducks and figuring out HSV values

Next is return.py, which was used to test returning the robot from any point in the lab to the rescue circle.

movement_test.py is a large file used to test our search algorithm and its handling of obstacles.  It runs a simulation of searching an 11x11 grid with 2 ducks and 2 obstacles.  This would have served as the basis for our lab-searching algorithm if we had more time.

waypoints.py is what we ultimately used for the lab competition.  We set waypoints around the lab our robot followed to bring ducks back.  Because the robot couldn't bring a duck from the lower area up onto the mat, we ensured it always stayed on the track.  The problem with the algorithm is that it does not control the robots orientation very well, so it had a lot of trouble going from point-to-point.  