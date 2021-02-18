import sys
import numpy as np
import cv2

_, cam, name, mode = sys.argv

if mode is 'photo':
    print('Trying take photo')
    cap = cv2.VideoCapture(cam)
    ret,frame = cap.read()
    # cv2.imshow('img1', frame)
    cv2.imwrite(name, frame)
    cv2.destroyAllWindows()
    cap.release()