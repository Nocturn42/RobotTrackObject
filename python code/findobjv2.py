from __future__ import print_function
import cv2 as cv
import numpy as np
import serial
import time
import argparse


#攝影機解析度 : 640*480 HD-3000

#ser = serial.Serial("/dev/ttyAMA0" , baudrate = 57600 , timeout = 1.0)

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value

window_capture_name = 'Frame'
window_detection_name = 'Mask'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

err_new = float(0.0)
kp = 1
kd = 0
sign = None
direction = None
area = 0
cX = 0
cY = 0

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)

def R1(direction):
    senddata = bytearray()
    senddata.append(0xff)
    senddata.append(0x55)      
    senddata.append(direction)
    return senddata


parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera devide number.', default=0, type=int)
args = parser.parse_args()
cap = cv.VideoCapture(args.camera)
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    blurred_frame = cv.GaussianBlur(frame, (11, 11), 0)
    
    frame_HSV = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)    
    
    
    #RGB轉成HSV 然後侵蝕與膨脹
    mask = cv.inRange(frame_HSV,  (low_H, low_S, low_V), (high_H, high_S, high_V))
    mask = cv.erode(mask, None, iterations=2)    
    mask = cv.dilate(mask, None, iterations=2)

    contours, ret = cv.findContours(mask.copy(), cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    
   
    for c in contours:        
        #find the biggest area
        
        c = max(contours, key = cv.contourArea)
        M = cv.moments(c)                      #將中心座標帶入M
        if M["m00"] != 0:                      #由於除數不能為0所以一定要先設判斷式才不會出錯
            cX = int(M["m10"] / M["m00"])      #找出中心的x座標
            cY = int(M["m01"] / M["m00"])      #找出中心的y座標
            cv.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        area = cv.contourArea(c) 
    
    print(cX, area)
    time.sleep(0.04)
    if area > 100000:
        direction = 2
    elif 100000 >= area >= 0:
        direction = 1
        if cX < width/2:
            direction = 3
        if cX > width/2:
            direction = 4
        if cX == width/2:
            direction = 1
    else:
        direction = 0

    print(direction)

  

    #TXD = R1(direction)
    #ser.write(TXD)
    



    cv.imshow(window_capture_name, frame)
    cv.imshow(window_detection_name, mask)


    key = cv.waitKey(1)

    if key ==27:
        break

#ser.close()
cap.release()
cv.destroyAllWindows()