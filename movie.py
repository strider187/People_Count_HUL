from moviepy.editor import *

video = VideoFileClip("Mangla_c2.mp4").subclip(1000, 1200)

video.write_videofile("test.mp4", fps = 30)
'''
import cv2
import numpy as np

cap = cv2.VideoCapture("test.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()'''