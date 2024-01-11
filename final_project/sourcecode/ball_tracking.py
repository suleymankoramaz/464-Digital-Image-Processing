import numpy as np
import cv2 as cv
import time

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

red = (0,0,255)
blue = (255,0,0)
green = (0,255,0)


detection = 1
max_tracking_frame  = 20
count_tracking_frame  = 0

fps = 60
prev = 0

low_thres = (29, 40, 40) 
high_thres = (90, 255, 255)


def boundingBox_putText(input_frame, box_color, index, first_point, second_point):
    cv.rectangle(input_frame, first_point, second_point, box_color, 2)
    cv.putText(input_frame,'Ball ' + str(index+1), first_point, cv.FONT_HERSHEY_COMPLEX_SMALL, 1, green, 1)


def hsv_processing(input_frame, low_thres, high_thres):
    gauss_filter = cv.GaussianBlur(input_frame, (3,3), 0)

    hsv = cv.cvtColor(gauss_filter, cv.COLOR_BGR2HSV)

    hsv_binary = cv.inRange(hsv, low_thres, high_thres)
    
    return hsv_binary


def noise_processing(input_frame):

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))

    out = cv.morphologyEx(input_frame, cv.MORPH_OPEN, kernel, iterations=2)

    out = cv.morphologyEx(out, cv.MORPH_CLOSE, kernel, iterations=4)
    
    return out


def findContours_processing(input_frame, ball_rois_list):
    contour, _ = cv.findContours(input_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    min_radius = 30
    max_radius = 90
    min_circularity = 0.75
    
    for index, cnt in enumerate(contour):
        _, radius = cv.minEnclosingCircle(cnt)
        radius = int(radius)
        
        if min_radius < radius < max_radius:
            circularity = 4 * np.pi * cv.contourArea(cnt) / (cv.arcLength(cnt, True) ** 2)
            
            if circularity > min_circularity:
                ball_rect = cv.boundingRect(cnt)
                
                first_point = (int(ball_rect[0]), int(ball_rect[1]))
                second_point = (int(ball_rect[0] + ball_rect[2]), int(ball_rect[1] + ball_rect[3]))

                ball_rois_list.append(ball_rect)

                boundingBox_putText(frame, red, index, first_point, second_point)

    return ball_rois_list


while True:
    timeElapsed = time.time() - prev
    if timeElapsed > 1./fps:
        prev = time.time()

        ret, frame = cap.read()
        ball_rois_list = []
        
        if detection == 1:
            hsv_work = hsv_processing(frame, low_thres, high_thres)

            noise_rmv = noise_processing(hsv_work)

            ball_detection = findContours_processing(noise_rmv,ball_rois_list)  

            multi_trackers = cv.legacy.MultiTracker_create()

            for ball_roi in ball_detection:
                multi_trackers.add(cv.legacy.TrackerCSRT_create(), frame, ball_roi)

            detection = 0
                
        else:
            if count_tracking_frame == max_tracking_frame:
                detection = 1
                count_tracking_frame = 0

            ret, objs = multi_trackers.update(frame)
            if ret:
                for index, obj in enumerate(objs):
                    if((float(obj[2])/float(obj[3])) < 0.93 or (float(obj[2])/float(obj[3])) > 1.36):
                        detection = 1

                    else:
                        first_point = (int(obj[0]), int(obj[1]))
                        second_point = (int(obj[0]+obj[2]), int(obj[1]+obj[3]))

                        boundingBox_putText(frame, blue, index, first_point, second_point)
                
            else:
                detection = 1
            
            count_tracking_frame += 1        
        

        cv.imshow('Ball Tracking', frame)
        cv.imshow('Mask', noise_rmv)
        if cv.waitKey(1) == ord('q'):
            break

cap.release()
cv.destroyAllWindows()