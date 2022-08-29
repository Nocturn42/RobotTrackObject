import cv2 as cv
import numpy as np
import serial
import time
from math import *

#追蹤單一顏色 到一定距離時停止 太靠近則後退
#攝影機解析度 : 640*480 HD-3000

#ser = serial.Serial("/dev/ttyAMA0" , baudrate = 57600 , timeout = 1.0)

direction = None
area = 0
cX = 0
cY = 0
mode = 0
D = 0.0
P = 0.0
P_know_proportion = 0.0

def R1(direction):
    senddata = bytearray()
    senddata.append(0xff)
    senddata.append(0x55)      
    senddata.append(direction)
    return senddata



cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_AUTOFOCUS, False)
width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    blurred_frame = cv.GaussianBlur(frame, (5, 5), 0)
    
    frame_HSV = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)    
    Lower = np.array([80, 80, 80])
    Upper = np.array([100, 255, 255])
    
    
    #RGB轉成HSV 然後侵蝕與膨脹
    mask = cv.inRange(frame_HSV, Lower, Upper)
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
            cv.drawContours(frame, [c], -1, (253, 199, 92), 2)
            cv.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        area = cv.contourArea(c) 

    
    P = area / 13.8

    P_know_proportion = sqrt( P / 1360 )
    D =  80  / P_know_proportion 
    

    cv.putText(frame, "%.2fm" % (D / 100),
             (frame.shape[1] - 200, frame.shape[0] - 20), cv.FONT_HERSHEY_SIMPLEX,
	     2.0, (191, 106, 66), 3)


    print(cX, D)
    
    if area > 100000:
        direction = 2
    elif 100000 > area > 0:
        direction = 1
        if 0 <= cX <= width/4:
            direction = 4
        if width/4 < cX < width/2:
            direction = 3
        if cX == width/2:
            direction = 1
        if width*0.75 > cX > width/2:
            direction = 5
        if width >= cX >= width*0.75:
            direction = 6        
    else:
        direction = 0

    print(direction)

  

    #TXD = R1(direction)
    #ser.write(TXD)
    


    cv.imshow("Frame", frame)
    cv.imshow("Mask", mask)


    key = cv.waitKey(1)

    if key ==27:
        break

#ser.close()
cap.release()
cv.destroyAllWindows()