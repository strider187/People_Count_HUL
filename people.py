from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2
import time

objects = OrderedDict()
disp = OrderedDict()
pid = 0
dispmax = 10
up = 0
down = 0

def register(centroid, pid):
    objects[pid] = centroid
    disp[pid] = 0

    pid =+ 1
    return pid

def deregister(id):
    del disp[id]
    del objects[id]


def update(rects, up, down, pid):
    up = up
    down = down
    pid = pid
    if(len(rects)==0):
        for i in disp.keys():
            disp[i] += 1
            if(disp[i]>dispmax):
                deregister(i)

        return up, down, pid

    incentroids = np.zeros((len(rects), 2) , dtype= "int")

    x = 0
    for(i) in rects:

        m = cv2.moments(i)
        cx = int(m['m10'] / m['m00'])
        cy = int(m['m01'] / m['m00'])

        incentroids[x]= (cx, cy)
        x =+ 1

    if(len(objects)==0):
        for i in range (0, len(incentroids)):
            pid = register(incentroids, pid)

    else:
        objectids = list(objects.keys())
        objectcentroid = list(objects.values())
        #print((objectcentroid.shape))
        print(objectcentroid)
        print((np.array(objectcentroid).shape))
        print(np.array(objectcentroid))
        d = dist.cdist(np.array(objectcentroid), incentroids)

        row = d.min(axis=1).argsort()
        col = d.argmin(axis=1)[row]

        usedrow = []
        usedcol = []

        for r,c in zip(row, col):
            if((r in usedrow) or (c in usedcol)):
                continue

            objectid = objectids[r]
            objects[objectid] = incentroids[c]
            dis[objectid] = 0

            usedrow.add(r)
            usedcol.add(c)

        unusedrow = set(range(0, d.shape[1]))
        unusedcol = unusedrow.difference(usedrow)

        if(d.shape[0] >= d.shape(1)):
            for r in unusedrow:
                objectid = objectids[r]

                dis[objectid] += 1
                if(dis[objectid]> dismax):
                    deregister(objectid)


        else:
            for c in unusedcol:
                pid = register(incentroids[c], pid)

    return up, down, pid


if __name__ == "__main__":
    pid = 0
    dispmax = 10
    up = 0
    down = 0
    print(type(pid))
    print(type(up))
    print(type(down))

    cap = cv2.cv2.VideoCapture("ch12_20190703090318.mp4")
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
    h = cap.get(4)
    w = cap.get(3)
    frameArea = h*w

    areaTH = frameArea / 40
    kernalOp = np.ones((3, 3), np.uint8)
    kernalOp2 = np.ones((5, 5), np.uint8)
    kernalCl = np.ones((11, 11), np.uint)

    while(cap.isOpened()):
        ret, frame = cap.read()

        fgmask = fgbg.apply(frame)
        fgmask2 = fgbg.apply(frame)

        if(ret == True):
            ret, imBin = cv2.threshold(fgmask, 100, 255, cv2.THRESH_BINARY)
            ret, imBin2 = cv2.threshold(fgmask2, 100, 255, cv2.THRESH_BINARY)

            mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp)
            mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_CLOSE, kernalOp)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernalCl)
            mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernalCl)


            cont = []
            #print(type(cont))

            countours0, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for cnt in countours0:
                area = cv2.contourArea(cnt)

                if area > areaTH:
                    cont.append(cnt)
                (x, y, wf, hf) = cv2.boundingRect(cnt)
                cv2.rectangle(mask, (x, y), (x + wf, y + hf), (0, 255, 0), 2)
            up, down, pid = update(cont, up , down, pid)


            # cv2.line(frame, (450, 300), (700, 300), (250, 0, 1), 2)  # blue line
            #            cv2.line(frame, (450,300), (700,300), (0, 0, 255), 2)  # red line

            rectagleCenterPont = ((x + x + wf) // 2, (y + y + hf) // 2)
            cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()