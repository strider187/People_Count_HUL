from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np


class detclass:
    #construtor to set the onjectud, objects to ordereddict and to intialize the disappeared as ordereddict
    def __int__(self, dismax = 5):
        #print("Dcontruct called")
        self.newobjid = 0
        self.objects = OrderedDict()
        self.dis = OrderedDict()

        self.dismax = dismax


    def register(self, centroid):

        self.objects[self.newobjid] = centroid
        print("registerd", centroid)

        self.dis[self.newobjid] = 0
        self.newobjid += 1


    def dereg(self, objectid):
        del self.objects[objectid]
        del self.dis[objectid]

    def update(self, rects, up, down):
        if(len(rects) == 0):
            #checl for the disappeared objects in the dis ordereddict
            for objectid in self.dis.keys():
                self.dis[objectid] +=1
                #deregster the disappeared object
                if(self.dis[objectid] > self.dismax):
                    self.dereg(objectid)
                #as no value left to update, return
            return self.objects, up , down

        #array of inpur centroids
        incentroid = np.zeros((len(rects), 2), dtype ="int")
        ##print(incentroid)

        for(i, (xt, yt, xb, yb)) in enumerate(rects):
            #print(("ennumerate"))
            #print(i)
            #print(xt, yt, xb, yb)
            (xt, yt, xb, yb) = rects[i]
            cx = int((xt+ xb)/2)
            cy = int((yt+yb)/2)
            #print(cx, cy)
            incentroid[i] = (cx, cy)
            #print ("incent11")
            #print(incentroid)
            #l = len(self.objects)
            ##print("no of object")
            ##print(l)
        #if there is no registered object as yet, register the incoming rects
        if(len(self.objects) == 0):
            for i in range(0, len(incentroid)):
                self.register(incentroid[i])

        #trac object
        else:
            objectids = list(self.objects.keys())
            objcentroid = list(self.objects.values())

            #calculate the distance of old and new centroid

            d = dist.cdist(np.array(objcentroid), incentroid)
            #print("d = ")
            print(d)
            row = d.min(axis = 1).argsort()

            col = d.argmin(axis = 1)[row]

            urow = set()
            ucol = set()

            for (rw,cl) in zip(row, col):
                #print("in row and column")
                if((rw in urow) or (cl in ucol)):
                    #print("gon")
                    continue
                #print("hello")
                objectid = objectids[rw]
                print("objectid")
                print(objectid)
                print("self.objects[objectid]")
                print(self.objects[objectid])
                print("incent")
                print(incentroid[cl])
                if(objectid!=0):
                    if((self.objects[objectid][1] >= 300 and incentroid[cl][1]<300) or (self.objects[objectid][1] > 300 and incentroid[cl][1]<=300)):
                        down += 1
                    elif((self.objects[objectid][1]<=300 and incentroid[cl][1] > 300) or (self.objects[objectid][1] < 300 and incentroid[cl][1] >+ 300)):
                        up += 1
                self.objects[objectid] = incentroid[cl]
                self.dis[objectid] = 0

                urow.add(rw)
                ucol.add(cl)

                unusedrow = set(range(0, d.shape[0]))
                unusedrow = unusedrow.difference(urow)
                #print("unusedrow")
                #print(unusedrow)
                unusedcol = set(range(0, d.shape[1]))
                unusedcol = unusedcol.difference(ucol)
                #unusedrow = unusedrow.difference(urow)
                #unusedcol = unusedcol.difference(ucol)

                if (d.shape[0] >= d.shape[1]):

                    for rw in unusedrow:
                        objectID = objectids[rw]
                        #print("discolumn")
                        #print(objectID)
                        #print(len(self.dis))
                        #print(len(self.objects))
                        self.dis[objectID] = self.dis[objectID] + 1

                        if self.dis[objectID] > self.dismax:

                            self.dereg(objectID)


                else:
                    for cl in unusedcol:
                        self.register(incentroid[cl])
        #print(up, down)
        return self.objects, up, down
