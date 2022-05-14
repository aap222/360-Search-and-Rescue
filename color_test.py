import cv2
import numpy as np

'''
    This file is for testing the color filter and blob detection
'''
 
cap = cv2.VideoCapture(0)
 
while(1):
    _, frame = cap.read()
    # It converts the BGR color space of image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     
    # Threshold of blue in HSV space
    lower_yellow = np.array([27, 35, 140])
    upper_yellow = np.array([40, 255, 255])
 
    # preparing the mask to overlay
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
     
    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all non-blue regions
    result = cv2.bitwise_and(frame, frame, mask = mask)
 
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

 
cv2.destroyAllWindows()
cap.release()