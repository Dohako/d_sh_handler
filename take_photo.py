import numpy as np
import cv2


def photo(photo_name, cam=0):
    cap = cv2.VideoCapture(cam)
    ret,frame = cap.read()
    cv2.imwrite(photo_name, frame)
    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    photo('./test.png')