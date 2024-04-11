import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
import webbrowser

#######################
brushThickness = 10
eraserThickness = 100
isOn = False
########################


folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.65, maxHands=1)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:

    # 1. Import image
    success, img = cap.read()
    #img = cv2.flip(img, 0)

    # 2. Find Hand Landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        # print(lmList)

        # tip of index and middle fingers
        try:
            x1, y1 = lmList[0][8][1:]
            x2, y2 = lmList[0][12][1:]
        except:
            print("Hands Are Out Of Range")
        # 3. Check which fingers are up
        try:
            fingers = detector.fingersUp()
        except:
            print("Fingers Out Of Range")

        # print(fingers)
        if fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:
            isOn = True

        if fingers[0] == False and fingers[1] == False and fingers[2] and fingers[3] == False and fingers[4] == False:
            # print("ss")

            if isOn:
                isOn = False
                url = 'https://www.youtube.com/watch?v=cDlGFbBipCo&ab_channel=LindseyStirling'
                webbrowser.register('chrome',
                                    None,
                                    webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))
                webbrowser.get('chrome').open(url)
            #os.system("shutdown /s /t 1")

        # 4. If Selection Mode - Two finger are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            #print("Selection Mode")
            # # Checking for the click
            if y1 < 200:
                if 50 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (100, 10, 10)  # swr
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 100, 0)  # shin
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)  # sawz
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25),
                          drawColor, cv2.FILLED)

        # 5. If Drawing Mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            #print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawColor, eraserThickness)

            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1),
                         drawColor, brushThickness)

            xp, yp = x1, y1

        # Clear Canvas when all fingers are up
        if all(x >= 1 for x in fingers):
            imgCanvas = np.zeros((720, 1280, 3), np.uint8)
    # print(isOn)
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Setting the header image
    img[0:125, 0:1280] = header
    #img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.flip(img, 3)
    cv2.imshow("Image", img)
    #cv2.imshow("Canvas", imgCanvas)
    #cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)
