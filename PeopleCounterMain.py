import argparse
import datetime
import imutils
import math
import cv2
import numpy as np
from detclass import detclass
#import vehicles
rects = []

width = 1280





def main(textOut, textIn):

    det.__int__()
    camera = cv2.VideoCapture("ch12_20190703090318.mp4")

    firstFrame = None

    # loop over the frames of the video
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('', gray)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        #cv2.imshow('',gray)

        # if the first frame is None, initialize it and treat it as the background
        if firstFrame is None:
            firstFrame = gray
            continue

        # computing the absolute difference between the current frame and background(first frame)
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilating the thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        #print (cnts)
        # loop over the contours
        xset= 0
        rects = []
        start = 0
        for c in cnts:
            #rects.append(c.astype("int"))

            xset+=1
            #print(c)
            #To track the moevement of the object
            up = 0
            down = 0
            movin = 0

            # if the contour is too small, ignore it

            #if cv2.contourArea(c) < 12000:
                #continue
            # compute the bounding box for the contour, draw it on the frame,
            cv2.line(frame, (450, 300), (700, 300), (0, 0, 255), 2)  # red line
            (x, y, w, h) = cv2.boundingRect(c)
            #print(cv2.boundingRect(c))
            rects.append(cv2.boundingRect(c))
            #print(rects[0])
            #print(enumerate(rects))


            #start = 1
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            #cv2.line(frame, (450, 300), (700, 300), (250, 0, 1), 2)  # blue line
#            cv2.line(frame, (450,300), (700,300), (0, 0, 255), 2)  # red line

            rectagleCenterPont = ((x + x + w) // 2, (y + y + h) // 2)
            cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)
            '''print(rectagleCenterPont)
            if(rectagleCenterPont[1]<300):
                down = 1
                movin = 0
            else:
                up = 1
                movin = 1
            print(down, up, movin)
            #check for in and out'''
        _, up, down = det.update(rects, up, down)
        textIn+=down
        textOut+=up

            # show the frame and record if the user presses a key
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.putText(frame, "In: {}".format(str(textIn)), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Out: {}".format(str(textOut)), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)

    #close any open windows
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    det = detclass()
    textOut = 0
    textIn = 0
    main(textOut, textIn)
