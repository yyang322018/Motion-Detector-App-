#-------------------------------------------------------------------------------
# Name:        Motion Detector
# Purpose:
#
# Author:      Yi Yang
#
# Created:     06/20/2021
# Copyright:   (c) Yi Yang 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import cv2,pandas
import time
from datetime import datetime

first_frame=None
status_list=[None,None]
times=[]
df=pandas.DataFrame(columns=["Start","End"])
video=cv2.VideoCapture(0)

time.sleep(3)

while True:
    check,frame=video.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0) #smooth image and increase accuracy, img/gaussian l/w/standard deviation

    #Capture first_frame
    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=2) #remove holes

    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour)<10000: #<100*100pixels pass
            continue
        status=1
        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

    status_list.append(status) 
    status_list=status_list[-2:]
    # status change from 0 to 1 or 1 to 0, record the datetime  
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("Gray frame",gray)
    cv2.imshow("Delta frame",delta_frame)
    cv2.imshow("Thresh frame",thresh_frame)
    cv2.imshow("Color frame",frame)
    
    key=cv2.waitKey(1)
    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break

for i in range(0,len(times)-1,2):
    df=df.append({"Start":times[i],"End":times[i+1]}, ignore_index=True)
df.to_csv("Times.csv")

print(status_list)
print(times)
video.release()
cv2.destroyAllWindows()