import cv2 as cv
import numpy as np
import serial
import time


#攝影機解析度 : 1280X720 C310

#ser = serial.Serial("/dev/ttyAMA0" , baudrate = 57600 , timeout = 1.0)

err_new = float(0.0)
kp = 1
kd = 0
sign = None
direction = None
area = None
cX = None
cY = None



def R1(speed, sign, direction):
    senddata = bytearray()
    senddata.append(0xff)
    senddata.append(0x55)
    senddata.append(speed)
    senddata.append(sign)
    senddata.append(direction)
    return senddata


cap = cv.VideoCapture(0)
width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

while True:
    ret, frame = cap.read()
    if frame is None:
        break
    blurred_frame = cv.GaussianBlur(frame, (11, 11), 0)
    
    frame_HSV = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)
    
    
    Lower = np.array([80, 80, 100])
    Upper = np.array([100, 150, 255])

    
    #RGB轉成HSV 然後侵蝕與膨脹
    mask = cv.inRange(frame_HSV, Lower, Upper)
    mask = cv.erode(mask, None, iterations=2)    
    mask = cv.dilate(mask, None, iterations=2)

    contours, ret = cv.findContours(mask.copy(), cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    
   
    for c in contours:
        time.sleep(0.1)
        #find the biggest area
        c = max(contours, key = cv.contourArea)
        M = cv.moments(c)                      #將中心座標帶入M
        if M["m00"] != 0:                      #由於除數不能為0所以一定要先設判斷式才不會出錯
            cX = int(M["m10"] / M["m00"])      #找出中心的x座標
            cY = int(M["m01"] / M["m00"])      #找出中心的y座標
            cv.drawContours(frame, [c], -1, (0, 255, 0), 2)
            cv.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        area = cv.contourArea(c) 
      
    if area > 15000:
        direction = 2
    elif 15000 >= area >= 0:
        direction = 1
   

            
    err_old = err_new
    err_new = float((cX - (width/2)) * 255 / (width/2))
    up = int(kp * err_new)
    ud = int(kd * ((err_new) - (err_old) / 0.1))
    u = up + ud

    print(u)
    if -255< u < 0 :
        sign = 1
        u = abs(u) 
    elif 255 >= u >= 0:
        sign = 0
    elif u < -255:
        sign = 1
        u = 255
    else:
        sign = 0
        u = 255
    
  

    TXD = R1(u, sign, direction)
    #ser.write(TXD)
    



    cv.imshow("Frame", frame)
    cv.imshow("Mask", mask)


    key = cv.waitKey(1)

    if key ==27:
        break

#ser.close()
cap.release()
cv.destroyAllWindows()