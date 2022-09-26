from imutils.video import VideoStream
import imutils
import cv2
import os
import urllib.request
import numpy as np
from django.conf import settings
from cvzone.FaceMeshModule import FaceMeshDetector




class VideoCamera(object):
    pointList = [22, 23, 24, 26, 110, 157,158,159,160,161, 130, 243]
    ratioList = []
    blink = 0
    counter = 0
    ratioavg = 0
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()


    #This function is used in views
    def get_frame(self):
        detect=FaceMeshDetector(maxFaces=5)

        
        success, image = self.video.read()
        frame_flip = cv2.flip(image, 1)

        img,faces=detect.findFaceMesh(image)
        if len(faces) == 0:
            cv2.putText(img,"Please keep your camera in front of you", (5,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
        if len(faces)>1:
            cv2.putText(img,"Maximum 1 face allowed", (5,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        if len(faces) == 1:
            face = faces[0]
            for id in self.pointList:
                cv2.circle(img, face[id], 3, (255,0,255), 2)
            
            leftUp = face[159]
            leftDown = face[23]

            leftLeft = face[130]
            leftRight = face[243]


            length_V,_= detect.findDistance(leftUp, leftDown)
            # print("Vert:", length_V)

            length_H,_ = detect.findDistance(leftLeft, leftRight)
            # print("Horiz: ", length_H)
            ratio = int((length_V/length_H)*100)
            self.ratioList.append(ratio)
            if len(self.ratioList)>5:
                self.ratioList.pop(0)
                self.ratioavg = sum(self.ratioList)/len(self.ratioList)
            if self.ratioavg < 35 and self.counter==0:
                self.blink+=1
                self.counter=1
                print(self.blink)
            if self.counter:
                self.counter+=1
                if self.counter>15:
                    self.counter=0
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes(), self.blink<4