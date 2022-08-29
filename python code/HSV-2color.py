from __future__ import print_function
import cv2 as cv
import argparse

max_value = 255
max_value_H = 360//2
#1
low_H1 = 0
low_S1 = 0
low_V1 = 0
high_H1 = max_value_H
high_S1 = max_value
high_V1 = max_value
#2
low_H2 = 0
low_S2 = 0
low_V2 = 0
high_H2 = max_value_H
high_S2 = max_value
high_V2 = max_value

window_capture_name1 = 'Video Capture1'
window_detection_name1 = 'Object Detection1'
window_capture_name2 = 'Video Capture2'
window_detection_name2 = 'Object Detection2'

low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

#1
def on_low_H_thresh_trackbar1(val):
    global low_H1
    global high_H1
    low_H1 = val
    low_H1 = min(high_H1-1, low_H1)
    cv.setTrackbarPos(low_H_name, window_detection_name1, low_H1)
def on_high_H_thresh_trackbar1(val):
    global low_H1
    global high_H1
    high_H1 = val
    high_H1 = max(high_H1, low_H1+1)
    cv.setTrackbarPos(high_H_name, window_detection_name1, high_H1)
def on_low_S_thresh_trackbar1(val):
    global low_S1
    global high_S1
    low_S1 = val
    low_S1 = min(high_S1-1, low_S1)
    cv.setTrackbarPos(low_S_name, window_detection_name1, low_S1)
def on_high_S_thresh_trackbar1(val):
    global low_S1
    global high_S1
    high_S1 = val
    high_S1 = max(high_S1, low_S1+1)
    cv.setTrackbarPos(high_S_name, window_detection_name1, high_S1)
def on_low_V_thresh_trackbar1(val):
    global low_V1
    global high_V1
    low_V1 = val
    low_V1 = min(high_V1-1, low_V1)
    cv.setTrackbarPos(low_V_name, window_detection_name1, low_V1)
def on_high_V_thresh_trackbar1(val):
    global low_V1
    global high_V1
    high_V1 = val
    high_V1 = max(high_V1, low_V1+1)
    cv.setTrackbarPos(high_V_name, window_detection_name1, high_V1)
#2
def on_low_H_thresh_trackbar2(val):
    global low_H2
    global high_H2
    low_H2 = val
    low_H2 = min(high_H2-1, low_H2)
    cv.setTrackbarPos(low_H_name, window_detection_name2, low_H2)
def on_high_H_thresh_trackbar2(val):
    global low_H2
    global high_H2
    high_H2 = val
    high_H2 = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name2, high_H2)
def on_low_S_thresh_trackbar2(val):
    global low_S2
    global high_S2
    low_S2 = val
    low_S2 = min(high_S2-1, low_S2)
    cv.setTrackbarPos(low_S_name, window_detection_name2, low_S2)
def on_high_S_thresh_trackbar2(val):
    global low_S2
    global high_S2
    high_S2 = val
    high_S2 = max(high_S2, low_S2+1)
    cv.setTrackbarPos(high_S_name, window_detection_name2, high_S2)
def on_low_V_thresh_trackbar2(val):
    global low_V2
    global high_V2
    low_V2 = val
    low_V2 = min(high_V2-1, low_V2)
    cv.setTrackbarPos(low_V_name, window_detection_name2, low_V2)
def on_high_V_thresh_trackbar2(val):
    global low_V2
    global high_V2
    high_V2 = val
    high_V2 = max(high_V2, low_V2+1)
    cv.setTrackbarPos(high_V_name, window_detection_name2, high_V2)


parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
parser.add_argument('--camera', help='Camera devide number.', default=0, type=int)
args = parser.parse_args()

cap = cv.VideoCapture(args.camera)
cv.namedWindow(window_capture_name1)
cv.namedWindow(window_detection_name1)
cv.namedWindow(window_capture_name2)
cv.namedWindow(window_detection_name2)
#1
cv.createTrackbar(low_H_name, window_detection_name1 , low_H1, max_value_H, on_low_H_thresh_trackbar1)
cv.createTrackbar(high_H_name, window_detection_name1 , high_H1, max_value_H, on_high_H_thresh_trackbar1)
cv.createTrackbar(low_S_name, window_detection_name1 , low_S1, max_value, on_low_S_thresh_trackbar1)
cv.createTrackbar(high_S_name, window_detection_name1 , high_S1, max_value, on_high_S_thresh_trackbar1)
cv.createTrackbar(low_V_name, window_detection_name1 , low_V1, max_value, on_low_V_thresh_trackbar1)
cv.createTrackbar(high_V_name, window_detection_name1 , high_V1, max_value, on_high_V_thresh_trackbar1)
#2
cv.createTrackbar(low_H_name, window_detection_name2 , low_H2, max_value_H, on_low_H_thresh_trackbar2)
cv.createTrackbar(high_H_name, window_detection_name2 , high_H2, max_value_H, on_high_H_thresh_trackbar2)
cv.createTrackbar(low_S_name, window_detection_name2 , low_S2, max_value, on_low_S_thresh_trackbar2)
cv.createTrackbar(high_S_name, window_detection_name2 , high_S2, max_value, on_high_S_thresh_trackbar2)
cv.createTrackbar(low_V_name, window_detection_name2 , low_V2, max_value, on_low_V_thresh_trackbar2)
cv.createTrackbar(high_V_name, window_detection_name2 , high_V2, max_value, on_high_V_thresh_trackbar2)

while True:
    
    ret, frame = cap.read()
    if frame is None:
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #1
    frame_threshold1 = cv.inRange(frame_HSV, (low_H1, low_S1, low_V1), (high_H1, high_S1, high_V1))
    #2
    frame_threshold2 = cv.inRange(frame_HSV, (low_H2, low_S2, low_V2), (high_H2, high_S2, high_V2))
    
    
    cv.imshow(window_capture_name1, frame)
    cv.imshow(window_detection_name1, frame_threshold1)
    cv.imshow(window_capture_name2, frame)
    cv.imshow(window_detection_name2, frame_threshold2)
    
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break