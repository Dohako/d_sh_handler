import math
from time import time
from cvzone import HandTrackingModule as HTM
import cv2

cap = cv2.VideoCapture(0)

p_time = 0

detector = HTM.HandDetector(maxHands=1, detectionCon=0.7)

while True:
    succes, img = cap.read()
    lm_list, img = detector.findHands(img)
    if len(lm_list) != 0:
        lm_list = lm_list[0]["lmList"]
        # print(lm_list[4], lm_list[8])
        x1, y1, x2, y2 = lm_list[4][0],lm_list[4][1], lm_list[8][0], lm_list[8][1]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255,0,255), cv2.FILLED)

        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)

        cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)

        lenght = math.hypot(x2 - x1, y2 - y1)
        print(lenght)
    c_time = time()
    fps = 1 / (c_time - p_time)
    p_time = c_time
    cv2.putText(img, f"FPS: {int(fps)}", (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("image", img)
    cv2.waitKey(1)