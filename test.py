import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
import tensorflow as tf

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
cls = Classifier("/Users/vel/Library/Mobile Documents/com~apple~CloudDocs/Desktop/projects/Git projects/signlanguage/Models/keras_model.h5","/Users/vel/Library/Mobile Documents/com~apple~CloudDocs/Desktop/projects/Git projects/signlanguage/Models/labels.txt")
offset = 20
imgSize = 300

labels = ["A","B","c"]
while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            pred,ind=Classifier.getPrediction(self=cls,img=imgWhite,draw=False  )
            print(pred,ind)

        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            pred,ind=Classifier.getPrediction(self=cls,img=imgWhite,draw=False)
        cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                      (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[ind], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x-offset, y-offset),
                      (x + w+offset, y + h+offset), (255, 0, 255), 4)

    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)