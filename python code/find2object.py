import cv2 as cv
import numpy as np
import serial
import time

#追蹤單一顏色 到一定距離時停止 太靠近則後退
#攝影機解析度 : 640*480 HD-3000

#ser = serial.Serial("/dev/ttyAMA0" , baudrate = 57600 , timeout = 1.0)

mode = 0
direction = None
area_1 = 0
cX_1 = 0
cY_1 = 0

area_2 = 0
cX_2 = 0
cY_2 = 0


def R1(direction):
    senddata = bytearray()
    senddata.append(0xff)
    senddata.append(0x55)      
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
    Lower_1 = np.array([80, 80, 100])
    Upper_1 = np.array([100, 150, 255])

    Lower_2 = np.array([0, 100, 0])
    Upper_2 = np.array([10, 255, 255])
    
    
    #RGB轉成HSV 然後侵蝕與膨脹
    #Phase 1
    if mode == 0:        
        mask_1 = cv.inRange(frame_HSV, Lower_1, Upper_1)
        mask_1 = cv.erode(mask_1, None, iterations=2)    
        mask_1 = cv.dilate(mask_1, None, iterations=2)

        contours_1, ret = cv.findContours(mask_1.copy(), cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    
   
        for c in contours_1:        
            #find the biggest area
        
            c = max(contours_1, key = cv.contourArea)
            M = cv.moments(c)                      #將中心座標帶入M
            if M["m00"] != 0:                      #由於除數不能為0所以一定要先設判斷式才不會出錯
                cX_1 = int(M["m10"] / M["m00"])      #找出中心的x座標
                cY_1 = int(M["m01"] / M["m00"])      #找出中心的y座標
                cv.drawContours(frame, [c], -1, (0, 255, 0), 2)
                cv.circle(frame, (cX_1, cY_1), 7, (255, 255, 255), -1)
            area_1 = cv.contourArea(c) 
    
        print(cX_1, area_1)
    
        if area_1 >= 100000:
            direction = 0
            mode += 1
        elif 100000 > area_1 > 0:
            direction = 1
            if 0 <= cX_1 <= width/4:
                direction = 4
            if width/4 < cX_1 < width/2:
                direction = 3
            if cX_1 == width/2:
                direction = 1
            if width*0.75 > cX_1 > width/2:
                direction = 5
            if width >= cX_1 >= width*0.75:
                direction = 6        
        else:
            direction = 0

    #Phase 2
    if mode == 1:
        mask_2 = cv.inRange(frame_HSV, Lower_2, Upper_2)
        mask_2 = cv.erode(mask_2, None, iterations=2)    
        mask_2 = cv.dilate(mask_2, None, iterations=2)

        contours_2, ret = cv.findContours(mask_2.copy(), cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)    
   
        for c in contours_2:        
            #find the biggest area
        
            c = max(contours_2, key = cv.contourArea)
            M = cv.moments(c)                      #將中心座標帶入M
            if M["m00"] != 0:                      #由於除數不能為0所以一定要先設判斷式才不會出錯
                cX_2 = int(M["m10"] / M["m00"])      #找出中心的x座標
                cY_2 = int(M["m01"] / M["m00"])      #找出中心的y座標
                cv.drawContours(frame, [c], -1, (0, 255, 255), 2)
                cv.circle(frame, (cX_2, cY_2), 7, (255, 255, 0), -1)
            area_2 = cv.contourArea(c) 

        print(cX_2, area_2)
    
        if area_2 >= 100000:
            direction = 0
        elif 100000 > area_2 > 0:
            direction = 1
            if 0 <= cX_2 <= width/4:
                direction = 4
            if width/4 < cX_2 < width/2:
                direction = 3
            if cX_2 == width/2:
                direction = 1
            if width*0.75 > cX_2 > width/2:
                direction = 5
            if width >= cX_2 >= width*0.75:
                direction = 6        
        else:
            direction = 0


    print(direction)

  

    #TXD = R1(direction)
    #ser.write(TXD)
    


    cv.imshow("Frame", frame)
    #cv.imshow("Mask_1", mask_1)
    #cv.imshow("Mask_2", mask_2)


    key = cv.waitKey(1)

    if key ==27:
        break

#ser.close()
cap.release()
cv.destroyAllWindows()