import cv2
import numpy as np
import vehicles
import time
import math
import os
import imutils


file = open("result.txt", "w")
start_time = time.time()
exact_start = start_time
present_time = 0
man_hours = 0
xs=1

cnt_up=0
cnt_down=0
cap_count = 0

num_in = 0

cap=cv2.VideoCapture("surveillance.m4v")
cap.set(cv2.CAP_PROP_POS_MSEC,10)
print(cap.get(5))

#no. of frames to skip everytime to speed up the video  #######Changing the divisor changes the number of frames to skip################
inc= 5


#Get width and height of video

w=cap.get(3)
h=cap.get(4)
print(h)
print(w)
h = int(h*3/4)
w = int(w*3/4)
frameArea=h*w

#threshold area defining gthe minimum sie of the contour
areaTH=frameArea/100
min = 40000
nid = 300000

#Lines
line_up=325
line_down=325

up_limit=150
down_limit=750

line_down_color=(255,0,0)
line_up_color=(255,0,255)

#line 1 defining the people going down
pt1 =  [0, line_down]
pt2 =  [w, line_down]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))

#line 2 defining the people ging up
pt3 =  [0, line_up]
pt4 =  [w, line_up]
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

#the line to define the upper limet of where a person can be till counting
pt5 =  [0, up_limit]
pt6 =  [w, up_limit]
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))


#the line defining the lower limit where the person can reach till counting
pt7 =  [0, down_limit]
pt8 =  [w, down_limit]
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

#Background Subtractor
fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=True)

#Kernals
kernalOp = np.ones((3,3),np.uint8)
kernalOp2 = np.ones((5,5),np.uint8)
kernalCl = np.ones((11,11),np.uint)


font = cv2.FONT_HERSHEY_SIMPLEX


persons = []
max_p_age = 5
pid = 1


#last negative counts if people going out is more than the people coming in
prev_negative = 0
prev_time = 0

while(cap.isOpened()):
    ret,frame=cap.read()

    #if(ret == True):
     #   frame = imutils.rotate_bound(frame, 90)
     #   frame = cv2.resize(frame, (1440,810), interpolation=cv2.INTER_LINEAR)
    #frame= frame[100:285, 0:200, :]
    for i in persons:
        i.age_one()
    fgmask=fgbg.apply(frame)
    fgmask2=fgbg.apply(frame)

    if ret==True:

        #Binarization
        ret,imBin=cv2.threshold(fgmask,20,255,cv2.THRESH_BINARY)
        ret,imBin2=cv2.threshold(fgmask2,20,255,cv2.THRESH_BINARY)
        #OPening i.e First Erode the dilate
        mask=cv2.morphologyEx(imBin,cv2.MORPH_OPEN,kernalOp)
        mask2=cv2.morphologyEx(imBin2,cv2.MORPH_CLOSE,kernalOp)

        #Closing i.e First Dilate then Erode
        mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernalCl)
        mask2=cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,kernalCl)


        cont = []
        #Find Contours
        countours0,hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in countours0:
            area=cv2.contourArea(cnt)
            #print(area)
            if area>areaTH:
                cont.append(cnt)
                ####Tracking######
                m=cv2.moments(cnt)
                cx=int(m['m10']/m['m00'])
                cy=int(m['m01']/m['m00'])
                x,y,w,h=cv2.boundingRect(cnt)
                num =  math.floor(m['m00']/min)
                #print("num; ", num)
               cv2.imwrite("/home/strider/Desktop/pcount/frames/"+numid+".jpg",frame)
                new=True
                if cy in range(up_limit,down_limit):
                    #numid = str(nid)
                    #nid += 1
                    #cv2.imwrite("/home/strider/Desktop/pcount/frames/"+numid+".jpg",frame)
                    for i in persons:
                        if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                            new = False
                            i.updateCoords(cx, cy)

                            if i.going_UP(line_down,line_up, start_time)==True:
                                cnt_up+=1
                                print(i.getId())

                                #print(int(abs(start_time- time.clock())/10))
                                present_time = time.time()

                                man_hours = man_hours + num_in * abs(start_time-present_time)

                                num_in += 1
                                #print(num_in)
                                '''if(num_in<0):
                                    print("In negative num")
                                    man_hours = man_hours + abs(num_in) * (abs(start_time - present_time)+prev_time)

                                    #prev_negative=+abs(num_in)

                                    prev_time= abs(start_time-present_time)
                                    num_in = 0
                                start_time = present_time'''
                                #print("ID:",i.getId(),'crossed going up at', time.strftime("%c"))
                            elif i.going_DOWN(line_down,line_up, start_time)==True:
                                cnt_down+=1
                                print(i.getId())
                                present_time = time.time()
                                man_hours = man_hours + num_in * abs(start_time - present_time)
                                start_time = present_time
                                num_in -= 1

                                if (num_in < 0):
                                    print("In negative num")
                                    man_hours = man_hours + abs(num_in) * (abs(start_time - present_time) + prev_time)

                                    # prev_negative=+abs(num_in)

                                    prev_time = abs(start_time - present_time)
                                    num_in = 0
                                start_time = present_time
                                #print(int(abs(start_time - time.clock())/60))
                                #print(num_in)

                                #print("ID:", i.getId(), 'crossed going up at', time.strftime("%c"))
                            break
                        if i.getState()=='1':
                            if i.getDir()=='down'and i.getY()>down_limit:
                                i.setDone()
                            elif i.getDir()=='up'and i.getY()<up_limit:
                                i.setDone()
                        if i.timedOut():
                            index=persons.index(i)
                            persons.pop(index)
                            del i

                    if new==True: #If nothing is detected,create new
                        p=vehicles.person(pid,cx,cy,max_p_age)
                        persons.append(p)
                        pid+=1

                cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
                img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)


        for i in persons:
            cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv2.LINE_AA)




        str_up='UP: '+str(cnt_up)
        str_down='DOWN: '+str(cnt_down)
        frame=cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
        frame=cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
        frame=cv2.polylines(frame,[pts_L3],False,(0,0,255),thickness=2)
        frame=cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=2)
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow('Frame',frame)
        #cv2.imshow('thresh', mask)
        #numid = str(nid)
        #nid+=1
        #cv2.imwrite("/home/strider/Desktop/pcount/frames/frame"+ numid+".jpg", frame)

        if cv2.waitKey(1)&0xff==ord('q'):
            break
        #if cv2.waitKey(1) & 0xff == ord('q'):
            #break

        cap_count += inc
        cap.set(1, cap_count)
    else:
        break



cap.release()
cv2.destroyAllWindows()
present_time = time.time()
man_hours = man_hours + num_in * abs(start_time - present_time)
print("Num In: ",num_in)
print("up number: ",cnt_up)
print("Down number:",cnt_down)
hours= int(man_hours/3600)
minutes = int((man_hours/60)%60)
seconds = int(man_hours%60)

h_string = str(hours)
m_string = str(minutes)
s_string= str(seconds)
final = "The number of man hours = "
final = final +h_string + ":" + m_string + ":" + s_string

file.write(final)
print("Hours: ")
print ('%.2f'%hours)
print ("Minutes: ")
print ('%.2f'%minutes)
print("Seconds: ")
print ('%.2f'%seconds)
print(man_hours)
exact_start = abs(time.time()-exact_start)
print("Total time to finish: ")
print(exact_start)





